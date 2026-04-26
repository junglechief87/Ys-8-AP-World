from typing import TYPE_CHECKING
from BaseClasses import CollectionState, ItemClassification
from worlds.generic.Rules import add_item_rule, add_rule, set_rule
from BaseClasses import Entrance
from .Items import item_table, event_item_table
from .Options import Ys8Options
from .Regions import regions
from .Boss_Level_Randomization import boss_stats

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

# Centralized battle requirement values used by battle_logic call sites.
_BATTLE_REQ: dict[str, int] = {
    "BYFTERIZA": boss_stats["Byfteriza"].str_threshold,
    "AVALODRAGIL": boss_stats["Avalodragil"].str_threshold,
    "SERPENTUS": boss_stats["Serpentus"].str_threshold,
    "CLAREON": boss_stats["Clareon"].str_threshold,
    "INTERCEPT_STAGE3_ALT": 150,
    "LONBRIGIUS": boss_stats["Lonbrigius"].str_threshold,
    "GARGANTULA": boss_stats["Gargantula"].str_threshold,
    "MAGAMANDRA": boss_stats["Magamandra"].str_threshold,
    "INTERCEPT_STAGE5_ALT": 260,
    "LASPISUS": boss_stats["Laspisus"].str_threshold,
    "GILKYRA": boss_stats["Gilkyra"].str_threshold,
    "AVALODRAGIL_2": boss_stats["Avalodragil 2"].str_threshold,
    "KIERGAARD_WEISSMAN": boss_stats["Kiergaard Weissman"].str_threshold,
    "GIASBURN": boss_stats["Giasburn"].str_threshold,
    "MASTER_KONG_RICOTTA": 400,
    "MASTER_KONG_SAHAD": 450,
    "BRACHION": boss_stats["Brachion"].str_threshold,
    "COELACANTOS": boss_stats["Coelacantos"].str_threshold,
    "EXMETAL": boss_stats["Exmetal"].str_threshold,
    "MASTER_KONG_DANA": 500,
    "MASTER_KONG_LAXIA": 500,
    "SILVIA": boss_stats["Silvia"].str_threshold,
    "MASTER_KONG_HUMMEL": 520,
    "FORCE_GARMR": boss_stats["Force Garmr"].str_threshold,
    "DOXA_GRIEL": boss_stats["Doxa Griel"].str_threshold,
    "PIRATE_REVENANT": boss_stats["Pirate Revenant"].str_threshold,
    "CARVEROS": boss_stats["Carveros"].str_threshold,
    "MASTER_KONG_ADOL": 600,
    "OCEANUS": boss_stats["Oceanus"].str_threshold,
    "BASILEUS": boss_stats["Basileus"].str_threshold,
    "OCTUS": boss_stats["Octus"].str_threshold,
    "PSYCHE_HYDRA": boss_stats["Psyche Hydra"].str_threshold,
    "PSYCHE_MINOS": boss_stats["Psyche Minos"].str_threshold,
    "PSYCHE_NESTOR": boss_stats["Psyche Nestor"].str_threshold,
    "PSYCHE_URA": boss_stats["Psyche Ura"].str_threshold,
    "MEPHORASH": boss_stats["Mephorash"].str_threshold,
    "FINAL_BOSS": boss_stats["Final Boss"].str_threshold,
    "PSYCHE_FIGHT_GENERIC": boss_stats["Psyche Ura"].str_threshold,
    "FSC_FIRST_BARRIER": boss_stats["FSC First Barrier"].str_threshold,
    "MELAIDUMA": boss_stats["Melaiduma"].str_threshold,
}

# (required_str_threshold, party_members_required, flame_stones_required_or_none)
_BATTLE_LOGIC_GATES: tuple[tuple[int, int, int | None], ...] = (
    (700, 3, 7),
    (650, 3, 6),
    (500, 3, 5),
    (450, 3, 3),
    (350, 2, 3),
    (250, 2, 2),
    (200, 2, None),
)

def set_all_rules(Ys8World: "Ys8World"):
    set_entrance_rules(Ys8World)
    set_location_rules(Ys8World)

def has_required_crew(Ys8World: "Ys8World", state: CollectionState, crew_count: int) -> bool:
    """Check if the player has access to at least crew_count crew members."""
    return state.has_from_list([item for item, data in item_table.items() if data.category == "Crew"], Ys8World.player, crew_count)

def has_required_party(Ys8World: "Ys8World", state: CollectionState, party_count: int) -> bool:
    """Check if the player has access to at least party_count party members."""
    return state.has_from_list([item for item, data in item_table.items() if data.is_party_member], Ys8World.player, party_count)

def has_required_recipes(Ys8World: "Ys8World", state: CollectionState, recipe_count: int) -> bool:
    """Check if the player has access to at least recipe_count recipes."""
    return state.has_from_list([item for item, data in item_table.items() if data.category == "Recipe Book"], Ys8World.player, recipe_count)

def has_discoveries(Ys8World: "Ys8World", state: CollectionState, discovery_count: int) -> bool:
    """Check if the player has collected at least discovery_count discoveries."""
    return state.has_from_list([item for item, data in item_table.items() if data.category == "Landmark"], Ys8World.player, discovery_count)

def bosses_defeated(Ys8World: "Ys8World", state: CollectionState) -> int:
    """Count the total number of bosses the player has defeated."""
    return sum(1 for item, data in event_item_table.items() if data.type == "Boss" and state.has(item, Ys8World.player))

def has_jewels(state: CollectionState, player: int, jewel_count: int) -> bool:
    """Check if the player has access to at least jewel_count jewels, counting stackable jewel items."""
    count = state.count("Prismatic Jewel", player)
    count += 2 * state.count("Prismatic Jewel x2", player)
    count += 3 * state.count("Prismatic Jewel x3", player)
    count += 5 * state.count("Prismatic Jewel x5", player)
    return count >= jewel_count

def material_access(Ys8World: "Ys8World", state: CollectionState, material: str) -> bool:
    """Returns True if the player can reach a viable farming spot for the named material."""
    player = Ys8World.player
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
        # M0605 Dandale — Lodinia Marshlands (Past) only at 10%; LM Near Sky Garden is the closest present-day proxy
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
        # M1010 Gigantyrannus Great River Valley 60%; M0641 Fabnir Lodinia Marshlands Back 15%
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

