from typing import TYPE_CHECKING, NamedTuple
from .Options import Ys8Options

if TYPE_CHECKING:
    from . import Ys8World

def dungeon_entrance_shuffle(Ys8World):
    multiworld = Ys8World.multiworld
    player     = Ys8World.player
    options    = Ys8World.options
    

    discovery_shuffle_dependent_exits: list = ["Meta TCF Entrance", "SB EV Entrance"]
    single_connector_exits: list = ["ORC SJ Entrance"]
    multi_connector_exits: list = ["WC Entrance", "NCN TCF Entrance", "GRV EVF Entrance", "GRVSC SJ Entrance", "PP MG Entrance",
                                   "SNA MGAB Entrance", "TGTG OO Entrance", "AC Entrance", "FSC Entrance", "BTLF Entrance", "LMB VOKBD Entrance",
                                   "ST Entrance", "NCA ECCBG Entrance"]
    multi_connector_regions: list = ["Towering Coral Forest Front", "Towering Coral Forest After Boss", "Eroded Valley Front",
                                    "Eroded Valley After Boss", "Schlamm Jungle Front", "Schlamm Jungle After Boss", "Mont Gendarme Front",
                                    "Mont Gendarme After Boss"]
    single_connector_regions: list = ["Waterdrop Cave", "East Coast Cave Before Gilkyra", "Silent Tower", "Octus Overlook","Former Sanctuary Crypt Front",
                                      "Baja Tower Lower Floors", "Archeozoic Chasm Front", "Valley of Kings Before Door"]
    entrance_pairs: list[dict[str, str]] = {"Towering Coral Forest Front": "TCF NCN Exit", "Towering Coral Forest After Boss": "TCFAB Meta Exit", "Eroded Valley Front": "EVF GRV Exit", 
                                             "Eroded Valley After Boss": "EVAB SB Exit", "Schlamm Jungle Front": "SJF GRVSC Exit", "Schlamm Jungle After Boss": "SJAB ORC Exit", 
                                             "Mont Gendarme Front": "MGF PPGE Exit", "Mont Gendarme After Boss": "MGPB SNA Exit", "Waterdrop Cave": "WC Exit", 
                                             "East Coast Cave Before Gilkyra": "ECCBG NCA Exit", "Silent Tower": "STE OST Exit", "Octus Overlook": "OO TGT Exit", 
                                             "Former Sanctuary Crypt Front": "FSCF ROEHP Exit", "Baja Tower Lower Floors": "BTLF THBTE Exit", "Archeozoic Chasm Front": "ACF BTAC Exit", 
                                             "Valley of Kings Before Door": "VOKBD LMB Exit"}
    region_pairs: list[dict[str, str]] = {"Meta TCF Entrance": "Metavolicalis Area", "SB EV Entrance": "Sunrise Beach", "ORC SJ Entrance": "Odd Rock Coast", 
                                          "WC Entrance": "Calm Inlet Area", "NCN TCF Entrance": "Nameless Coast North", "GRV EVF Entrance": "Great River Valley Area",
                                          "GRVSC SJ Entrance": "Great River Valley South Camp", "PP MG Entrance": "Primordial Passage Gendarme Entrance", 
                                          "SNA MGAB Entrance": "Seiren North Access", "TGTG OO Entrance": "Temple of the Great Tree Garden", "AC Entrance": "Bridge to Archeozoic Chasm", 
                                          "FSC Entrance": "Ruins of Eternia Hidden Passage", "BTLF Entrance": "Towal Highway Baja Tower Entrance", 
                                          "LMB VOKBD Entrance": "Lodinia Marshlands Back", "ST Entrance": "Silent Tower Entrance", "NCA ECCBG Entrance": "Nostalgia Cape Area"}
    merged_regions: list = []
    shuffled_connectors: dict[str, str] = {}
    
    # Manually set the connections for entrances that are not shuffled
    if not options.former_sanctuary_crypt.value:
        shuffled_connectors["FSC Entrance"] = "Former Sanctuary Crypt Front"
        shuffled_connectors[entrance_pairs["Former Sanctuary Crypt Front"]] = region_pairs["FSC Entrance"]

    # Set the connections for entrances that are shuffled but have dependencies
    if not options.discovery_sanity.value:
        single_connector_exits.extend(discovery_shuffle_dependent_exits)
    elif options.discovery_sanity.value:
        multi_connector_exits.extend(discovery_shuffle_dependent_exits)

    # Guarantee our single connector exits are shuffled into multi connector regions first, preventing isolation 
    Ys8World.multiworld.random.shuffle(multi_connector_regions)
    for region_exit in single_connector_exits:
        if region_exit in shuffled_connectors.keys():
            continue
        shuffled_connectors[region_exit] = multi_connector_regions.pop()
        Ys8World.entrance_spoiler.append((region_exit + "=>" +shuffled_connectors[region_exit]))
    
    # Merge the remaining multi connectors because it doesn't matter anymore and do the rest of the shuffling
    merged_regions.extend(single_connector_regions)
    merged_regions.extend(multi_connector_regions)
    Ys8World.multiworld.random.shuffle(merged_regions)
    for region_exit in multi_connector_exits:
        if region_exit in shuffled_connectors.keys():
            continue
        shuffled_connectors[region_exit] = merged_regions.pop()
        Ys8World.entrance_spoiler.append((region_exit + "=>" +shuffled_connectors[region_exit]))

    Ys8World.dungeon_connections = shuffled_connectors.copy()

    # Get connector pairs to make sure our connections are correct in both directions
    for region_exit, region in shuffled_connectors.items():
        Ys8World.dungeon_connections[entrance_pairs[region]] = region_pairs[region_exit]

    
        Ys8World.entrance_spoiler.append(entrance_pairs[region] + "=>" + region_pairs[region_exit])

    for line in Ys8World.entrance_spoiler:
        print(line)