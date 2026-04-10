from typing import Dict, List, NamedTuple, Optional, TYPE_CHECKING
from BaseClasses import MultiWorld, Region, Entrance
from .Locations import Ys8Location, location_table

if TYPE_CHECKING:
    from . import Ys8World

class Ys8RegionData(NamedTuple):
    locations: List[str]
    region_exits: Optional[List[str]]

def create_regions(Ys8World):
    multiworld = Ys8World.multiworld
    player     = Ys8World.player
    options    = Ys8World.options

    regions: Dict[str, Ys8RegionData] = {
        "Calm Inlet Area": Ys8RegionData([],["CIA to WC", "CIA to NC North of Boulder", "CIA to Rainbow Falls", "CIA to Parasequoia", 
                                             "CIA to Metavolicalis", "CIA to IL 1", "CIA to IL 2", "CIA to IL 3", "CIA to Map Completion", 
                                             "CIA to Jewel Trade", "CIA to Fish Trade", "CIA to Discovery Turn In", "CIA to Airs Cairn", 
                                             "CIA to Chimney Rock", "CIA to Milky White Vein", "CIA to Indigo Mineral Vein", "CIA to Beached Remains",
                                             "CIA to FoMH", "CIA to Beehive", "CIA to Hidden Pirate Storehouse", "CIA to Ship Graveyard", "CIA to WH",
                                             "CIA to Zephyr Hill", "CIA to Solitude Island", "CIA to Lapis Mineral Vein Area", "CIA to Prismatic Mineral Vein", 
                                             "CIA to Unicalamites", "CIA to Breath Fountain", "CIA to Ancient Tree"]),
        "Calm Inlet: Intercept List 1": Ys8RegionData([], ["IL 1 to CIA"]),
        "Calm Inlet: Intercept List 2": Ys8RegionData([], ["IL 2 to CIA"]),
        "Calm Inlet: Intercept List 3": Ys8RegionData([], ["IL 3 to CIA"]),
        "Calm Inlet: Map Completion": Ys8RegionData([], ["Map Completion to CIA"]),
        "Calm Inlet: Jewel Trade": Ys8RegionData([], ["Jewel Trade to CIA"]),
        "Calm Inlet: Fish Trade": Ys8RegionData([], ["Fish Trade to CIA"]),
        "Calm Inlet: Discovery Turn In": Ys8RegionData([], ["Discovery Turn In to CIA"]),
        "Waterdrop Cave": Ys8RegionData([],["WC to CIA"]),
        "Nameless Coast North of Boulder": Ys8RegionData([], ["NC North of Boulder to NC South of Boulder", "TCF Front", "NC North of Boulder to GRV"]),
        "Towering Coral Forest Front": Ys8RegionData([], ["TCF Exit to NC", "TCF Front to TCF Mid-Boss Area"]),
        "Towering Coral Forest Mid-Boss Arena": Ys8RegionData([], ["TCF Mid-Boss Arena to TCF Front", "TCF Mid-Boss Arena to TCF Corpse"]),
        "Towering Coral Forest Corpse": Ys8RegionData([], ["TCF Corpse to TCF Mid-Boss Area", "TCF Corpse to TCF RF"]),
        "Towering Coral Forest Rainbow Falls": Ys8RegionData([], ["Rainbow Falls to CIA", "Rainbow Falls to TCF Front", "Rainbow Falls to TCF Boss Area", 
                                                                  "Rainbow Falls to TCF Corpse"]),
        "Towering Coral Forest Boss Area": Ys8RegionData([], ["TCF Boss Area to TCF Front", "TCF Boss Area to TCF RF", "TCF Boss Area to TCF Boss"]),
        "Towering Coral Forest Boss Arena": Ys8RegionData([], ["TCF Exit to Meta Area", "TCF Boss to TCF Boss Area"]),
        "Metavolicalis Area": Ys8RegionData([], ["TCF Back", "Meta Area to Para Area", "Metavolicalis to CIA"]),
        "Parasequoia Area": Ys8RegionData([], ["Para Area to Meta Area","Parasequoia to CIA"]),
        "Great River Valley Area": Ys8RegionData([], ["GRV to NC North of Boulder", "GRV to Base of WF Gendarme", "Chimney Rock to CIA", "GRV to WG Dark Area",
                                                      "GRV to LCA", "GRV to EV Front", "GRV to SJ Front", "GRV to PP"]),
        "Base of Western Foot of Gendarme": Ys8RegionData([], ["Base of WF Gendarme to GRV", "Base of WF Gendarme to WF Gendarme"]),
        "Western Foot of Gendarme": Ys8RegionData([], ["WF Gendarme to Base of WF Gendarme", "Airs Cairn to CIA"]),
        "Milky White Vein": Ys8RegionData([], ["Milky White Vein to CIA", "Milky White Vein to WG Dark Area"]),
        "Waterfall Grotto Dark Area": Ys8RegionData([], ["WG Dark Area to Milky White Vein", "WG Dark Area to GRV"]),
        "Longhorn Coast Area": Ys8RegionData([], ["LCA to GRV", "LCA to Outside ST", "LCA to Nostalgia Cape", "LCA to Beehive"]),
        "Beehive": Ys8RegionData([], ["Beehive to LCA", "Beehive to CIA"]),
        "Eroded Valley Front": Ys8RegionData([], ["EV Front to GRV", "EV Front to EV Dark Area", "EV Front to EV Mid-Boss Arena"]),
        "Eroded Valley Dark Area": Ys8RegionData([], ["EV Dark Area to EV Front", "EV Dark Area to EV Indigo Mineral Vein"]),
        "Eroded Valley Indigo Mineral Vein": Ys8RegionData([], ["EV Indigo Mineral Vein to EV Dark Area", "Indigo Mineral Vein to CIA"]),
        "Eroded Valley Mid-Boss Arena": Ys8RegionData([], ["EV Mid-Boss Arena to EV Front", "EV Mid-Boss Arena to EV Webbed Walkway"]),
        "Eroded Valley Webbed Walkway": Ys8RegionData([], ["EV Webbed Walkway to EV Front", "EV Webbed Walkway to EV Before Boss", "EV Webbed Walkway to EV Mid-Boss Arena"]),
        "Eroded Valley Before Boss": Ys8RegionData([], ["EV Before Boss to EV Webbed Walkway", "EV Before Boss to EV Boss Arena"]),
        "Eroded Valley Boss Arena": Ys8RegionData([], ["EV Boss Arena to EV Before Boss", "EV Boss Arena to SB"]),
        "Sunrise Beach": Ys8RegionData([], ["SB to EV Boss Arena", "Beached Remains to CIA"]),
        "Schlamm Jungle Front": Ys8RegionData([], ["SJ Front to GRV", "SJ Front to SJ Mid-Boss Arena"]),
        "Schlamm Jungle Mid-Boss Arena": Ys8RegionData([], ["SJ Mid-Boss Arena to SJ Front", "SJ Mid-Boss Arena to SJ Muddy Path"]),
        "Schlamm Jungle Muddy Path": Ys8RegionData([], ["SJ Muddy Path to SJ Mid-Boss Arena", "SJ Muddy Path to SJ Before Boss", "SJ Muddy Path to SJ FoMH"]),
        "Schlamm Jungle Field of Medicinal Herbs": Ys8RegionData([], ["SJ FoMH to SJ Muddy Path", "SJ FoMH to CIA"]),
        "Schlamm Jungle Before Boss": Ys8RegionData([], ["SJ Before Boss to SJ Muddy Path", "SJ Before Boss to SJ Boss Arena"]),
        "Schlamm Jungle Boss Arena": Ys8RegionData([], ["SJ Boss Arena to SJ Before Boss", "SJ Boss Arena to ORC"]),
        "Odd Rock Coast": Ys8RegionData([], ["ORC to SJ Boss Arena"]),
        "Nostalgia Cape Area": Ys8RegionData([], ["Nostalgia Cape to LCA", "Nostalgia Cape to ECC", "Ship Graveyard to CIA"]),
        "East Coast Cave Before Gilkyra": Ys8RegionData([], ["ECC to Nostalgia Cape", "ECC BG to ECC AG", "Hidden Pirate Storehouse to CIA"]),
        "East Coast Cave After Gilkyra": Ys8RegionData([], ["ECC AG to ECC BG", "ECC AG to PSE"]),
        "Pirate Ship Eleftheria": Ys8RegionData([], ["PSE to ECC AG", "PSE to PSE Submerged Hold"]),
        "Pirate Ship Eleftheria Submerged Hold": Ys8RegionData([], ["PSE Submerged Hold to PSE"]),
        "Primordial Passage": Ys8RegionData([], ["PP to GRV", "PP to MG"]),
        "Outside Silent Tower": Ys8RegionData([], ["Outside ST to LCA", "Outside ST to ST"]),
        "Silent Tower": Ys8RegionData([], ["ST to Outside ST"]),
        "Solitude Island": Ys8RegionData([], ["Solitude Island to CIA"]),
        "Weathervane Hills": Ys8RegionData([], ["WH to CIA", "Zephyr Hill to CIA", "WH to WH Past Insect Nests", "WH to UMV"]),
        "WH Past Insect Nests": Ys8RegionData([], ["WH Past Insect Nests to WH"]),
        "Underground Water Vein": Ys8RegionData([], ["UWV to WH", "UWV to Lapis Mineral Vein Area"]),
        "Lapis Mineral Vein Area": Ys8RegionData([], ["Lapis Mineral Vein Area to UWV", "Lapis Mineral Vein Area to CIA"]),
        "Mont Gendarme Front": Ys8RegionData([], ["MG to PP", "MG Front to MG Mid"]),
        "Mont Gendarme Middle": Ys8RegionData([], ["MG Mid to MG Front", "MG Mid to MG Mid-Boss Arena"]),
        "Mont Gendarme Mid-Boss Arena": Ys8RegionData([], ["MG Mid-Boss Arena to MG Mid", "MG Mid-Boss Arena to MG Upper"]),
        "Mont Gendarme Upper": Ys8RegionData([], ["MG Upper to MG Mid-Boss Arena", "MG Upper to MG Boss Arena"]),
        "Mont Gendarme Boss Arena": Ys8RegionData([], ["MG Boss Arena to MG Upper", "MG Boss Arena to Seiren North"]),
        # WIP
        "Seiren North Access": Ys8RegionData([], ["Seiren North to MG Boss Arena", "Seiren North to SPWC", "Seiren North to TotGT", "Seiren North to RoE", 
                                                  "Prismatic Mineral Vein to CIA", "Unicalamites to CIA", "Breath Fountain to CIA", "Ancient Tree to CIA"]),
        "Stone Pillar Wind Cave": Ys8RegionData([], []),
        "Temple of the Great Tree": Ys8RegionData([], []),
        "Temple of the Great Tree Boss Arena": Ys8RegionData([], []),
        "Temple of the Great Tree Gardenden": Ys8RegionData([], []),
        "Octus Overlook": Ys8RegionData([], []),
        "Selection Sphere": Ys8RegionData([], []),
        "Ruins of Eternia": Ys8RegionData([], []),
        "Towal Highway": Ys8RegionData([], []),
    }

    for location in location_table:
        print(location)
        regions[location_table[location].category].locations.append(location)
    
    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))