def grind_level(Ys8World: "Ys8World", state: CollectionState) -> int:
    """Returns the level a player could theoretically reach through grinding,
    based on which grind areas they can access. Each accessible area adds 2 levels,
    capped at a total gain of 30 (so max returned value is 31).
    Night explorations are worth more: TCF Night and MG Night add 4 levels each;
    Pangaia Plains (Night) adds 10 levels."""
    player = Ys8World.player
    gained = 2  # Calm Inlet Area is always accessible from the start

    # Single-entrance areas: count +2 if item is held
    single_entrance_items = [
        "Grind: Western Foot of Gendarme",
        "Grind: Seiren North Access",
        "Grind: Temple of the Great Tree",
        "Grind: Towal Highway",
        "Grind: Baja Tower",
        "Grind: Nostalgia Cape Area",
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

def accessory_str(Ys8World: "Ys8World", state: CollectionState) -> int:
    player = Ys8World.player
    # Blade Rings — mutually exclusive group, take best found
    if state.has("Blade Ring III", player):
        ringStr = 30
    elif state.has("Blade Ring II", player):
        ringStr = 20
    elif state.has("Blade Ring", player):
        ringStr = 10
    else:
        ringStr = 0

    # Ancient accessories — mutually exclusive group, take best found
    if state.has_any({"Stone of Anitquity", "Ocean Hogeki"}, player):
        ancientStr = 40
    elif state.has("Shrine Maiden Amulet", player) and \
            state.has_any({"Laxia", "Dana", "Ricotta"}, player):
        ancientStr = 15
    else:
        ancientStr = 0

    # Pyrios accessories — mutually exclusive group, take best found
    if state.has("Pyrios Stone", player):
        pyriosStr = 15
    elif state.has("Pyrios Talisman", player):
        pyriosStr = 5
    else:
        pyriosStr = 0

    # Stackable accessories
    accStrList = [ringStr, ancientStr, pyriosStr]
    if state.has("Hope Stone", player):
        accStrList.append(20)
    if state.has("Fenrir Talisman", player):
        accStrList.append(5)

    accStrList.sort(reverse=True)
    return accStrList[0] + accStrList[1]

def battle_logic(Ys8World: "Ys8World", state: CollectionState, required_str: int) -> bool:
    options = Ys8World.options
    player = Ys8World.player
    if not options.battle_logic.value:
        return True

    weaponStr = 0
    armorStr = 0
    armStr = 0
    accStr = 0
    boss_count = bosses_defeated(Ys8World, state)

    # Cache material_access results within this call to avoid redundant state lookups
    _mat_cache: dict[str, bool] = {}
    def mat(name: str) -> bool:
        if name not in _mat_cache:
            _mat_cache[name] = material_access(Ys8World, state, name)
        return _mat_cache[name]

    player_level = boss_count * 3 + 3 + grind_level(Ys8World, state)  # Base level 3, +3 per boss, +grind levels

    baseStr = _GRIND_STR[max(5, min((player_level // 5) * 5, 95))]

    # Weapon strength — based on rounded averages of accessible weapons at their base levels
    if options.progressive_super_weapons.value:
        super_weapons = (state.has("Broken Mistilteinn", player) and state.has("Adol", player)) or \
                        (state.has("Broken Spirit Ring", player) and state.has("Dana", player))
    else:
        super_weapons = (state.has("Mistilteinn", player) and state.has("Adol", player)) or \
                        (state.has("Spirit Ring Celesdia", player) and state.has("Dana", player))
    
    if options.progressive_super_weapons.value and state.has("Progressive Shop Rank", player, 7) and super_weapons:
        weaponStr = 290
    elif not options.progressive_super_weapons.value and super_weapons:
        weaponStr = 290
    elif state.has("Progressive Shop Rank", player, 7) and mat("Dragon Crest Stone"):
        weaponStr = 270
    elif state.has("Progressive Shop Rank", player, 6) and (
            (mat("Essence Stone") and
             mat("Iron Ore") and
             mat("Tektite Ore")) or
            (mat("Dragon Crest Stone") and state.has("Dina", player))):
        weaponStr = 240
    elif state.has("Progressive Shop Rank", player, 5) and (
            (mat("Essence Stone") and
             mat("Iron Ore") and
             mat("Tektite Ore")) or
            (mat("Dragon Crest Stone") and state.has("Dina", player))):
        weaponStr = 210
    elif state.has("Progressive Shop Rank", player, 4) and (
            (mat("Essence Stone") and state.has("Dina", player)) or
            (mat("Dragon Crest Stone") and state.has("Dina", player)) or
            (mat("Iron Ore") and mat("Tektite Ore"))):
        weaponStr = 180
    elif state.has("Progressive Shop Rank", player, 3):
        weaponStr = 150
    elif state.has("Progressive Shop Rank", player, 2) and (
            (mat("Essence Stone") and state.has("Dina", player)) or
            (mat("Dragon Crest Stone") and state.has("Dina", player)) or
            (mat("Tektite Ore") and state.has("Dina", player)) or
            mat("Iron Ore")):
        weaponStr = 100
    elif state.has("Progressive Shop Rank", player, 1) and (
            (mat("Essence Stone") and state.has("Dina", player)) or
            (mat("Dragon Crest Stone") and state.has("Dina", player)) or
            (mat("Tektite Ore") and state.has("Dina", player)) or
            mat("Iron Ore")):
        weaponStr = 50

    # Armor strength
    if state.has("Progressive Shop Rank", player, 7) and mat("Underworld Hide") and \
            mat("Underworld Bone"):
        armorStr = 25
    elif state.has("Progressive Shop Rank", player, 6) and (
            (mat("Underworld Hide") and \
            mat("Underworld Bone") and state.has("Dina", player)) or
            (mat("Ancient Bone") and
             mat("Ancient Hide") and
             mat("Saurian Scale"))):
        armorStr = 20
    elif state.has("Progressive Shop Rank", player, 5) and (
            (mat("Underworld Hide") and \
            mat("Underworld Bone") and state.has("Dina", player)) or
            (mat("Ancient Bone") and
             mat("Ancient Hide") and
             mat("Saurian Scale"))):
        armorStr = 16
    elif state.has("Progressive Shop Rank", player, 4) and (
            (mat("Underworld Hide") and \
            mat("Underworld Bone") and state.has("Dina", player)) or
            (mat("Ancient Bone") and
             mat("Ancient Hide") and
             mat("Saurian Scale") and state.has("Dina", player)) or
            (mat("Beast Hide") and \
            mat("Beast Bone") and state.has("Dina", player))):
        armorStr = 13
    elif state.has("Progressive Shop Rank", player, 2) and (
            (mat("Underworld Hide") and \
            mat("Underworld Bone") and state.has("Dina", player)) or
            (mat("Ancient Bone") and
             mat("Ancient Hide") and
             mat("Saurian Scale") and state.has("Dina", player)) or
            (mat("Beast Hide") and \
            mat("Beast Bone"))):
        armorStr = 10
    elif state.has("Progressive Shop Rank", player, 1) and (
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
    if (state.has("Progressive Shop Rank", player, 7) and state.has("Euron", player) and \
            (mat("Beast Hide") and \
                mat("Beast Bone"))) or \
                    state.has("Battle Armlet", player):
        armStr = 30
    elif (state.has("Progressive Shop Rank", player, 6) and state.has("Euron", player) and \
            mat("Saurian Scale") and mat("Ancient Hide")) or \
                state.has("Warrior Wrist", player):
        armStr = 20
    elif state.has("Progressive Shop Rank", player, 4) and state.has("Euron", player) and \
            mat("Dragon Crest Stone") and mat("Dandale Horn"):
        armStr = 10

    # Accessory strength — shop logic; categories that conflict are kept separate, best-of each added together
    foundAccStr = accessory_str(Ys8World, state)
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
    if state.has("Euron", player) and state.has("Progressive Shop Rank", player, 2):
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
    if state.has("Euron", player) and state.has("Progressive Shop Rank", player, 4):
        if mat("Thunder Claw") and mat("Tektite Ore"):
            otherAcc.append(10)   # Lightning Stone
        if mat("Thunder Claw") and mat("Beast Hide"):
            bladeRings.append(30) # Blade Ring 3
        if mat("Dandale Horn") and mat("Tektite Ore"):
            otherAcc.append(10)   # Crow Stone
        if mat("Tektite Ore") and mat("Ancient Lumber"):
            otherAcc.append(10)   # Snake Stone
    if state.has("Euron", player) and state.has("Progressive Shop Rank", player, 5):
        if mat("Lustrous Scale") and mat("Stalactite"):
            dragonAcc.append(10)  # Dragon Pauldron
        if mat("Dandale Horn"):
            dragonAcc.append(20)  # Dragon Stone
        if mat("Dandale Horn") and mat("Dragon Crest Stone"):
            fenrirAcc.append(15)  # Fenrir Stone
            pyriosAcc.append(15)  # Pyrios Stone
            otherAcc.append(10)   # Nature Talisman
    if state.has("Euron", player) and state.has("Progressive Shop Rank", player, 7):
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

    total = baseStr + weaponStr + armorStr + armStr + accStr

    if state.has("Recipe Book/Great Pumpkin Pie", player):
        total *= 1.5  # Bonus for having at least one vit recipe book, to account for food buffs
    elif state.has("Recipe Book/Colorful Meuniere", player):
        total *= 1.2 

    for threshold, party_required, flame_required in _BATTLE_LOGIC_GATES:
        if required_str >= threshold:
            if total < required_str or not has_required_party(Ys8World, state, party_required):
                return False
            return flame_required is None or state.has("Progressive Shop Rank", player, flame_required)
    
    return total >= required_str

def map_completion_logic(state: CollectionState, player: int, percent_goal: int) -> bool:
    reachable = len(state.reachable_regions[player])
    total = sum(1 for r in state.multiworld.regions if r.player == player)
    completion_percent = int(100 * reachable / total) if total > 0 else 0
    return completion_percent >= percent_goal

def set_entrance_rules(Ys8World: "Ys8World"):
    player = Ys8World.player
    options = Ys8World.options

    def get_ent(EntranceName: str) -> Entrance:
        return Ys8World.multiworld.get_entrance(EntranceName, player)

    # Calm Inlet Area Connections
    set_rule(get_ent("NCN Link"), lambda state: state.has("Grip Gloves", player) or has_required_crew(Ys8World, state, 6))
    set_rule(get_ent("TCFRF Link"), lambda state: state.has("Rainbow Falls", player))
    set_rule(get_ent("Para Link"), lambda state: state.has("Parasequoia", player))
    set_rule(get_ent("Meta Link"), lambda state: state.has("Metavolicalis", player))
    set_rule(get_ent("CIA IL1 Link"), lambda state: state.has_any(["T's Memo", "T's Memo A", "T's Memo B", "T's Memo C"], player))
    set_rule(get_ent("CIA IL2 Link"), lambda state: state.has_from_list(["T's Memo", "T's Memo A", "T's Memo B", "T's Memo C"], player, 2))
    set_rule(get_ent("CIA IL3 Link"), lambda state: state.has_from_list(["T's Memo", "T's Memo A", "T's Memo B", "T's Memo C"], player, 3))
    set_rule(get_ent("CIA MC Link"), lambda state: state.has("Euron", player))
    set_rule(get_ent("CIA JT Link"), lambda state: state.has("Dina", player) and has_jewels(state, player, 23))
    set_rule(get_ent("CIA FT Link"), lambda state: state.has("Fishing Rod", player))
    set_rule(get_ent("CIA DTI Link"), lambda state: state.has("Austin", player))
    set_rule(get_ent("WFG Link"), lambda state: state.has("Airs Cairn", player))
    set_rule(get_ent("GRV Link"), lambda state: state.has("Chimney Rock", player))
    set_rule(get_ent("MWV Link"), lambda state: state.has("Milky White Vein", player))
    set_rule(get_ent("EVIMV Link"), lambda state: state.has("Indigo Mineral Vein", player))
    set_rule(get_ent("SB Link"), lambda state: state.has("Beached Remains", player))
    set_rule(get_ent("BH Link"), lambda state: state.has("Beehive", player))
    set_rule(get_ent("SJFMH Link"), lambda state: state.has("Field of Medicinal Herbs", player))
    set_rule(get_ent("ECCBG Link"), lambda state: state.has("Hidden Pirate Storehouse", player))
    set_rule(get_ent("NCA Link"), lambda state: state.has("Ship Graveyard", player))
    set_rule(get_ent("SI Link"), lambda state: state.has_any(["Ship Blueprint", "Magna Carpa"], player))
    set_rule(get_ent("WH Link"), lambda state: (state.has("Grip Gloves", player) and has_required_crew(Ys8World, state, 11)) or state.has("Zephyr Hill", player))
    set_rule(get_ent("LMVA Link"), lambda state: state.has("Lapis Mineral Vein", player))
    set_rule(get_ent("SH Link"), lambda state: state.has("Soundless Hall", player))
    set_rule(get_ent("SG Link"), lambda state: state.has("Sky Garden", player))
    set_rule(get_ent("GOAH Link"), lambda state: state.has("Graves of Ancient Heroes", player))
    if not options.north_side_open.value:
        set_rule(get_ent("SNA Link"), lambda state: state.has_any(["Prismatic Mineral Vein", "Unicalamites", "Breath Fountain", "Ancient Tree"], player))

    # Towering Coral Forest Connections
    set_rule(get_ent("TCFMB Exit"), lambda state: state.has("Serpentus Defeated", player))
    set_rule(get_ent("TCFMB Corpse Link"), lambda state: state.has("Serpentus Defeated", player))
    set_rule(get_ent("TCFC RF Link"), lambda state: state.has("Grip Gloves", player)) 
    set_rule(get_ent("TCFRF BB Link"), lambda state: state.has("Grip Gloves", player))
    set_rule(get_ent("TCFBB RF Exit"), lambda state: state.has("Grip Gloves", player))
    set_rule(get_ent("TCF Boss Entrance"), lambda state: state.has("Grip Gloves", player))
    set_rule(get_ent("TCF Boss Exit"), lambda state: state.has("Clareon Defeated", player))
    add_rule(get_ent("TCF Post-Boss Link"), lambda state: state.has("Clareon Defeated", player))

    # Metavolicalis Area Connections
    set_rule(get_ent("Meta Para Link"), lambda state: has_required_crew(Ys8World, state, 14))

    # Nameless Coast North Connections
    set_rule(get_ent("NCN GRV Link"), lambda state: state.has("Archeopteryx Wings", player) or has_required_crew(Ys8World, state, 8))
    set_rule(get_ent("TCFNFH Link"), lambda state: state.has("Glow Stone", player))

    # Great River Valley Area Connections
    set_rule(get_ent("GRV BWFG Link"), lambda state: state.has("Float Shoes", player))
    set_rule(get_ent("GRV WGDA Link"), lambda state: state.has("Glow Stone", player))
    set_rule(get_ent("GRV LCA Link"), lambda state: state.has("Dina", player))
    set_rule(get_ent("GRV SC Link"), lambda state: state.has("Dina", player))
    set_rule(get_ent("GRV PP Link"), lambda state: state.has("Maiden Journal", player) and state.has("Grip Gloves", player))

    # Great River Valley South Camp
    set_rule(get_ent("GRV SC Exit"), lambda state: state.has("Dina", player))
    
    # Base of Western Foot of Gendarme Connections
    set_rule(get_ent("WFG Entrance"), lambda state: has_required_crew(Ys8World, state, 11))

    # Western Foot of Gendarme Connections
    set_rule(get_ent("WFG Exit"), lambda state: has_required_crew(Ys8World, state, 11))

    # Waterfall Grotto Connections
    set_rule(get_ent("MWV WGDA Link"), lambda state: state.has("Glow Stone", player))
    set_rule(get_ent("WGDA MWV Exit"), lambda state: state.has("Glow Stone", player))
    set_rule(get_ent("WGDA GRV Exit"), lambda state: state.has("Glow Stone", player))

    # Longhorn Coast Area Connections
    set_rule(get_ent("LCA GRV Exit"), lambda state: state.has("Dina", player))
    set_rule(get_ent("LCA OST Link"), lambda state: state.has("Archeopteryx Wings", player))
    set_rule(get_ent("LCA NCA Link"), lambda state: state.has("Archeopteryx Wings", player))
    set_rule(get_ent("LCA BH Link"), lambda state: state.has("Dina", player))

    # Eroded Valley Connections
    set_rule(get_ent("EVF EVDA Link"), lambda state: state.has("Glow Stone", player))
    set_rule(get_ent("EVDA EVF Exit"), lambda state: state.has("Glow Stone", player))
    set_rule(get_ent("EVDA EVIMV Link"), lambda state: state.has("Glow Stone", player))
    set_rule(get_ent("EVIMV EVDA Exit"), lambda state: state.has("Glow Stone", player))
    set_rule(get_ent("EVMB EVF Exit"), lambda state: state.has("Lonbrigius Defeated", player))
    set_rule(get_ent("EVMB WW Link"), lambda state: state.has_all(["Lonbrigius Defeated", "Glow Stone"], player))
    set_rule(get_ent("EVWW BB Link"), lambda state: state.has("Glow Stone", player))
    set_rule(get_ent("EVBB WW Exit"), lambda state: state.has("Glow Stone", player))
    set_rule(get_ent("EV Boss Entrance"), lambda state: state.has("Glow Stone", player))
    set_rule(get_ent("EV Boss Exit"), lambda state: state.has("Gargantula Defeated", player))
    set_rule(get_ent("EV Post-Boss Link"), lambda state: state.has("Gargantula Defeated", player))

    # Schlamm Jungle Connections
    set_rule(get_ent("SJMB SJF Exit"), lambda state: state.has("Magamandra Defeated", player))
    set_rule(get_ent("SJMB MP Link"), lambda state: state.has("Magamandra Defeated", player) and 
             state.has_any(["Archeopteryx Wings", "Float Shoes"], player))
    set_rule(get_ent("SJMP BB Link"), lambda state: state.has("Float Shoes", player))
    set_rule(get_ent("SJMP FMH Link"), lambda state: state.has("Dina", player) and state.has("Grip Gloves", player))
    set_rule(get_ent("SJFMH MP Exit"), lambda state: state.has("Dina", player))
    set_rule(get_ent("SJBB MP Exit"), lambda state: state.has("Float Shoes", player))
    set_rule(get_ent("SJ Boss Exit"), lambda state: state.has("Laspisus Defeated", player))
    set_rule(get_ent("SJ Post-Boss Link"), lambda state: state.has("Laspisus Defeated", player))

    
    # East Coast Cave Connections
    set_rule(get_ent("ECCBG ECCAG Link"), lambda state: state.has("Gilkyra Encounter Defeated", player))
    set_rule(get_ent("ECCAG ECCBG Exit"), lambda state: state.has_all(["Gilkyra Encounter Defeated", "Archeopteryx Wings"], player))
    set_rule(get_ent("PSE Entrance"), lambda state: state.has("Logbook 1", player))

    # Pirate Ship Eleftheria Connections
    set_rule(get_ent("PSE SH Entrance"), lambda state: state.has("Hermit's Scale", player))
    set_rule(get_ent("PSESH PSE Exit"), lambda state: state.has("Hermit's Scale", player))

    # Primordial Passage Connections
    set_rule(get_ent("GRV PP Link"), lambda state: state.has("Maiden Journal", player))
    set_rule(get_ent("PP MGNFH Link"), lambda state: state.has("Glow Stone", player))

    # Primordial Passage Gendarme Entrance Connections
    set_rule(get_ent("PPGE PP Exit"), lambda state: state.has("Maiden Journal", player))

    # Outside Silent Tower Connections
    set_rule(get_ent("OST LCA Exit"), lambda state: state.has("Archeopteryx Wings", player))
    set_rule(get_ent("OST STE Link"), lambda state: has_required_crew(Ys8World, state, 24))
    set_rule(get_ent("STE OST Link"), lambda state: has_required_crew(Ys8World, state, 24))

    # Weathervane Hills Connections
    set_rule(get_ent("WH WHPIN Link"), lambda state: state.has("Dina", player))
    set_rule(get_ent("WH UWV Link"), lambda state: state.has("Hermit's Scale", player))

    # Underground Water Vein Connections
    set_rule(get_ent("LMVA UWV Exit"), lambda state: state.has("Hermit's Scale", player))
    set_rule(get_ent("UWV LMVA Link"), lambda state: state.has("Hermit's Scale", player))
    set_rule(get_ent("UWV WH Exit"), lambda state: state.has("Hermit's Scale", player))
    
    # Mont Gendarme Connections
    set_rule(get_ent("MGF MGM Link"), lambda state: state.has("Grip Gloves", player))
    set_rule(get_ent("MGM MB Link"), lambda state: state.has("Grip Gloves", player))
    set_rule(get_ent("MGMB MGM Exit"), lambda state: state.has("Avalodragil 2 Defeated", player))
    set_rule(get_ent("MGMB MGU Link"), lambda state: state.has_all(["Avalodragil 2 Defeated", "Grip Gloves"], player))
    set_rule(get_ent("MG Boss Entrance"), lambda state: state.has("Grip Gloves", player))
    set_rule(get_ent("MG Boss Exit"), lambda state: state.has("Giasburn Defeated", player))
    add_rule(get_ent("MG Post-Boss Link"), lambda state: state.has("Giasburn Defeated", player))

    # Seiren North Connections
    set_rule(get_ent("SNA SPWC Link"), lambda state: has_required_crew(Ys8World, state, 18))
    set_rule(get_ent("SNA TGT Link"), lambda state: state.has("Dana", player))
    set_rule(get_ent("SNA ROE Link"), lambda state: state.has("Blue Seal of Whirling Water", player))
    set_rule(get_ent("SNA PPN Link"), lambda state: state.has("Glow Stone", player))

    # Stone Pillar Wind Cave Connections
    set_rule(get_ent("SPWC SPWCU Link"), lambda state: state.has("Grip Gloves", player))

    # Temple of the Great Tree Connections
    set_rule(get_ent("TGT SNA Exit"), lambda state: state.has("Dana", player))
    set_rule(get_ent("TGT ROE Link"), lambda state: state.has("Green Seal of Roaring Stone", player))
    set_rule(get_ent("TGT Boss Exit"), lambda state: state.has("Brachion Defeated", player))
    set_rule(get_ent("TGT Garden Link"), lambda state: state.has("Brachion Defeated", player))

    # Ruins of Eternia Connections
    set_rule(get_ent("ROE SNA Exit"), lambda state: state.has("Blue Seal of Whirling Water", player))
    set_rule(get_ent("ROE TGT Exit"), lambda state: state.has("Green Seal of Roaring Stone", player))
    set_rule(get_ent("ROE TH Link"), lambda state: state.has("Dana", player))
    set_rule(get_ent("ROE BM Link"), lambda state: state.has("Frozen Flower", player))
    set_rule(get_ent("BM BMB Link"), lambda state: state.has("Glow Stone", player))
    set_rule(get_ent("ROE BTAC Link"), lambda state: state.has("Frozen Flower", player))
    set_rule(get_ent("BTAC ROE Exit"), lambda state: state.has("Frozen Flower", player))

    if options.former_sanctuary_crypt.value:
        set_rule(get_ent("ROE ROEHP Link"), lambda state: state.has("Jade Pendant", player))
        set_rule(get_ent("ROEHP ROE Exit"), lambda state: state.has("Jade Pendant", player))

    # Former Sanctuary Connections
    if options.former_sanctuary_crypt.value:
        set_rule(get_ent("FSCF FSCFB Link"), lambda state: state.has("Dina", player) and battle_logic(Ys8World, state, _BATTLE_REQ["FSC_FIRST_BARRIER"]))
        set_rule(get_ent("FSCFB FSCSF Link"), lambda state: state.has_all(["Essence Key Stone", "Archeopteryx Wings"], player))
        set_rule(get_ent("FSC NBR Entrance"), lambda state: state.has_all_counts({"Essence Key Stone": 9}, player))
        set_rule(get_ent("FSCSF FSCSB Link"), lambda state: state.has_all_counts({"Essence Key Stone": 3}, player))
        set_rule(get_ent("FSC SB Entrance"), lambda state: state.has("Purifying Bell", player))
        set_rule(get_ent("FSCSBA FSCTF Link"), lambda state: state.has("Float Shoes", player))
        set_rule(get_ent("FSC TFSR Entrance"), lambda state: state.has_all_counts({"Essence Key Stone": 9}, player))
        set_rule(get_ent("FSCTB FSCFF Link"), lambda state: state.has_all_counts({"Essence Key Stone": 6}, player))
        set_rule(get_ent("FSC FFSR Entrance"), lambda state: state.has_all_counts({"Essence Key Stone": 9}, player))

    # Towal Highway Connections
    set_rule(get_ent("TH ROE Exit"), lambda state: state.has("Dana", player))
    set_rule(get_ent("TH THBTE Link"), lambda state: state.has_all(["Grip Gloves", "Golden Seal of Piercing Light"], player))

    # Baja Tower Connections
    set_rule(get_ent("BTLF BTUF Link"), lambda state: state.has_all(["Grip Gloves", "Archeopteryx Wings"], player))
    set_rule(get_ent("BTBA Entrance"), lambda state: state.has("Exmetal Defeated", player))

    # Archeozoic Chasm Connections
    set_rule(get_ent("ACF ACSA Link"), lambda state: state.has("Hermit's Scale", player))
    set_rule(get_ent("AC Boss Entrance"), lambda state: state.has("Hermit's Scale", player))

    # Vista Ridge Connections
    set_rule(get_ent("VR VRU Link"), lambda state: state.has("Grip Gloves", player) and has_required_crew(Ys8World, state, 21))

    # Lodinia Marshlands Connections
    set_rule(get_ent("LMF VR Exit"), lambda state: state.has("Archeopteryx Wings", player))
    set_rule(get_ent("LMF LMNSC Link"), lambda state: state.has("Treasure Chest Key", player))
    set_rule(get_ent("LMNSC LMF Exit"), lambda state: state.has("Treasure Chest Key", player))
    set_rule(get_ent("LMF LMS Link"), lambda state: state.has("Float Shoes", player))
    set_rule(get_ent("LMNSC LMNSG Link"), lambda state: state.has_any(["Float Shoes", "Hermit's Scale"], player))
    set_rule(get_ent("SC Entrance"), lambda state: has_required_crew(Ys8World, state, 22) and state.has_all(["Glow Stone", "Hermit's Scale"], player))
    set_rule(get_ent("LMNSG SG Link"), lambda state: state.has_all(["Grip Gloves", "Archeopteryx Wings"], player))
    set_rule(get_ent("LMNSG LMB Link"), lambda state: state.has_any(["Float Shoes", "Hermit's Scale"], player))
    set_rule(get_ent("LMNSG LMNSC Exit"), lambda state: state.has_any(["Float Shoes", "Hermit's Scale"], player))
    set_rule(get_ent("LMB LMNSG Exit"), lambda state: state.has_any(["Float Shoes", "Hermit's Scale"], player))
    set_rule(get_ent("LMB GOAH Link"), lambda state: state.has_all(["Shrine Maiden Amulet", "Grip Gloves"], player))
    set_rule(get_ent("GOAH LMB Exit"), lambda state: state.has("Shrine Maiden Amulet", player))

    # Valley of Kings Connections
    set_rule(get_ent("VOKBD VOKAD Link"), lambda state: state.has("Force Garmr Defeated", player))
    set_rule(get_ent("VOK Boss Entrance"), lambda state: state.has("Force Garmr Defeated", player))

    # Submerged Cemetery Connections
    set_rule(get_ent("SC LMNSC Exit"), lambda state: has_required_crew(Ys8World, state, 22))
    set_rule(get_ent("BMHR Link"), lambda state: state.has_all(["Glow Stone", "Hermit's Scale"], player))
    set_rule(get_ent("SC SH Link"), lambda state: state.has_all(["Glow Stone", "Hermit's Scale"], player))
    set_rule(get_ent("SH SC Exit"), lambda state: state.has_all(["Glow Stone", "Hermit's Scale"], player))
    set_rule(get_ent("BMHR SC Exit"), lambda state: state.has_all(["Glow Stone", "Hermit's Scale"], player))

    # Night Connections
    set_rule(get_ent("TCFNFH TCFNRH Link"), lambda state: state.has("Grip Gloves", player))
    set_rule(get_ent("MGNFH MGNRH Link"), lambda state: state.has("Grip Gloves", player))
    
    

    
    if options.final_boss_access == 0:
        set_rule(get_ent("TGTG OO Entrance"), lambda state: 
                 has_required_crew(Ys8World, state, options.octus_count_crew_mode.value) and battle_logic(Ys8World, state, _BATTLE_REQ["OCTUS"]))
    if options.final_boss_access == 2:
        set_rule(get_ent("TGTG OO Entrance"), lambda state:
                 state.has_from_list(["Psyches of the Sky Era", "Psyches of the Insectoid Era", "Psyches of the Ocean Era", "Psyches of the Frozen Era"],\
                                      player, options.octus_count_psyches_mode.value) and battle_logic(Ys8World, state, _BATTLE_REQ["OCTUS"]))
    

def set_location_rules(Ys8World: "Ys8World"):
    multiworld = Ys8World.multiworld
    player = Ys8World.player
    options = Ys8World.options

    def loc(name: str):
        return multiworld.get_location(name, player)

    # Former Sanctuary Crypt B4 — underwater chests
    if options.former_sanctuary_crypt.value:
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
             lambda state: has_required_crew(Ys8World, state, 20))

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
             lambda state: state.has("Doxa Griel Defeated", player))
    add_rule(loc("Valley of Kings End Chest 1"),
             lambda state: state.has("Archeopteryx Wings", player))
    add_rule(loc("Valley of Kings End Chest 2"),
             lambda state: state.has("Archeopteryx Wings", player))

    # Towal Highway — kattheway chest requires climb
    add_rule(loc("Towal Highway Baja Tower Approach Katthew Join"),
             lambda state: state.has("Grip Gloves", player))
    
    # Archeozoic Chasm — Crater overlook Chest 2 requires large crew
    add_rule(loc("Archeozoic Chasm Cliffs Overlooking Crater Chest 2"),
             lambda state: has_required_crew(Ys8World, state, 23))

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

    # Great River Valley — large shoreline behind boulder
    add_rule(loc("Great River Valley Large Shoreline Chest 2"),
             lambda state: has_required_crew(Ys8World, state, 10))

    # Nostalgia Cape — Ed Join requires crew
    add_rule(loc("Nostalgia Cape Nostalgia Cape Ed Join"),
            lambda state: has_required_crew(Ys8World, state, 16))
    
    # Stone Pillar Wind Cave — Chest 4 additionally needs double jump
    add_rule(loc("Stone Pillar Wind Cave Stone Pillar Wind Cave Chest 4"),
             lambda state: state.has("Archeopteryx Wings", player))

    # Lodinia Marshlands — Entrance chests 2/3 and Near Cemetery Chest 2
    add_rule(loc("Lodinia Marshlands Entrance from Vista Ridge Chest 2"),
             lambda state: state.has_any(["Archeopteryx Wings", "Float Shoes"], player))
    add_rule(loc("Lodinia Marshlands Entrance from Vista Ridge Chest 3"),
             lambda state: state.has_any(["Archeopteryx Wings", "Float Shoes"], player))
    add_rule(loc("Lodinia Marshlands Near Submerged Cemetery Chest 2"),
             lambda state: state.has("Float Shoes", player))
        
    # NPC Checks for Calm Inlet Area
    # Jewel Trade - Dina
    if options.jewel_trade_items >= 25:
        add_rule(loc("Calm Inlet Jewel Trade Item 5"),
                lambda state: state.has("Fishing Rod", player)
                            and state.can_reach_region("Pangaia Plains (Night)", player))
    
    if options.jewel_trade_items < 25:
        add_item_rule(loc("Calm Inlet Jewel Trade Item 5"),
            lambda item: item.classification == ItemClassification.filler)
    if options.jewel_trade_items < 10:
        add_item_rule(loc("Calm Inlet Jewel Trade Item 4"),
            lambda item: item.classification == ItemClassification.filler)
    if options.jewel_trade_items < 3:
        add_item_rule(loc("Calm Inlet Jewel Trade Past Item 5"),
            lambda item: item.classification == ItemClassification.filler)
    if options.jewel_trade_items < 2:
        add_item_rule(loc("Calm Inlet Jewel Trade Item 3"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Calm Inlet Jewel Trade Past Item 3"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Calm Inlet Jewel Trade Past Item 4"),
            lambda item: item.classification == ItemClassification.filler)
    if options.jewel_trade_items < 1:
        add_item_rule(loc("Calm Inlet Jewel Trade Item 1"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Calm Inlet Jewel Trade Item 2"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Calm Inlet Jewel Trade Past Item 1"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Calm Inlet Jewel Trade Past Item 2"),
            lambda item: item.classification == ItemClassification.filler)
    
    # Fish Trade
    if options.fish_trades >= 5:
        add_rule(loc("Calm Inlet Fish Trade Fish 20"), lambda state: state.can_reach_region("Nameless Coast North", player))
    if options.fish_trades >= 6:
        add_rule(loc("Calm Inlet Fish Trade Fish 24"), lambda state: state.can_reach_region("Great River Valley Area", player))
    
    if options.fish_trades < 6:
        add_item_rule(loc("Calm Inlet Fish Trade Fish 24"),
            lambda item: item.classification == ItemClassification.filler)
    if options.fish_trades < 5:
        add_item_rule(loc("Calm Inlet Fish Trade Fish 20"),
            lambda item: item.classification == ItemClassification.filler)
    if options.fish_trades < 4:
        add_item_rule(loc("Calm Inlet Fish Trade Fish 16"),
            lambda item: item.classification == ItemClassification.filler)
    if options.fish_trades < 3:
        add_item_rule(loc("Calm Inlet Fish Trade Fish 12"),
            lambda item: item.classification == ItemClassification.filler)
    if options.fish_trades < 2:
        add_item_rule(loc("Calm Inlet Fish Trade Fish 8"),
            lambda item: item.classification == ItemClassification.filler)
    if options.fish_trades < 1:
        add_item_rule(loc("Calm Inlet Fish Trade Fish 4"),
            lambda item: item.classification == ItemClassification.filler)
    
    # Mont Gendarme — Mishy Rewards require Avalodragil 2 Defeated
    if options.food_trades >= 1:
        add_rule(loc("Mont Gendarme Mishy Rewards Food 2"),
            lambda state: state.has("Avalodragil 2 Defeated", player) and has_required_recipes(Ys8World, state, 1))
    if options.food_trades >= 2:
        add_rule(loc("Mont Gendarme Mishy Rewards Food 4"),
            lambda state: state.has("Avalodragil 2 Defeated", player) and has_required_recipes(Ys8World, state, 2))
    if options.food_trades >= 3:
        add_rule(loc("Mont Gendarme Mishy Rewards Food 6"),
            lambda state: state.has("Avalodragil 2 Defeated", player) and has_required_recipes(Ys8World, state, 3))
    if options.food_trades >= 4:
        add_rule(loc("Mont Gendarme Mishy Rewards Food 8"),
            lambda state: state.has("Avalodragil 2 Defeated", player) and has_required_recipes(Ys8World, state, 4))
    if options.food_trades >= 5:
        add_rule(loc("Mont Gendarme Mishy Rewards Food 10"),
            lambda state: state.has("Avalodragil 2 Defeated", player) and has_required_recipes(Ys8World, state, 5))
    if options.food_trades >= 6:
        add_rule(loc("Mont Gendarme Mishy Rewards Food 12"),
            lambda state: state.has("Avalodragil 2 Defeated", player) and has_required_recipes(Ys8World, state, 6))
    
    if options.food_trades < 6:
        add_item_rule(loc("Mont Gendarme Mishy Rewards Food 12"),
             lambda item: item.classification == ItemClassification.filler)
    if options.food_trades < 5:
        add_item_rule(loc("Mont Gendarme Mishy Rewards Food 10"),
             lambda item: item.classification == ItemClassification.filler)
    if options.food_trades < 4:
        add_item_rule(loc("Mont Gendarme Mishy Rewards Food 8"),
             lambda item: item.classification == ItemClassification.filler)
    if options.food_trades < 3:
        add_item_rule(loc("Mont Gendarme Mishy Rewards Food 6"),
             lambda item: item.classification == ItemClassification.filler)
    if options.food_trades < 2:
        add_item_rule(loc("Mont Gendarme Mishy Rewards Food 4"),
             lambda item: item.classification == ItemClassification.filler)
    if options.food_trades < 1:
        add_item_rule(loc("Mont Gendarme Mishy Rewards Food 2"),
                lambda item: item.classification == ItemClassification.filler)
    
    # Map Completion - Euron
    if options.map_completion >= 10:
        add_rule(loc("Calm Inlet Map Completion Percent 10"),
                lambda state: map_completion_logic(state, player, 13))
    if options.map_completion >= 20:
        add_rule(loc("Calm Inlet Map Completion Percent 20"),
                 lambda state: map_completion_logic(state, player, 23))
    if options.map_completion >= 30:
        add_rule(loc("Calm Inlet Map Completion Percent 30"),
                 lambda state: map_completion_logic(state, player, 33))
    if options.map_completion >= 40:
        add_rule(loc("Calm Inlet Map Completion Percent 40"),
                 lambda state: map_completion_logic(state, player, 43))
    if options.map_completion >= 50:
        add_rule(loc("Calm Inlet Map Completion Percent 50"),
                 lambda state: map_completion_logic(state, player, 53))
    if options.map_completion >= 60:
        add_rule(loc("Calm Inlet Map Completion Percent 60"),
                 lambda state: map_completion_logic(state, player, 63))
    if options.map_completion >= 70:
        add_rule(loc("Calm Inlet Map Completion Percent 70"),
                 lambda state: map_completion_logic(state, player, 73))
    if options.map_completion >= 80:
        add_rule(loc("Calm Inlet Map Completion Percent 80"),
                 lambda state: map_completion_logic(state, player, 83))
    if options.map_completion >= 90:
        add_rule(loc("Calm Inlet Map Completion Percent 90"),
                 lambda state: map_completion_logic(state, player, 93))
        
    add_item_rule(loc("Calm Inlet Map Completion Percent 100"),
                  lambda item: item.classification == ItemClassification.filler)
    
    if options.map_completion < 90:
        add_item_rule(loc("Calm Inlet Map Completion Percent 90"),
            lambda item: item.classification == ItemClassification.filler)
    if options.map_completion < 80:
        add_item_rule(loc("Calm Inlet Map Completion Percent 80"),
            lambda item: item.classification == ItemClassification.filler)
    if options.map_completion < 70:
        add_item_rule(loc("Calm Inlet Map Completion Percent 70"),
            lambda item: item.classification == ItemClassification.filler)
    if options.map_completion < 60:
        add_item_rule(loc("Calm Inlet Map Completion Percent 60"),
            lambda item: item.classification == ItemClassification.filler)
    if options.map_completion < 50:
        add_item_rule(loc("Calm Inlet Map Completion Percent 50"),
            lambda item: item.classification == ItemClassification.filler)
    if options.map_completion < 40:
        add_item_rule(loc("Calm Inlet Map Completion Percent 40"),
            lambda item: item.classification == ItemClassification.filler)
    if options.map_completion < 30:
        add_item_rule(loc("Calm Inlet Map Completion Percent 30"),
            lambda item: item.classification == ItemClassification.filler)
    if options.map_completion < 20:
        add_item_rule(loc("Calm Inlet Map Completion Percent 20"),
            lambda item: item.classification == ItemClassification.filler)
    if options.map_completion < 10:
        add_item_rule(loc("Calm Inlet Map Completion Percent 10"),
            lambda item: item.classification == ItemClassification.filler)
    
    # Discoveries - Austin
    if options.discoveries >= 1:
        add_rule(loc("Calm Inlet Discovery Rewards Half"), lambda state: has_discoveries(Ys8World, state, 12))
    if options.discoveries >= 2:
        add_rule(loc("Calm Inlet Discovery Rewards All"), lambda state: has_discoveries(Ys8World, state, 24))

    if options.discoveries < 2:
        add_item_rule(loc("Calm Inlet Discovery Rewards All"),
            lambda item: item.classification == ItemClassification.filler)
    if options.discoveries < 1:
        add_item_rule(loc("Calm Inlet Discovery Rewards Half"),
            lambda item: item.classification == ItemClassification.filler)
    
    # Shoebill
    add_rule(loc("Calm Inlet Ricotta and Shoebill Reunite Shoebill Join"),
             lambda state: state.has("Ricotta", player))
        
    # Calm Inlet — Intercept stages
    if options.dogi_intercept_rewards.value:
        add_rule(loc("Calm Inlet Intercept Stage 2"),
            lambda state: (battle_logic(Ys8World, state, _BATTLE_REQ["AVALODRAGIL"]) and has_required_party(Ys8World, state, 2))
                    or battle_logic(Ys8World, state, _BATTLE_REQ["CLAREON"]))
        add_rule(loc("Calm Inlet Intercept Stage 3"),
            lambda state: (battle_logic(Ys8World, state, _BATTLE_REQ["CLAREON"]) and has_required_party(Ys8World, state, 2))
                    or battle_logic(Ys8World, state, _BATTLE_REQ["INTERCEPT_STAGE3_ALT"]))
        add_rule(loc("Calm Inlet Intercept Stage 5"),
            lambda state: (battle_logic(Ys8World, state, _BATTLE_REQ["GARGANTULA"]) and has_required_party(Ys8World, state, 2))
                    or battle_logic(Ys8World, state, _BATTLE_REQ["INTERCEPT_STAGE5_ALT"]))
        add_rule(loc("Calm Inlet Intercept Stage 7"),
                lambda state: state.has("Progressive Shop Rank", player, 3)
                            and has_required_party(Ys8World, state, 2))
        add_rule(loc("Calm Inlet Intercept Stage 9"),
                lambda state: state.has("Progressive Shop Rank", player, 3)
                    and battle_logic(Ys8World, state, _BATTLE_REQ["GARGANTULA"]))
    else:
        add_item_rule(loc("Calm Inlet Intercept Stage 2"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Calm Inlet Intercept Stage 3"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Calm Inlet Intercept Stage 5"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Calm Inlet Intercept Stage 7"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Calm Inlet Intercept Stage 9"),
            lambda item: item.classification == ItemClassification.filler)

    # =====================================================================
    # STARTING SKILL RULES
    # =====================================================================
    add_rule(loc("Adol Starting Skill Skill 1 Sonic Slide"),
        lambda state: state.has("Adol", player))
    add_rule(loc("Adol Starting Skill Skill 2 Arc Shot"),
        lambda state: state.has("Adol", player))
    add_rule(loc("Laxia Starting Skill Skill 1 Dagger Fling"),
        lambda state: state.has("Laxia", player))
    add_rule(loc("Laxia Starting Skill Skill 2 Wake Up!"),
        lambda state: state.has("Laxia", player))
    add_rule(loc("Sahad Starting Skill Skill 1 High Wave"),
        lambda state: state.has("Sahad", player))
    add_rule(loc("Sahad Starting Skill Skill 2 Grand Anchor"),
        lambda state: state.has("Sahad", player))
    add_rule(loc("Hummel Starting Skill Skill 1 Burst Shot"),
        lambda state: state.has("Hummel", player))
    add_rule(loc("Hummel Starting Skill Skill 2 Venomous Bullet"),
        lambda state: state.has("Hummel", player))
    add_rule(loc("Ricotta Starting Skill Skill 1 Wild Spin"),
        lambda state: state.has("Ricotta", player))
    add_rule(loc("Ricotta Starting Skill Skill 2 Handmade Trap"),
        lambda state: state.has("Ricotta", player))
    add_rule(loc("Dana Starting Skill Skill 1 Twin Edge"),
        lambda state: state.has("Dana", player))
    add_rule(loc("Dana Starting Skill Skill 2 Sonic Rise"),
        lambda state: state.has("Dana", player))

    # =====================================================================
    # BOSS SKILL CHECKS AND CHESTS BLOCKED BY BOSS CHECKS
    # =====================================================================

    # Calm Inlet — Silvia (early boss)
    if options.silvia_progression.value:
        add_rule(loc("Calm Inlet Calm Inlet (Castaway Village Area) Silvia Skill 1"),
                lambda state: state.has("Silvia Defeated", player))
        add_rule(loc("Calm Inlet Calm Inlet (Castaway Village Area) Silvia Skill 2"),
                lambda state: state.has("Silvia Defeated", player))
    else:
        add_item_rule(loc("Calm Inlet Calm Inlet (Castaway Village Area) Silvia Skill 1"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Calm Inlet Calm Inlet (Castaway Village Area) Silvia Skill 2"),
            lambda item: item.classification == ItemClassification.filler)

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
    add_rule(loc("Mont Gendarme Mid-Boss Arena Ricotta Join"),
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
    if options.final_boss_access == 2:
        add_rule(loc("Valley of Kings Seren Garden Mistilteinn Event"),
                 lambda state: state.has("Basileus Defeated", player) and 
                 state.has_all(["Psyches of the Sky Era", "Psyches of the Insectoid Era", "Psyches of the Ocean Era", "Psyches of the Frozen Era"], player))
    else:
        add_rule(loc("Valley of Kings Seren Garden Mistilteinn Event"),
                 lambda state: state.has("Basileus Defeated", player) and 
                 state.has_all(["Psyche-Ura Defeated", "Psyche-Nestor Defeated", "Psyche-Minos Defeated", "Psyche-Hydra Defeated"], player))
        
    # Waterdrop Cave — Byfteriza
    add_rule(loc("Waterdrop Cave Boss Arena Byfteriza Skill"),
             lambda state: state.has("Byfteriza Defeated", player))

    # Silent Tower — Mephorash
    if options.mephorash_progression.value:
        add_rule(loc("Silent Tower Second Basement Mephorash Skill"),
                lambda state: state.has("Mephorash Defeated", player))
        add_rule(loc("Silent Tower Second Basement Chest 4"),
                lambda state: state.has("Mephorash Defeated", player))
    else:
        add_item_rule(loc("Silent Tower Second Basement Mephorash Skill"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Silent Tower Second Basement Chest 4"),
            lambda item: item.classification == ItemClassification.filler)

    # Former Sanctuary Crypt — Melaiduma (final boss)
    if options.former_sanctuary_crypt.value:
        add_rule(loc("Former Sanctuary Crypt - Final Floor Boss Arena Melaiduma Skill"),
                 lambda state: state.has("Melaiduma Defeated", player))
        add_rule(loc("Former Sanctuary Crypt - Final Floor Boss Arena Melaiduma Medals"),
                 lambda state: state.has("Melaiduma Defeated", player))

    if not options.final_boss_access == 2:
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

    # If paths aren't opened we need to check for boss beatability to access areas of octus, 
    # but if we're doing release the psyches then the bosses aren't there so we don't need to check for them.
    if not options.octus_paths_opened.value and not options.final_boss_access == 2:
        add_rule(loc("Octus Overlook Path of the Frozen Era Chest 1"),
                lambda state: state.has("Psyche-Hydra Defeated", player))
        add_rule(loc("Octus Overlook Path of the Frozen Era Chest 2"),
                lambda state: state.has("Psyche-Hydra Defeated", player))
        add_rule(loc("Octus Overlook Path of the Frozen Era Chest 3"),
                lambda state: state.has("Psyche-Hydra Defeated", player))
        add_rule(loc("Octus Overlook Path of the Insectoid Era Chest 1"),
                lambda state: state.has("Psyche-Minos Defeated", player))
        add_rule(loc("Octus Overlook Path of the Insectoid Era Chest 2"),
                lambda state: state.has("Psyche-Minos Defeated", player))
        add_rule(loc("Octus Overlook Path of the Insectoid Era Chest 3"),
                lambda state: state.has("Psyche-Minos Defeated", player))
        add_rule(loc("Octus Overlook Path of the Sky Era Chest 1"),
                lambda state: state.has("Psyche-Nestor Defeated", player))
        add_rule(loc("Octus Overlook Path of the Sky Era Chest 2"),
                lambda state: state.has("Psyche-Nestor Defeated", player))
        add_rule(loc("Octus Overlook Path of the Sky Era Chest 3"),
                lambda state: state.has("Psyche-Nestor Defeated", player))

    # =====================================================================
    # MASTER KONG SKILL CHECKS
    # =====================================================================

    if options.master_kong_rewards.value:
        # Parasequoia — Master Kong Ricotta
        add_rule(loc("Roaring Seashore Parasequoia Master Kong Skill Ricotta"),
                lambda state: state.has("Master Kong Ricotta Defeated", player))
        # Sunrise Beach — Master Kong Sahad
        add_rule(loc("Sunrise Beach Sunrise Beach Master Kong Skill Sahad"),
                lambda state: state.has("Master Kong Sahad Defeated", player))
        # Odd Rock Coast — Master Kong Dana
        add_rule(loc("Odd Rock Coast Odd Rock Coast Master Kong Skill Dana"),
                lambda state: state.has("Master Kong Dana Defeated", player))
        # Mont Gendarme Boss Arena — Master Kong Laxia
        add_rule(loc("Mont Gendarme Mid-Boss Arena Master Kong Skill Laxia"),
                lambda state: state.has("Master Kong Laxia Defeated", player))
        # Pangaia Plains — Master Kong Hummel
        add_rule(loc("Pangaia Plains Ancient Tree Master Kong Skill Hummel"),
                lambda state: state.has("Master Kong Hummel Defeated", player))
        # Vista Ridge — Master Kong Adol
        add_rule(loc("Vista Ridge Vista Ridge Lower Master Kong Skill Adol"),
                lambda state: state.has("Master Kong Adol Defeated", player))
        add_rule(loc("Vista Ridge Vista Ridge Lower Master Kong Join"),
                lambda state: state.has("Master Kong Adol Defeated", player))
    else:
        add_item_rule(loc("Roaring Seashore Parasequoia Master Kong Skill Ricotta"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Sunrise Beach Sunrise Beach Master Kong Skill Sahad"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Odd Rock Coast Odd Rock Coast Master Kong Skill Dana"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Mont Gendarme Mid-Boss Arena Master Kong Skill Laxia"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Pangaia Plains Ancient Tree Master Kong Skill Hummel"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Vista Ridge Vista Ridge Lower Master Kong Skill Adol"),
            lambda item: item.classification == ItemClassification.filler)
        add_item_rule(loc("Vista Ridge Vista Ridge Lower Master Kong Join"),
            lambda item: item.classification == ItemClassification.filler)
        
    # =====================================================================
    # BOSS & ENCOUNTER EVENTS  (ordered by battle_logic threshold)
    # =====================================================================

    # --- Calm Inlet Area ---
    set_rule(loc("Nameless Coast First Avalodragil Arena Avalodragil"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["AVALODRAGIL"]))
    set_rule(loc("Waterdrop Cave Boss Arena Byfteriza"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["BYFTERIZA"]))

    # --- Towering Coral Forest ---
    set_rule(loc("Towering Coral Forest Mid-Boss Arena Serpentus"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["SERPENTUS"]))
    set_rule(loc("Towering Coral Forest Boss Arena Clareon"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["CLAREON"]))

    # --- Eroded Valley ---
    set_rule(loc("Eroded Valley Mid-Boss Arena Lonbrigius"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["LONBRIGIUS"]))
    set_rule(loc("Eroded Valley Boss Arena Gargantula"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["GARGANTULA"]) and state.has("Glow Stone", player))

    # --- Schlamm Jungle ---
    set_rule(loc("Schlamm Jungle Mid-Boss Arena Magamandra"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["MAGAMANDRA"]))
    set_rule(loc("Schlamm Jungle Boss Arena Laspisus"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["LASPISUS"]) and state.has("Float Shoes", player))

    # --- ---
    set_rule(loc("Eroded Valley Dark Passage Chest"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["LASPISUS"]))
    set_rule(loc("East Coast Cave East Coast Cave Gilkyra Encounter"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["GILKYRA"]))

    # --- ---
    set_rule(loc("Mont Gendarme Mid-Boss Arena Avalodragil 2"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["AVALODRAGIL_2"]))
    set_rule(loc("Odd Rock Coast Odd Rock Coast Kiergaard Weissman"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["KIERGAARD_WEISSMAN"]))
    add_rule(loc("Roaring Seashore Parasequoia Master Kong Ricotta"), # Gendarme Night grind required only to make sure Ripe Mango is farmable.
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["MASTER_KONG_RICOTTA"]) and state.has_all(["Ricotta", "Grind: Mont Gendarme Night"], player)) 
    add_rule(loc("Sunrise Beach Sunrise Beach Master Kong Sahad"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["MASTER_KONG_SAHAD"]) and state.has_all(["Sahad","Master Kong Ricotta Defeated"], player))

    # --- ---
    set_rule(loc("Baja Tower Mid-Boss Arena Exmetal"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["EXMETAL"]))
    set_rule(loc("Mont Gendarme Boss Arena Giasburn"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["GIASBURN"]))
    add_rule(loc("Odd Rock Coast Odd Rock Coast Master Kong Dana"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["MASTER_KONG_DANA"]) and state.has_all(["Dana","Master Kong Sahad Defeated"], player))

    # --- ---
    set_rule(loc("Temple of the Great Tree Temple Boss Arena Brachion"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["BRACHION"]))
    add_rule(loc("Mont Gendarme Boss Arena Master Kong Laxia"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["MASTER_KONG_LAXIA"]) and state.has_all(["Laxia","Master Kong Dana Defeated"], player))
    add_rule(loc("Pangaia Plains Ancient Tree Master Kong Hummel"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["MASTER_KONG_HUMMEL"]) and state.has_all(["Hummel","Master Kong Laxia Defeated"], player))
    add_rule(loc("Vista Ridge Vista Ridge Lower Master Kong Adol"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["MASTER_KONG_ADOL"]) and state.has_all(["Adol","Master Kong Hummel Defeated"], player))

    # --- ---
    set_rule(loc("Archeozoic Chasm Mid-Boss Arena Coelacantos"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["COELACANTOS"]))
    set_rule(loc("Calm Inlet Calm Inlet (Castaway Village Area) Silvia"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["SILVIA"]) and state.has("Silvia", player))

    # --- ---
    set_rule(loc("Valley of Kings Before Door Force Garmr Encounter"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["FORCE_GARMR"]) and state.has("Purifying Bell", player))
    set_rule(loc("Valley of Kings Mid-Boss Arena Doxa Griel"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["DOXA_GRIEL"]) and state.has("Purifying Bell", player))
    set_rule(loc("Pirate Ship Eleftheria Deck Pirate Revenant"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["PIRATE_REVENANT"]))

    # --- ---
    set_rule(loc("Baja Tower Boss Arena Carveros"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["CARVEROS"]))
    set_rule(loc("Archeozoic Chasm Boss Arena Oceanus"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["OCEANUS"]))
    set_rule(loc("Valley of Kings Boss Arena Basileus"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["BASILEUS"]) and state.has("Purifying Bell", player))
    if not options.final_boss_access == 2:
        set_rule(loc("Octus Overlook Path of the Ocean Era Psyche-Hydra"),
                lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["PSYCHE_HYDRA"]))
        set_rule(loc("Octus Overlook Path of the Frozen Era Psyche-Minos"),
                lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["PSYCHE_MINOS"]))
        set_rule(loc("Octus Overlook Path of the Insectoid Era Psyche-Nestor"),
                lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["PSYCHE_NESTOR"]))
        set_rule(loc("Octus Overlook Path of the Sky Era Psyche-Ura"),
                lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["PSYCHE_URA"]))
        
    set_rule(loc("Silent Tower Second Basement Mephorash"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["MEPHORASH"]))
    
    if options.former_sanctuary_crypt.value:
        set_rule(loc("Former Sanctuary Crypt - Final Floor Boss Arena Melaiduma"),
            lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["MELAIDUMA"]))

    # --- Goal (placeholder) ---
    set_rule(loc("Octus Overlook Selection Sphere Goal"),
             lambda state: battle_logic(Ys8World, state, _BATTLE_REQ["FINAL_BOSS"]))
    
    if options.final_boss_access == 0:
        add_rule(loc("Octus Overlook Selection Sphere Goal"),
                 lambda state: has_required_crew(Ys8World, state, options.goal_count_crew_final_boss))
    elif options.final_boss_access == 1:
        if options.progressive_super_weapons.value:
            add_rule(loc("Octus Overlook Selection Sphere Goal"),
                 lambda state: state.has_all(["Broken Mistilteinn", "Ship Blueprint", "Seiren Nautical Chart"], player))
        else:
            add_rule(loc("Octus Overlook Selection Sphere Goal"),
                    lambda state: state.has_all(["Mistilteinn", "Ship Blueprint", "Seiren Nautical Chart"], player))
    elif options.final_boss_access == 2:
        add_rule(loc("Octus Overlook Selection Sphere Goal"),
                 lambda state: state.has_from_list(["Psyches of the Sky Era", "Psyches of the Insectoid Era", "Psyches of the Ocean Era", "Psyches of the Frozen Era"], 
                                                   player, options.goal_count_psyches_final_boss.value))
        
        region_boss_mapping = {
            "Silent Tower": "Mephorash Defeated",
            "Former Sanctuary Crypt Boss Room": "Melaiduma Defeated",
            "Valley of Kings Boss Arena": "Basileus Defeated",
            "Archeozoic Chasm Boss Arena": "Oceanus Defeated",
            "Baja Tower Boss Arena": "Carveros Defeated",
            "Pirate Ship Eleftheria": "Pirate Revenant Defeated",
            "Mont Gendarme Boss Arena": "Giasburn Defeated",
            "Temple of the Great Tree Boss Arena": "Brachion Defeated",
            "Schlamm Jungle Boss Arena": "Laspisus Defeated",
            "Eroded Valley Boss Arena": "Gargantula Defeated",
            "Towering Coral Forest Boss Arena": "Clareon Defeated"
        }

        access_item_names = [item_name for item_name, data in event_item_table.items() if data.category == "Psyches Access"]
        for i, (psyche_location, psyche_fight) in enumerate(zip(Ys8World.chosen_psyche_location_list, Ys8World.chosen_psyche_fight_list)):
            access_item_name = access_item_names[i]
            psyche_loc = loc(psyche_location)
            region_name = psyche_loc.parent_region.name if psyche_loc.parent_region else None
            boss_defeat = region_boss_mapping.get(region_name)
            add_rule(psyche_loc, lambda state: state.has(boss_defeat, player))
            add_rule(loc(psyche_fight), lambda state: state.has(access_item_name, player) and battle_logic(Ys8World, state, _BATTLE_REQ["PSYCHE_FIGHT_GENERIC"]))

    elif options.final_boss_access == 3:
        add_rule(loc("Octus Overlook Selection Sphere Goal"),
                 lambda state: state.has("Melaiduma Defeated", player))

    multiworld.completion_condition[player] = lambda state: state.has("End the Lacrimosa", player)

