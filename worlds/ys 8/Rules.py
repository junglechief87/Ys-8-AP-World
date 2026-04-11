from typing import TYPE_CHECKING
from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from math import ceil
from BaseClasses import Entrance, Location
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
    set_rule(get_ent("CIA to Lapis Mineral Vein Area"), lambda state: state.has("Lapis Mineral Vein", Ys8World.player))
    set_rule(get_ent("CIA to Soundless Hall"), lambda state: state.has("Soundless Hall", Ys8World.player))
    set_rule(get_ent("CIA to Sky Garden"), lambda state: state.has("Sky Garden", Ys8World.player))
    set_rule(get_ent("CIA to Graves of Ancient Heroes"), lambda state: state.has("Graves of Ancient Heroes", Ys8World.player))
    set_rule(get_ent("CIA to TCF Near Boss"), lambda state: state.has("Glow Stone", Ys8World.player))

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
    set_rule(get_ent("GRV to SJ:Bridge"), lambda state: state.has("Dina", Ys8World.player))
    set_rule(get_ent("GRV to PP"), lambda state: state.has("Maiden Journal", Ys8World.player) and state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("SJ:Bridge to GRV"), lambda state: state.has("Dina", Ys8World.player))

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
    set_rule(get_ent("MG:Bridge to PP"), lambda state: state.has("Maiden Journal", Ys8World.player))
    set_rule(get_ent("PP to MG Night"), lambda state: state.has("Glow Stone", Ys8World.player))

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
    set_rule(get_ent("Seiren North to Pangaia Plans Night"), lambda state: state.has("Glow Stone", Ys8World.player))

    # Stone Pillar Wind Cave Connections
    set_rule(get_ent("SPWC to SPWC Upper"), lambda state: state.has("Grip Gloves", Ys8World.player))

    # Temple of the Great Tree Connections
    set_rule(get_ent("TotGT to Seiren North"), lambda state: state.has("Dana", Ys8World.player))
    set_rule(get_ent("TotGT to RoE"), lambda state: state.has("Green Seal of Roaring Stone", Ys8World.player))
    set_rule(get_ent("TotGT Boss Arena to TotGT Garden"), lambda state: battle_logic(state, Ys8World.player, 200, Ys8World.options))
    set_rule(get_ent("TotGT Boss Arena to TotGT"), lambda state: battle_logic(state, Ys8World.player, 200, Ys8World.options))
    set_rule(get_ent("TotGT Garden to Octus"), lambda state: has_required_crew(state, Ys8World.player, 20)) # placeholder until options are completed

    # Ruins of Eternia Connections
    set_rule(get_ent("RoE to Seiren North"), lambda state: state.has("Blue Seal of Whirling Water", Ys8World.player))
    set_rule(get_ent("RoE to TotGT"), lambda state: state.has("Green Seal of Roaring Stone", Ys8World.player))
    set_rule(get_ent("RoE to AC:Bridge"), lambda state: state.has("Frozen Flower", Ys8World.player))
    set_rule(get_ent("RoE to TH"), lambda state: state.has("Dana", Ys8World.player))
    set_rule(get_ent("RoE to FSC First Barrier"), lambda state: state.has_all(["Jade Pendant", "Dina"], Ys8World.player))
    set_rule(get_ent("RoE to Bolado"), lambda state: state.has("Frozen Flower", Ys8World.player))
    set_rule(get_ent("Bolado to Bolado Basement"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("AC:Bridge to RoE"), lambda state: state.has("Frozen Flower", Ys8World.player))

    # Former Sanctuary Connections
    set_rule(get_ent("FSC First Barrier to RoE"), lambda state: state.has_all(["Jade Pendant", "Dina"], Ys8World.player))
    set_rule(get_ent("FSC First Barrier to FSC Second Floor"), lambda state: state.has("Essence Key Stone", Ys8World.player))
    set_rule(get_ent("FSC First Barrier to FSC First Barrier North Brazier Room"), lambda state: state.has_all_counts({"Essence Key Stone": 9}, Ys8World.player))
    set_rule(get_ent("FSC First Barrier to FSC Second Floor"), lambda state: state.has("Archeopteryx Wings", Ys8World.player))
    set_rule(get_ent("FSC Second Floor to FSC Second Barrier"), lambda state: state.has_all_counts({"Essence Key Stone": 3}, Ys8World.player))
    set_rule(get_ent("FSC Second Floor to FSC Second Boss Arena"), lambda state: state.has("Purifying Bell", Ys8World.player))
    set_rule(get_ent("FSC Second Boss Arena to FSC Third Floor"), lambda state: state.has("Float Shoes", Ys8World.player))
    set_rule(get_ent("FSC Third Floor Side Rooms to FSC Third Floor"), lambda state: state.has_all_counts({"Essence Key Stone": 9}, Ys8World.player))
    set_rule(get_ent("FSC Third Barrier to FSC Final Floors"), lambda state: state.has_all_counts({"Essence Key Stone": 6}, Ys8World.player))
    set_rule(get_ent("FSC Final Floors to FSC Final Floor Side Rooms"), lambda state: state.has_all_counts({"Essence Key Stone": 9}, Ys8World.player))
    set_rule(get_ent("FSC Final Floors to FSC Boss Room"), lambda state: has_required_crew(state, Ys8World.player, 20)) # placeholder until options are completed                                                                              

    # Towal Highway Connections
    set_rule(get_ent("TH to RoE"), lambda state: state.has("Dana", Ys8World.player))
    set_rule(get_ent("TH to Baja"), lambda state: state.has_all(["Grip Gloves", "Golden Seal of Piercing Light"], Ys8World.player))

    # Baja Tower Connections
    set_rule(get_ent("Baja Tower Lower Floors to Baja Tower Upper Floors"), lambda state: state.has_all(["Grip Gloves", "Archeopteryx Wings"], Ys8World.player))
    set_rule(get_ent("Baja Tower Upper Floors to Baja Tower Boss Arena"), lambda state: battle_logic(state, Ys8World.player, 200, Ys8World.options))

    # Archeozoic Chasm Connections
    set_rule(get_ent("AC Front to AC Submerged Area"), lambda state: state.has("Hermit's Scale", Ys8World.player))
    set_rule(get_ent("AC Submerged Area to AC Boss Arena"), lambda state: state.has("Hermit's Scale", Ys8World.player))

    # Vista Ridge Connections
    set_rule(get_ent("Vista Ridge to Vista Ridge Upper"), lambda state: state.has("Grip Gloves", Ys8World.player) and has_required_crew(state, Ys8World.player, 21))

    # Lodinia Marshland Connections
    set_rule(get_ent("LM Entrance to LM Near Submerged Cemetery"), lambda state: state.has("Treasure Chest Key", Ys8World.player))
    set_rule(get_ent("LM Near Submerged Cemetery to LM Entrance"), lambda state: state.has("Treasure Chest Key", Ys8World.player))
    set_rule(get_ent("LM Entrance to LM South"), lambda state: state.has("Float Shoes", Ys8World.player))
    set_rule(get_ent("LM Near Submerged Cemetery to Near Sky Garden"), lambda state: state.has_any(["Float Shoes", "Hermit's Scale"], Ys8World.player))
    set_rule(get_ent("LM Near Submerged Cemetery to Submerged Cemetery"), lambda state: has_required_crew(state, Ys8World.player, 22) and state.has_all(["Glow Stone", "Hermit's Scale"], Ys8World.player))
    set_rule(get_ent("LM Near Sky Garden to Sky Garden"), lambda state: state.has_all(["Grip Gloves", "Archeopteryx Wings"], Ys8World.player))
    set_rule(get_ent("LM Near Sky Garden to VoK Entrance"), lambda state: state.has_any(["Float Shoes", "Hermit's Scale"], Ys8World.player))
    set_rule(get_ent("LM Near Sky Garden to LM Near Submerged Cemetery"), lambda state: state.has_any(["Float Shoes", "Hermit's Scale"], Ys8World.player))
    
    # Valley of Kings Connections
    set_rule(get_ent("VoK Entrance to LM Near Sky Garden"), lambda state: state.has_any(["Float Shoes", "Hermit's Scale"], Ys8World.player))
    set_rule(get_ent("VoK Entrance to Graves of Ancient Heroes"), lambda state: state.has_all(["Shrine Maiden Amulet", "Grip Gloves"], Ys8World.player))
    set_rule(get_ent("VoK Before Door to VoK After Door"), lambda state: state.has("Purifying Bell", Ys8World.player))
    set_rule(get_ent("VoK After Door to VoK Boss Arena"), lambda state: battle_logic(state, Ys8World.player, 150, Ys8World.options) and state.has("Purifying Bell", Ys8World.player))
    set_rule(get_ent("Graves of Ancient Heroes to VoK Entrance"), lambda state: state.has("Shrine Maiden Amulet", Ys8World.player))

    # Submerged Cemetery Connections
    set_rule(get_ent("Submerged Cemetery to LM Near Submerged Cemetery"), lambda state: has_required_crew(state, Ys8World.player, 22))
    set_rule(get_ent("Submerged Cemetery to Bolado Hidden Room"), lambda state: state.has_all(["Glow Stone", "Hermit's Scale"], Ys8World.player))
    set_rule(get_ent("Submerged Cemetery to Soundless Hall"), lambda state: state.has_all(["Glow Stone", "Hermit's Scale"], Ys8World.player))
    set_rule(get_ent("Soundless Hall to Submerged Cemetery"), lambda state: state.has_all(["Glow Stone", "Hermit's Scale"], Ys8World.player))
    set_rule(get_ent("Bolado Hidden Room to Submerged Cemetery"), lambda state: state.has_all(["Glow Stone", "Hermit's Scale"], Ys8World.player))

    # Night Connections
    set_rule(get_ent("TCF Night Front to TCF Night Rear"), lambda state: state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("MG Night Front to MG Night Rear"), lambda state: state.has("Grip Gloves", Ys8World.player))

def set_location_rules(Ys8World: Ys8World):
    pass

