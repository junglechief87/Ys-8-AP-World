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
        "Calm Inlet Area":      Ys8RegionData([],["Waterdrop Cave"]),
        "Waterdrop Cave":       Ys8RegionData([],["Calm Inlet Area"])
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
    
    multiworld.get_entrance("Calm Inlet Area", player).connect(multiworld.get_region("Calm Inlet Area", player))
    multiworld.get_entrance("Waterdrop Cave", player).connect(multiworld.get_region("Waterdrop Cave", player))

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