def connect_entrances(Ys8World: Ys8World):
    multiworld = Ys8World.multiworld
    player     = Ys8World.player
    options    = Ys8World.options
    
    def connect(entrance_name: str, region_name: str):
        multiworld.get_entrance(entrance_name, player).connect(multiworld.get_region(region_name, player))
    
    # Calm Inlet Area Connections
    connect("CIA to WC", "Waterdrop Cave")
    connect("CIA to NC North of Boulder", "Nameless Coast North of Boulder")
    connect("CIA to Rainbow Falls", "Towering Coral Forest Rainbow Falls")
    connect("CIA to Parasequoia", "Parasequoia Area")
    connect("CIA to Metavolicalis", "Metavolicalis Area")
    connect("CIA to IL 1", "Calm Inlet: Intercept List 1")
    connect("CIA to IL 2", "Calm Inlet: Intercept List 2")
    connect("CIA to IL 3", "Calm Inlet: Intercept List 3")
    connect("CIA to Map Completion", "Calm Inlet: Map Completion")
    connect("CIA to Jewel Trade", "Calm Inlet: Jewel Trade")
    connect("CIA to Fish Trade", "Calm Inlet: Fish Trade")
    connect("CIA to Discovery Turn In", "Calm Inlet: Discovery Turn In")
    connect("CIA to Airs Cairn", "Western Foot of Gendarme")
    connect("CIA to Chimney Rock", "Great River Valley Area")
    connect("CIA to Beached Remains", "Sunrise Beach")
    connect("CIA to Milky White Vein", "Milky White Vein")
    connect("CIA to Beehive", "Beehive")
    connect("CIA to FoMH", "Schlamm Jungle Field of Medicinal Herbs")
    connect("CIA to Hidden Pirate Storehouse", "East Coast Cave Before Gilkyra")
    connect("CIA to Ship Graveyard", "Nostalgia Cape Area")
    connect("CIA to WH", "Weathervane Hills")
    connect("CIA to Zephyr Hill", "Weathervane Hills")
    connect("CIA to Solitude Island", "Solitude Island")
    connect("CIA to Lapis Mineral Vein Area", "Lapis Mineral Vein Area")
    connect("CIA to Prismatic Mineral Vein", "Seiren North Access")
    connect("CIA to Unicalamites", "Seiren North Access")
    connect("CIA to Breath Fountain", "Seiren North Access")
    connect("CIA to Ancient Tree", "Seiren North Access")
    
    # Calm Inlet NPC Connections
    connect("Jewel Trade to CIA", "Calm Inlet Area")
    connect("Fish Trade to CIA", "Calm Inlet Area")
    connect("Discovery Turn In to CIA", "Calm Inlet Area")
    connect("Map Completion to CIA", "Calm Inlet Area")
    connect("IL 1 to CIA", "Calm Inlet Area")
    connect("IL 2 to CIA", "Calm Inlet Area")
    connect("IL 3 to CIA", "Calm Inlet Area")
    
    # Waterdrop Cave Connections
    connect("WC to CIA", "Calm Inlet Area")
    
    # Nameless Coast North of Boulder Connections
    connect("NC North of Boulder to NC South of Boulder", "Calm Inlet Area")
    connect("TCF Front", "Towering Coral Forest Front")
    connect("NC North of Boulder to GRV", "Great River Valley Area")
    
    # Towering Coral Forest Connections
    connect("TCF Exit to NC", "Nameless Coast North of Boulder")
    connect("TCF Front to TCF Mid-Boss Arena", "Towering Coral Forest Mid-Boss Arena")
    connect("TCF Mid-Boss Arena to TCF Front", "Towering Coral Forest Front")
    connect("TCF Mid-Boss Arena to TCF Corpse", "Towering Coral Forest Corpse")
    connect("TCF Corpse to TCF Mid-Boss Area", "Towering Coral Forest Mid-Boss Arena")
    connect("TCF Corpse to TCF RF", "Towering Coral Forest Rainbow Falls")
    connect("Rainbow Falls to TCF Corpse", "Towering Coral Forest Corpse")
    connect("Rainbow Falls to TCF Boss Area", "Towering Coral Forest Boss Area")
    connect("Rainbow Falls to CIA", "Calm Inlet Area")
    connect("Rainbow Falls to TCF Front", "Towering Coral Forest Front")
    connect("TCF Boss Area to TCF Front", "Towering Coral Forest Front")
    connect("TCF Boss Area to TCF RF", "Towering Coral Forest Rainbow Falls")
    connect("TCF Boss Area to TCF Boss", "Towering Coral Forest Boss Arena")
    connect("TCF Boss to TCF Boss Area", "Towering Coral Forest Boss Area")
    connect("TCF Exit to Meta Area", "Metavolicalis Area")
    
    # Metavolicalis Connections
    connect("TCF Back", "Towering Coral Forest Boss Area")
    connect("Meta Area to Para Area", "Parasequoia Area")
    connect("Metavolicalis to CIA", "Calm Inlet Area")
    
    # Parasequoia Connections
    connect("Para Area to Meta Area", "Metavolicalis Area")
    connect("Parasequoia to CIA", "Calm Inlet Area")
    
    # Great River Valley Connections
    connect("GRV to NC North of Boulder", "Nameless Coast North of Boulder")
    connect("GRV to Base of WF Gendarme", "Base of Western Foot of Gendarme")
    connect("Chimney Rock to CIA", "Calm Inlet Area")
    connect("GRV to WG Dark Area", "Waterfall Grotto Dark Area")
    connect("GRV to LCA", "Longhorn Coast Area")
    connect("GRV to EV Front", "Eroded Valley Front")
    connect("GRV to SJ Front", "Schlamm Jungle Front")
    connect("GRV to PP", "Primordial Passage")
    
    # Base of Western Foot of Gendarme Connections
    connect("Base of WF Gendarme to GRV", "Great River Valley Area")
    connect("Base of WF Gendarme to WF Gendarme", "Western Foot of Gendarme")
    
    # Western Foot of Gendarme Connections
    connect("Airs Cairn to CIA", "Calm Inlet Area")
    connect("WF Gendarme to Base of WF Gendarme", "Base of Western Foot of Gendarme")
    
    # Waterfall Grotto Connections
    connect("Milky White Vein to CIA", "Calm Inlet Area")
    connect("Milky White Vein to WG Dark Area", "Waterfall Grotto Dark Area")
    connect("WG Dark Area to Milky White Vein", "Milky White Vein")
    connect("WG Dark Area to GRV", "Great River Valley Area")

    # Longhorn Coast Connections
    connect("LCA to GRV", "Great River Valley Area")
    connect("LCA to Outside ST", "Outside Silent Tower")
    connect("LCA to Nostalgia Cape", "Nostalgia Cape")
    connect("LCA to Beehive", "Beehive")
    connect("Beehive to LCA", "Longhorn Coast Area")
    connect("Beehive to CIA", "Calm Inlet Area")

    # Eroded Valley Connections
    connect("EV Front to GRV", "Great River Valley Area")
    connect("EV Front to EV Dark Area", "Eroded Valley Dark Area")
    connect("EV Front to EV Mid-Boss Arena", "Eroded Valley Mid-Boss Arena")
    connect("EV Dark Area to EV Front", "Eroded Valley Front")
    connect("EV Dark Area to EV Indigo Mineral Vein", "Eroded Valley Indigo Mineral Vein")
    connect("EV Indigo Mineral Vein to EV Dark Area", "Eroded Valley Dark Area")
    connect("Indigo Mineral Vein to CIA", "Calm Inlet Area")
    connect("EV Mid-Boss Arena to EV Front", "Eroded Valley Front")
    connect("EV Mid-Boss Arena to EV Webbed Walkway", "Eroded Valley Webbed Walkway")
    connect("EV Webbed Walkway to EV Front", "Eroded Valley Front")
    connect("EV Webbed Walkway to EV Before Boss", "Eroded Valley Before Boss")
    connect("EV Webbed Walkway to EV Mid-Boss Arena", "Eroded Valley Mid-Boss Arena")
    connect("EV Before Boss to EV Webbed Walkway", "Eroded Valley Webbed Walkway")
    connect("EV Before Boss to EV Boss Arena", "Eroded Valley Boss Arena")
    connect("EV Boss Arena to EV Before Boss", "Eroded Valley Before Boss")
    connect("EV Boss Arena to SB", "Sunrise Beach")

    # Sunrise Beach Connections
    connect("SB to EV Boss Arena", "Eroded Valley Boss Arena")
    connect("Beached Remains to CIA", "Calm Inlet Area")

    # Schlamm Jungle Connections
    connect("SJ Front to GRV", "Great River Valley Area")
    connect("SJ Front to SJ Mid-Boss Arena", "Schlamm Jungle Mid-Boss Arena")
    connect("SJ Mid-Boss Arena to SJ Front", "Schlamm Jungle Front")
    connect("SJ Mid-Boss Arena to SJ Muddy Path", "Schlamm Jungle Muddy Path")
    connect("SJ Muddy Path to SJ Mid-Boss Arena", "Schlamm Jungle Mid-Boss Arena")
    connect("SJ Muddy Path to SJ Before Boss", "Schlamm Jungle Before Boss")
    connect("SJ Muddy Path to SJ FoMH", "Schlamm Jungle Field of Medicinal Herbs")
    connect("SJ FoMH to SJ Muddy Path", "Schlamm Jungle Muddy Path")
    connect("SJ FoMH to CIA", "Calm Inlet Area")
    connect("SJ Before Boss to SJ Muddy Path", "Schlamm Jungle Muddy Path")
    connect("SJ Before Boss to SJ Boss Arena", "Schlamm Jungle Boss Arena")
    connect("SJ Boss Arena to SJ Before Boss", "Schlamm Jungle Before Boss")
    connect("SJ Boss Arena to ORC", "Odd Rock Coast")

    # Odd Rock Coast Connections
    connect("ORC to SJ Boss Arena", "Schlamm Jungle Boss Arena")

    # Nostalgia Cape Connections
    connect("Nostalgia Cape to LCA", "Longhorn Coast Area")
    connect("Nostalgia Cape to ECC", "East Coast Cave Before Gilkyra")
    connect("Ship Graveyard to CIA", "Calm Inlet Area")

    # East Coast Cave Connections
    connect("ECC to Nostalgia Cape", "Nostalgia Cape")
    connect("ECC BG to ECC AG", "East Coast Cave After Gilkyra")
    connect("ECC AG to ECC BG", "East Coast Cave Before Gilkyra")
    connect("ECC AG to PSE", "Pirate Ship Eleftheria")
    connect("Hidden Pirate Storehouse to CIA", "Calm Inlet Area")

    # Pirate Ship Eleftheria Connections
    connect("PSE to ECC AG", "East Coast Cave After Gilkyra")
    connect("PSE to PSE Submerged Hold", "Pirate Ship Eleftheria Submerged Hold")
    connect("PSE Submerged Hold to PSE", "Pirate Ship Eleftheria")

    # Primordial Passage Connections
    connect("PP to GRV", "Great River Valley Area")
    connect("PP to MG", "Mont Gendarme Front")

    # Silent Tower Connections
    connect("Outside ST to LCA", "Longhorn Coast Area")
    connect("Outside ST to ST", "Silent Tower")
    connect("ST to Outside ST", "Outside Silent Tower")

    # Weathervane Hills Connections
    connect("WH to CIA", "Calm Inlet Area")
    connect("Zephyr Hill to CIA", "Calm Inlet Area")
    connect("WH to WH Past Insect Nests", "WH Past Insect Nests")
    connect("WH Past Insect Nests to WH", "Weathervane Hills")
    connect("WH to UMV", "Underground Water Vein")

    # Underground Water Vein Connections
    connect("UWV to WH", "Weathervane Hills")
    connect("UWV to Lapis Mineral Vein Area", "Lapis Mineral Vein Area")
    connect("Lapis Mineral Vein Area to UWV", "Underground Water Vein Area")
    connect("Lapis Mineral Vein Area to CIA", "Calm Inlet Area")

    # Mont Gendarme Connections
    connect("MG to PP", "Primordial Passage")
    connect("MG Front to MG Mid", "Mont Gendarme Middle")
    connect("MG Mid to MG Front", "Mont Gendarme Front")
    connect("MG Mid to MG Mid-Boss Arena", "Mont Gendarme Mid-Boss Arena")
    connect("MG Mid-Boss Arena to MG Mid", "Mont Gendarme Middle")
    connect("MG Mid-Boss Arena to MG Upper", "Mont Gendarme Upper")
    connect("MG Upper to MG Mid-Boss Arena", "Mont Gendarme Mid-Boss Arena")
    connect("MG Upper to MG Boss Arena", "Mont Gendarme Boss Arena")
    connect("MG Boss Arena to MG Upper", "Mont Gendarme Upper")
    connect("MG Boss Arena to Seiren North", "Seiren North Access")

    # Seiren North Connections
    connect("Seiren North to MG Boss Arena", "Mont Gendarme Boss Arena")
    connect("Seiren North to SPWC", "Stone Pillar Wind Cave")
    connect("Seiren North to TotGT", "Temple of the Great Tree")
    connect("Seiren North to RoE", "Ruins of Eternia")
    connect("Prismatic Mineral Vein to CIA", "Calm Inlet Area")
    connect("Unicalamites to CIA", "Calm Inlet Area")
    connect("Breath Fountain to CIA", "Calm Inlet Area")
    connect("Ancient Tree to CIA", "Calm Inlet Area")

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