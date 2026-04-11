"""
Archipelago init file for The Ys 8
"""
import dataclasses
from logging import error, warning
from typing import Any, Dict, List, Optional, cast
from BaseClasses import CollectionState, Entrance, Location, LocationProgressType, Region, Tutorial
from Options import OptionError, PerGameCommonOptions, Toggle
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, Type, launch
from .Options import Ys8Options, Ys8_option_groups, Ys8_option_presets
from .Locations import Ys8Location, location_table, location_name_groups
from .Items import Ys8Item, Ys8ItemData, get_items_by_category, item_table, item_name_groups, event_item_table
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
        pass

    def create_regions(self):
        create_regions(self)

    def connect_entrances(self):
        connect_entrances(self)

    def create_items(self):
        self.place_predetermined_items()

        # Determine Starting Character and add to precollected items
        party = [item_name for item_name in item_table.keys() if "Party" in item_table[item_name].flags]
        starting_character = self.random.choice(party)
        item = self.create_item(starting_character)
        self.multiworld.push_precollected(item, self.multiworld, self.player)

        LocationsToFill = len(self.multiworld.get_unfilled_locations(self.player))
        ItemPool = []
        for name, data in item_table.items():
            ItemPool.append(self.create_item(name) )
            if len(ItemPool) >= LocationsToFill:
                break

        while LocationsToFill >= len(ItemPool):
            ItemPool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += ItemPool
        print(self.multiworld.itempool)

    def place_predetermined_items(self):
        # Place event items that are required for progression or victory
        for item_name in event_item_table.keys():
            item = self.create_event(item_name)
            location = self.multiworld.get_location(event_item_table[item_name].category, self.player)
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
        return Ys8Item(name, data.classification, data.code, self.player)
    
    def create_event(self, name: str) -> Ys8Item:
        data = event_item_table[name]
        return Ys8Item(name, data.classification, data.code, self.player)
    
    def set_rules(self):
        set_all_rules(self)

