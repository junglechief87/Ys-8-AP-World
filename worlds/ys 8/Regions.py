from typing import Dict, List, NamedTuple, Optional, TYPE_CHECKING
from BaseClasses import MultiWorld, Region, Entrance
from .Locations import (Ys8Location, location_table, event_location_table, psyche_location_table, psyche_fight_names, 
                        chosen_psyche_fight_list, chosen_psyche_location_list)
from . import Locations
from .Entrance_Shuffle import dungeon_entrance_shuffle
import Locations

if TYPE_CHECKING:
    from . import Ys8World

class Ys8RegionData(NamedTuple):
    locations: List[str]
    region_exits: Optional[List[Dict[str, str]]]

regions: Dict[str, Ys8RegionData] = {}
region_connections: Dict[str, list] = {}

def create_regions(Ys8World):
    multiworld = Ys8World.multiworld
    player     = Ys8World.player
    options    = Ys8World.options

    region_connections = {
        "Calm Inlet Area": ["Entrance: Waterdrop Cave", "Nameless Coast North", "Towering Coral Forest Rainbow Falls", "Parasequoia Area", 
                            "Metavolicalis Area", "Calm Inlet: Intercept List 1", "Calm Inlet: Intercept List 2", "Calm Inlet: Intercept List 3", 
                            "Calm Inlet: Map Completion", "Calm Inlet: Jewel Trade", "Calm Inlet: Fish Trade", "Calm Inlet: Discovery Turn In", 
                            "Western Foot of Gendarme", "Great River Valley Area", "Milky White Vein", "Eroded Valley Indigo Mineral Vein", 
                            "Sunrise Beach", "Schlamm Jungle Field of Medicinal Herbs", "Beehive", "East Coast Cave Before Gilkyra", "Nostalgia Cape Area", 
                            "Weathervane Hills", "Solitude Island", "Lapis Mineral Vein Area", "Seiren North Access", "Soundless Hall", "Sky Garden",
                            "Graves of Ancient Heroes", "Towering Coral Forest (Night) Front Half"],
        "Calm Inlet: Intercept List 1": [],
        "Calm Inlet: Intercept List 2": [],
        "Calm Inlet: Intercept List 3": [],
        "Calm Inlet: Map Completion": [],
        "Calm Inlet: Jewel Trade": [],
        "Calm Inlet: Fish Trade": [],
        "Calm Inlet: Discovery Turn In": [],
        "Waterdrop Cave": ["Entrance: Waterdrop Cave"],
        "Nameless Coast North": ["Calm Inlet Area", "Entrance: Towering Coral Forest Front", "Great River Valley Area"],
        "Towering Coral Forest Front": ["Entrance: Towering Coral Forest Front", "Towering Coral Forest Mid-Boss Arena"],
        "Towering Coral Forest Mid-Boss Arena": ["Towering Coral Forest Front", "Towering Coral Forest Corpse"],
        "Towering Coral Forest Corpse": ["Towering Coral Forest Mid-Boss Arena", "Towering Coral Forest Rainbow Falls"],
        "Towering Coral Forest Rainbow Falls": ["Towering Coral Forest Front", "Towering Coral Forest Before Boss", "Towering Coral Forest Corpse"],
        "Towering Coral Forest Before Boss": ["Towering Coral Forest Front", "Towering Coral Forest Rainbow Falls", "Towering Coral Forest Boss Arena"],
        "Towering Coral Forest Boss Arena": ["Entrance: Towering Coral Forest Boss Arena", "Towering Coral Forest Before Boss"],
        "Metavolicalis Area": ["Entrance: Towering Coral Forest Boss Arena", "Parasequoia Area"],
        "Parasequoia Area": ["Metavolicalis Area"],
        "Great River Valley Area": ["Nameless Coast North", "Base of Western Foot of Gendarme", "Waterfall Grotto Dark Area", 
                                    "Longhorn Coast Area", "Entrance: Eroded Valley Front", "Entrance: Schlamm Jungle Front",
                                    "Primordial Passage"],
        "Base of Western Foot of Gendarme": ["Great River Valley Area", "Western Foot of Gendarme"],
        "Western Foot of Gendarme": ["Base of Western Foot of Gendarme"],
        "Milky White Vein": ["Waterfall Grotto Dark Area"],
        "Waterfall Grotto Dark Area": ["Milky White Vein", "Great River Valley Area"],
        "Longhorn Coast Area": ["Great River Valley Area", "Outside Silent Tower", "Nostalgia Cape Area", "Beehive"],
        "Beehive": ["Longhorn Coast Area"],
        "Eroded Valley Front": ["Entrance: Eroded Valley Front", "Eroded Valley Dark Area", "Eroded Valley Mid-Boss Arena"],
        "Eroded Valley Dark Area": ["Eroded Valley Front", "Eroded Valley Indigo Mineral Vein"],
        "Eroded Valley Indigo Mineral Vein": ["Eroded Valley Dark Area"],
        "Eroded Valley Mid-Boss Arena": ["Eroded Valley Front", "Eroded Valley Webbed Walkway"],
        "Eroded Valley Webbed Walkway": ["Eroded Valley Front", "Eroded Valley Before Boss", "Eroded Valley Mid-Boss Arena"],
        "Eroded Valley Before Boss": ["Eroded Valley Webbed Walkway", "Eroded Valley Boss Arena"],
        "Eroded Valley Boss Arena": ["Eroded Valley Before Boss", "Entrance: Eroded Valley Boss Arena"],
        "Sunrise Beach": ["Entrance: Eroded Valley Boss Arena"],
        "Schlamm Jungle Front": ["Entrance: Schlamm Jungle Front", "Schlamm Jungle Mid-Boss Arena"],
        "Schlamm Jungle Mid-Boss Arena": ["Schlamm Jungle Front", "Schlamm Jungle Muddy Path"],
        "Schlamm Jungle Muddy Path": ["Schlamm Jungle Mid-Boss Arena", "Schlamm Jungle Before Boss", "Schlamm Jungle Field of Medicinal Herbs"],
        "Schlamm Jungle Field of Medicinal Herbs": ["Schlamm Jungle Muddy Path"],
        "Schlamm Jungle Before Boss": ["Schlamm Jungle Muddy Path", "Schlamm Jungle Boss Arena"],
        "Schlamm Jungle Boss Arena": ["Schlamm Jungle Before Boss", "Entrance: Schlamm Jungle Boss Arena"],
        "Odd Rock Coast": ["Entrance: Schlamm Jungle Boss Arena"],
        "Nostalgia Cape Area": ["Longhorn Coast Area", "East Coast Cave Before Gilkyra"],
        "East Coast Cave Before Gilkyra": ["Nostalgia Cape Area", "East Coast Cave After Gilkyra"],
        "East Coast Cave After Gilkyra": ["East Coast Cave Before Gilkyra", "Pirate Ship Eleftheria"],
        "Pirate Ship Eleftheria": ["East Coast Cave After Gilkyra", "Pirate Ship Eleftheria Submerged Hold"],
        "Pirate Ship Eleftheria Submerged Hold": ["Pirate Ship Eleftheria"],
        "Primordial Passage": ["Great River Valley Area", "Entrance: Mont Gendarme Front", "Mont Gendarme (Night) Front Half"],
        "Outside Silent Tower": ["Longhorn Coast Area", "Entrance: Silent Tower"],
        "Silent Tower": ["Entrance: Silent Tower"],
        "Solitude Island": [],
        "Weathervane Hills": ["Weathervane Hills Past Insect Nests", "Underground Water Vein"],
        "Weathervane Hills Past Insect Nests": ["Weathervane Hills"],
        "Underground Water Vein": ["Weathervane Hills", "Lapis Mineral Vein Area"],
        "Lapis Mineral Vein Area": ["Underground Water Vein"],
        "Mont Gendarme Front": ["Entrance: Mont Gendarme Front", "Mont Gendarme Middle"],
        "Mont Gendarme Middle": ["Mont Gendarme Front", "Mont Gendarme Mid-Boss Arena"],
        "Mont Gendarme Mid-Boss Arena": ["Mont Gendarme Middle", "Mont Gendarme Upper"],
        "Mont Gendarme Upper": ["Mont Gendarme Mid-Boss Arena", "Mont Gendarme Boss Arena"],
        "Mont Gendarme Boss Arena": ["Mont Gendarme Upper", "Entrance: Mont Gendarme Boss Arena"],
        "Seiren North Access": ["Entrance: Mont Gendarme Boss Arena", "Stone Pillar Wind Cave", "Temple of the Great Tree", "Ruins of Eternia", 
                                "Pangaia Plains (Night)"],
        "Stone Pillar Wind Cave": ["Seiren North Access", "Stone Pillar Wind Cave Upper"],
        "Stone Pillar Wind Cave Upper": ["Stone Pillar Wind Cave"],
        "Temple of the Great Tree": ["Seiren North Access", "Temple of the Great Tree Boss Arena", "Ruins of Eternia", "Vista Ridge"],
        "Temple of the Great Tree Boss Arena": ["Temple of the Great Tree", "Temple of the Great Tree Garden"],
        "Temple of the Great Tree Garden": ["Temple of the Great Tree Boss Arena", "Entrance: Octus Overlook"],
        "Octus Overlook": ["Entrance: Octus Overlook", "Selection Sphere"],
        "Selection Sphere": ["Octus Overlook"],
        "Ruins of Eternia": ["Seiren North Access", "Temple of the Great Tree", "Entrance: Archeozoic Chasm", "Towal Highway", "Entrance: Former Sanctuary Crypt", "Bolado Monastery"],
        "Bolado Monastery":["Ruins of Eternia", "Bolado Monastery Basement"],
        "Bolado Monastery Basement": ["Bolado Monastery"],
        "Former Sanctuary Crypt Front": ["Entrance: Former Sanctuary Crypt", "Former Sanctuary Crypt First Barrier"],
        "Former Sanctuary Crypt First Barrier": ["Former Sanctuary Crypt Front", "Former Sanctuary Crypt Second Floor", 
                                                                   "Former Sanctuary Crypt First Barrier North Brazier Room"],
        "Former Sanctuary Crypt First Barrier North Brazier Room": ["Former Sanctuary Crypt First Barrier"],
        "Former Sanctuary Crypt Second Floor": ["Former Sanctuary Crypt First Barrier", "Former Sanctuary Crypt Second Barrier"],
        "Former Sanctuary Crypt Second Barrier": ["Former Sanctuary Crypt Second Floor", "Former Sanctuary Crypt Second Boss Arena"],
        "Former Sanctuary Crypt Second Boss Arena": ["Former Sanctuary Crypt Second Barrier", "Former Sanctuary Crypt Third Floor"],
        "Former Sanctuary Crypt Third Floor": ["Former Sanctuary Crypt Second Boss Arena", "Former Sanctuary Crypt Third Barrier", "Former Sanctuary Crypt Third Floor Side Rooms"],
        "Former Sanctuary Crypt Third Floor Side Rooms": ["Former Sanctuary Crypt Third Floor"],
        "Former Sanctuary Crypt Third Barrier": ["Former Sanctuary Crypt Third Floor", "Former Sanctuary Crypt Final Floors"],
        "Former Sanctuary Crypt Final Floors": ["Former Sanctuary Crypt Third Barrier", "Former Sanctuary Crypt Boss Room", "Former Sanctuary Crypt Final Floors Side Rooms"],
        "Former Sanctuary Crypt Final Floors Side Rooms": ["Former Sanctuary Crypt Final Floors"],
        "Former Sanctuary Crypt Boss Room": ["Former Sanctuary Crypt Final Floors"],
        "Towal Highway": ["Ruins of Eternia", "Entrance: Baja Tower"],
        "Baja Tower Lower Floors": ["Entrance: Baja Tower", "Baja Tower Upper Floors"],
        "Baja Tower Upper Floors": ["Baja Tower Lower Floors", "Baja Tower Boss Arena"],
        "Baja Tower Boss Arena": ["Baja Tower Upper Floors"],
        "Archeozoic Chasm Front": ["Entrance: Archeozoic Chasm", "Archeozoic Chasm Submerged Area"],
        "Archeozoic Chasm Submerged Area": ["Archeozoic Chasm Front", "Archeozoic Chasm Boss Arena"],
        "Archeozoic Chasm Boss Arena": ["Archeozoic Chasm Submerged Area"],
        "Vista Ridge": ["Temple of the Great Tree", "Vista Ridge Upper", "Lodinia Marshlands Front"],
        "Vista Ridge Upper": ["Vista Ridge"],
        "Lodinia Marshlands Front": ["Vista Ridge", "Lodinia Marshlands South", "Lodinia Marshlands Near Submerged Cemetery"],
        "Lodinia Marshlands South": ["Lodinia Marshlands Front"],
        "Lodinia Marshlands Near Submerged Cemetery": ["Lodinia Marshlands Front", "Submerged Cemetery", "Lodinia Marshlands Near Sky Garden"],
        "Lodinia Marshlands Near Sky Garden": ["Lodinia Marshlands Near Submerged Cemetery", "Sky Garden", "Lodinia Marshlands Back"],
        "Lodinia Marshlands Back": ["Lodinia Marshlands Near Sky Garden", "Entrance: Valley of Kings", "Graves of Ancient Heroes"],
        "Valley of Kings Before Door": ["Entrance: Valley of Kings", "Valley of Kings After Door"],
        "Valley of Kings After Door": ["Valley of Kings Before Door", "Valley of Kings Boss Arena"],
        "Valley of Kings Boss Arena": ["Valley of Kings After Door"],
        "Graves of Ancient Heroes": ["Lodinia Marshlands Back"],
        "Sky Garden": ["Lodinia Marshlands Near Sky Garden"],
        "Submerged Cemetery": ["Lodinia Marshlands Near Submerged Cemetery", "Bolado Monastery Hidden Room", "Soundless Hall"],
        "Soundless Hall": ["Submerged Cemetery"],
        "Bolado Monastery Hidden Room": ["Submerged Cemetery"],
        "Towering Coral Forest (Night) Front Half": ["Towering Coral Forest (Night) Rear Half"],
        "Towering Coral Forest (Night) Rear Half": ["Towering Coral Forest (Night) Front Half"],
        "Mont Gendarme (Night) Front Half": ["Primordial Passage", "Mont Gendarme (Night) Rear Half"],
        "Mont Gendarme (Night) Rear Half": ["Mont Gendarme (Night) Front Half"],
        "Pangaia Plains (Night)": ["Seiren North Access"],
        "Entrance: Waterdrop Cave": ["Calm Inlet Area", "Waterdrop Cave"],
        "Entrance: Towering Coral Forest Front": ["Nameless Coast North", "Towering Coral Forest Front"],
        "Entrance: Towering Coral Forest Boss Arena": ["Towering Coral Forest Boss Arena", "Metavolicalis Area"],
        "Entrance: Eroded Valley Front": ["Great River Valley Area", "Eroded Valley Front"],
        "Entrance: Eroded Valley Boss Arena": ["Eroded Valley Boss Arena", "Sunrise Beach"],
        "Entrance: Schlamm Jungle Front": ["Schlamm Jungle Front", "Great River Valley Area"],
        "Entrance: Schlamm Jungle Boss Arena": ["Odd Rock Coast", "Schlamm Jungle Boss Arena"],
        "Entrance: Silent Tower": ["Silent Tower", "Outside Silent Tower"],
        "Entrance: Mont Gendarme Front": ["Primordial Passage", "Mont Gendarme Front"],
        "Entrance: Mont Gendarme Boss Arena": ["Seiren North Access", "Mont Gendarme Boss Arena"],
        "Entrance: Octus Overlook": ["Temple of the Great Tree Garden", "Octus Overlook"],
        "Entrance: Former Sanctuary Crypt": ["Ruins of Eternia", "Former Sanctuary Crypt Front"],
        "Entrance: Baja Tower": ["Towal Highway", "Baja Tower Lower Floors"],
        "Entrance: Archeozoic Chasm": ["Ruins of Eternia", "Archeozoic Chasm Front"],
        "Entrance: Valley of Kings": ["Valley of Kings Before Door", "Lodinia Marshlands Back"],
    }

    # Shuffle entrances if enabled
    if options.entrance_shuffle:
        dungeon_entrance_shuffle(Ys8World, region_connections)

    for region in region_connections:
        connections = [{region_exit: region + " to " + region_exit} for region_exit in region_connections[region]]
        regions[region] = Ys8RegionData([], connections)
    
    for location in location_table:
        regions[location_table[location].category].locations.append(location)

    for location in event_location_table:
        regions[event_location_table[location].category].locations.append(location)

    if options.final_boss_access == 2:  # Psyche Fight Shuffle
        psyche_num = 4
        fight_samples = multiworld.random.sample(list(psyche_fight_names.items()), psyche_num)
        location_samples = multiworld.random.sample(list(psyche_location_table.items()), psyche_num)
        
        chosen_psyche_fight_list[:] = [name for name, _ in fight_samples]
        chosen_psyche_location_list[:] = [name for name, _ in location_samples]
        
        for (fight_name, fight_data), (location_name, location_data) in zip(fight_samples, location_samples):
            regions[fight_data.category].locations.append(fight_name)
            regions[location_data.category].locations.append(location_name)

    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))

def connect_entrances(Ys8World: "Ys8World"):
    multiworld = Ys8World.multiworld
    player     = Ys8World.player
    
    def connect(entrance_name: str, region_name: str):
        multiworld.get_entrance(entrance_name, player).connect(multiworld.get_region(region_name, player))
    
    for region, exits in region_connections.items():
        for region_exit in exits:
            connect(region + " to " + region_exit, region_exit)

def create_region(multiworld: MultiWorld, player: int, name: str, data: Ys8RegionData):
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = Ys8Location(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)

    if data.region_exits:
        for exit_dict in data.region_exits:
            for connector_name in exit_dict.values():
                entrance = Entrance(player, connector_name, region)
                region.exits.append(entrance)

    return region