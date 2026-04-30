"""
Archipelago init file for The Ys 8
"""
from logging import error, warning
from typing import Any, Dict, List, TextIO
from BaseClasses import ItemClassification, Tutorial
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_item_rule
from .Options import Ys8Options, Ys8_option_groups, Ys8_option_presets
from .Locations import location_table, location_name_groups
from .Items import Ys8Item, get_item_pool_quantity, get_items_by_category, item_table, item_name_groups, event_item_table
from .Rules import set_all_rules
from .Regions import create_regions, connect_entrances
from .Generate_Json import generate_json
from .Entrance_Shuffle import dungeon_entrance_shuffle

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

    def __init__(self, multiworld, player):
        super(Ys8World, self).__init__(multiworld, player)
        self.chosen_psyche_fight_list = None
        self.chosen_psyche_location_list = None
        self.boss_spoiler = []
        self.dungeon_connections = {}
        self.entrance_spoiler = []
        self.starting_character = None
        self.adol_starting_skills = []
        self.sahad_starting_skills = []
        self.laxia_starting_skills = []
        self.ricotta_starting_skills = []
        self.hummel_starting_skills = []
        self.dana_starting_skills = []
        self.starting_skills = []
        self.max_psyche_num = 4

    def generate_early(self):
        # Force Former Sanctuary Crypt on if Untouchable final boss access is selected or esscence key sanity
        if self.options.final_boss_access.value == 3 or self.options.essence_key_sanity.value:
            self.options.former_sanctuary_crypt.value = True

        

        if self.options.dungeon_entrance_shuffle.value:
            dungeon_entrance_shuffle(self)

    def create_regions(self):
        create_regions(self)

    def connect_entrances(self):
        connect_entrances(self)

    def create_items(self):
        self.place_predetermined_items() # event item handling

        if self.options.former_sanctuary_crypt.value and not self.options.essence_key_sanity.value:
            for location in self.multiworld.get_unfilled_locations(self.player):
                in_fsc = location.parent_region and location.parent_region.name.startswith("Former Sanctuary Crypt")
                if not in_fsc:
                    add_item_rule(location, lambda item: item.name != "Essence Key Stone")

        if not self.options.discovery_sanity.value:
            for name in get_items_by_category("Landmark"):
                item = self.create_item(name)
                location = self.multiworld.get_location(item_table[name].default_loc, self.player)
                location.place_locked_item(item)
                
        # Determine Starting Character and add to precollected items
        party = [item_name for item_name in item_table.keys() if item_table[item_name].is_party_member]
        party_weights = [self.options.starting_character_weights.value.get(item_name, 0) for item_name in party]
        if not any(weight > 0 for weight in party_weights):
            self.starting_character = self.random.choice(party) # Force even distribution if all weights are zero
        else:
            self.starting_character = self.random.choices(party, weights=party_weights, k=1)[0]
        item = self.create_item(self.starting_character)
        self.multiworld.push_precollected(item)

        self.adol_starting_skills = self.multiworld.random.sample([item for item in get_items_by_category("Adol Skill").keys()], 2)
        self.sahad_starting_skills = self.multiworld.random.sample([item for item in get_items_by_category("Sahad Skill").keys()], 2)
        self.laxia_starting_skills = self.multiworld.random.sample([item for item in get_items_by_category("Laxia Skill").keys()], 2)
        self.ricotta_starting_skills = self.multiworld.random.sample([item for item in get_items_by_category("Ricotta Skill").keys()], 2)
        self.hummel_starting_skills = self.multiworld.random.sample([item for item in get_items_by_category("Hummel Skill").keys()], 2)
        self.dana_starting_skills = self.multiworld.random.sample([item for item in get_items_by_category("Dana Skill").keys()], 2)

        self.starting_skills = (self.adol_starting_skills + self.sahad_starting_skills + self.laxia_starting_skills + 
                                self.ricotta_starting_skills + self.hummel_starting_skills + self.dana_starting_skills)
        
        location = self.get_location("Adol Starting Skill Skill 1 Sonic Slide")
        location.place_locked_item(self.create_item(self.adol_starting_skills[0]))
        location = self.get_location("Adol Starting Skill Skill 2 Arc Shot")
        location.place_locked_item(self.create_item(self.adol_starting_skills[1]))
        location = self.get_location("Sahad Starting Skill Skill 1 High Wave")
        location.place_locked_item(self.create_item(self.sahad_starting_skills[0]))
        location = self.get_location("Sahad Starting Skill Skill 2 Grand Anchor")
        location.place_locked_item(self.create_item(self.sahad_starting_skills[1]))
        location = self.get_location("Laxia Starting Skill Skill 1 Dagger Fling")
        location.place_locked_item(self.create_item(self.laxia_starting_skills[0]))
        location = self.get_location("Laxia Starting Skill Skill 2 Wake Up!")
        location.place_locked_item(self.create_item(self.laxia_starting_skills[1]))
        location = self.get_location("Ricotta Starting Skill Skill 1 Wild Spin")
        location.place_locked_item(self.create_item(self.ricotta_starting_skills[0]))
        location = self.get_location("Ricotta Starting Skill Skill 2 Handmade Trap")
        location.place_locked_item(self.create_item(self.ricotta_starting_skills[1]))
        location = self.get_location("Hummel Starting Skill Skill 1 Burst Shot")
        location.place_locked_item(self.create_item(self.hummel_starting_skills[0]))
        location = self.get_location("Hummel Starting Skill Skill 2 Venomous Bullet")
        location.place_locked_item(self.create_item(self.hummel_starting_skills[1]))
        location = self.get_location("Dana Starting Skill Skill 1 Twin Edge")
        location.place_locked_item(self.create_item(self.dana_starting_skills[0]))
        location = self.get_location("Dana Starting Skill Skill 2 Sonic Rise")
        location.place_locked_item(self.create_item(self.dana_starting_skills[1]))

        locations_to_fill = len(self.multiworld.get_unfilled_locations(self.player))
        item_pool: List[Ys8Item] = []
        filler_pool: List[Ys8Item] = []

        # Always include all configured non-filler items so required progression cannot be dropped by pool size.
        # Use global item_table for deterministic iteration, then add landmarks separately if needed
        for name, data in item_table.items():
            if name in ["Essence Key Stone", "Jade Pendant"] and not self.options.former_sanctuary_crypt.value:
                continue
            if name == self.starting_character:
                continue
            if not self.options.discovery_sanity.value and data.category and data.category == "Landmark":
                continue
            if self.options.progressive_super_weapons.value and data.category and data.category == "Progressive Super Weapon":
                continue
            if not self.options.progressive_super_weapons.value and data.category and data.category == "Progressive Super Weapon":
                continue
            if name in self.starting_skills:
                continue
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
        for name, data in event_item_table.items():
            if name == "Melaiduma Defeated" and not self.options.former_sanctuary_crypt.value:
                continue
            if data.category in ["Psyches", "Psyches Access"]:
                continue
            if name in ["Psyche-Hydra Defeated", "Psyche-Minos Defeated", "Psyche-Nestor Defeated", "Psyche-Ura Defeated"] and self.options.final_boss_access.value == 2:
                continue
            location_name = data.category  # Using category field to store associated location for event items
            item = self.create_event(name)
            location = self.multiworld.get_location(location_name, self.player)
            location.place_locked_item(item)
        
        if self.options.final_boss_access == 2:  # Psyche Fight Shuffle
            psyche_access_item_table = {name: data for name, data in event_item_table.items() if data.category == "Psyches Access"}
            psyche_item_table = {name: data for name, data in event_item_table.items() if data.category == "Psyches"}
            for i, (access_item_name, psyche_item_name) in enumerate(zip(psyche_access_item_table.keys(), psyche_item_table.keys())):
                access_item = self.create_event(access_item_name)
                psyche_item = self.create_event(psyche_item_name)
                access_location = self.multiworld.get_location(list(self.chosen_psyche_location_list.keys())[i], self.player)
                psyche_location = self.multiworld.get_location(list(self.chosen_psyche_fight_list.keys())[i], self.player)
                access_location.place_locked_item(access_item)
                psyche_location.place_locked_item(psyche_item)

    def get_filler_item_name(self) -> str:
        weights = [data.weight for data in self.fillers.values()]
        return self.random.choices([filler for filler in self.fillers.keys()], weights)[0]

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = {}
        slot_options = ["final_boss_access", "octus_count_crew_mode", "octus_count_psyches_mode", "goal_count_crew_final_boss", "goal_count_psyches_final_boss",
                        "discovery_sanity", "dungeon_entrance_shuffle", "jewel_trade_items", "fish_trades", "food_trades", "map_completion", "discoveries", 
                        "dogi_intercept_rewards", "master_kong_rewards", "silvia_progression", "mephorash_progression", "former_sanctuary_crypt", "experience_multiplier", 
                        "additional_intercept_rewards", "battle_logic", "progressive_super_weapons", "octus_paths_opened", "extra_flame_stones", 
                        "recipes_with_ingredients", "north_side_open", "infinity_mode", "scale_exp_items", "final_boss", "theos_start_phase", "origin_care_package", "origin_start_phase",
                        "essence_key_sanity", "starting_character_weights", "death_link"]

        slot_data = {"options": {option_name: getattr(self.options, option_name).value for option_name in slot_options}}

        return slot_data

    def create_item(self, name: str) -> Ys8Item:
        data = item_table[name]
        return Ys8Item(name, data.classification, data.code, self.player)
    
    def create_event(self, name: str) -> Ys8Item:
        data = event_item_table[name]
        return Ys8Item(name, data.classification, data.code, self.player)
    
    def set_rules(self):
        set_all_rules(self)
    
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        player_name = self.multiworld.get_player_name(self.player)
        spoiler_handle.write(f"\n\nYs 8 Dungeon Entrance Randomization for {player_name}:\n")
        
        for entrance in self.entrance_spoiler:
            spoiler_handle.write(f"\t{entrance}\n")
        
        spoiler_handle.write(f"\n\nYs 8 Starting Character and Skills for {player_name}:\n")
        spoiler_handle.write(f"\tStarting Character: {self.starting_character}\n")
        spoiler_handle.write(f"\tAdol Starting Skills: {', '.join(self.adol_starting_skills)}\n")
        spoiler_handle.write(f"\tSahad Starting Skills: {', '.join(self.sahad_starting_skills)}\n")
        spoiler_handle.write(f"\tLaxia Starting Skills: {', '.join(self.laxia_starting_skills)}\n")
        spoiler_handle.write(f"\tRicotta Starting Skills: {', '.join(self.ricotta_starting_skills)}\n")
        spoiler_handle.write(f"\tHummel Starting Skills: {', '.join(self.hummel_starting_skills)}\n")
        spoiler_handle.write(f"\tDana Starting Skills: {', '.join(self.dana_starting_skills)}\n")

        if self.options.final_boss_access == 2:
            # Build mapping: psyche boss location → access item location
            fights = list(self.chosen_psyche_fight_list.keys())
            locations = list(self.chosen_psyche_location_list.keys())
            
            spoiler_handle.write(f"\n\nPsyche Fight Shuffle for {player_name}:\n")
            for fight_location, access_location in zip(fights, locations):
                spoiler_handle.write(f"\t{fight_location} is accessed by {access_location}\n")

    def generate_output(self, output_directory: str):
        generate_json(self, output_directory)
    
    

