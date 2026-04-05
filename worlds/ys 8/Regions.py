from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import Ys8Location, location_table

class Ys8RegionData(NamedTuple):
    locations: List[str]
    region_exits: Optional[List[str]]

def create_regions(Ys8World):
    multiworld = Ys8World.multiworld
    player     = Ys8World.player
    options    = Ys8World.options

    regions: Dict[str, Ys8RegionData] = {
        "Calm Inlet Area":      Ys8RegionData([],["Exit to Waterdrop Cave", "Exit to North of Boulder"]),
        "Waterdrop Cave":       Ys8RegionData([],["Exit to Calm Inlet Cave"]),
        "Nameless Coast North of Boulder": Ys8RegionData([], ["Exit to South of Boulder", "Exit to TCF Before Mid-Boss"]),
        "Towering Coral Forest Before Mid-Boss": Ys8RegionData([], ["Exit to TCF After Mid-Boss", "Exit to North of Boulder"]),
        "Towering Coral Forest After Mid-Boss": Ys8RegionData([], ["Exit to TCF Before Mid-Boss", "Exit After TCF Boss"]),
    }

    for location in location_table:
        print(location)
        regions[location_table[location].category].locations.append(location)
    
    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))

def connect_entrances(Ys8World):
    multiworld = Ys8World.multiworld
    player     = Ys8World.player
    options    = Ys8World.options
    
    multiworld.get_entrance("Exit to Calm Inlet Cave", player).connect(multiworld.get_region("Calm Inlet Area", player))
    multiworld.get_entrance("Exit to South of Boulder", player).connect(multiworld.get_region("Calm Inlet Area", player))
    multiworld.get_entrance("Exit to Waterdrop Cave", player).connect(multiworld.get_region("Waterdrop Cave", player))
    multiworld.get_entrance("Exit to North of Boulder", player).connect(multiworld.get_region("Nameless Coast North of Boulder", player))
    multiworld.get_entrance("Exit to TCF Before Mid-Boss", player).connect(multiworld.get_region("Nameless Coast North of Boulder", player))
    multiworld.get_entrance("Exit to TCF Before Mid-Boss", player).connect(multiworld.get_region("Towering Coral Forest Before Mid-Boss", player))
    multiworld.get_entrance("Exit to TCF After Mid-Boss", player).connect(multiworld.get_region("Towering Coral Forest After Mid-Boss", player))

def create_region(multiworld: MultiWorld, player: int, name: str, data: Ys8RegionData):
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = Ys8Location(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)

    if data.region_exits:
        for exit in data.region_exits:
            entrance = Entrance(player, exit, region)
            region.exits.append(entrance)

    return region