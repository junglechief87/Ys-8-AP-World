"""
Archipelago init file for The Ys 8
"""
from logging import error, warning
from typing import Any, Dict, List
from BaseClasses import ItemClassification, Tutorial
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_item_rule
from .Options import Ys8Options, Ys8_option_groups, Ys8_option_presets
from .Locations import location_table, location_name_groups
from .Items import Ys8Item, get_item_pool_quantity, get_items_by_category, scale_exp_item, item_table, item_name_groups, psyche_item_table, psyche_access_item_table, event_item_table
from .Rules import set_all_rules
from .Regions import create_regions, connect_entrances
from .Generate_Json import generate_json

class Ys8Web(WebWorld):
    theme = "jungle"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Ys 8 with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["NewSoupVi", "Jarno"]
    )
    tutorials = [setup_en]

    options_presets = Ys8_option_presets
    option_groups = Ys8_option_groups

class Ys8World(World):
    """
    Description of game.
    """
    game = "Ys 8"
    origin_region_name = "Calm Inlet Area"
    options_dataclass = Ys8Options
    options: Ys8Options
    web = Ys8Web()
    topology_present = True

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups
    fillers = {}
    fillers.update(get_items_by_category("Consumable"))

    def generate_early(self):
        from .Locations import (location_table, event_location_table, psyche_location_table, psyche_fight_names,
                                fsc_location_table, fsc_event_location_table, fsc_psyche_location_table, fsc_psyche_fight_names,
                                silent_tower_psyche_location_table, landmark_location_table)
        from .Items import (item_table, event_item_table,
                            landmark_item_table, fsc_event_item_table,
                            super_weapons_item_table, progressive_super_weapon_item_table)
        
        # Create instance copies of all tables to avoid state pollution across multiple world generations
        # Each world gets fresh copies of these base tables
        self.item_table = dict(item_table)
        self.event_item_table = dict(event_item_table)
        self.location_table = dict(location_table)
        self.event_location_table = dict(event_location_table)
        self.psyche_location_table = dict(psyche_location_table)
        self.psyche_fight_names = dict(psyche_fight_names)
        
        # Initialize psyche selection lists as instance attributes (for deterministic generation)
        self.chosen_psyche_fight_list: List[str] = []
        self.chosen_psyche_location_list: List[str] = []
        
        # Force Former Sanctuary Crypt on if Untouchable final boss access is selected
        if self.options.final_boss_access.value == 3:  # option_untouchable
            self.options.former_sanctuary_crypt.value = True
        
        if self.options.essence_key_sanity.value:
            self.options.former_sanctuary_crypt.value = True

        # Adjust location tables based on options using instance copies
        if self.options.former_sanctuary_crypt.value:
            self.event_item_table.update(fsc_event_item_table)
            self.location_table.update(fsc_location_table)
            self.event_location_table.update(fsc_event_location_table)
            self.psyche_location_table.update(fsc_psyche_location_table)
        else:
            self.psyche_fight_names.update(fsc_psyche_fight_names)
        
        if self.options.mephorash_progression.value:
            self.psyche_location_table.update(silent_tower_psyche_location_table)

        # Add landmark locations and items if Discovery Sanity is enabled
        if self.options.discovery_sanity.value:
            self.item_table.update(landmark_item_table)
            self.location_table.update(landmark_location_table)
        else:
            # Keep landmark logic online by forcing landmark items to their default landmark locations
            self.event_item_table.update(landmark_item_table)
            self.event_location_table.update(landmark_location_table)

        if self.options.progressive_super_weapons.value:
            self.item_table.update(progressive_super_weapon_item_table)
        else:
            self.item_table.update(super_weapons_item_table)

    def create_regions(self):
        create_regions(self)

    def connect_entrances(self):
        connect_entrances(self)

    def create_items(self):
        self.place_predetermined_items()

        if self.options.former_sanctuary_crypt.value and not self.options.essence_key_sanity.value:
            for location in self.multiworld.get_unfilled_locations(self.player):
                in_fsc = location.parent_region and location.parent_region.name.startswith("Former Sanctuary Crypt")
                if not in_fsc:
                    add_item_rule(location, lambda item: item.name != "Essence Key Stone")

        # Determine Starting Character and add to precollected items
        party = [item_name for item_name in self.item_table.keys() if self.item_table[item_name].is_party_member]
        party_weights = [self.options.starting_character_weights.value.get(item_name, 0) for item_name in party]
        if not any(weight > 0 for weight in party_weights):
            starting_character = self.random.choice(party) # Force even distribution if all weights are zero
        else:
            starting_character = self.random.choices(party, weights=party_weights, k=1)[0]
        item = self.create_item(starting_character)
        self.multiworld.push_precollected(item)

        locations_to_fill = len(self.multiworld.get_unfilled_locations(self.player))
        item_pool: List[Ys8Item] = []
        filler_pool: List[Ys8Item] = []

        # Always include all configured non-filler items so required progression cannot be dropped by pool size.
        # Use global item_table for deterministic iteration, then add landmarks separately if needed
        for name, data in item_table.items():
            if name in ["Essence Key Stone", "Jade Pendant"] and not self.options.former_sanctuary_crypt.value:
                continue
            if name == starting_character:
                continue
            # Skip items that are being replaced by scaling (they're created via the scaling of their source items)
            if self.options.scale_exp_items.value and name in ["Bitter Remedy x2", "Bitter Remedy x3", "Sweet Remedy x3", "Sweet Remedy x5"]:
                continue
            if self.options.scale_exp_items.value and name in ["Bitter Remedy", "Bitter Remedy x2", "Bitter Remedy x3", "Hermit's Elixir", "Hermit's Elixir x3"]:
                name = scale_exp_item(name, data, self.options)
            for _ in range(get_item_pool_quantity(name, data, self.options)):
                item = self.create_item(name)
                if item.classification == ItemClassification.filler:
                    filler_pool.append(item)
                else:
                    item_pool.append(item)

        if len(item_pool) > locations_to_fill:
            raise OptionError(
                f"Non-filler item pool ({len(item_pool)}) exceeds available locations ({locations_to_fill})."
            )

        # Use configured filler entries first, randomized without replacement,
        # then weighted filler draws for any remaining slots.
        remaining_slots = locations_to_fill - len(item_pool)
        self.random.shuffle(filler_pool)
        item_pool.extend(filler_pool[:remaining_slots])

        while len(item_pool) < locations_to_fill:
            item_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += item_pool
        print(self.multiworld.itempool)

    def place_predetermined_items(self):
        # Place event items that are required for progression or victory
        for item_name in self.event_item_table.keys():
            if self.event_item_table[item_name].category == "Landmark":
                location_name = self.event_item_table[item_name].default_loc
            else:
                location_name = self.event_item_table[item_name].category

            item = self.create_event(item_name)
            location = self.multiworld.get_location(location_name, self.player)
            location.place_locked_item(item)
        
        if self.options.final_boss_access == 2:  # Psyche Fight Shuffle
            self.event_item_table.update(psyche_access_item_table)
            self.event_item_table.update(psyche_item_table)
            for i, (access_item_name, psyche_item_name) in enumerate(zip(psyche_access_item_table.keys(), psyche_item_table.keys())):
                access_item = self.create_event(access_item_name)
                psyche_item = self.create_event(psyche_item_name)
                access_location = self.multiworld.get_location(self.chosen_psyche_location_list[i], self.player)
                psyche_location = self.multiworld.get_location(self.chosen_psyche_fight_list[i], self.player)
                access_location.place_locked_item(access_item)
                psyche_location.place_locked_item(psyche_item)

    def get_filler_item_name(self) -> str:
        weights = [data.weight for data in self.fillers.values()]
        return self.random.choices([filler for filler in self.fillers.keys()], weights)[0]

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = {}
        slot_options = ["final_boss_access", "goal_count_crew_mode", "goal_count_psyches_mode", "goal_count_crew_final_boss", "goal_count_psyches_final_boss",
                        "discovery_sanity", "dungeon_entrance_shuffle", "jewel_trade_items", "fish_trades", "food_trades", "map_completion", "discoveries", 
                        "dogi_intercept_rewards", "master_kong_rewards", "silvia_progression", "mephorash_progression", "former_sanctuary_crypt", "experience_multiplier", 
                        "additional_intercept_rewards", "battle_logic", "scaled_encounters", "progressive_super_weapons", "octus_paths_opened", "extra_flame_stones", 
                        "recipes_with_ingredients", "north_side_open", "infinity_mode", "scale_exp_items", "final_boss", "theos_start_phase", "origin_care_package", "origin_start_phase",
                        "essence_key_sanity", "starting_character_weights"]

        slot_data = {"options": {option_name: getattr(self.options, option_name).value for option_name in slot_options}}

        return slot_data

    def create_item(self, name: str) -> Ys8Item:
        data = self.item_table[name]
        classification = data.classification
        if name == "Jade Pendant":
            classification = (ItemClassification.progression
                              if self.options.former_sanctuary_crypt.value
                              else ItemClassification.useful)
        if name == "Essence Key Stone":
            classification = (ItemClassification.progression
                              if self.options.former_sanctuary_crypt.value
                              else ItemClassification.filler)
        if self.options.battle_logic and data.battle_logic:
            classification = ItemClassification.progression
        return Ys8Item(name, classification, data.code, self.player)
    
    def create_event(self, name: str) -> Ys8Item:
        data = self.event_item_table[name]
        return Ys8Item(name, data.classification, data.code, self.player)
    
    def set_rules(self):
        set_all_rules(self)
    
    def generate_output(self, output_directory: str):
        generate_json(self, output_directory)
    
    

