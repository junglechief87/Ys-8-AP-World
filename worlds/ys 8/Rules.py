from typing import TYPE_CHECKING
from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from math import ceil
from BaseClasses import Entrance, Location
from .Locations import Ys8Location, location_table
from .Items import Ys8Item, item_table, event_item_table
from .Options import Ys8Options

if TYPE_CHECKING:
    from . import Ys8World

# STR values from Level Scaling.csv, keyed by level at intervals of 5.
# Used with player_level floored to the nearest multiple of 5.
_GRIND_STR: dict[int, int] = {
     5:  20, 10:  43, 15:  66, 20:  90, 25: 113,
    30: 138, 35: 162, 40: 187, 45: 211, 50: 236,
    55: 260, 60: 285, 65: 310, 70: 335, 75: 359,
    80: 384, 85: 408, 90: 434, 95: 459,
}

def set_all_rules(Ys8World: Ys8World):
    set_entrance_rules(Ys8World)
    set_location_rules(Ys8World)

def has_required_crew(state: CollectionState, player: int, crew_count: int) -> bool:
    return state.has_from_list([item for item, data in item_table.items() if data.category == "Crew"], player, crew_count)

def has_required_party(state: CollectionState, player: int, party_count: int) -> bool:
    return state.has_from_list([item for item, data in item_table.items() if data.flags and "Party" in data.flags], player, party_count)

def bosses_defeated(state: CollectionState, player: int) -> int:
    return sum(1 for item, data in event_item_table.items() if data.type == "Boss" and state.has(item, player))

def material_access(material: str, state: CollectionState, player: int) -> bool:
    """Returns True if the player can reach a viable farming spot for the named material."""
    if material == "Iron Ore":
        # Item points: Eroded Valley (10–20%, many nodes), Towering Coral Forest (10%)
        return state.has_any({
            "Material: Iron Ore (Eroded Valley)",
            "Material: Iron Ore (Towering Coral Forest)",
        }, player)
    if material == "Tektite Ore":
        # Item points: Western Foot of Gendarme (10%), Mont Gendarme (10%), Towal Highway (10%)
        return state.has_any({
            "Material: Tektite Ore (Western Foot of Gendarme)",
            "Material: Tektite Ore (Mont Gendarme)",
            "Material: Tektite Ore (Towal Highway)",
        }, player)
    if material == "Essence Stone":
        # Enemy drops: Baja Tower M0623 Masquard 15%, Valley of Kings M0642 80%
        return state.has_any({
            "Material: Essence Stone (Baja Tower)",
            "Material: Essence Stone (Valley of Kings)",
        }, player)
    if material == "Dragon Crest Stone":
        # Enemy drops: Valley of Kings M0642 10%, Silent Tower M0942 15%
        return state.has_any({
            "Material: Dragon Crest Stone (Valley of Kings)",
            "Material: Dragon Crest Stone (Silent Tower)",
        }, player)
    if material == "Ancient Bone":
        # Enemy drops: TotGT M0680 Ratnilarda 80% (Dana gate), AC M0663 Dornicle 80% (Frozen Flower gate)
        return state.has_any({
            "Material: Ancient Bone (Temple of the Great Tree)",
            "Material: Ancient Bone (Archeozoic Chasm)",
        }, player)
    if material == "Ancient Hide":
        # Enemy drops: Specklamander M1405 60% in Waterdrop Cave (early) and Nostalgia Cape (AW gate)
        return state.has_any({
            "Material: Ancient Hide (Waterdrop Cave)",
            "Material: Ancient Hide (Nostalgia Cape)",
        }, player)
    if material == "Saurian Scale":
        # Enemy drops: GRV M1010 Gigantyrannus 80% (crew 8/AW gate), Towal Highway M1021 Primarivaur 80% (Dana gate)
        return state.has_any({
            "Material: Saurian Scale (Great River Valley)",
            "Material: Saurian Scale (Towal Highway)",
        }, player)
    if material == "Underworld Hide":
        # Enemy drops: Octus Overlook Vula-Menua variants 80% (only accessible source)
        return state.has("Material: Underworld Hide (Octus Overlook)", player)
    if material == "Underworld Bone":
        # Enemy drops: Octus Overlook Vula-Marut variants 80% (only accessible source)
        return state.has("Material: Underworld Bone (Octus Overlook)", player)
    if material == "Beast Hide":
        # Enemy drops: Schlamm Jungle M0300 Shabil 80% (Float Shoes gate), WF Gendarme M0302 Badessa 80% (crew 11 gate)
        return state.has_any({
            "Material: Beast Hide (Schlamm Jungle)",
            "Material: Beast Hide (Western Foot of Gendarme)",
        }, player)
    if material == "Beast Bone":
        # Enemy drops: East Coast Cave M0700 Gibo 80% (Hidden Pirate Storehouse item), Vista Ridge M0504 Gilaaf 80% (post-TotGT)
        return state.has_any({
            "Material: Beast Bone (East Coast Cave)",
            "Material: Beast Bone (Vista Ridge)",
        }, player)
    if material == "Dandale Horn":
        # M0605 Dandale — Lodinia Marshland (Past) only at 10%; LM Near Sky Garden is the closest present-day proxy
        return state.has("Material: Dandale Horn (Lodinia Marshlands)", player)
    if material == "Beautiful Flower":
        # Nameless Coast item points; always accessible
        return state.has("Material: Beautiful Flower (Nameless Coast)", player)
    if material == "Stalactite":
        # Nameless Coast item points; always accessible
        return state.has("Material: Stalactite (Nameless Coast)", player)
    if material == "Glow Rock":
        # TCF Night (t2) item points; requires Glow Stone (CIA → TCF Night)
        return state.has("Material: Glow Rock (Towering Coral Forest Night)", player)
    if material == "Flexible Branch":
        # M0124 Larfo TCF Night Front 80%; M0910 Cramatange Waterfall Grotto Dark Area 80%
        return state.has_any({
            "Material: Flexible Branch (Towering Coral Forest Night)",
            "Material: Flexible Branch (Waterfall Grotto)",
        }, player)
    if material == "Beast Claw":
        # M0303 Warsadessa Western Foot of Gendarme 80%
        return state.has("Material: Beast Claw (Western Foot of Gendarme)", player)
    if material == "Razor Feather":
        # M0202 Valquito Schlamm Jungle Front 15% rare
        return state.has("Material: Razor Feather (Schlamm Jungle)", player)
    if material == "Sword Tip Fang":
        # M0303 Warsadessa Western Foot of Gendarme 40% special
        return state.has("Material: Sword Tip Fang (Western Foot of Gendarme)", player)
    if material == "Thick Hide":
        # M0302 Badessa WFG 80%; M0300 Shabil Schlamm Jungle Front 80%
        return state.has_any({
            "Material: Thick Hide (Western Foot of Gendarme)",
            "Material: Thick Hide (Schlamm Jungle)",
        }, player)
    if material == "Lustrous Scale":
        # M1401 Orseapus East Coast Cave Before Gilkyra 5%; Nostalgia Cape 5%
        return state.has_any({
            "Material: Lustrous Scale (East Coast Cave)",
            "Material: Lustrous Scale (Nostalgia Cape)",
        }, player)
    if material == "Accursed Shell":
        # M0303 Warsadessa Western Foot of Gendarme 60% special
        return state.has("Material: Accursed Shell (Western Foot of Gendarme)", player)
    if material == "Thunder Claw":
        # M1010 Gigantyrannus Great River Valley 60%; M0641 Fabnir Valley of Kings Entrance 15%
        return state.has_any({
            "Material: Thunder Claw (Great River Valley)",
            "Material: Thunder Claw (Valley of Kings)",
        }, player)
    if material == "Ancient Lumber":
        # M0680 Ratnilarda Temple of the Great Tree 10%; M0831 Squeed Octus Overlook 5%
        return state.has_any({
            "Material: Ancient Lumber (Temple of the Great Tree)",
            "Material: Ancient Lumber (Octus Overlook)",
        }, player)
    return True

