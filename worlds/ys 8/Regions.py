from typing import Dict, List, NamedTuple, Optional, TYPE_CHECKING
from BaseClasses import MultiWorld, Region, Entrance
from .Locations import (Ys8Location)
from .Locations import (psyche_fight_names, psyche_location_table, fsc_psyche_fight_names, fsc_psyche_location_table, 
                        silent_tower_psyche_location_table, location_table, event_location_table)

if TYPE_CHECKING:
    from . import Ys8World

class Ys8RegionData(NamedTuple):
    locations: List[str]
    region_exits: Optional[Dict[str, str]]

regions: Dict[str, Ys8RegionData] = {}
region_connections: Dict[str, list] = {}
excluded_locations: List[str] = []

def create_regions(Ys8World):
    multiworld = Ys8World.multiworld
    player     = Ys8World.player
    options    = Ys8World.options
    
    region_connections = {
        "Calm Inlet Area": ["WC Entrance", "NCN Link", "TCFRF Link", "Para Link", "Meta Link", "CIA IL1 Link", "CIA IL2 Link", "CIA IL3 Link", 
                            "CIA MC Link", "CIA JT Link", "CIA FT Link", "CIA DTI Link", "WFG Link", "GRV Link", "MWV Link", "EVIMV Link", 
                            "SB Link", "SJFMH Link", "BH Link", "ECCBG Link", "NCA Link", "WH Link", "SI Link", "LMVA Link",
                            "SNA Link", "SH Link", "SG Link", "GOAH Link"],
        "Calm Inlet: Intercept List 1": [],
        "Calm Inlet: Intercept List 2": [],
        "Calm Inlet: Intercept List 3": [],
        "Calm Inlet: Map Completion": [],
        "Calm Inlet: Jewel Trade": [],
        "Calm Inlet: Fish Trade": [],
        "Calm Inlet: Discovery Turn In": [],
        "Waterdrop Cave": ["WC Exit"],
        "Nameless Coast North": ["NCN CIA Exit", "NCN GRV Link", "NCN TCF Entrance", "TCFNFH Link"],
        "Towering Coral Forest Front": ["TCF MB Entrance", "TCF NCN Exit"],
        "Towering Coral Forest Mid-Boss Arena": ["TCFMB Exit", "TCFMB Corpse Link"],
        "Towering Coral Forest Corpse": ["TCFC MB Exit", "TCFC RF Link"],
        "Towering Coral Forest Rainbow Falls": ["TCFRF TCF Exit", "TCFRF BB Link", "TCFRF Corpse Exit"],
        "Towering Coral Forest Before Boss": ["TCFBB TCF Exit", "TCFBB RF Exit", "TCF Boss Entrance"],
        "Towering Coral Forest Boss Arena": ["TCF Boss Exit", "TCF Post-Boss Link"],
        "Towering Coral Forest After Boss": ["TCFAB Boss Exit", "TCFAB Meta Exit"],
        "Metavolicalis Area": ["Meta Para Link", "Meta TCF Entrance"],
        "Parasequoia Area": ["Para Meta Exit"],
        "Great River Valley Area": ["GRV NCN Exit", "GRV BWFG Link", "GRV WGDA Link", "GRV LCA Link", "GRV PP Link", "GRV SC Link", "GRV EVF Entrance"],
        "Great River Valley South Camp": ["GRV SC Exit", "GRVSC SJ Entrance"],
        "Base of Western Foot of Gendarme": ["BWFG GRV Exit", "WFG Entrance"],
        "Western Foot of Gendarme": ["WFG Exit"],
        "Milky White Vein": ["MWV WGDA Link"],
        "Waterfall Grotto Dark Area": ["WGDA MWV Exit", "WGDA GRV Exit"],
        "Longhorn Coast Area": ["LCA GRV Exit", "LCA OST Link", "LCA NCA Link", "LCA BH Link"],
        "Beehive": ["BH LCA Exit"],
        "Eroded Valley Front": ["EVF GRV Exit", "EVF EVDA Link", "EV MB Entrance"],
        "Eroded Valley Dark Area": ["EVDA EVF Exit", "EVDA EVIMV Link"],
        "Eroded Valley Indigo Mineral Vein": ["EVIMV EVDA Exit"],
        "Eroded Valley Mid-Boss Arena": ["EVMB EVF Exit", "EVMB WW Link"],
        "Eroded Valley Webbed Walkway": ["EVWW EVF Exit", "EVWW BB Link", "EVWW MB Exit"],
        "Eroded Valley Before Boss": ["EVBB WW Exit", "EV Boss Entrance"],
        "Eroded Valley Boss Arena": ["EV Boss Exit", "EV Post-Boss Link"],
        "Eroded Valley After Boss": ["EVAB Boss Exit", "EVAB SB Exit"],
        "Sunrise Beach": ["SB EV Entrance"],
        "Schlamm Jungle Front": ["SJ MB Entrance", "SJF GRVSC Exit"],
        "Schlamm Jungle Mid-Boss Arena": ["SJMB SJF Exit", "SJMB MP Link"],
        "Schlamm Jungle Muddy Path": ["SJMP MB Exit", "SJMP BB Link", "SJMP FMH Link"],
        "Schlamm Jungle Field of Medicinal Herbs": ["SJFMH MP Exit"],
        "Schlamm Jungle Before Boss": ["SJBB MP Exit", "SJ Boss Entrance"],
        "Schlamm Jungle Boss Arena": ["SJ Boss Exit", "SJ Post-Boss Link"],
        "Schlamm Jungle After Boss": ["SJAB Boss Exit", "SJAB ORC Exit"],
        "Odd Rock Coast": ["ORC SJ Entrance"],
        "Nostalgia Cape Area": ["NCA LCA Exit", "NCA ECCBG Entrance"],
        "East Coast Cave Before Gilkyra": ["ECCBG ECCAG Link", "ECCBG NCA Exit"],
        "East Coast Cave After Gilkyra": ["ECCAG ECCBG Exit", "PSE Entrance"],
        "Pirate Ship Eleftheria": ["PSE ECC Exit", "PSE SH Entrance"],
        "Pirate Ship Eleftheria Submerged Hold": ["PSESH PSE Exit"],
        "Primordial Passage": ["PP GRV Exit", "PP MGNFH Link", "PP PPGE Link"],
        "Primordial Passage Gendarme Entrance": ["PPGE PP Exit", "PP MG Entrance"],
        "Outside Silent Tower": ["OST LCA Exit", "OST STE Link"],
        "Silent Tower Entrance": ["STE OST Link", "ST Entrance"],
        "Silent Tower": ["STE OST Exit"],
        "Solitude Island": [],
        "Weathervane Hills": ["WH WHPIN Link", "WH UWV Link"],
        "Weathervane Hills Past Insect Nests": ["WHPIN WH Exit"],
        "Underground Water Vein": ["UWV WH Exit", "UWV LMVA Link"],
        "Lapis Mineral Vein Area": ["LMVA UWV Exit"],
        "Mont Gendarme Front": ["MGF PPGE Exit", "MGF MGM Link"],
        "Mont Gendarme Middle": ["MGM MGF Exit", "MGM MB Link"],
        "Mont Gendarme Mid-Boss Arena": ["MGMB MGM Exit", "MGMB MGU Link"],
        "Mont Gendarme Upper": ["MGU MB Exit", "MG Boss Entrance"],
        "Mont Gendarme Boss Arena": ["MG Boss Exit", "MG Post-Boss Link"],
        "Mont Gendarme After Boss": ["MGPB Boss Exit", "MGPB SNA Exit"],
        "Seiren North Access": ["SNA SPWC Link", "SNA TGT Link", "SNA ROE Link", "SNA PPN Link", "SNA MGAB Entrance"],
        "Stone Pillar Wind Cave": ["SPWC SNA Exit", "SPWC SPWCU Link"],
        "Stone Pillar Wind Cave Upper": ["SPWCU SPWC Exit"],
        "Temple of the Great Tree": ["TGT SNA Exit", "TGT Boss Entrance", "TGT ROE Link", "TGT VR Link"],
        "Temple of the Great Tree Boss Arena": ["TGT Boss Exit", "TGT Garden Link"],
        "Temple of the Great Tree Garden": ["TGTG TGT Exit", "TGTG OO Entrance"],
        "Octus Overlook": ["OO SS Link", "OO TGT Exit"],
        "Selection Sphere": ["SS OO Exit"],
        "Ruins of Eternia": ["ROE SNA Exit", "ROE TGT Exit", "ROE TH Link", "ROE BM Link", "ROE ROEHP Link", "ROE BTAC Link"],
        "Bridge to Archeozoic Chasm": ["BTAC ROE Exit", "AC Entrance"],
        "Ruins of Eternia Hidden Passage": ["ROEHP ROE Exit", "FSC Entrance"],
        "Bolado Monastery": ["BM ROE Exit", "BM BMB Link"],
        "Bolado Monastery Basement": ["BMB BM Exit"],
        "Former Sanctuary Crypt Front": ["FSCF FSCFB Link", "FSCF ROEHP Exit"],
        "Former Sanctuary Crypt First Barrier": ["FSCFB FSCF Exit", "FSCFB FSCSF Link", "FSC NBR Entrance"],
        "Former Sanctuary Crypt First Barrier North Brazier Room": ["FSCFBNBR FSCFB Exit"],
        "Former Sanctuary Crypt Second Floor": ["FSCSF FSCFB Exit", "FSCSF FSCSB Link"],
        "Former Sanctuary Crypt Second Barrier": ["FSCSB FSCSF Exit", "FSC SB Entrance"],
        "Former Sanctuary Crypt Second Boss Arena": ["FSCSBA FSCSB Exit", "FSCSBA FSCTF Link"],
        "Former Sanctuary Crypt Third Floor": ["FSCTF FSCSBA Exit", "FSCTF FSCTB Link", "FSC TFSR Entrance"],
        "Former Sanctuary Crypt Third Floor Side Rooms": ["FSCTFSR FSCTF Exit"],
        "Former Sanctuary Crypt Third Barrier": ["FSCTB FSCTF Exit", "FSCTB FSCFF Link"],
        "Former Sanctuary Crypt Final Floors": ["FSCFF FSCTB Exit", "FSC Boss Entrance", "FSC FFSR Entrance"],
        "Former Sanctuary Crypt Final Floors Side Rooms": ["FSCFFSR FSCFF Exit"],
        "Former Sanctuary Crypt Boss Room": ["FSCBR FSCFF Exit"],
        "Towal Highway": ["TH ROE Exit", "TH THBTE Link"],
        "Towal Highway Baja Tower Entrance": ["THBTE TH Exit", "BTLF Entrance"],
        "Baja Tower Lower Floors": ["BTLF THBTE Exit", "BTLF BTUF Link"],
        "Baja Tower Upper Floors": ["BTUF BTLF Exit", "BTBA Entrance"],
        "Baja Tower Boss Arena": ["BTBA BTUF Exit"],
        "Archeozoic Chasm Front": ["ACF BTAC Exit", "ACF ACSA Link"],
        "Archeozoic Chasm Submerged Area": ["ACSA ACF Exit", "AC Boss Entrance"],
        "Archeozoic Chasm Boss Arena": ["ACBA ACSA Exit"],
        "Vista Ridge": ["VR TGT Exit", "VR VRU Link", "VR LMF Link"],
        "Vista Ridge Upper": ["VRU VR Exit"],
        "Lodinia Marshlands Front": ["LMF VR Exit", "LMF LMS Link", "LMF LMNSC Link"],
        "Lodinia Marshlands South": ["LMS LMF Exit"],
        "Lodinia Marshlands Near Submerged Cemetery": ["LMNSC LMF Exit", "SC Entrance", "LMNSC LMNSG Link"],
        "Lodinia Marshlands Near Sky Garden": ["LMNSG LMNSC Exit", "LMNSG SG Link", "LMNSG LMB Link"],
        "Lodinia Marshlands Back": ["LMB LMNSG Exit", "LMB GOAH Link", "LMB VOKBD Entrance"],
        "Valley of Kings Before Door": ["VOKBD VOKAD Link", "VOKBD LMB Exit"],
        "Valley of Kings After Door": ["VOKAD VOKBD Exit", "VOK Boss Entrance"],
        "Valley of Kings Boss Arena": ["VOKBA VOKAD Exit"],
        "Graves of Ancient Heroes": ["GOAH LMB Exit"],
        "Sky Garden": ["SG LMNSG Exit"],
        "Submerged Cemetery": ["SC LMNSC Exit", "BMHR Link", "SC SH Link"],
        "Soundless Hall": ["SH SC Exit"],
        "Bolado Monastery Hidden Room": ["BMHR SC Exit"],
        "Towering Coral Forest (Night) Front Half": ["TCFNFH TCFNRH Link"],
        "Towering Coral Forest (Night) Rear Half": ["TCFNRH TCFNFH Exit"],
        "Mont Gendarme (Night) Front Half": ["MGNFH PP Exit", "MGNFH MGNRH Link"],
        "Mont Gendarme (Night) Rear Half": ["MGNRH MGNFH Exit"],
        "Pangaia Plains (Night)": ["PPHN SNA Exit"],
    }

    for region in region_connections.keys():
        connections = region_connections[region]
        regions[region] = Ys8RegionData([], connections)

    if options.final_boss_access == 2:  # Psyche Fight Shuffle, we do this here because it add locations to the regions
        excluded_locations = ["Former Sanctuary Crypt - Final Floor Boss Arena Melaiduma", 
                             "Former Sanctuary Crypt - Final Floor Boss Arena Melaiduma Skill", 
                             "Former Sanctuary Crypt - Final Floor Boss Arena Melaiduma Medals",
                             "Octus Overlook Path of the Sky Era Psyche-Ura", 
                             "Octus Overlook Path of the Insectoid Era Psyche-Nestor", 
                             "Octus Overlook Path of the Frozen Era Psyche-Minos", 
                             "Octus Overlook Path of the Ocean Era Psyche-Hydra",
                             "Octus Overlook Path of the Sky Era Psyche-Ura Skill 1", 
                             "Octus Overlook Path of the Sky Era Psyche-Ura Skill 2", 
                             "Octus Overlook Path of the Insectoid Era Psyche-Nestor Skill 1", 
                             "Octus Overlook Path of the Insectoid Era Psyche-Nestor Skill 2",
                             "Octus Overlook Path of the Frozen Era Psyche-Minos Skill 1", 
                             "Octus Overlook Path of the Frozen Era Psyche-Minos Skill 2", 
                             "Octus Overlook Path of the Ocean Era Psyche-Hydra Skill 1", 
                             "Octus Overlook Path of the Ocean Era Psyche-Hydra Skill 2"]
        
        psyche_num = 4
        if options.former_sanctuary_crypt.value:
            psyche_location_table.update(fsc_psyche_location_table)
        else:
            psyche_fight_names.update(fsc_psyche_fight_names)

        if options.mephorash_progression.value:
            psyche_location_table.update(silent_tower_psyche_location_table)

        fight_samples = multiworld.random.sample(list(psyche_fight_names.items()), psyche_num)
        location_samples = multiworld.random.sample(list(psyche_location_table.items()), psyche_num)
        
        Ys8World.chosen_psyche_fight_list = dict(fight_samples)
        Ys8World.chosen_psyche_location_list = dict(location_samples)
        
        for (fight_name, fight_data), (location_name, location_data) in zip(fight_samples, location_samples):
            regions[fight_data.category].locations.append(fight_name)
            regions[location_data.category].locations.append(location_name)
    
    for location in location_table:
        if not options.former_sanctuary_crypt.value and location.startswith("Former Sanctuary Crypt"):
            continue
        if location in excluded_locations:
            continue
        
        regions[location_table[location].category].locations.append(location)

    for location in event_location_table:
        if not options.former_sanctuary_crypt.value and location.startswith("Former Sanctuary Crypt"):
            continue
        if location in excluded_locations:
            continue

        regions[event_location_table[location].category].locations.append(location)

    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))

