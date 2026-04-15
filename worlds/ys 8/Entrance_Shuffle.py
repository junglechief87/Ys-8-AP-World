from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from . import Ys8World

def dungeon_entrance_shuffle(Ys8World, region_connections: Dict[str, list]):
    multiworld = Ys8World.multiworld

    dungeon_entrances: Dict[str, str] = {
        "Entrance: Waterdrop Cave": "Calm Inlet Area",
        "Entrance: Towering Coral Forest Front": "Nameless Coast North",
        "Entrance: Towering Coral Forest Boss Arena": "Metavolicalis Area",
        "Entrance: Eroded Valley Front": "Eroded Valley Front",
        "Entrance: Eroded Valley Boss Arena": "Sunrise Beach",
        "Entrance: Schlamm Jungle Front": "Schlamm Jungle Front",
        "Entrance: Schlamm Jungle Boss Arena": "Odd Rock Coast",
        "Entrance: Silent Tower": "Silent Tower",
        "Entrance: Mont Gendarme Front": "Mont Gendarme Front",
        "Entrance: Mont Gendarme Boss Arena": "Seiren North Access",
        "Entrance: Octus Overlook": "Octus Overlook",
        "Entrance: Former Sanctuary Crypt": "Former Sanctuary Crypt Front",
        "Entrance: Baja Tower": "Baja Tower Lower Floors",
        "Entrance: Archeozoic Chasm": "Archeozoic Chasm Front",
        "Entrance: Valley of Kings": "Valley of Kings Before Door",
    }
    
    dungeon_entrance_pairs: Dict[str, str] = {
        "Calm Inlet Area": "Entrance: Waterdrop Cave",
        "Nameless Coast North": "Entrance: Towering Coral Forest Front",
        "Metavolicalis Area": "Entrance: Towering Coral Forest Boss Arena",
        "Eroded Valley Front": "Entrance: Eroded Valley Front",
        "Sunrise Beach": "Entrance: Eroded Valley Boss Arena",
        "Schlamm Jungle Front": "Entrance: Schlamm Jungle Front",
        "Odd Rock Coast": "Entrance: Schlamm Jungle Boss Arena",
        "Nostalgia Cape Area": "East Coast Cave Before Gilkyra",
        "Silent Tower": "Entrance: Silent Tower",
        "Mont Gendarme Front": "Entrance: Mont Gendarme Front",
        "Seiren North Access": "Entrance: Mont Gendarme Boss Arena",
        "Octus Overlook": "Entrance: Octus Overlook",
        "Former Sanctuary Crypt Front": "Entrance: Former Sanctuary Crypt",
        "Baja Tower Lower Floors": "Entrance: Baja Tower",
        "Archeozoic Chasm Front": "Entrance: Archeozoic Chasm",
        "Valley of Kings Before Door": "Entrance: Valley of Kings"
    }

    # Shuffle the target regions for each entrance
    entrance_list = list(dungeon_entrances.keys())
    region_list = list(dungeon_entrances.values())
    multiworld.random.shuffle(region_list)
    
    original_entrances = dungeon_entrances.copy()
    shuffled_entrances = dict(zip(entrance_list, region_list))
    
    # Update region_connections with the shuffled entrances
    for entrance, old_region in original_entrances.items():
        new_region = shuffled_entrances[entrance]
        
        # Remove entrance from old region's connections
        if entrance in region_connections[old_region]:
            region_connections[old_region].remove(entrance)
        
        # Add entrance to new region's connections
        if entrance not in region_connections[new_region]:
            region_connections[new_region].append(entrance)
        
        # Update the dungeon_entrances mapping
        dungeon_entrances[entrance] = new_region
        
        # Update the reverse mapping (region to entrance)
        if old_region in dungeon_entrance_pairs and dungeon_entrance_pairs[old_region] == entrance:
            del dungeon_entrance_pairs[old_region]
        dungeon_entrance_pairs[new_region] = entrance
    