# TODO: implement — returns True if the player has access to grinding spots yielding ~threshold EXP
def grind_level(state: CollectionState, player: int) -> int:
    """Returns the level a player could theoretically reach through grinding,
    based on which grind areas they can access. Each accessible area adds 2 levels,
    capped at a total gain of 30 (so max returned value is 31).
    Night explorations are worth more: TCF Night and MG Night add 4 levels each;
    Pangaia Plains (Night) adds 10 levels."""
    gained = 2  # Calm Inlet Area is always accessible from the start

    # Single-entrance areas: count +2 if item is held
    single_entrance_items = [
        "Grind: Western Foot of Gendarme",
        "Grind: Seiren North Access",
        "Grind: Temple of the Great Tree",
        "Grind: Towal Highway",
        "Grind: Baja Tower",
        "Grind: Nostalgia Cape",
        "Grind: Archeozoic Chasm",
        "Grind: Bolado Monastery",
        "Grind: Valley of Kings",
        "Grind: Silent Tower",
        "Grind: Octus Overlook",
    ]
    for item in single_entrance_items:
        if state.has(item, player):
            gained += 2

    # Dual-entrance areas: count +2 once if accessible from either end
    dual_entrance_areas = [
        ("Grind: Towering Coral Forest",    "Grind: Towering Coral Forest Rear"),
        ("Grind: Eroded Valley",             "Grind: Eroded Valley Rear"),
        ("Grind: Schlamm Jungle",            "Grind: Schlamm Jungle Rear"),
        ("Grind: Mont Gendarme",             "Grind: Mont Gendarme Rear"),
        ("Grind: Lodinia Marshlands",        "Grind: Lodinia Marshlands Rear"),
    ]
    for front_item, rear_item in dual_entrance_areas:
        if state.has_any({front_item, rear_item}, player):
            gained += 2

    # Night explorations: higher EXP density warrants larger level gains
    if state.has("Grind: Towering Coral Forest Night", player):
        gained += 4
    if state.has("Grind: Mont Gendarme Night", player):
        gained += 4
    if state.has("Grind: Pangaia Plains Night", player):
        gained += 10

    return 1 + min(gained, 30)

# TODO: implement — returns the highest armlet strength value from found checks
def armlet_str(state: CollectionState, player: int) -> int:
    return 0

# TODO: implement — returns the highest accessory strength value from found checks
def accessory_str(state: CollectionState, player: int) -> int:
    return 0

# TODO: implement — returns True if a strength-boosting recipe is accessible
def has_str_recipe(state: CollectionState, player: int) -> bool:
    return True