def connect_entrances(Ys8World: "Ys8World"):
    multiworld = Ys8World.multiworld
    player     = Ys8World.player
    options    = Ys8World.options
    
    def connect(entrance_name: str, region_name: str):
        multiworld.get_entrance(entrance_name, player).connect(multiworld.get_region(region_name, player))
    
    # Calm Inlet Area
    connect("WC Entrance", "Waterdrop Cave")
    connect("NCN Link", "Nameless Coast North")
    connect("TCFRF Link", "Towering Coral Forest Rainbow Falls")
    connect("Para Link", "Parasequoia Area")
    connect("Meta Link", "Metavolicalis Area")
    connect("CIA IL1 Link", "Calm Inlet: Intercept List 1")
    connect("CIA IL2 Link", "Calm Inlet: Intercept List 2")
    connect("CIA IL3 Link", "Calm Inlet: Intercept List 3")
    connect("CIA MC Link", "Calm Inlet: Map Completion")
    connect("CIA JT Link", "Calm Inlet: Jewel Trade")
    connect("CIA FT Link", "Calm Inlet: Fish Trade")
    connect("CIA DTI Link", "Calm Inlet: Discovery Turn In")
    connect("WFG Link", "Western Foot of Gendarme")
    connect("GRV Link", "Great River Valley Area")
    connect("MWV Link", "Milky White Vein")
    connect("EVIMV Link", "Eroded Valley Indigo Mineral Vein")
    connect("SB Link", "Sunrise Beach")
    connect("SJFMH Link", "Schlamm Jungle Field of Medicinal Herbs")
    connect("BH Link", "Beehive")
    connect("ECCBG Link", "East Coast Cave Before Gilkyra")
    connect("NCA Link", "Nostalgia Cape Area")
    connect("WH Link", "Weathervane Hills")
    connect("SI Link", "Solitude Island")
    connect("LMVA Link", "Lapis Mineral Vein Area")
    connect("SNA Link", "Seiren North Access")
    connect("SH Link", "Soundless Hall")
    connect("SG Link", "Sky Garden")
    connect("GOAH Link", "Graves of Ancient Heroes")
    connect("TCFNFH Link", "Towering Coral Forest (Night) Front Half")
    
    # Waterdrop Cave
    connect("WC Exit", "Calm Inlet Area")
    
    # Nameless Coast North
    connect("NCN CIA Exit", "Calm Inlet Area")
    connect("NCN GRV Link", "Great River Valley Area")
    connect("NCN TCF Entrance", "Towering Coral Forest Front")
    
    # Towering Coral Forest Front
    connect("TCF MB Entrance", "Towering Coral Forest Mid-Boss Arena")
    connect("TCF NCN Exit", "Nameless Coast North")
    
    # Towering Coral Forest Mid-Boss Arena
    connect("TCFMB Exit", "Towering Coral Forest Front")
    connect("TCFMB Corpse Link", "Towering Coral Forest Corpse")
    
    # Towering Coral Forest Corpse
    connect("TCFC MB Exit", "Towering Coral Forest Mid-Boss Arena")
    connect("TCFC RF Link", "Towering Coral Forest Rainbow Falls")
    
    # Towering Coral Forest Rainbow Falls
    connect("TCFRF TCF Exit", "Towering Coral Forest Front")
    connect("TCFRF BB Link", "Towering Coral Forest Before Boss")
    connect("TCFRF Corpse Exit", "Towering Coral Forest Corpse")
    
    # Towering Coral Forest Before Boss
    connect("TCFBB TCF Exit", "Towering Coral Forest Front")
    connect("TCFBB RF Exit", "Towering Coral Forest Rainbow Falls")
    connect("TCF Boss Entrance", "Towering Coral Forest Boss Arena")
    
    # Towering Coral Forest Boss Arena
    connect("TCF Boss Exit", "Towering Coral Forest Before Boss")
    connect("TCF Post-Boss Link", "Towering Coral Forest After Boss")
    
    # Towering Coral Forest After Boss
    connect("TCFAB Boss Exit", "Towering Coral Forest Boss Arena")
    connect("TCFAB Meta Exit", "Metavolicalis Area")
    
    # Metavolicalis Area
    connect("Meta Para Link", "Parasequoia Area")
    connect("Meta TCF Entrance", "Towering Coral Forest After Boss")
    
    # Parasequoia Area
    connect("Para Meta Exit", "Metavolicalis Area")
    
    # Great River Valley Area
    connect("GRV NCN Exit", "Nameless Coast North")
    connect("GRV BWFG Link", "Base of Western Foot of Gendarme")
    connect("GRV WGDA Link", "Waterfall Grotto Dark Area")
    connect("GRV LCA Link", "Longhorn Coast Area")
    connect("GRV PP Link", "Primordial Passage")
    connect("GRV SC Link", "Great River Valley South Camp")
    connect("GRV EVF Entrance", "Eroded Valley Front")
    
    # Great River Valley South Camp
    connect("GRV SC Exit", "Great River Valley Area")
    connect("GRVSC SJ Entrance", "Schlamm Jungle Front")

    # Base of Western Foot of Gendarme
    connect("BWFG GRV Exit", "Great River Valley Area")
    connect("WFG Entrance", "Western Foot of Gendarme")
    
    # Western Foot of Gendarme
    connect("WFG Exit", "Base of Western Foot of Gendarme")
    
    # Milky White Vein
    connect("MWV WGDA Link", "Waterfall Grotto Dark Area")
    
    # Waterfall Grotto Dark Area
    connect("WGDA MWV Exit", "Milky White Vein")
    connect("WGDA GRV Exit", "Great River Valley Area")
    
    # Longhorn Coast Area
    connect("LCA GRV Exit", "Great River Valley Area")
    connect("LCA OST Link", "Outside Silent Tower")
    connect("LCA NCA Link", "Nostalgia Cape Area")
    connect("LCA BH Link", "Beehive")
    
    # Beehive
    connect("BH LCA Exit", "Longhorn Coast Area")
    
    # Eroded Valley Front
    connect("EVF GRV Exit", "Great River Valley Area")
    connect("EVF EVDA Link", "Eroded Valley Dark Area")
    connect("EV MB Entrance", "Eroded Valley Mid-Boss Arena")
    
    # Eroded Valley Dark Area
    connect("EVDA EVF Exit", "Eroded Valley Front")
    connect("EVDA EVIMV Link", "Eroded Valley Indigo Mineral Vein")
    
    # Eroded Valley Indigo Mineral Vein
    connect("EVIMV EVDA Exit", "Eroded Valley Dark Area")
    
    # Eroded Valley Mid-Boss Arena
    connect("EVMB EVF Exit", "Eroded Valley Front")
    connect("EVMB WW Link", "Eroded Valley Webbed Walkway")
    
    # Eroded Valley Webbed Walkway
    connect("EVWW EVF Exit", "Eroded Valley Front")
    connect("EVWW BB Link", "Eroded Valley Before Boss")
    connect("EVWW MB Exit", "Eroded Valley Mid-Boss Arena")
    
    # Eroded Valley Before Boss
    connect("EVBB WW Exit", "Eroded Valley Webbed Walkway")
    connect("EV Boss Entrance", "Eroded Valley Boss Arena")
    
    # Eroded Valley Boss Arena
    connect("EV Boss Exit", "Eroded Valley Before Boss")
    connect("EV Post-Boss Link", "Eroded Valley After Boss")
    
    # Eroded Valley After Boss
    connect("EVAB Boss Exit", "Eroded Valley Boss Arena")
    connect("EVAB SB Exit", "Sunrise Beach")
    
    # Sunrise Beach
    connect("SB EV Entrance", "Eroded Valley After Boss")
    
    # Schlamm Jungle Front
    connect("SJ MB Entrance", "Schlamm Jungle Mid-Boss Arena")
    connect("SJF GRVSC Exit", "Great River Valley South Camp")
    
    # Schlamm Jungle Mid-Boss Arena
    connect("SJMB SJF Exit", "Schlamm Jungle Front")
    connect("SJMB MP Link", "Schlamm Jungle Muddy Path")
    
    # Schlamm Jungle Muddy Path
    connect("SJMP MB Exit", "Schlamm Jungle Mid-Boss Arena")
    connect("SJMP BB Link", "Schlamm Jungle Before Boss")
    connect("SJMP FMH Link", "Schlamm Jungle Field of Medicinal Herbs")
    
    # Schlamm Jungle Field of Medicinal Herbs
    connect("SJFMH MP Exit", "Schlamm Jungle Muddy Path")
    
    # Schlamm Jungle Before Boss
    connect("SJBB MP Exit", "Schlamm Jungle Muddy Path")
    connect("SJ Boss Entrance", "Schlamm Jungle Boss Arena")
    
    # Schlamm Jungle Boss Arena
    connect("SJ Boss Exit", "Schlamm Jungle Before Boss")
    connect("SJ Post-Boss Link", "Schlamm Jungle After Boss")
    
    # Schlamm Jungle After Boss
    connect("SJAB Boss Exit", "Schlamm Jungle Boss Arena")
    connect("SJAB ORC Exit", "Odd Rock Coast")
    
    # Odd Rock Coast
    connect("ORC SJ Entrance", "Schlamm Jungle After Boss")
    
    # Nostalgia Cape Area
    connect("NCA LCA Exit", "Longhorn Coast Area")
    connect("NCA ECCBG Entrance", "East Coast Cave Before Gilkyra")
    
    # East Coast Cave Before Gilkyra
    connect("ECCBG NCA Exit", "Nostalgia Cape Area")
    connect("ECCBG ECCAG Link", "East Coast Cave After Gilkyra")
    
    # East Coast Cave After Gilkyra
    connect("ECCAG ECCBG Exit", "East Coast Cave Before Gilkyra")
    connect("PSE Entrance", "Pirate Ship Eleftheria")
    
    # Pirate Ship Eleftheria
    connect("PSE ECC Exit", "East Coast Cave After Gilkyra")
    connect("PSE SH Entrance", "Pirate Ship Eleftheria Submerged Hold")
    
    # Pirate Ship Eleftheria Submerged Hold
    connect("PSESH PSE Exit", "Pirate Ship Eleftheria")
    
    # Primordial Passage
    connect("PP GRV Exit", "Great River Valley Area")
    connect("PP MGNFH Link", "Mont Gendarme (Night) Front Half")
    connect("PP PPGE Link", "Primordial Passage Gendarme Entrance")
    
    # Primordial Passage Gendarme Entrance
    connect("PPGE PP Exit", "Primordial Passage")
    connect("PP MG Entrance", "Mont Gendarme Front")
    
    # Outside Silent Tower
    connect("OST LCA Exit", "Longhorn Coast Area")
    connect("OST STE Link", "Silent Tower Entrance")
    
    # Silent Tower Entrance
    connect("STE OST Link", "Outside Silent Tower")
    connect("ST Entrance", "Silent Tower")

    # Silent Tower
    connect("STE OST Exit", "Silent Tower Entrance")
    
    # Weathervane Hills
    connect("WH WHPIN Link", "Weathervane Hills Past Insect Nests")
    connect("WH UWV Link", "Underground Water Vein")
    
    # Weathervane Hills Past Insect Nests
    connect("WHPIN WH Exit", "Weathervane Hills")
    
    # Underground Water Vein
    connect("UWV WH Exit", "Weathervane Hills")
    connect("UWV LMVA Link", "Lapis Mineral Vein Area")
    
    # Lapis Mineral Vein Area
    connect("LMVA UWV Exit", "Underground Water Vein")
    
    # Mont Gendarme Front
    connect("MGF PPGE Exit", "Primordial Passage Gendarme Entrance")
    connect("MGF MGM Link", "Mont Gendarme Middle")
    
    # Mont Gendarme Middle
    connect("MGM MGF Exit", "Mont Gendarme Front")
    connect("MGM MB Link", "Mont Gendarme Mid-Boss Arena")
    
    # Mont Gendarme Mid-Boss Arena
    connect("MGMB MGM Exit", "Mont Gendarme Middle")
    connect("MGMB MGU Link", "Mont Gendarme Upper")
    
    # Mont Gendarme Upper
    connect("MGU MB Exit", "Mont Gendarme Mid-Boss Arena")
    connect("MG Boss Entrance", "Mont Gendarme Boss Arena")
    
    # Mont Gendarme Boss Arena
    connect("MG Boss Exit", "Mont Gendarme Upper")
    connect("MG Post-Boss Link", "Mont Gendarme After Boss")
    
    # Mont Gendarme Post Boss
    connect("MGPB Boss Exit", "Mont Gendarme Boss Arena")
    connect("MGPB SNA Exit", "Seiren North Access")
    
    # Seiren North Access
    connect("SNA MGAB Entrance", "Mont Gendarme After Boss")
    connect("SNA SPWC Link", "Stone Pillar Wind Cave")
    connect("SNA TGT Link", "Temple of the Great Tree")
    connect("SNA ROE Link", "Ruins of Eternia")
    connect("SNA PPN Link", "Pangaia Plains (Night)")
    
    # Stone Pillar Wind Cave
    connect("SPWC SNA Exit", "Seiren North Access")
    connect("SPWC SPWCU Link", "Stone Pillar Wind Cave Upper")
    
    # Stone Pillar Wind Cave Upper
    connect("SPWCU SPWC Exit", "Stone Pillar Wind Cave")
    
    # Temple of the Great Tree
    connect("TGT SNA Exit", "Seiren North Access")
    connect("TGT Boss Entrance", "Temple of the Great Tree Boss Arena")
    connect("TGT ROE Link", "Ruins of Eternia")
    connect("TGT VR Link", "Vista Ridge")
    
    # Temple of the Great Tree Boss Arena
    connect("TGT Boss Exit", "Temple of the Great Tree")
    connect("TGT Garden Link", "Temple of the Great Tree Garden")
    
    # Temple of the Great Tree Garden
    connect("TGTG TGT Exit", "Temple of the Great Tree Boss Arena")
    connect("TGTG OO Entrance", "Octus Overlook")

    # Octus Overlook
    connect("OO TGT Exit", "Temple of the Great Tree Garden")
    connect("OO SS Link", "Selection Sphere")
    
    # Selection Sphere
    connect("SS OO Exit", "Octus Overlook")
    
    # Ruins of Eternia
    connect("ROE SNA Exit", "Seiren North Access")
    connect("ROE TGT Exit", "Temple of the Great Tree")
    connect("ROE TH Link", "Towal Highway")
    connect("ROE BM Link", "Bolado Monastery")
    connect("ROE ROEHP Link", "Ruins of Eternia Hidden Passage")
    connect("ROE BTAC Link", "Bridge to Archeozoic Chasm")
    
    # Bridge to Archeozoic Chasm
    connect("BTAC ROE Exit", "Ruins of Eternia")
    connect("AC Entrance", "Archeozoic Chasm Front")
    
    # Ruins of Eternia Hidden Passage
    connect("ROEHP ROE Exit", "Ruins of Eternia")
    connect("FSC Entrance", "Former Sanctuary Crypt Front")
    
    # Bolado Monastery
    connect("BM ROE Exit", "Ruins of Eternia")
    connect("BM BMB Link", "Bolado Monastery Basement")
    
    # Bolado Monastery Basement
    connect("BMB BM Exit", "Bolado Monastery")
    
    # Former Sanctuary Crypt Front
    connect("FSCF FSCFB Link", "Former Sanctuary Crypt First Barrier")
    connect("FSCF ROEHP Exit", "Ruins of Eternia Hidden Passage")
    
    # Former Sanctuary Crypt First Barrier
    connect("FSCFB FSCF Exit", "Former Sanctuary Crypt Front")
    connect("FSCFB FSCSF Link", "Former Sanctuary Crypt Second Floor")
    connect("FSC NBR Entrance", "Former Sanctuary Crypt First Barrier North Brazier Room")
    
    # Former Sanctuary Crypt First Barrier North Brazier Room
    connect("FSCFBNBR FSCFB Exit", "Former Sanctuary Crypt First Barrier")
    
    # Former Sanctuary Crypt Second Floor
    connect("FSCSF FSCFB Exit", "Former Sanctuary Crypt First Barrier")
    connect("FSCSF FSCSB Link", "Former Sanctuary Crypt Second Barrier")
    
    # Former Sanctuary Crypt Second Barrier
    connect("FSCSB FSCSF Exit", "Former Sanctuary Crypt Second Floor")
    connect("FSC SB Entrance", "Former Sanctuary Crypt Second Boss Arena")
    
    # Former Sanctuary Crypt Second Boss Arena
    connect("FSCSBA FSCSB Exit", "Former Sanctuary Crypt Second Barrier")
    connect("FSCSBA FSCTF Link", "Former Sanctuary Crypt Third Floor")
    
    # Former Sanctuary Crypt Third Floor
    connect("FSCTF FSCSBA Exit", "Former Sanctuary Crypt Second Boss Arena")
    connect("FSCTF FSCTB Link", "Former Sanctuary Crypt Third Barrier")
    connect("FSC TFSR Entrance", "Former Sanctuary Crypt Third Floor Side Rooms")
    
    # Former Sanctuary Crypt Third Floor Side Rooms
    connect("FSCTFSR FSCTF Exit", "Former Sanctuary Crypt Third Floor")
    
    # Former Sanctuary Crypt Third Barrier
    connect("FSCTB FSCTF Exit", "Former Sanctuary Crypt Third Floor")
    connect("FSCTB FSCFF Link", "Former Sanctuary Crypt Final Floors")
    
    # Former Sanctuary Crypt Final Floors
    connect("FSCFF FSCTB Exit", "Former Sanctuary Crypt Third Barrier")
    connect("FSC Boss Entrance", "Former Sanctuary Crypt Boss Room")
    connect("FSC FFSR Entrance", "Former Sanctuary Crypt Final Floors Side Rooms")
    
    # Former Sanctuary Crypt Final Floors Side Rooms
    connect("FSCFFSR FSCFF Exit", "Former Sanctuary Crypt Final Floors")
    
    # Former Sanctuary Crypt Boss Room
    connect("FSCBR FSCFF Exit", "Former Sanctuary Crypt Final Floors")
    
    # Towal Highway
    connect("TH ROE Exit", "Ruins of Eternia")
    connect("TH THBTE Link", "Towal Highway Baja Tower Entrance")
    
    # Towal Highway Baja Tower Entrance
    connect("THBTE TH Exit", "Towal Highway")
    connect("BTLF Entrance", "Baja Tower Lower Floors")
    
    # Baja Tower Lower Floors
    connect("BTLF THBTE Exit", "Towal Highway Baja Tower Entrance")
    connect("BTLF BTUF Link", "Baja Tower Upper Floors")
    
    # Baja Tower Upper Floors
    connect("BTUF BTLF Exit", "Baja Tower Lower Floors")
    connect("BTBA Entrance", "Baja Tower Boss Arena")
    
    # Baja Tower Boss Arena
    connect("BTBA BTUF Exit", "Baja Tower Upper Floors")
    
    # Archeozoic Chasm Front
    connect("ACF BTAC Exit", "Bridge to Archeozoic Chasm")
    connect("ACF ACSA Link", "Archeozoic Chasm Submerged Area")
    
    # Archeozoic Chasm Submerged Area
    connect("ACSA ACF Exit", "Archeozoic Chasm Front")
    connect("AC Boss Entrance", "Archeozoic Chasm Boss Arena")
    
    # Archeozoic Chasm Boss Arena
    connect("ACBA ACSA Exit", "Archeozoic Chasm Submerged Area")
    
    # Vista Ridge
    connect("VR TGT Exit", "Temple of the Great Tree")
    connect("VR VRU Link", "Vista Ridge Upper")
    connect("VR LMF Link", "Lodinia Marshlands Front")
    
    # Vista Ridge Upper
    connect("VRU VR Exit", "Vista Ridge")
    
    # Lodinia Marshlands Front
    connect("LMF VR Exit", "Vista Ridge")
    connect("LMF LMS Link", "Lodinia Marshlands South")
    connect("LMF LMNSC Link", "Lodinia Marshlands Near Submerged Cemetery")
    
    # Lodinia Marshlands South
    connect("LMS LMF Exit", "Lodinia Marshlands Front")
    
    # Lodinia Marshlands Near Submerged Cemetery
    connect("LMNSC LMF Exit", "Lodinia Marshlands Front")
    connect("SC Entrance", "Submerged Cemetery")
    connect("LMNSC LMNSG Link", "Lodinia Marshlands Near Sky Garden")
    
    # Lodinia Marshlands Near Sky Garden
    connect("LMNSG LMNSC Exit", "Lodinia Marshlands Near Submerged Cemetery")
    connect("LMNSG SG Link", "Sky Garden")
    connect("LMNSG LMB Link", "Lodinia Marshlands Back")
    
    # Lodinia Marshlands Back
    connect("LMB LMNSG Exit", "Lodinia Marshlands Near Sky Garden")
    connect("LMB GOAH Link", "Graves of Ancient Heroes")
    connect("LMB VOKBD Entrance", "Valley of Kings Before Door")
    
    # Valley of Kings Before Door
    connect("VOKBD LMB Exit", "Lodinia Marshlands Back")
    connect("VOKBD VOKAD Link", "Valley of Kings After Door")
    
    # Valley of Kings After Door
    connect("VOKAD VOKBD Exit", "Valley of Kings Before Door")
    connect("VOK Boss Entrance", "Valley of Kings Boss Arena")
    
    # Valley of Kings Boss Arena
    connect("VOKBA VOKAD Exit", "Valley of Kings After Door")
    
    # Graves of Ancient Heroes
    connect("GOAH LMB Exit", "Lodinia Marshlands Back")
    
    # Sky Garden
    connect("SG LMNSG Exit", "Lodinia Marshlands Near Sky Garden")
    
    # Submerged Cemetery
    connect("SC LMNSC Exit", "Lodinia Marshlands Near Submerged Cemetery")
    connect("BMHR Link", "Bolado Monastery Hidden Room")
    connect("SC SH Link", "Soundless Hall")
    
    # Soundless Hall
    connect("SH SC Exit", "Submerged Cemetery")
    
    # Bolado Monastery Hidden Room
    connect("BMHR SC Exit", "Submerged Cemetery")
    
    # Towering Coral Forest (Night) Front Half
    connect("TCFNFH TCFNRH Link", "Towering Coral Forest (Night) Rear Half")
    
    # Towering Coral Forest (Night) Rear Half
    connect("TCFNRH TCFNFH Exit", "Towering Coral Forest (Night) Front Half")
    
    # Mont Gendarme (Night) Front Half
    connect("MGNFH PP Exit", "Primordial Passage")
    connect("MGNFH MGNRH Link", "Mont Gendarme (Night) Rear Half")
    
    # Mont Gendarme (Night) Rear Half
    connect("MGNRH MGNFH Exit", "Mont Gendarme (Night) Front Half")
    
    # Pangaia Plains (Night)
    connect("PPHN SNA Exit", "Seiren North Access")

    # Shuffle entrances if enabled
    if options.dungeon_entrance_shuffle.value:

        # Update the world's dungeon connections with the shuffled entrances
        for entrance_name, region_name in Ys8World.dungeon_connections.items():
            entrance = multiworld.get_entrance(entrance_name, player)
            child_region = entrance.connected_region
            child_region.entrances.remove(entrance)
            entrance.connected_region = None
            connect(entrance_name, region_name)

def create_region(multiworld: MultiWorld, player: int, name: str, data: Ys8RegionData):
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = Ys8Location(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)

    if data.region_exits:
        for connector_name in data.region_exits:
            entrance = Entrance(player, connector_name, region)
            region.exits.append(entrance)

    return region