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

    # :Bridge regions are meant to represent connections between two regions that are not normally connected in the base game. 
    # They are used to allow for more flexible world design and to accommodate the randomization of entrances and exits. 
    # They should not contain any locations and are used to keep from putting logic on entrances that could move between regions.
    regions: Dict[str, Ys8RegionData] = {
        "Calm Inlet Area": Ys8RegionData([],["CIA to WC", "CIA to NC North of Boulder", "CIA to Rainbow Falls", "CIA to Parasequoia", 
                                             "CIA to Metavolicalis", "CIA to IL 1", "CIA to IL 2", "CIA to IL 3", "CIA to Map Completion", 
                                             "CIA to Jewel Trade", "CIA to Fish Trade", "CIA to Discovery Turn In", "CIA to Airs Cairn", 
                                             "CIA to Chimney Rock", "CIA to Milky White Vein", "CIA to Indigo Mineral Vein", "CIA to Beached Remains",
                                             "CIA to FoMH", "CIA to Beehive", "CIA to Hidden Pirate Storehouse", "CIA to Ship Graveyard", "CIA to WH",
                                             "CIA to Zephyr Hill", "CIA to Solitude Island", "CIA to Lapis Mineral Vein Area", "CIA to Prismatic Mineral Vein", 
                                             "CIA to Unicalamites", "CIA to Breath Fountain", "CIA to Ancient Tree", "CIA to Soundless Hall", "CIA to Sky Garden",
                                             "CIA to Graves of Ancient Heroes", "CIA to TCF Night"]),
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
        "Schlamm Jungle Bridge": Ys8RegionData([], ["SJ:Bridge to GRV", "SJ:Bridge to SJ Front"]),
        "Schlamm Jungle Front": Ys8RegionData([], ["SJ Front to SJ:Bridge", "SJ Front to SJ Mid-Boss Arena"]),
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
        "Primordial Passage": Ys8RegionData([], ["PP to GRV", "PP to MG:Bridge", "PP to MG Night"]),
        "Mont Gendarme Bridge": Ys8RegionData([], ["MG:Bridge to PP", "MG:Bridge to MG Front"]),
        "Outside Silent Tower": Ys8RegionData([], ["Outside ST to LCA", "Outside ST to ST"]),
        "Silent Tower": Ys8RegionData([], ["ST to Outside ST"]),
        "Solitude Island": Ys8RegionData([], ["Solitude Island to CIA"]),
        "Weathervane Hills": Ys8RegionData([], ["WH to CIA", "Zephyr Hill to CIA", "WH to WH Past Insect Nests", "WH to UMV"]),
        "WH Past Insect Nests": Ys8RegionData([], ["WH Past Insect Nests to WH"]),
        "Underground Water Vein": Ys8RegionData([], ["UWV to WH", "UWV to Lapis Mineral Vein Area"]),
        "Lapis Mineral Vein Area": Ys8RegionData([], ["Lapis Mineral Vein Area to UWV", "Lapis Mineral Vein Area to CIA"]),
        "Mont Gendarme Front": Ys8RegionData([], ["MG Front to MG:Bridge", "MG Front to MG Mid"]),
        "Mont Gendarme Middle": Ys8RegionData([], ["MG Mid to MG Front", "MG Mid to MG Mid-Boss Arena"]),
        "Mont Gendarme Mid-Boss Arena": Ys8RegionData([], ["MG Mid-Boss Arena to MG Mid", "MG Mid-Boss Arena to MG Upper"]),
        "Mont Gendarme Upper": Ys8RegionData([], ["MG Upper to MG Mid-Boss Arena", "MG Upper to MG Boss Arena"]),
        "Mont Gendarme Boss Arena": Ys8RegionData([], ["MG Boss Arena to MG Upper", "MG Boss Arena to Seiren North"]),
        "Seiren North Access": Ys8RegionData([], ["Seiren North to MG Boss Arena", "Seiren North to SPWC", "Seiren North to TotGT", "Seiren North to RoE", 
                                                  "Prismatic Mineral Vein to CIA", "Unicalamites to CIA", "Breath Fountain to CIA", "Ancient Tree to CIA",
                                                  "Seiren North to Pangaia Plains Night"]),
        #WIP
        "Stone Pillar Wind Cave": Ys8RegionData([], ["SPWC to Seiren North", "SPWC to SPWC Upper"]),
        "Temple of the Great Tree": Ys8RegionData([], ["TotGT to Seiren North", "TotGT to TotGT Boss Arena", "TotGT to RoE", "TotGT to Vista Ridge"]),
        "Temple of the Great Tree Boss Arena": Ys8RegionData([], ["TotGT Boss Arena to TotGT", "TotGT Boss Arena to TotGT Garden"]),
        "Temple of the Great Tree Garden": Ys8RegionData([], ["TotGT Garden to TotGT Boss Arena", "TotGT Garden to Octus"]),
        "Octus Overlook": Ys8RegionData([], ["Octus to TotGT Garden", "Octus to Selection Sphere"]),
        "Selection Sphere": Ys8RegionData([], ["Selection Sphere to Octus"]),
        "Ruins of Eternia": Ys8RegionData([], ["RoE to Seiren North", "RoE to TotGT", "RoE to AC:Bridge", "RoE to TH", "RoE to FSC First Barrier", "RoE to Bolado"]),
        "Bolado Monastery": Ys8RegionData([], ["Bolado to RoE", "Bolado to Bolado Basement"]),
        "Bolado Monastery Basement": Ys8RegionData([], ["Bolado Basement to Bolado"]),
        "Former Sanctuary Crypt First Barrier": Ys8RegionData([], ["FSC First Barrier to RoE", "FSC First Barrier to FSC Second Floor", "FSC First Barrier to FSC First Barrier North Brazier Room"]),
        "Former Sanctuary Crypt First Barrier North Brazier Room": Ys8RegionData([], ["FSC First Barrier North Brazier Room to FSC First Barrier"]),
        "Former Sanctuary Crypt Second Floor": Ys8RegionData([], ["FSC Second Floor to FSC First Barrier", "FSC Second Floor to FSC Second Barrier"]),
        "Former Sanctuary Crypt Second Barrier": Ys8RegionData([], ["FSC Second Barrier to FSC Second Floor", "FSC Second Barrier to FSC Second Boss Arena"]),
        "Former Sanctuary Crypt Second Boss Arena": Ys8RegionData([], ["FSC Second Boss Arena to FSC Second Barrier", "FSC Second Boss Arena to FSC Third Floor"]),
        "Former Sanctuary Crypt Third Floor": Ys8RegionData([], ["FSC Third Floor to FSC Second Boss Arena", "FSC Third Floor to FSC Third Barrier", "FSC Third Floor to FSC Third Floor Side Rooms"]),
        "Former Sanctuary Crypt Third Floor Side Rooms": Ys8RegionData([], ["FSC Third Floor Side Rooms to FSC Third Floor"]),
        "Former Sanctuary Crypt Third Barrier": Ys8RegionData([], ["FSC Third Barrier to FSC Third Floor", "FSC Third Barrier to FSC Final Floors"]),
        "Former Sanctuary Crypt Final Floors": Ys8RegionData([], ["FSC Final Floors to FSC Third Barrier", "FSC Final Floors to FSC Boss Room", "FSC Final Floors to FSC Final Floor Side Rooms"]),
        "Former Sanctuary Crypt Final Floor Side Rooms": Ys8RegionData([], ["FSC Final Floor Side Rooms to FSC Final Floors"]),
        "Former Sanctuary Crypt Boss Room": Ys8RegionData([], ["FSC Boss Room to FSC Final Floors"]),
        "Towal Highway": Ys8RegionData([], ["TH to RoE", "TH to Baja"]),
        "Baja Tower Lower Floors": Ys8RegionData([], ["Baja to TH", "Baja to Baja Tower Upper Floors"]),
        "Baja Tower Upper Floors": Ys8RegionData([], ["Baja Upper to Baja Boss Arena"]),
        "Baja Tower Boss Arena": Ys8RegionData([], ["Baja Boss to Baja Upper"]),
        "Archeozoic Chasm Bridge": Ys8RegionData([], ["AC:Bridge to RoE", "AC:Bridge to AC Front"]),
        "Archeozoic Chasm Front": Ys8RegionData([], ["AC Front to AC:Bridge", "AC Front to AC Submerged Area"]),
        "Archeozoic Chasm Submerged Area": Ys8RegionData([], ["AC Submerged Area to AC Front", "AC Submerged Area to AC Boss Arena"]),
        "Archeozoic Chasm Boss Arena": Ys8RegionData([], ["AC Boss Arena to AC Submerged Area"]),
        "Vista Ridge": Ys8RegionData([], ["Vista Ridge to TotGT", "Vista Ridge to Vista Ridge Upper", "Vista Ridge to LM Entrance"]),
        "Lodinia Marshlands Entrance": Ys8RegionData([], ["LM Entrance to Vista Ridge", "LM Entrance to LM South", "LM Entrance to LM Near Submerged Cemetery"]),
        "Lodinia Marshlands South": Ys8RegionData([], ["LM South to LM Entrance"]),
        "Lodinia Marshlands Near Submerged Cemetery": Ys8RegionData([], ["LM Near Submerged Cemetery to LM Entrance", "LM Near Submerged Cemetery to Submerged Cemetery",
                                                                         "LM Near Submerged Cemetery to Near Sky Garden"]),
        "Lodinia Marshlands Near Sky Garden": Ys8RegionData([], ["LM Near Sky Garden to LM Near Submerged Cemetery", "LM Near Sky Garden to Sky Garden", "LM Near Sky Garden to VoK Entrance"]),
        "Valley of Kings Entrance": Ys8RegionData([], ["VoK Entrance to LM Near Sky Garden", "VoK Entrance to VoK Before Door", "VoK Entrance to Graves of Ancient Heroes"]),
        "Valley of Kings Before Door": Ys8RegionData([], ["VoK Before Door to VoK Entrance", "VoK Before Door to VoK After Door"]),
        "Valley of Kings After Door": Ys8RegionData([], ["VoK After Door to VoK Before Door", "VoK After Door to VoK Boss Arena"]),
        "Valley of Kings Boss Arena": Ys8RegionData([], ["VoK Boss Arena to VoK After Door"]),
        "Graves of Ancient Heroes": Ys8RegionData([], ["Graves of Ancient Heroes to VoK Entrance", "Graves of Ancient Heroes to CIA"]),
        "Sky Garden": Ys8RegionData([], ["Sky Garden to LM Near Sky Garden", "Sky Garden to CIA"]),
        "Submerged Cemetery": Ys8RegionData([], ["Submerged Cemetery to LM Near Submerged Cemetery", "Submerged Cemetery to Bolado Hidden Room", "Submerged Cemetery to Soundless Hall"]),
        "Soundless Hall": Ys8RegionData([], ["SH to Submerged Cemetery", "SH to CIA"]),
        "Bolado Monastery Hidden Room": Ys8RegionData([], ["Bolado Hidden Room to Submerged Cemetery"]),
        "Towering Coral Forest (Night) Front Half": Ys8RegionData([], ["TCF Night Front to CIA", "TCF Night Front to TCF Night Rear"]),
        "Towering Coral Forest (Night) Rear Half": Ys8RegionData([], ["TCF Night Rear to TCF Night Front"]),
        "Mont Gendarme (Night) Front Half": Ys8RegionData([], ["MG Night Front to PP", "MG Night Front to MG Night Rear"]),
        "Mont Gendarme (Night) Rear Half": Ys8RegionData([], ["MG Night Rear to MG Night Front"]),
        "Pangaia Plains (Night)": Ys8RegionData([], ["Pangaia Plains Night to Seiren North"]),
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
    connect("CIA to Soundless Hall", "Soundless Hall")
    connect("CIA to Sky Garden", "Sky Garden")
    connect("CIA to Graves of Ancient Heroes", "Graves of Ancient Heroes")
    connect("CIA to TCF Night", "Towering Coral Forest (Night) Front Half")
    
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
    connect("GRV to SJ:Bridge", "Schlamm Jungle Bridge")
    connect("SJ:Bridge to GRV", "Great River Valley Area")
    connect("SJ:Bridge to SJ Front", "Schlamm Jungle Front")
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
    connect("LCA to Nostalgia Cape", "Nostalgia Cape Area")
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
    connect("ECC to Nostalgia Cape", "Nostalgia Cape Area")
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
    connect("PP to MG:Bridge", "Mont Gendarme Bridge")
    connect("MG:Bridge to PP", "Primordial Passage")
    connect("MG:Bridge to MG Front", "Mont Gendarme Front")
    connect("PP to MG Night", "Mont Gendarme (Night) Front Half")

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
    connect("Lapis Mineral Vein Area to UWV", "Underground Water Vein")
    connect("Lapis Mineral Vein Area to CIA", "Calm Inlet Area")

    # Mont Gendarme Connections
    connect("MG Front to MG:Bridge", "Mont Gendarme Bridge")
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
    connect("Seiren North to Pangaia Plains Night", "Pangaia Plains (Night)")

    # Stone Pillar Wind Cave Connections
    connect("SPWC to Seiren North", "Seiren North Access")
    connect("SPWC to SPWC Upper", "Stone Pillar Wind Cave")

    # Temple of the Great Tree Connections
    connect("TotGT to Seiren North", "Seiren North Access")
    connect("TotGT to TotGT Boss Arena", "Temple of the Great Tree Boss Arena")
    connect("TotGT to RoE", "Ruins of Eternia")
    connect("TotGT to Vista Ridge", "Vista Ridge")
    connect("TotGT Boss Arena to TotGT", "Temple of the Great Tree")
    connect("TotGT Boss Arena to TotGT Garden", "Temple of the Great Tree Garden")
    connect("TotGT Garden to TotGT Boss Arena", "Temple of the Great Tree Boss Arena")
    connect("TotGT Garden to Octus", "Octus Overlook")

    # Octus Overlook Connections
    connect("Octus to TotGT Garden", "Temple of the Great Tree Garden")
    connect("Octus to Selection Sphere", "Selection Sphere")
    connect("Selection Sphere to Octus", "Octus Overlook")

    # Ruins of Eternia Connections
    connect("RoE to Seiren North", "Seiren North Access")
    connect("RoE to TotGT", "Temple of the Great Tree")
    connect("RoE to AC:Bridge", "Archeozoic Chasm Bridge")
    connect("RoE to TH", "Towal Highway")
    connect("RoE to FSC First Barrier", "Former Sanctuary Crypt First Barrier")
    connect("RoE to Bolado", "Bolado Monastery")
    connect("Bolado to RoE", "Ruins of Eternia")
    connect("Bolado to Bolado Basement", "Bolado Monastery Basement")
    connect("Bolado Basement to Bolado", "Bolado Monastery")
    connect("AC:Bridge to RoE", "Ruins of Eternia")
    connect("AC:Bridge to AC Front", "Archeozoic Chasm Front")
    connect("RoE to AC:Bridge", "Archeozoic Chasm Bridge")

    # Former Sanctuary Crypt Connections
    connect("FSC First Barrier to RoE", "Ruins of Eternia")
    connect("FSC First Barrier to FSC Second Floor", "Former Sanctuary Crypt Second Floor")
    connect("FSC First Barrier to FSC First Barrier North Brazier Room", "Former Sanctuary Crypt First Barrier North Brazier Room")
    connect("FSC First Barrier North Brazier Room to FSC First Barrier", "Former Sanctuary Crypt First Barrier")
    connect("FSC Second Floor to FSC First Barrier", "Former Sanctuary Crypt First Barrier")
    connect("FSC Second Floor to FSC Second Barrier", "Former Sanctuary Crypt Second Barrier")
    connect("FSC Second Barrier to FSC Second Floor", "Former Sanctuary Crypt Second Floor")
    connect("FSC Second Barrier to FSC Boss Arena", "Former Sanctuary Crypt Second Boss Arena")
    connect("FSC Second Boss Arena to FSC Second Barrier", "Former Sanctuary Crypt Second Barrier")
    connect("FSC Second Boss Arena to FSC Third Floor", "Former Sanctuary Crypt Third Floor")
    connect("FSC Third Floor to FSC Second Boss Arena", "Former Sanctuary Crypt Second Boss Arena")
    connect("FSC Third Floor to FSC Third Barrier", "Former Sanctuary Crypt Third Barrier")
    connect("FSC Third Floor to FSC Third Floor Side Rooms", "Former Sanctuary Crypt Third Floor Side Rooms")
    connect("FSC Third Floor Side Rooms to FSC Third Floor", "Former Sanctuary Crypt Third Floor")
    connect("FSC Third Barrier to FSC Third Floor", "Former Sanctuary Crypt Third Floor")
    connect("FSC Third Barrier to FSC Final Floors", "Former Sanctuary Crypt Final Floors")
    connect("FSC Final Floors to FSC Third Barrier", "Former Sanctuary Crypt Third Barrier")
    connect("FSC Final Floors to FSC Boss Room", "Former Sanctuary Crypt Boss Room")
    connect("FSC Final Floors to FSC Final Floor Side Rooms", "Former Sanctuary Crypt Final Floor Side Rooms")
    connect("FSC Final Floor Side Rooms to FSC Final Floors", "Former Sanctuary Crypt Final Floors")
    connect("FSC Boss Room to FSC Final Floors", "Former Sanctuary Crypt Final Floors")

    # Towal Highway Connections
    connect("TH to RoE", "Ruins of Eternia")
    connect("TH to Baja", "Baja Tower Lower Floors")

    # Baja Tower Connections
    connect("Baja to TH", "Towal Highway")
    connect("Baja to Baja Tower Upper Floors", "Baja Tower Upper Floors")
    connect("Baja Upper to Baja Boss Arena", "Baja Tower Boss Arena")
    connect("Baja Boss to Baja Upper", "Baja Tower Upper Floors")

    # Archeozoic Chasm Connections
    connect("AC Front to AC:Bridge", "Archeozoic Chasm Bridge")
    connect("AC Front to AC Submerged Area", "Archeozoic Chasm Submerged Area")
    connect("AC Submerged Area to AC Front", "Archeozoic Chasm Front")
    connect("AC Submerged Area to AC Boss Arena", "Archeozoic Chasm Boss Arena")
    connect("AC Boss Arena to AC Submerged Area", "Archeozoic Chasm Submerged Area")

    # Vista Ridge Connections
    connect("Vista Ridge to TotGT", "Temple of the Great Tree")
    connect("Vista Ridge to Vista Ridge Upper", "Vista Ridge")
    connect("Vista Ridge to LM Entrance", "Lodinia Marshlands Entrance")

    # Lodinia Marshlands Connections
    connect("LM Entrance to Vista Ridge", "Vista Ridge")
    connect("LM Entrance to LM South", "Lodinia Marshlands South")
    connect("LM Entrance to LM Near Submerged Cemetery", "Lodinia Marshlands Near Submerged Cemetery")
    connect("LM South to LM Entrance", "Lodinia Marshlands Entrance")
    connect("LM Near Submerged Cemetery to LM Entrance", "Lodinia Marshlands Entrance")
    connect("LM Near Submerged Cemetery to Near Sky Garden", "Lodinia Marshlands Near Sky Garden")
    connect("LM Near Submerged Cemetery to Submerged Cemetery", "Submerged Cemetery")
    connect("Sky Garden to LM Near Sky Garden", "Lodinia Marshlands Near Sky Garden")
    connect("Sky Garden to CIA", "Calm Inlet Area")
    connect("Near Sky Garden to LM Near Submerged Cemetery", "Lodinia Marshlands Near Submerged Cemetery")
    connect("Near Sky Garden to Sky Garden", "Sky Garden")
    connect("Near Sky Garden to VoK Entrance", "Valley of Kings Entrance")

    # Submerged Cemetery Connections
    connect("Submerged Cemetery to LM Near Submerged Cemetery", "Lodinia Marshlands Near Submerged Cemetery")
    connect("Submerged Cemetery to Bolado Hidden Room", "Bolado Monastery Hidden Room")
    connect("Submerged Cemetery to Soundless Hall", "Soundless Hall")
    connect("SH to Submerged Cemetery", "Submerged Cemetery")
    connect("SH to CIA", "Calm Inlet Area")

    # Valley of Kings Connections
    connect("VoK Entrance to LM Near Sky Garden", "Lodinia Marshlands Near Sky Garden")
    connect("VoK Entrance to VoK Before Door", "Valley of Kings Before Door")
    connect("VoK Entrance to Graves of Ancient Heroes", "Graves of Ancient Heroes")
    connect("VoK Before Door to VoK Entrance", "Valley of Kings Entrance")
    connect("VoK Before Door to VoK After Door", "Valley of Kings After Door")
    connect("VoK After Door to VoK Before Door", "Valley of Kings Before Door")
    connect("VoK After Door to VoK Boss Arena", "Valley of Kings Boss Arena")
    connect("VoK Boss Arena to VoK After Door", "Valley of Kings After Door")
    connect("Graves of Ancient Heroes to VoK Entrance", "Valley of Kings Entrance")
    connect("Graves of Ancient Heroes to CIA", "Calm Inlet Area")

    # Towering Coral Forest (Night) Connections
    connect("TCF Night Front to CIA", "Calm Inlet Area")
    connect("TCF Night Front to TCF Night Rear", "Towering Coral Forest (Night) Rear Half")
    connect("TCF Night Rear to TCF Night Front", "Towering Coral Forest (Night) Front Half")

    # Mont Gendarme (Night) Connections
    connect("MG Night Front to PP", "Primordial Passage")
    connect("MG Night Front to MG Night Rear", "Mont Gendarme (Night) Rear Half")
    connect("MG Night Rear to MG Night Front", "Mont Gendarme (Night) Front Half")

    # Pangaia Plains (Night) Connections
    connect("Pangaia Plains Night to Seiren North", "Seiren North Access")

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