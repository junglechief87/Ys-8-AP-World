"""
Archipelago init file for The Ys 8
"""
import dataclasses
from logging import error, warning
from typing import Any, Dict, List, Optional, cast
from BaseClasses import CollectionState, Entrance, ItemClassification, Location, Region, Tutorial
from Options import OptionError, PerGameCommonOptions, Toggle
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, Type, launch
from .Options import Ys8Options, Ys8_option_groups, Ys8_option_presets
from .Locations import Ys8Location, location_table, location_name_groups, chosen_psyche_fight_list, chosen_psyche_location_list
from .Items import Ys8Item, Ys8ItemData, get_item_pool_quantity, get_items_by_category, item_table, item_name_groups, psyche_item_table, psyche_access_item_table, event_item_table
from .Rules import set_all_rules
from .Regions import create_regions, connect_entrances

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
        from .Locations import extend_location_tables_with_fsc, extend_psyche_location_table_with_fsc_off, extend_location_tables_with_landmarks, extend_psyche_location_table_with_silent_tower
        from .Items import extend_item_tables_with_landmarks
        
        # Force Former Sanctuary Crypt on if Untouchable final boss access is selected
        if self.options.final_boss_access.value == 3:  # option_untouchable
            self.options.former_sanctuary_crypt.value = True
        
        # Adjust location tables based on options
        if self.options.former_sanctuary_crypt.value:
            extend_location_tables_with_fsc()
        else:
            extend_psyche_location_table_with_fsc_off()
        
        if self.options.mephorash_progression.value:
            extend_psyche_location_table_with_silent_tower()

        # Add landmark locations and items if Discovery Sanity is enabled
        if self.options.discovery_sanity.value:
            extend_item_tables_with_landmarks()
            extend_location_tables_with_landmarks()

    def create_regions(self):
        create_regions(self)

    def connect_entrances(self):
        connect_entrances(self)

    def create_items(self):
        self.place_predetermined_items()

        # Determine Starting Character and add to precollected items
        party = [item_name for item_name in item_table.keys() if item_table[item_name].is_party_member]
        starting_character = self.random.choice(party)
        item = self.create_item(starting_character)
        self.multiworld.push_precollected(item)

        if self.options.final_boss_access == 2:  # Psyche Fight Shuffle
            for i, (access_item_name, psyche_item_name) in enumerate(zip(psyche_access_item_table.keys(), psyche_item_table.keys())):
                access_item = self.create_item(access_item_name)
                psyche_item = self.create_item(psyche_item_name)
                access_location = self.multiworld.get_location(chosen_psyche_location_list[i], self.player)
                psyche_location = self.multiworld.get_location(chosen_psyche_fight_list[i], self.player)
                access_location.place_locked_item(access_item)
                psyche_location.place_locked_item(psyche_item)

        locations_to_fill = len(self.multiworld.get_unfilled_locations(self.player))
        item_pool: List[Ys8Item] = []
        filler_pool: List[Ys8Item] = []

        # Always include all configured non-filler items so required progression cannot be dropped by pool size.
        for name, data in item_table.items():
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
        for item_name in event_item_table.keys():
            location_name = event_item_table[item_name].category
            item = self.create_event(item_name)
            location = self.multiworld.get_location(location_name, self.player)
            location.place_locked_item(item)

    def get_filler_item_name(self) -> str:
        weights = [data.weight for data in self.fillers.values()]
        return self.random.choices([filler for filler in self.fillers.keys()], weights)[0]

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = {}
        slot_options = ["final_boss_access"]

        slot_data = {"options": {option_name: getattr(self.options, option_name).value for option_name in slot_options}}

        return slot_data

    def create_item(self, name: str) -> Ys8Item:
        data = item_table[name]
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
        data = event_item_table[name]
        return Ys8Item(name, data.classification, data.code, self.player)
    
    def set_rules(self):
        set_all_rules(self)

