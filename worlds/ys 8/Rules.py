from typing import TYPE_CHECKING
from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from math import ceil
from BaseClasses import ItemClassification
from .Locations import Ys8Location, location_table
from .Items import Ys8Item, item_table
from .Options import Ys8Options

if TYPE_CHECKING:
    from . import Ys8World
    
def set_all_rules(Ys8World: Ys8World):
    set_entrance_rules(Ys8World)
    set_location_rules(Ys8World)

def has_required_crew(state: CollectionState, player: int, crew_count: int) -> bool:
    return state.has_from_list([item for item, data in item_table.items() if data.category == "Crew"], player, crew_count)

def battle_logic(state: CollectionState, player: int, required_str: int, options: Ys8Options) -> bool:
    return True

def map_completion_logic(state: CollectionState, player: int, options: Ys8Options) -> bool:
    return True

def set_entrance_rules(Ys8World: Ys8World): 

    def get_ent(EntranceName: str) -> Entrance:
        return Ys8World.multiworld.get_entrance(EntranceName, Ys8World.player)

    # Calm Inlet Area Connections
    set_rule(get_ent("CIA to NC North of Boulder"), lambda state: state.has("Grip Gloves", Ys8World.player) or has_required_crew(state, Ys8World.player, 6))
    set_rule(get_ent("CIA to Rainbow Falls"), lambda state: state.has("Rainbow Falls", Ys8World.player))
    set_rule(get_ent("CIA to Parasequoia"), lambda state: state.has("Parasequoia", Ys8World.player))
    set_rule(get_ent("CIA to Rainbow Falls"), lambda state: state.has("Rainbow Falls", Ys8World.player))
    set_rule(get_ent("CIA to Metavolicalis"), lambda state: state.has("Metavolicalis", Ys8World.player))
    set_rule(get_ent("CIA to IL 1"), lambda state: state.has_any(["T's Memo", "T's Memo A", "T's Memo B", "T's Memo C"], Ys8World.player))
    set_rule(get_ent("CIA to IL 2"), lambda state: state.has_any_count(["T's Memo", "T's Memo A", "T's Memo B", "T's Memo C"], Ys8World.player, 2))
    set_rule(get_ent("CIA to IL 3"), lambda state: state.has_any_count(["T's Memo", "T's Memo A", "T's Memo B", "T's Memo C"], Ys8World.player, 3))
    set_rule(get_ent("CIA to Map Completion"), lambda state: state.has("Euron", Ys8World.player))
    set_rule(get_ent("CIA to Jewel Trade"), lambda state: state.has("Dina", Ys8World.player))
    set_rule(get_ent("CIA to Fish Trade"), lambda state: state.has("Fishing Rod", Ys8World.player))
    set_rule(get_ent("CIA to Discovery Turn In"), lambda state: state.has("Austin", Ys8World.player))
    set_rule(get_ent("CIA to Airs Cairn"), lambda state: state.has("Airs Cairn", Ys8World.player))
    set_rule(get_ent("CIA to Chimney Rock"), lambda state: state.has("Chimney Rock", Ys8World.player))
    set_rule(get_ent("CIA to Milky White Vein"), lambda state: state.has("Milky White Vein", Ys8World.player))
    set_rule(get_ent("CIA to Indigo Mineral Vein"), lambda state: state.has("Indigo Mineral Vein", Ys8World.player))
    set_rule(get_ent("CIA to Beached Remains"), lambda state: state.has("Beached Remains", Ys8World.player))
    set_rule(get_ent("CIA to Beehive"), lambda state: state.has("Beehive", Ys8World.player))
    set_rule(get_ent("CIA to FoMH"), lambda state: state.has("Field of Medicinal Herbs", Ys8World.player))
    set_rule(get_ent("CIA to Hidden Pirate Storehouse"), lambda state: state.has("Hidden Pirate Storehouse", Ys8World.player))
    set_rule(get_ent("CIA to Ship Graveyard"), lambda state: state.has("Ship Graveyard", Ys8World.player))
    set_rule(get_ent("CIA to Solitude Island"), lambda state: state.has_any(["Ship Blueprint", "Magna Carpa"], Ys8World.player))
    set_rule(get_ent("CIA to WH"), lambda state: state.has("Grip Gloves", Ys8World.player) and has_required_crew(state, Ys8World.player, 11))
    set_rule(get_ent("CIA to Zephyr Hill"), lambda state: state.has("Zephyr Hill", Ys8World.player))
    set_rule(get_ent("CIA to Lapis Mineral Vein Area"), lambda state: state.has("Lapis Mineral Vein", Ys8World.player))
    set_rule(get_ent("CIA to Prismatic Mineral Vein"), lambda state: state.has("Prismatic Mineral Vein", Ys8World.player))
    set_rule(get_ent("CIA to Unicalamites"), lambda state: state.has("Unicalamites", Ys8World.player))
    set_rule(get_ent("CIA to Breath Fountain"), lambda state: state.has("Breath Fountain", Ys8World.player))
    set_rule(get_ent("CIA to Ancient Tree"), lambda state: state.has("Ancient Tree", Ys8World.player))

    # Towering Coral Forest Connections
    set_rule(get_ent("TCF Mid-Boss Arena to TCF Front"), lambda state: battle_logic(state, Ys8World.player, 10, Ys8World.options))
    set_rule(get_ent("TCF Mid-Boss Arena to TCF Corpse"), lambda state: battle_logic(state, Ys8World.player, 10, Ys8World.options))
    set_rule(get_ent("TCF Corpse to TCF RF"), lambda state: state.has("Grip Gloves", Ys8World.player)) 
    set_rule(get_ent("Rainbow Falls to TCF Boss Area"), lambda state: state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("TCF Boss Area to TCF RF"), lambda state: state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("TCF Boss Area to TCF Boss"), lambda state: state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("TCF Boss to TCF Boss Area"), lambda state: battle_logic(state, Ys8World.player, 30, Ys8World.options))
    set_rule(get_ent("TCF Exit to Meta Area"), lambda state: battle_logic(state, Ys8World.player, 30, Ys8World.options))

    # Metavolicalis Area Connections
    set_rule(get_ent("Meta Area to Para Area"), lambda state: has_required_crew(state, Ys8World.player, 14))

    # Nameless Coast North of Boulder Connections
    set_rule(get_ent("NC North of Boulder to GRV"), lambda state: state.has("Archeopteryx Wings", Ys8World.player) or has_required_crew(state, Ys8World.player, 8))

    # Great River Valley Area Connections
    set_rule(get_ent("GRV to Base of WF Gendarme"), lambda state: state.has("Float Shoes", Ys8World.player))
    set_rule(get_ent("GRV to WG Dark Area"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("GRV to LCA"), lambda state: state.has("Dina", Ys8World.player))
    set_rule(get_ent("GRV to SJ Front"), lambda state: state.has("Dina", Ys8World.player))
    set_rule(get_ent("GRV to PP"), lambda state: state.has("Maiden Journal", Ys8World.player) and state.has("Grip Gloves", Ys8World.player))

    # Base of Western Foot of Gendarme Connections
    set_rule(get_ent("Base of WF Gendarme to WF Gendarme"), lambda state: has_required_crew(state, Ys8World.player, 11))

    # Western Foot of Gendarme Connections
    set_rule(get_ent("CIA to Airs Cairn"), lambda state: state.has("Airs Cairn", Ys8World.player))
    set_rule(get_ent("WF Gendarme to Base of WF Gendarme"), lambda state: has_required_crew(state, Ys8World.player, 11))

    # Waterfall Grotto Connections
    set_rule(get_ent("Milky White Vein to WG Dark Area"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("WG Dark Area to Milky White Vein"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("WG Dark Area to GRV"), lambda state: state.has("Glow Stone", Ys8World.player))

    # Longhorn Coast Area Connections
    set_rule(get_ent("LCA to GRV"), lambda state: state.has("Dina", Ys8World.player))
    set_rule(get_ent("LCA to Outside ST"), lambda state: state.has("Archeopteryx Wings", Ys8World.player))
    set_rule(get_ent("LCA to Nostalgia Cape"), lambda state: state.has("Archeopteryx Wings", Ys8World.player))
    set_rule(get_ent("LCA to Beehive"), lambda state: state.has("Dina", Ys8World.player))

    # Eroded Valley Connections
    set_rule(get_ent("EV Front to EV Dark Area"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("EV Dark Area to EV Front"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("EV Dark Area to EV Indigo Mineral Vein"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("EV Indigo Mineral Vein to EV Dark Area"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("EV Mid-Boss Arena to EV Front"), lambda state: battle_logic(state, Ys8World.player, 60, Ys8World.options))
    set_rule(get_ent("EV Mid-Boss Arena to EV Webbed Walkway"), lambda state: battle_logic(state, Ys8World.player, 60, Ys8World.options) and state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("EV Webbed Walkway to EV Before Boss"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("EV Before Boss to EV Webbed Walkway"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("EV Before Boss to EV Boss Arena"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("EV Boss Arena to EV Before Boss"), lambda state: battle_logic(state, Ys8World.player, 80, Ys8World.options) and state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("EV Boss Arena to SB"), lambda state: battle_logic(state, Ys8World.player, 80, Ys8World.options))

    # Schlamm Jungle Connections
    set_rule(get_ent("SJ Front to GRV"), lambda state: state.has("Dina", Ys8World.player))
    set_rule(get_ent("SJ Mid-Boss Arena to SJ Front"), lambda state: battle_logic(state, Ys8World.player, 100, Ys8World.options))
    set_rule(get_ent("SJ Mid-Boss Arena to SJ Muddy Path"), lambda state: battle_logic(state, Ys8World.player, 100, Ys8World.options))
    set_rule(get_ent("SJ Muddy Path to SJ Mid-Boss Arena"), lambda state: battle_logic(state, Ys8World.player, 100, Ys8World.options))
    set_rule(get_ent("SJ Muddy Path to SJ Before Boss"), lambda state: state.has("Float Shoes", Ys8World.player))
    set_rule(get_ent("SJ Muddy Path to SJ FoMH"), lambda state: state.has("Dina", Ys8World.player) and state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("SJ FoMH to SJ Muddy Path"), lambda state: state.has("Dina", Ys8World.player))
    set_rule(get_ent("SJ Before Boss to SJ Muddy Path"), lambda state: state.has("Float Shoes", Ys8World.player))
    set_rule(get_ent("SJ Boss Arena to SJ Before Boss"), lambda state: battle_logic(state, Ys8World.player, 120, Ys8World.options) and state.has("Float Shoes", Ys8World.player))
    set_rule(get_ent("SJ Boss Arena to ORC"), lambda state: battle_logic(state, Ys8World.player, 120, Ys8World.options) and state.has("Float Shoes", Ys8World.player))
    
    # East Coast Cave Connections
    set_rule(get_ent("ECC BG to ECC AG"), lambda state:  battle_logic(state, Ys8World.player, 170, Ys8World.options))
    set_rule(get_ent("ECC AG to ECC BG"), lambda state: battle_logic(state, Ys8World.player, 170, Ys8World.options) and state.has("Archeopteryx Wings", Ys8World.player))
    set_rule(get_ent("ECC AG to PSE"), lambda state: state.has("Logbook 1", Ys8World.player))

    # Pirate Ship Eleftheria Connections
    set_rule(get_ent("PSE to PSE Submerged Hold"), lambda state: state.has("Hermit's Scale", Ys8World.player))
    set_rule(get_ent("PSE Submerged Hold to PSE"), lambda state: state.has("Hermit's Scale", Ys8World.player))

    # Primordial Passage Connections
    set_rule(get_ent("PP to GRV"), lambda state: state.has("Maiden Journal", Ys8World.player))
    set_rule(get_ent("PP to MG"), lambda state: state.has("Maiden Journal", Ys8World.player))

    # Outside Silent Tower Connections
    set_rule(get_ent("Outside ST to ST"), lambda state: has_required_crew(state, Ys8World.player, 24))

    # Weathervane Hills Connections
    set_rule(get_ent("WH to Past Insect Nests"), lambda state: state.has("Dina", Ys8World.player))
    set_rule(get_ent("WH to UMV"), lambda state: state.has("Hermit's Scale", Ys8World.player))

    # Underground Water Vein Connections
    set_rule(get_ent("Lapis Mineral Vein Area to UWV"), lambda state: state.has("Hermit's Scale", Ys8World.player))
    set_rule(get_ent("UWV to Lapis Mineral Vein Area"), lambda state: state.has("Hermit's Scale", Ys8World.player))
    set_rule(get_ent("UWV to WH"), lambda state: state.has("Hermit's Scale", Ys8World.player))
    
    # Mont Gendarme Connections
    set_rule(get_ent("MG to MG Mid"), lambda state: state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("MG Mid to MG Mid-Boss Arena"), lambda state: state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("MG Mid-Boss Arena to MG Mid"), lambda state: battle_logic(state, Ys8World.player, 160, Ys8World.options))
    set_rule(get_ent("MG Mid-Boss Arena to MG Upper"), lambda state: battle_logic(state, Ys8World.player, 160, Ys8World.options) and state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("MG Upper to MG Boss Arena"), lambda state: state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("MG Boss Arena to MG Upper"), lambda state: battle_logic(state, Ys8World.player, 230, Ys8World.options))
    set_rule(get_ent("MG Boss Arena to Seiren North"), lambda state: battle_logic(state, Ys8World.player, 230, Ys8World.options))

    # Seiren North Connections
    set_rule(get_ent("Seiren North to SPWC"), lambda state: has_required_crew(state, Ys8World.player, 18))
    set_rule(get_ent("Seiren North to TotGT"), lambda state: state.has("Dana", Ys8World.player))
    set_rule(get_ent("Seiren North to RoE"), lambda state: state.has("Blue Seal of Whirling Water", Ys8World.player))
                                                                                  
def set_location_rules(Ys8World: Ys8World):
    pass

