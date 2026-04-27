import os
import io
from typing import TYPE_CHECKING, Dict, List, Optional, cast
import Utils
import zipfile
import json

from settings import get_settings
from .Locations import Ys8Location, location_table, event_location_table
from .Items import item_table, event_item_table
from worlds.Files import APPlayerContainer


class Ys8Container(APPlayerContainer):
    game: str = 'Ys 8'
    patch_file_ending = ".dana"

    def __init__(
        self,
        patch_data: Dict[str, str] | io.BytesIO,
        base_path: str = "",
        output_directory: str = "",
        player: Optional[int] = None,
        player_name: str = "",
        server: str = "",
    ):
        self.patch_data = patch_data
        self.file_path = base_path
        container_path = os.path.join(output_directory, base_path + self.patch_file_ending)
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for filename, text in self.patch_data.items():
            opened_zipfile.writestr(filename, text)
        super().write_contents(opened_zipfile)

def generate_json(world, output_directory):
    mod_name = f"AP-{world.multiworld.seed_name}-P{world.player}-{world.multiworld.get_file_safe_player_name(world.player)}"
    mod_dir = os.path.join(output_directory, mod_name + "_" + Utils.__version__)

    item_location_map = get_item_location_map(world)
    settings = get_settings(world)

    files = {
        "item_location_map.json": json.dumps(item_location_map),
        "starting_character.json": json.dumps(world.starting_character),
        "dungeon_entrance_randomization.json": json.dumps(world.dungeon_connections),
        "settings.json": json.dumps(settings),
    }

    mod = Ys8Container(
        files,
        mod_dir,
        output_directory,
        world.player,
        world.multiworld.get_file_safe_player_name(world.player),
    )
    mod.write()

def get_item_location_map(world):
    location_item_map = {}
    for location in world.multiworld.get_filled_locations(world.player):
        location_id = get_location_id(location)
        if location.item.code is None:
                continue
        item_data = get_item_data(location.item.name)
        location_item_map[location_id] = {
            "player": world.multiworld.get_player_name(location.item.player),
            "location_name": location.name,
            "location_type": location_table[location.name].type if location.name in location_table else "",
            # Convert item code to item ID by removing the last two digits,
            # if offworld item make AP item code. If item code is None, set to None.
            "item_id": (((location.item.code - (location.item.code % 100)) // 100) if location.item.player == location.player else 149),
            "item_name": location.item.name,
            "item_quantity": item_data.quantity if item_data else 1,
            "item_type": item_data.type if item_data else "",
            "category": item_data.category if item_data else "",
            "party_flag": item_data.is_party_member if item_data else False,
        }
    return location_item_map

def get_item_data(item_name):
    return item_table.get(item_name) or event_item_table.get(item_name)

def get_location_id(location):
    if isinstance(location.address, int):
        return location.address
    location_data = location_table.get(location.name)
    if location_data:
        return location_data.code
    event_location_data = event_location_table.get(location.name)
    return event_location_data.code if event_location_data else None

def get_settings(world):
    settings = world.fill_slot_data() or {}
    settings["seed"] = world.multiworld.seed

    # If Release the Psyches mode is enabled, include a map of psyche bosses
    # and where their access items are placed    
    if world.options.final_boss_access == 2:
        # Build mapping: psyche boss location → access item location
        fights = list(world.chosen_psyche_fight_list.keys())
        locations = list(world.chosen_psyche_location_list.keys())
        
        psyche_map = {}
        psyche_rewards = {}
        for fight_location, access_location in zip(fights, locations):
            location = world.multiworld.get_location(fight_location, world.player)
            item_name = location.item.name if location.item else None
            psyche_map[fight_location] = access_location
            psyche_rewards[fight_location] = item_name
        
        settings["psyche_map"] = psyche_map
        settings["psyche_rewards"] = psyche_rewards
    
    return settings