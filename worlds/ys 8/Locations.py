from typing import Dict, NamedTuple, Optional, Set
import typing

from BaseClasses import Location

class Ys8Location(Location):
    game: str = "Ys 8"

class Ys8LocationData(NamedTuple):
    category: str
    code: Optional[int] = None
    type: Optional[str] = None
    
def get_locations_by_type(type: str) -> Dict[str, Ys8LocationData]:
    return {name: data for name, data in location_table.items() if data.type == type}

location_table: Dict[str, Ys8LocationData] = {
    "Waterdrop Cave Living Space Chest 1":                                              Ys8LocationData("Waterdrop Cave", 378, "Chest"),
    "Waterdrop Cave Living Space Chest 2":                                              Ys8LocationData("Waterdrop Cave", 379, "Chest"),
    "Waterdrop Cave Before Boss Arena Chest":                                           Ys8LocationData("Waterdrop Cave", 380, "Chest")
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}

#Make location categories
location_name_groups: Dict[str, Set[str]] = {}
for location in location_table.keys():
    category = location_table[location].category
    if category not in location_name_groups.keys():
        location_name_groups[category] = set()
    location_name_groups[category].add(location)

    