def battle_logic(state: CollectionState, player: int, required_str: int, options: Ys8Options) -> bool:
    if not options.battle_logic:
        return True

    scaled = False  # TODO: set True when options.battle_logic == scaled mode

    weaponStr = 0
    armorStr = 0
    armStr = 0
    accStr = 0
    boss_count = bosses_defeated(state, player)

    # Cache material_access results within this call to avoid redundant state lookups
    _mat_cache: dict[str, bool] = {}
    def mat(name: str) -> bool:
        if name not in _mat_cache:
            _mat_cache[name] = material_access(name, state, player)
        return _mat_cache[name]

    player_level = boss_count * 3 + 3 + grind_level(state, player)  # Base level 3, +3 per boss, +grind levels

    baseStr = _GRIND_STR[max(5, min((player_level // 5) * 5, 95))]

    if scaled:
        if boss_count >= 21:
            required_str = 425
        elif boss_count == 20:
            required_str = 380
        elif boss_count == 19:
            required_str = 330
        elif boss_count == 18:
            required_str = 320
        elif boss_count == 17:
            required_str = 280
        elif boss_count == 16:
            required_str = 270
        elif boss_count in [14, 15]:
            required_str = 260
        elif boss_count == 13:
            required_str = 250
        elif boss_count in [10, 11, 12]:
            required_str = 230
        elif boss_count == 9:
            required_str = 140
        elif boss_count in [7, 8]:
            required_str = 120
        elif boss_count == 6:
            required_str = 100
        elif boss_count == 5:
            required_str = 75
        elif boss_count == 4:
            required_str = 60
        elif boss_count in [2, 3]:
            required_str = 30
        else:
            return True

    # Weapon strength — based on rounded averages of accessible weapons at their base levels
    super_weapons = (state.has("Mistilteinn", player) and state.has("Adol", player)) or \
                    (state.has("Spirit Ring Celesdia", player) and state.has("Dana", player))
    if options.progressive_super_weapons and state.has("Flame Stone", player, 7) and super_weapons:
        weaponStr = 290
    elif not options.progressive_super_weapons and super_weapons:
        weaponStr = 290
    elif state.has("Flame Stone", player, 7) and mat("Dragon Crest Stone"):
        weaponStr = 270
    elif state.has("Flame Stone", player, 6) and (
            (mat("Essence Stone") and
             mat("Iron Ore") and
             mat("Tektite Ore")) or
            (mat("Dragon Crest Stone") and state.has("Dina", player))):
        weaponStr = 240
    elif state.has("Flame Stone", player, 5) and (
            (mat("Essence Stone") and
             mat("Iron Ore") and
             mat("Tektite Ore")) or
            (mat("Dragon Crest Stone") and state.has("Dina", player))):
        weaponStr = 210
    elif state.has("Flame Stone", player, 4) and (
            (mat("Essence Stone") and state.has("Dina", player)) or
            (mat("Dragon Crest Stone") and state.has("Dina", player)) or
            (mat("Iron Ore") and mat("Tektite Ore"))):
        weaponStr = 180
    elif state.has("Flame Stone", player, 3):
        weaponStr = 150
    elif state.has("Flame Stone", player, 2) and (
            (mat("Essence Stone") and state.has("Dina", player)) or
            (mat("Dragon Crest Stone") and state.has("Dina", player)) or
            (mat("Tektite Ore") and state.has("Dina", player)) or
            mat("Iron Ore")):
        weaponStr = 100
    elif state.has("Flame Stone", player, 1) and (
            (mat("Essence Stone") and state.has("Dina", player)) or
            (mat("Dragon Crest Stone") and state.has("Dina", player)) or
            (mat("Tektite Ore") and state.has("Dina", player)) or
            mat("Iron Ore")):
        weaponStr = 50

    # Armor strength
    if state.has("Flame Stone", player, 7) and mat("Underworld Hide") and \
                        mat("Underworld Bone"):
        armorStr = 25
    elif state.has("Flame Stone", player, 6) and (
            (mat("Underworld Hide") and \
            mat("Underworld Bone") and state.has("Dina", player)) or
            (mat("Ancient Bone") and
             mat("Ancient Hide") and
             mat("Saurian Scale"))):
        armorStr = 20
    elif state.has("Flame Stone", player, 5) and (
            (mat("Underworld Hide") and \
            mat("Underworld Bone") and state.has("Dina", player)) or
            (mat("Ancient Bone") and
             mat("Ancient Hide") and
             mat("Saurian Scale"))):
        armorStr = 16
    elif state.has("Flame Stone", player, 4) and (
            (mat("Underworld Hide") and \
            mat("Underworld Bone") and state.has("Dina", player)) or
            (mat("Ancient Bone") and
             mat("Ancient Hide") and
             mat("Saurian Scale") and state.has("Dina", player)) or
            (mat("Beast Hide") and \
            mat("Beast Bone") and state.has("Dina", player))):
        armorStr = 13
    elif state.has("Flame Stone", player, 2) and (
            (mat("Underworld Hide") and \
            mat("Underworld Bone") and state.has("Dina", player)) or
            (mat("Ancient Bone") and
             mat("Ancient Hide") and
             mat("Saurian Scale") and state.has("Dina", player)) or
            (mat("Beast Hide") and \
            mat("Beast Bone"))):
        armorStr = 10
    elif state.has("Flame Stone", player, 1) and (
            (mat("Underworld Hide") and \
            mat("Underworld Bone") and state.has("Dina", player)) or
            (mat("Ancient Bone") and
             mat("Ancient Hide") and
             mat("Saurian Scale") and state.has("Dina", player)) or
             (mat("Beast Hide") and \
            mat("Beast Bone")) or
            state.has("Dina", player)):
        armorStr = 6

    # Armlet strength — take the higher of shop tiers and found items
    foundArmStr = armlet_str(state, player)
    if state.has("Flame Stone", player, 7) and state.has("Euron", player) and \
            (mat("Beast Hide") and \
                mat("Beast Bone")):
        armStr = 30
    elif state.has("Flame Stone", player, 6) and state.has("Euron", player) and \
            mat("Saurian Scale") and mat("Ancient Hide"):
        armStr = 20
    elif state.has("Flame Stone", player, 4) and state.has("Euron", player) and \
            mat("Dragon Crest Stone") and mat("Dandale Horn"):
        armStr = 10
    armStr = max(armStr, foundArmStr)

    # Accessory strength — shop logic; categories that conflict are kept separate, best-of each added together
    foundAccStr = accessory_str(state, player)
    bladeRings = [0]
    pyriosAcc  = [0]
    fenrirAcc  = [0]
    hopeAndLum = [0]
    dragonAcc  = [0]
    otherAcc   = [0]

    if state.has("Alison", player) and not state.has("Euron", player) and \
            mat("Beast Claw"):
        bladeRings.append(10)  # Blade Ring
        if mat("Glow Rock") and mat("Flexible Branch") and \
                    mat("Beautiful Flower") or state.has("Dina", player):
            hopeAndLum.append(20)  # Hope Stone
    if state.has("Euron", player) and state.has("Flame Stone", player, 2):
        if mat("Razor Feather") and mat("Stalactite"):
            fenrirAcc.append(5)   # Fenrir Talisman
        if mat("Sword Tip Fang") and mat("Thick Hide"):
            bladeRings.append(20) # Blade Ring 2
        if ((state.has("Fishing Rod", player) and state.has("Large Pearl", player, 8)) or
                state.has("Dina", player)) and mat("Lustrous Scale") and \
                    mat("Beautiful Flower"):
            hopeAndLum.append(40) # Luminous Ring
        if mat("Accursed Shell") and mat("Stalactite"):
            pyriosAcc.append(5)   # Pyrios Talisman
    if state.has("Euron", player) and state.has("Flame Stone", player, 4):
        if mat("Thunder Claw") and mat("Tektite Ore"):
            otherAcc.append(10)   # Lightning Stone
        if mat("Thunder Claw") and mat("Beast Hide"):
            bladeRings.append(30) # Blade Ring 3
        if mat("Dandale Horn") and mat("Tektite Ore"):
            otherAcc.append(10)   # Crow Stone
        if mat("Tektite Ore") and mat("Ancient Lumber"):
            otherAcc.append(10)   # Snake Stone
    if state.has("Euron", player) and state.has("Flame Stone", player, 5):
        if mat("Lustrous Scale") and mat("Stalactite"):
            dragonAcc.append(10)  # Dragon Pauldron
        if mat("Dandale Horn"):
            dragonAcc.append(20)  # Dragon Stone
        if mat("Dandale Horn") and mat("Dragon Crest Stone"):
            fenrirAcc.append(15)  # Fenrir Stone
            pyriosAcc.append(15)  # Pyrios Stone
            otherAcc.append(10)   # Nature Talisman
    if state.has("Euron", player) and state.has("Flame Stone", player, 7):
        if mat("Dragon Crest Stone") and mat("Ancient Hide"):
            bladeRings.append(40) # Blade Ring 4

    # Combine: take best from each conflicting category, sum top two of the merged list
    bladeRings.sort(reverse=True)
    pyriosAcc.sort(reverse=True)
    fenrirAcc.sort(reverse=True)
    hopeAndLum.sort(reverse=True)
    dragonAcc.sort(reverse=True)
    otherAcc.extend([bladeRings[0], pyriosAcc[0], fenrirAcc[0], hopeAndLum[0], dragonAcc[0]])
    otherAcc.sort(reverse=True)
    accStr = otherAcc[0] + otherAcc[1]
    accStr = max(accStr, foundAccStr)

    total = weaponStr + armorStr + armStr + accStr
    if required_str >= 350:
        return (total >= required_str and has_required_party(state, player, 3) and
                state.has("Flame Stone", player, 6) and
                has_str_recipe(state, player))
    elif required_str >= 300:
        return (total >= required_str and has_required_party(state, player, 3) and
                state.has("Flame Stone", player, 5) and
                has_str_recipe(state, player))
    elif required_str >= 250:
        return (total >= required_str and has_required_party(state, player, 3) and
                state.has("Flame Stone", player, 3))
    elif required_str >= 230:
        return (total >= required_str and has_required_party(state, player, 2) and
                state.has("Flame Stone", player, 3))
    elif required_str >= 200:
        return (total >= required_str and has_required_party(state, player, 2) and
                state.has("Flame Stone", player, 2))
    elif required_str >= 150:
        return (total >= required_str and has_required_party(state, player, 2))
    else:
        return total >= required_str

def map_completion_logic(state: CollectionState, player: int, options: Ys8Options) -> bool:
    return True

def set_entrance_rules(Ys8World: Ys8World):
    player = Ys8World.player
    options = Ys8World.options

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
    set_rule(get_ent("TCF Mid-Boss Arena to TCF Front"), lambda state: state.has("Serpentus Defeated", Ys8World.player))
    set_rule(get_ent("TCF Mid-Boss Arena to TCF Corpse"), lambda state: state.has("Serpentus Defeated", Ys8World.player))
    set_rule(get_ent("TCF Corpse to TCF RF"), lambda state: state.has("Grip Gloves", Ys8World.player)) 
    set_rule(get_ent("Rainbow Falls to TCF Boss Area"), lambda state: state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("TCF Boss Area to TCF RF"), lambda state: state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("TCF Boss Area to TCF Boss"), lambda state: state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("TCF Boss to TCF Boss Area"), lambda state: state.has("Clareon Defeated", Ys8World.player))
    set_rule(get_ent("TCF Exit to Meta Area"), lambda state: state.has("Clareon Defeated", Ys8World.player))

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
    set_rule(get_ent("EV Mid-Boss Arena to EV Front"), lambda state: state.has("Lonbrigius Defeated", Ys8World.player))
    set_rule(get_ent("EV Mid-Boss Arena to EV Webbed Walkway"), lambda state: state.has_all(["Lonbrigius Defeated", "Glow Stone"], Ys8World.player))
    set_rule(get_ent("EV Webbed Walkway to EV Before Boss"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("EV Before Boss to EV Webbed Walkway"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("EV Before Boss to EV Boss Arena"), lambda state: state.has("Glow Stone", Ys8World.player))
    set_rule(get_ent("EV Boss Arena to EV Before Boss"), lambda state: state.has_all(["Gargantula Defeated", "Glow Stone"], Ys8World.player))
    set_rule(get_ent("EV Boss Arena to SB"), lambda state: state.has("Gargantula Defeated", Ys8World.player))

    # Schlamm Jungle Connections
    set_rule(get_ent("SJ Mid-Boss Arena to SJ Front"), lambda state: state.has("Magamandra Defeated", Ys8World.player))
    set_rule(get_ent("SJ Mid-Boss Arena to SJ Muddy Path"), lambda state: state.has("Magamandra Defeated", Ys8World.player) and 
             state.has_any(["Archeopteryx Wings", "Float Shoes"], Ys8World.player))
    set_rule(get_ent("SJ Muddy Path to SJ Before Boss"), lambda state: state.has("Float Shoes", Ys8World.player))
    set_rule(get_ent("SJ Muddy Path to SJ FoMH"), lambda state: state.has("Dina", Ys8World.player) and state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("SJ FoMH to SJ Muddy Path"), lambda state: state.has("Dina", Ys8World.player))
    set_rule(get_ent("SJ Before Boss to SJ Muddy Path"), lambda state: state.has("Float Shoes", Ys8World.player))
    set_rule(get_ent("SJ Boss Arena to SJ Before Boss"), lambda state: state.has_all(["Laspisus Defeated", "Float Shoes"], Ys8World.player))
    set_rule(get_ent("SJ Boss Arena to ORC"), lambda state: state.has_all(["Laspisus Defeated", "Float Shoes"], Ys8World.player))
    
    # East Coast Cave Connections
    set_rule(get_ent("ECC BG to ECC AG"), lambda state: state.has("Gilkyra Encounter Defeated", Ys8World.player))
    set_rule(get_ent("ECC AG to ECC BG"), lambda state: state.has_all(["Gilkyra Encounter Defeated", "Archeopteryx Wings"], Ys8World.player))
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
    set_rule(get_ent("MG Mid-Boss Arena to MG Mid"), lambda state: state.has("Avalodragil 2 Defeated", Ys8World.player))
    set_rule(get_ent("MG Mid-Boss Arena to MG Upper"), lambda state: state.has_all(["Avalodragil 2 Defeated", "Grip Gloves"], Ys8World.player))
    set_rule(get_ent("MG Upper to MG Boss Arena"), lambda state: state.has("Grip Gloves", Ys8World.player))
    set_rule(get_ent("MG Boss Arena to MG Upper"), lambda state: state.has("Giasburn Defeated", Ys8World.player))
    set_rule(get_ent("MG Boss Arena to Seiren North"), lambda state: state.has("Giasburn Defeated", Ys8World.player))

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
    set_rule(get_ent("TotGT Boss Arena to TotGT Garden"), lambda state: state.has("Brachion Defeated", Ys8World.player))
    set_rule(get_ent("TotGT Boss Arena to TotGT"), lambda state: state.has("Brachion Defeated", Ys8World.player))
    set_rule(get_ent("TotGT Garden to Octus"), lambda state: has_required_crew(state, Ys8World.player, 20)) # placeholder until options are completed

    # Ruins of Eternia Connections
    set_rule(get_ent("RoE to Seiren North"), lambda state: state.has("Blue Seal of Whirling Water", Ys8World.player))
    set_rule(get_ent("RoE to TotGT"), lambda state: state.has("Green Seal of Roaring Stone", Ys8World.player))
    set_rule(get_ent("RoE to AC:Bridge"), lambda state: state.has("Frozen Flower", Ys8World.player))
    set_rule(get_ent("RoE to TH"), lambda state: state.has("Dana", Ys8World.player))
    set_rule(get_ent("RoE to FSC First Barrier"), lambda state: state.has_all(["Jade Pendant", "Dina"], Ys8World.player) and battle_logic(state, player, 800, options)) 
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
    set_rule(get_ent("Baja Tower Upper Floors to Baja Tower Boss Arena"), lambda state: state.has("Exmetal Defeated", Ys8World.player))

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
    set_rule(get_ent("VoK After Door to VoK Boss Arena"), lambda state: state.has_all(["Doxa Griel Defeated", "Purifying Bell"], Ys8World.player))
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
    multiworld = Ys8World.multiworld
    player = Ys8World.player
    options = Ys8World.options

    def loc(name: str):
        return multiworld.get_location(name, player)

    # Former Sanctuary Crypt B4 — underwater chests
    add_rule(loc("Former Sanctuary Crypt - B4 Entrance Chest 2"),
             lambda state: state.has("Hermit's Scale", player))
    add_rule(loc("Former Sanctuary Crypt - B4 Frozen Statue Room Chest 1"),
             lambda state: state.has("Hermit's Scale", player))
    add_rule(loc("Former Sanctuary Crypt - B4 Frozen Statue Room Chest 4"),
             lambda state: state.has("Hermit's Scale", player))

    # Bolado Monastery — dark entrance chests
    add_rule(loc("Bolado Monastery Entrance Chest 1"),
             lambda state: state.has("Glow Stone", player))
    add_rule(loc("Bolado Monastery Entrance Chest 2"),
             lambda state: state.has("Glow Stone", player))
    add_rule(loc("Bolado Monastery Entrance Chest 3"),
             lambda state: state.has("Glow Stone", player))

    # White Sand Cape — Cobalt Crag upper chests
    add_rule(loc("White Sand Cape Cobalt Crag Chest 2"),
             lambda state: state.has("Archeopteryx Wings", player))
    add_rule(loc("White Sand Cape Cobalt Crag Chest 3"),
             lambda state: has_required_crew(state, player, 20))

    # Nameless Coast — Treebridge Chest 3 requires climb or jump
    add_rule(loc("Nameless Coast Cliffs South - Treebridge Chest 3"),
             lambda state: state.has_any(["Grip Gloves", "Archeopteryx Wings"], player))

    # Towering Coral Forest Walkways — upper chests require climb or jump
    add_rule(loc("Towering Coral Forest Walkways Chest 3"),
             lambda state: state.has_any(["Grip Gloves", "Archeopteryx Wings"], player))
    add_rule(loc("Towering Coral Forest Walkways Chest 6"),
             lambda state: state.has_any(["Grip Gloves", "Archeopteryx Wings"], player))

    # Baja Tower — Third Floor Chest 3 requires double jump
    add_rule(loc("Baja Tower Third Floor Chest 3"),
             lambda state: state.has("Archeopteryx Wings", player))

    # Valley of Kings — Mid-Boss Arena chest and End double-jump chests
    add_rule(loc("Valley of Kings Mid-Boss Arena Chest"),
             lambda state: state.has("Purifying Bell", player))
    add_rule(loc("Valley of Kings End Chest 1"),
             lambda state: state.has("Archeopteryx Wings", player))
    add_rule(loc("Valley of Kings End Chest 2"),
             lambda state: state.has("Archeopteryx Wings", player))

    # Archeozoic Chasm — Crater overlook Chest 2 requires large crew
    add_rule(loc("Archeozoic Chasm Cliffs Overlooking Crater Chest 2"),
             lambda state: has_required_crew(state, player, 23))

    # Schlamm Jungle Entrance — per-chest movement requirements
    add_rule(loc("Schlamm Jungle Entrance Chest 2"),
             lambda state: state.has_all(["Grip Gloves", "Dina"], player))
    add_rule(loc("Schlamm Jungle Entrance Chest 3"),
             lambda state: state.has_any(["Float Shoes", "Archeopteryx Wings"], player))
    add_rule(loc("Schlamm Jungle North of Entrance Chest"),
             lambda state: state.has("Grip Gloves", player))

    # Schlamm Jungle Muddy Path — movement only (Magamandra gated by Mid-Boss connector,
    # Dina/FoMH access gated by SJ FoMH to SJ Muddy Path connector)
    add_rule(loc("Schlamm Jungle Midpoint Corpse"),
             lambda state: state.has_any(["Float Shoes", "Archeopteryx Wings"], player))
    add_rule(loc("Schlamm Jungle Small Passage Chest 1"),
             lambda state: state.has("Grip Gloves", player) and
                 state.has_any(["Float Shoes", "Archeopteryx Wings"], player))
    add_rule(loc("Schlamm Jungle Small Passage Chest 2"),
             lambda state: state.has_any(["Float Shoes", "Archeopteryx Wings"], player))
    add_rule(loc("Schlamm Jungle Muddy Passage Chest 2"),
             lambda state: state.has("Archeopteryx Wings", player) or
                 state.has_all(["Float Shoes", "Grip Gloves"], player))
    # Schlamm Jungle Muddy Passage Chest 1 is in Field of Medicinal Herbs region —
    # fully gated by CIA to FoMH (Field of Medicinal Herbs item) or SJ Muddy Path to SJ FoMH (Dina + Grip)

    # Stone Pillar Wind Cave — Chest 4 additionally needs double jump
    add_rule(loc("Stone Pillar Wind Cave Stone Pillar Wind Cave Chest 4"),
             lambda state: state.has("Archeopteryx Wings", player))

    # Lodinia Marshland — Entrance chests 2/3 and Near Cemetery Chest 2
    add_rule(loc("Lodinia Marshland Entrance from Vista Ridge Chest 2"),
             lambda state: state.has_any(["Archeopteryx Wings", "Float Shoes"], player))
    add_rule(loc("Lodinia Marshland Entrance from Vista Ridge Chest 3"),
             lambda state: state.has_any(["Archeopteryx Wings", "Float Shoes"], player))
    add_rule(loc("Lodinia Marshland Near Submerged Cemetery Chest 2"),
             lambda state: state.has("Float Shoes", player))

    # Calm Inlet — Intercept stages
    add_rule(loc("Calm Inlet Intercept Stage 2"),
             lambda state: (battle_logic(state, player, 45, options) and has_required_party(state, player, 2))
                           or battle_logic(state, player, 80, options))
    add_rule(loc("Calm Inlet Intercept Stage 3"),
             lambda state: (battle_logic(state, player, 80, options) and has_required_party(state, player, 2))
                           or battle_logic(state, player, 130, options))
    add_rule(loc("Calm Inlet Intercept Stage 5"),
             lambda state: (battle_logic(state, player, 200, options) and has_required_party(state, player, 2))
                           or battle_logic(state, player, 240, options))
    add_rule(loc("Calm Inlet Intercept Stage 7"),
             lambda state: state.has("Flame Stone", player, 3)
                           and has_required_party(state, player, 2))
    add_rule(loc("Calm Inlet Intercept Stage 9"),
             lambda state: state.has("Flame Stone", player, 3)
                           and battle_logic(state, player, 200, options))

    # Mont Gendarme — Mishy Rewards require Avalodragil 2 Defeated
    add_rule(loc("Mont Gendarme Mishy Rewards Food 2"),
             lambda state: state.has("Avalodragil 2 Defeated", player))
    add_rule(loc("Mont Gendarme Mishy Rewards Food 4"),
             lambda state: state.has("Avalodragil 2 Defeated", player))
    add_rule(loc("Mont Gendarme Mishy Rewards Food 6"),
             lambda state: state.has("Avalodragil 2 Defeated", player))
    add_rule(loc("Mont Gendarme Mishy Rewards Food 8"),
             lambda state: state.has("Avalodragil 2 Defeated", player))
    add_rule(loc("Mont Gendarme Mishy Rewards Food 10"),
             lambda state: state.has("Avalodragil 2 Defeated", player))
    add_rule(loc("Mont Gendarme Mishy Rewards Food 12"),
             lambda state: state.has("Avalodragil 2 Defeated", player))

    # Calm Inlet — Trade items requiring exploration or movement
    add_rule(loc("Calm Inlet Jewel Trade Item 5"),
             lambda state: state.has_all(["Glow Stone", "Fishing Rod"], player)
                           and has_required_crew(state, player, 18))
    add_rule(loc("Calm Inlet Fish Trade Fish 20"),
             lambda state: state.has("Grip Gloves", player) or has_required_crew(state, player, 6))
    add_rule(loc("Calm Inlet Fish Trade Fish 24"),
             lambda state: has_required_crew(state, player, 8) or state.has("Archeopteryx Wings", player))

    # =====================================================================
    # BOSS SKILL CHECKS
    # =====================================================================

    # Calm Inlet — Silvia (early boss)
    add_rule(loc("Calm Inlet Calm Inlet (Castaway Village Area) Silvia Skill 1"),
             lambda state: state.has("Silvia Defeated", player))
    add_rule(loc("Calm Inlet Calm Inlet (Castaway Village Area) Silvia Skill 2"),
             lambda state: state.has("Silvia Defeated", player))

    # Nameless Coast — Avalodragil (early boss)
    add_rule(loc("Nameless Coast First Avalodragil Arena Avalodragil Skill"),
             lambda state: state.has("Avalodragil Defeated", player))

    # Towering Coral Forest — Serpentus (mid-boss) and Clareon (boss)
    add_rule(loc("Towering Coral Forest Mid-Boss Arena Serpentus Skill 1"),
             lambda state: state.has("Serpentus Defeated", player))
    add_rule(loc("Towering Coral Forest Mid-Boss Arena Serpentus Skill 2"),
             lambda state: state.has("Serpentus Defeated", player))
    add_rule(loc("Towering Coral Forest Boss Arena Clareon Skill 1"),
             lambda state: state.has("Clareon Defeated", player))
    add_rule(loc("Towering Coral Forest Boss Arena Clareon Skill 2"),
             lambda state: state.has("Clareon Defeated", player))

    # Eroded Valley — Lonbrigius (mid-boss) and Gargantula (boss)
    add_rule(loc("Eroded Valley Mid-Boss Arena Lonbrigius Skill 1"),
             lambda state: state.has("Lonbrigius Defeated", player))
    add_rule(loc("Eroded Valley Mid-Boss Arena Lonbrigius Skill 2"),
             lambda state: state.has("Lonbrigius Defeated", player))
    add_rule(loc("Eroded Valley Boss Arena Gargantula Skill 1"),
             lambda state: state.has("Gargantula Defeated", player))
    add_rule(loc("Eroded Valley Boss Arena Gargantula Skill 2"),
             lambda state: state.has("Gargantula Defeated", player))
    add_rule(loc("Eroded Valley Boss Arena Kill Boss"),
             lambda state: state.has("Gargantula Defeated", player))
    add_rule(loc("Eroded Valley Mid-Boss Arena Chest"),
             lambda state: state.has("Lonbrigius Defeated", player))

    # Schlamm Jungle — Magamandra (mid-boss) and Laspisus (boss)
    add_rule(loc("Schlamm Jungle Mid-Boss Arena Magamandra Skill 1"),
             lambda state: state.has("Magamandra Defeated", player))
    add_rule(loc("Schlamm Jungle Mid-Boss Arena Magamandra Skill 2"),
             lambda state: state.has("Magamandra Defeated", player))
    add_rule(loc("Schlamm Jungle Boss Arena Laspisus Skill 1"),
             lambda state: state.has("Laspisus Defeated", player))
    add_rule(loc("Schlamm Jungle Boss Arena Laspisus Skill 2"),
             lambda state: state.has("Laspisus Defeated", player))
    add_rule(loc("Schlamm Jungle Mid-Boss Arena Chest"),
             lambda state: state.has("Magamandra Defeated", player))

    # Pirate Ship Eleftheria — Pirate Revenant
    add_rule(loc("Pirate Ship Eleftheria Deck Kill Boss"),
             lambda state: state.has("Pirate Revenant Defeated", player))
    add_rule(loc("Pirate Ship Eleftheria Deck Pirate Revenant Skill 1"),
             lambda state: state.has("Pirate Revenant Defeated", player))
    add_rule(loc("Pirate Ship Eleftheria Deck Pirate Revenant Skill 2"),
             lambda state: state.has("Pirate Revenant Defeated", player))
    add_rule(loc("Pirate Ship Eleftheria Deck Chest"),
             lambda state: state.has("Pirate Revenant Defeated", player))

    # Baja Tower — Exmetal (mid-boss) and Carveros (boss)
    add_rule(loc("Baja Tower Mid-Boss Arena Exmetal Skill 1"),
             lambda state: state.has("Exmetal Defeated", player))
    add_rule(loc("Baja Tower Mid-Boss Arena Exmetal Skill 2"),
             lambda state: state.has("Exmetal Defeated", player))
    add_rule(loc("Baja Tower Mid-Boss Arena Chest"),
             lambda state: state.has("Exmetal Defeated", player))
    add_rule(loc("Baja Tower Boss Arena Carveros Skill 1"),
             lambda state: state.has("Carveros Defeated", player))
    add_rule(loc("Baja Tower Boss Arena Carveros Skill 2"),
             lambda state: state.has("Carveros Defeated", player))

    # Temple of the Great Tree — Brachion (boss)
    add_rule(loc("Temple of the Great Tree Temple Boss Arena Brachion Skill 1"),
             lambda state: state.has("Brachion Defeated", player))
    add_rule(loc("Temple of the Great Tree Temple Boss Arena Brachion Skill 2"),
             lambda state: state.has("Brachion Defeated", player))

    # Mont Gendarme — Avalodragil 2 (mid-boss) and Giasburn (boss)
    add_rule(loc("Mont Gendarme Mid-Boss Arena Avalodragil 2 Skill 1"),
             lambda state: state.has("Avalodragil 2 Defeated", player))
    add_rule(loc("Mont Gendarme Mid-Boss Arena Avalodragil 2 Skill 2"),
             lambda state: state.has("Avalodragil 2 Defeated", player))
    add_rule(loc("Mont Gendarme Boss Arena Giasburn Skill 1"),
             lambda state: state.has("Giasburn Defeated", player))
    add_rule(loc("Mont Gendarme Boss Arena Giasburn Skill 2"),
             lambda state: state.has("Giasburn Defeated", player))

    # Odd Rock Coast — Kiergaard/Weissman
    add_rule(loc("Odd Rock Coast Odd Rock Coast Kiergaard Weissman Skill 1"),
             lambda state: state.has("Kiergaard Weissman Defeated", player))
    add_rule(loc("Odd Rock Coast Odd Rock Coast Kiergaard Weissman Skill 2"),
             lambda state: state.has("Kiergaard Weissman Defeated", player))

    # Archeozoic Chasm — Coelacantos (mid-boss) and Oceanus (boss)
    add_rule(loc("Archeozoic Chasm Mid-Boss Arena Coelacantos Skill 1"),
             lambda state: state.has("Coelacantos Defeated", player))
    add_rule(loc("Archeozoic Chasm Mid-Boss Arena Coelacantos Skill 2"),
             lambda state: state.has("Coelacantos Defeated", player))
    add_rule(loc("Archeozoic Chasm Boss Arena Oceanus Skill 1"),
             lambda state: state.has("Oceanus Defeated", player))
    add_rule(loc("Archeozoic Chasm Boss Arena Oceanus Skill 2"),
             lambda state: state.has("Oceanus Defeated", player))
    add_rule(loc("Archeozoic Chasm Boss Arena Kill Boss"),
             lambda state: state.has("Oceanus Defeated", player))

    # Valley of Kings — Doxa Griel (mid-boss) and Basileus (boss)
    add_rule(loc("Valley of Kings Mid-Boss Arena Doxa Griel Skill 1"),
             lambda state: state.has("Doxa Griel Defeated", player))
    add_rule(loc("Valley of Kings Mid-Boss Arena Doxa Griel Skill 2"),
             lambda state: state.has("Doxa Griel Defeated", player))
    add_rule(loc("Valley of Kings Boss Arena Basileus Skill 1"),
             lambda state: state.has("Basileus Defeated", player))
    add_rule(loc("Valley of Kings Boss Arena Basileus Skill 2"),
             lambda state: state.has("Basileus Defeated", player))
    add_rule(loc("Valley of Kings Boss Arena Kill Boss"),
             lambda state: state.has("Basileus Defeated", player))

    # Waterdrop Cave — Byfteriza
    add_rule(loc("Waterdrop Cave Boss Arena Byfteriza Skill"),
             lambda state: state.has("Byfteriza Defeated", player))

    # Silent Tower — Mephorash
    add_rule(loc("Silent Tower Second Basement Mephorash Skill"),
             lambda state: state.has("Mephorash Defeated", player))

    # Former Sanctuary Crypt — Melaiduma (final boss)
    add_rule(loc("Former Sanctuary Crypt - Final Floor Boss Arena Melaiduma Skill"),
             lambda state: state.has("Melaiduma Defeated", player))

    # Octus Overlook — Psyche-Ura, Psyche-Nestor, Psyche-Minos, Psyche-Hydra
    add_rule(loc("Octus Overlook Path of the Sky Era Psyche-Ura Skill 1"),
             lambda state: state.has("Psyche-Ura Defeated", player))
    add_rule(loc("Octus Overlook Path of the Sky Era Psyche-Ura Skill 2"),
             lambda state: state.has("Psyche-Ura Defeated", player))
    add_rule(loc("Octus Overlook Path of the Insectoid Era Psyche-Nestor Skill 1"),
             lambda state: state.has("Psyche-Nestor Defeated", player))
    add_rule(loc("Octus Overlook Path of the Insectoid Era Psyche-Nestor Skill 2"),
             lambda state: state.has("Psyche-Nestor Defeated", player))
    add_rule(loc("Octus Overlook Path of the Frozen Era Psyche-Minos Skill 1"),
             lambda state: state.has("Psyche-Minos Defeated", player))
    add_rule(loc("Octus Overlook Path of the Frozen Era Psyche-Minos Skill 2"),
             lambda state: state.has("Psyche-Minos Defeated", player))
    add_rule(loc("Octus Overlook Path of the Ocean Era Psyche-Hydra Skill 1"),
             lambda state: state.has("Psyche-Hydra Defeated", player))
    add_rule(loc("Octus Overlook Path of the Ocean Era Psyche-Hydra Skill 2"),
             lambda state: state.has("Psyche-Hydra Defeated", player))

    # =====================================================================
    # MASTER KONG SKILL CHECKS
    # =====================================================================

    # Parasequoia — Master Kong Ricotta
    add_rule(loc("Roaring Seashore Parasequoia Master Kong Ricotta"),
             lambda state: state.has("Ricotta", player))
    add_rule(loc("Roaring Seashore Parasequoia Master Kong Skill Ricotta"),
             lambda state: state.has_all(["Ricotta", "Master Kong Ricotta Defeated"], player))

    # Sunrise Beach — Master Kong Sahad
    add_rule(loc("Sunrise Beach Sunrise Beach Master Kong Sahad"),
             lambda state: state.has_all(["Sahad", "Master Kong Ricotta Defeated"], player))
    add_rule(loc("Sunrise Beach Sunrise Beach Master Kong Skill Sahad"),
             lambda state: state.has_all(["Sahad", "Master Kong Sahad Defeated"], player))

    # Odd Rock Coast — Master Kong Dana
    add_rule(loc("Odd Rock Coast Odd Rock Coast Master Kong Dana"),
             lambda state: state.has_all(["Dana", "Master Kong Sahad Defeated"], player))
    add_rule(loc("Odd Rock Coast Odd Rock Coast Master Kong Skill Dana"),
             lambda state: state.has_all(["Dana", "Master Kong Dana Defeated"], player))

    # Mont Gendarme Boss Arena — Master Kong Laxia (sequential: requires Dana fight + Giasburn arena)
    add_rule(loc("Mont Gendarme Boss Arena Master Kong Laxia"),
             lambda state: state.has_all(["Laxia", "Giasburn Defeated", "Master Kong Dana Defeated"], player))

    # Pangaia Plains — Master Kong Hummel
    add_rule(loc("Pangaia Plains Ancient Tree Master Kong Hummel"),
             lambda state: state.has_all(["Hummel", "Master Kong Laxia Defeated"], player))
    add_rule(loc("Pangaia Plains Ancient Tree Master Kong Skill Hummel"),
             lambda state: state.has_all(["Hummel", "Master Kong Hummel Defeated"], player))

    # Vista Ridge — Master Kong Adol
    add_rule(loc("Vista Ridge Vista Ridge Lower Master Kong Adol"),
             lambda state: state.has_all(["Adol", "Master Kong Hummel Defeated"], player))
    add_rule(loc("Vista Ridge Vista Ridge Lower Master Kong Skill Adol"),
             lambda state: state.has_all(["Adol", "Master Kong Adol Defeated"], player))

    # =====================================================================
    # BOSS & ENCOUNTER EVENTS  (ordered by battle_logic threshold)
    # =====================================================================

    # --- Calm Inlet Area ---
    set_rule(loc("Nameless Coast First Avalodragil Arena Avalodragil"),
             lambda state: battle_logic(state, player, 45, options))
    set_rule(loc("Waterdrop Cave Boss Arena Byfteriza"),
             lambda state: battle_logic(state, player, 10, options))

    # --- Towering Coral Forest ---
    set_rule(loc("Towering Coral Forest Mid-Boss Arena Serpentus"),
             lambda state: battle_logic(state, player, 70, options))
    set_rule(loc("Towering Coral Forest Boss Arena Clareon"),
             lambda state: battle_logic(state, player, 80, options))

    # --- Eroded Valley ---
    set_rule(loc("Eroded Valley Mid-Boss Arena Lonbrigius"),
             lambda state: battle_logic(state, player, 180, options))
    set_rule(loc("Eroded Valley Boss Arena Gargantula"),
             lambda state: battle_logic(state, player, 200, options))

    # --- Schlamm Jungle ---
    set_rule(loc("Schlamm Jungle Mid-Boss Arena Magamandra"),
             lambda state: battle_logic(state, player, 220, options))
    set_rule(loc("Schlamm Jungle Boss Arena Laspisus"),
             lambda state: battle_logic(state, player, 250, options))

    # --- 155-170 ---
    set_rule(loc("Eroded Valley Dark Passage Chest"),
             lambda state: battle_logic(state, player, 250, options))
    set_rule(loc("East Coast Cave East Coast Cave Gilkyra Encounter"),
             lambda state: battle_logic(state, player, 320, options))

    # --- 200 ---
    set_rule(loc("Mont Gendarme Mid-Boss Arena Avalodragil 2"),
             lambda state: battle_logic(state, player, 320, options))
    set_rule(loc("Odd Rock Coast Odd Rock Coast Kiergaard Weissman"),
             lambda state: battle_logic(state, player, 320, options))
    add_rule(loc("Roaring Seashore Parasequoia Master Kong Ricotta"),
             lambda state: battle_logic(state, player, 360, options))
    add_rule(loc("Sunrise Beach Sunrise Beach Master Kong Sahad"),
             lambda state: battle_logic(state, player, 400, options))

    # --- 230 ---
    set_rule(loc("Baja Tower Mid-Boss Arena Exmetal"),
             lambda state: battle_logic(state, player, 420, options))
    set_rule(loc("Mont Gendarme Boss Arena Giasburn"),
             lambda state: battle_logic(state, player, 350, options))
    add_rule(loc("Odd Rock Coast Odd Rock Coast Master Kong Dana"),
             lambda state: battle_logic(state, player, 430, options))

    # --- 240 ---
    set_rule(loc("Temple of the Great Tree Temple Boss Arena Brachion"),
             lambda state: battle_logic(state, player, 400, options))
    add_rule(loc("Mont Gendarme Boss Arena Master Kong Laxia"),
             lambda state: battle_logic(state, player, 440, options))
    add_rule(loc("Pangaia Plains Ancient Tree Master Kong Hummel"),
             lambda state: battle_logic(state, player, 450, options))
    add_rule(loc("Vista Ridge Vista Ridge Lower Master Kong Adol"),
             lambda state: battle_logic(state, player, 550, options))

    # --- 250-260 ---
    set_rule(loc("Archeozoic Chasm Mid-Boss Arena Coelacantos"),
             lambda state: battle_logic(state, player, 400, options))
    set_rule(loc("Calm Inlet Calm Inlet (Castaway Village Area) Silvia"),
             lambda state: battle_logic(state, player, 440, options))

    # --- 270 ---
    set_rule(loc("Valley of Kings Entrance Force Garmr Encounter"),
             lambda state: battle_logic(state, player, 450, options))
    set_rule(loc("Valley of Kings Mid-Boss Arena Doxa Griel"),
             lambda state: battle_logic(state, player, 450, options))
    set_rule(loc("Pirate Ship Eleftheria Deck Pirate Revenant"),
             lambda state: battle_logic(state, player, 450, options))

    # --- 280-425 ---
    set_rule(loc("Baja Tower Boss Arena Carveros"),
             lambda state: battle_logic(state, player, 500, options))
    set_rule(loc("Archeozoic Chasm Boss Arena Oceanus"),
             lambda state: battle_logic(state, player, 600, options))
    set_rule(loc("Valley of Kings Boss Arena Basileus"),
             lambda state: battle_logic(state, player, 650, options))
    set_rule(loc("Octus Overlook Path of the Ocean Era Psyche-Hydra"),
             lambda state: battle_logic(state, player, 700, options))
    set_rule(loc("Octus Overlook Path of the Frozen Era Psyche-Minos"),
             lambda state: battle_logic(state, player, 720, options))
    set_rule(loc("Octus Overlook Path of the Insectoid Era Psyche-Nestor"),
             lambda state: battle_logic(state, player, 740, options))
    set_rule(loc("Octus Overlook Path of the Sky Era Psyche-Ura"),
             lambda state: battle_logic(state, player, 760, options))
    set_rule(loc("Silent Tower Second Basement Mephorash"),
             lambda state: battle_logic(state, player, 760, options))
    set_rule(loc("Former Sanctuary Crypt - Final Floor Boss Arena Melaiduma"),
             lambda state: battle_logic(state, player, 850, options))

    # --- Goal (placeholder) ---
    set_rule(loc("Octus Overlook Selection Sphere Goal"),
             lambda state: battle_logic(state, player, 760, options))
    
    if options.final_boss_access == 0:
        add_rule(loc("Octus Overlook Selection Sphere Goal"),
                 lambda state: has_required_crew(state, player, options.goal_count_crew_threshold))
    elif options.final_boss_access == 1:
        add_rule(loc("Octus Overlook Selection Sphere Goal"),
                 lambda state: state.has_all(["Mistiltein", "Ship Blueprint", "Seiren Nautical Chart"], player))
    elif options.final_boss_access == 2:
        add_rule(loc("Octus Overlook Selection Sphere Goal"),
                 lambda state: state.has_all(["Psyche-Ura Defeated", "Psyche-Nestor Defeated", "Psyche-Minos Defeated", "Psyche-Hydra Defeated"], player))
    elif options.final_boss_access == 3:
        add_rule(loc("Octus Overlook Selection Sphere Goal"),
                 lambda state: state.has("Melaiduma Defeated", player))
