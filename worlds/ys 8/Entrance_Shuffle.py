from typing import TYPE_CHECKING, Dict
from .Options import Ys8Options

if TYPE_CHECKING:
    from . import Ys8World

def build_paired_connections(Ys8World):
    paired_connections = {dungeon: field for field, dungeon in Ys8World.dungeon_connections.items()}
    Ys8World.dungeon_connections.update(paired_connections)

def dungeon_entrance_shuffle(Ys8World):
    options = Ys8World.options

    dungeon_connections = Ys8World.dungeon_connections
    
    two_way_connector_dungeon_entrances: Dict[str, str] = {
        "Towering Coral Forest Front":"Towering Coral Forest Boss Arena", "Towering Coral Forest Boss Arena":"Towering Coral Forest Front", 
        "Eroded Valley Front":"Eroded Valley Boss Arena", "Eroded Valley Boss Arena":"Eroded Valley Front", 
        "Schlamm Jungle Front":"Schlamm Jungle Boss Arena", "Schlamm Jungle Boss Arena":"Schlamm Jungle Front",
        "Mont Gendarme Front":"Mont Gendarme Boss Arena", "Mont Gendarme Boss Arena":"Mont Gendarme Front"}
    
    # Potentially growing list of locations based on settings
    isolated_regions = ["Odd Rock Coast"]
    if not options.discovery_sanity.value:
        isolated_regions.extend(["Sunrise Beach", "Metavolicalis Area"])

    # Shuffle the target regions for each entrance
    field_list = list(dungeon_connections.keys())
    dungeon_list = list(dungeon_connections.values())
    Ys8World.multiworld.random.shuffle(dungeon_list)
    
    original_connections = dungeon_connections.copy()
    new_dungeon_connections = {}
    placed_fields = set()

    while len(placed_fields) < len(field_list):
        for field in field_list:
            if field in placed_fields:
                continue
            
            placed = False
            for dungeon in dungeon_list:
                if dungeon in new_dungeon_connections.values():
                    continue
                
                if field in isolated_regions and dungeon not in two_way_connector_dungeon_entrances.keys():
                    continue
                if field in isolated_regions and dungeon in two_way_connector_dungeon_entrances.keys():
                    # Get the paired dungeon entrance and find which field it's assigned to
                    paired_dungeon_entrance = two_way_connector_dungeon_entrances[dungeon]
                    paired_field = None
                    for f, d in new_dungeon_connections.items():
                        if d == paired_dungeon_entrance:
                            paired_field = f
                            break
                    
                    # If paired field is also in isolated regions, we can't assign this dungeon to the current field
                    if paired_field in isolated_regions:
                        continue
                
                new_dungeon_connections[field] = dungeon
                placed_fields.add(field)
                placed = True
                break
            
            if not placed:
                # Failed to place this field, restart everything
                new_dungeon_connections = {}
                dungeon_list = list(dungeon_connections.values())
                Ys8World.multiworld.random.shuffle(dungeon_list)
                placed_fields = set()
                break
    
    Ys8World.dungeon_connections = new_dungeon_connections