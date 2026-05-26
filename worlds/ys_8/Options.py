from dataclasses import dataclass
from typing import Dict, Any
from Options import (
    Choice,
    OptionCounter,
    OptionGroup,
    PerGameCommonOptions,
    Range,
    Toggle,
)


# Goal Settings
class FinalBossAccess(Choice):
    """
    Sets the goal for reaching the final boss and unlocking the Selection Sphere.
    
    Find Crew: Find the required number of castaways (1-28, tied to moving objects).
    Seiren Escape: Find three specific items: Seiren Area Map, Ship Blueprints, and Mistilteinn.
    Release the Psyches: Defeat the specified number of Wardens of Evolution (4 will exist and will be chosen randomly). 
        Interact with the starting checkpoint crystal to see which bosses exist and what bosses are required to access them.
    Untouchable: Reach the bottom of Former Sanctuary Crypt and defeat Melaiduma. Forces Former Sanctuary Crypt on.
    """
    display_name = "Final Boss Access"
    option_find_crew = 0
    option_seiren_escape = 1
    option_release_the_psyches = 2
    option_untouchable = 3
    default = 0


class OctusCountCrewMode(Range):
    """
    For Find Crew mode: Sets the number of castaways required to open Octus Overlook Entrance.
    """
    display_name = "Goal Count to Open Octus (Find Crew)"
    range_start = 1
    range_end = 29
    default = 16


class OctusCountPsychesMode(Range):
    """
    For Release the Psyches mode: Sets the number of Wardens of Evolution required to defeat
    to open Octus Overlook Entrance.
    """
    display_name = "Goal Count to Open Octus (Release the Psyches)"
    range_start = 1
    range_end = 4
    default = 2


class GoalCountCrewFinalBoss(Range):
    """
    For Find Crew mode: Sets the number of castaways required to access the final boss.
    """
    display_name = "Goal Count to Access Final Boss (Find Crew)"
    range_start = 1
    range_end = 29
    default = 20


class GoalCountPsychesFinalBoss(Range):
    """
    For Release the Psyches mode: Sets the number of Wardens of Evolution required to defeat
    to access the final boss.
    """
    display_name = "Goal Count to Access Final Boss (Release the Psyches)"
    range_start = 1
    range_end = 4
    default = 3


# Shuffle Modifiers
class DiscoverySanity(Toggle):
    """
    Puts the landmarks in the item pool. Finding a landmark unlocks the ability to warp to it on the map.
    This drastically changes logic and movement around the world. This also creates way more ways to espace
    the starting area and access the North Side early. It is recommended on for AP as it makes BK pretty unlikely 
    outside of very early game scenarios.
    """
    display_name = "Discovery-Sanity"
    default = True


class DungeonEntranceShuffle(Toggle):
    """
    Shuffles the entrances to dungeon maps. The entrance to one dungeon may lead to another.
    East Coast Cave is treated as the entrance for Pirate Ship Eleftheria with this setting on.
    """
    display_name = "Dungeon Entrance Shuffle"
    default = False

class ShuffleBossLevels(Choice):
    """
    Shuffles the levels of bosses.
    With this setting off, bosses are found at their intended level.
    Balanced: Boss levels are shuffled but distributed in a way to avoid extreme outliers and to keep early game bosses at relatively lower levels.
    Chaotic: Boss levels are completely shuffled with no restrictions. This can lead to extreme outliers and early game bosses being late game levels.
    """
    display_name = "Boss Level Shuffle"
    option_none = 0
    option_balanced = 1
    option_chaotic = 2
    default = 0


# Progression Placement Modifiers
class JewelTradeItems(Choice):
    """
    Sets which Prismatic Jewel trades at Dina's shop can become progression items.
    Dina must join the village to access these trades.
    There are 10 total trades distributed across different jewel costs.
    """
    display_name = "Jewel Trade Items"
    option_none = 0
    option_up_to_1_jewel = 1
    option_up_to_2_jewels = 2
    option_up_to_3_jewels = 3
    option_up_to_10_jewels = 10
    option_up_to_25_jewels = 25
    default = 10


class FishTrades(Choice):
    """
    Sets the number of unique fish required for Shoebill's rewards.
    Shoebill joining the village is not required. The fishing rod is required to make these checks.
    There are 6 total rewards, now at 1, 2, 3, 4, 5, and 6 unique fish respectively.
    """
    display_name = "Fish Trades"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    option_5 = 5
    option_6 = 6
    default = 6


class FoodTrades(Choice):
    """
    Sets the number of unique cooked recipes required for Mishy Mishy's rewards.
    There are 6 total rewards, now at 1, 2, 3, 4, 5, and 6 unique recipes respectively.
    Access to Gendarme's Midpoint is required to make these checks.
    """
    display_name = "Food Trades"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    option_5 = 5
    option_6 = 6
    default = 6


class MapCompletion(Choice):
    """
    Sets the map completion percentage required for Euron/Captain Barbaros rewards.
    Euron must join the village to make these checks.
    The Eagle Eye Orb is considered required for percentages of 60% or greater.
    Logically progression can never land at 100%.
    """
    display_name = "Map Completion"
    option_none = 0
    option_10_percent = 10
    option_20_percent = 20
    option_30_percent = 30
    option_40_percent = 40
    option_50_percent = 50
    option_60_percent = 60
    option_70_percent = 70
    option_80_percent = 80
    option_90_percent = 90
    default = 60


class Discoveries(Choice):
    """
    Sets whether to require half (12) or all (24) discoveries for the rewards.
    Austin must join the village to make these checks.
    Both rewards are on by default with the 'all' setting.
    """
    display_name = "Discoveries"
    option_none = 0
    option_half = 1
    option_all = 2
    default = 2


class DogiInterceptRewards(Toggle):
    """
    Enables Dogi's 5 rewards for completing specific intercept stages (2, 3, 5, 7, and 9).
    Intercepts are now unlocked via Progressive Raid Lists found in the world. 
    Dogi is unlocked from the first one found. 
    """
    display_name = "Dogi Intercept Rewards"
    default = True


class MasterKongRewards(Toggle):
    """
    Sets whether Master Kong rewards can contain progression items.
    Master Kong involves a fairly lengthy chain that spans the game.
    """
    display_name = "Master Kong Rewards"
    default = False


class SilviaProgression(Toggle):
    """
    Sets whether Silvia can block progression.
    This only refers to the optional boss fight.
    """
    display_name = "Silvia Progression"
    default = False


class MephorashProgression(Toggle):
    """
    Sets whether Mephorash can block progression.
    Mephorash is the highest level optional fight in the game outside Former Sanctuary Crypt
    and the Silent Tower is a high requirement location. Silent Tower can still have progression,
    just not the item from Mephorash or the chest behind him.
    """
    display_name = "Mephorash Progression"
    default = False


class FormerSanctuaryCrypt(Toggle):
    """
    Sets whether Former Sanctuary Crypt exists as a location.
    If turned off, the dungeon is closed.
    Also controls if it's entrances is used for dungeon entrance shuffle and if Melaiduma 
    can be a boss in Release the Psyches mode.
    All essence keystones are placed within the dungeon unless Essence Key Sanity is on.
    """
    display_name = "Former Sanctuary Crypt"
    default = False


# Pacing Modifiers
class ExperienceMultiplier(Range):
    """
    Divides character's min and max Exp values allowing for quicker leveling.
    A multiplier of 8 provides well-balanced pacing for quick seeds.
    A couple things to remember. Ys 8 has a pretty aggressive fall off 
    for experience if you outlevel enemies and Nightmare and Inferno cut experience gain in half.
    Level exp growth in Ys is also exponential. So it's a game that generally favors higher multipliers.
    """
    display_name = "Experience Multiplier"
    range_start = 1
    range_end = 20
    default = 8


class AdditionalInterceptRewards(Toggle):
    """
    Causes intercepts to give out up to four additional rewards after returning
    to Castaway Village post-intercept. These are meant to help with resource gathering,
    leveling, etc.
    """
    display_name = "Additional Intercept Rewards"
    default = False


class BattleLogic(Choice):
    """
    Attempts to smooth combat pacing by guaranteeing the player always has access
    to some amount of strength for each boss. No battle logic is applied to non-forced 
    encounters, with the small exceptions of Octus and Former Sanctuary Crypt having some 
    battle logic applied to entering them.
    Highly recommended to be left on, especially for Inferno difficulty.
    """
    display_name = "Battle Logic"
    option_none = 0
    option_easy = 1
    option_normal = 2
    option_hard = 3
    default = 2

class ProgressiveSuperItems(Toggle):
    """
    Both the Mistilteinn and Spirit Ring are in the pool.
    Players find Broken Mistilteinn or Broken Spirit Ring instead.
    Speaking with Kathleen after maxing the forge will fix the broken weapon.
    If "Fun Items" are on then there are broken versions of Laxia, Sahad, Hummel, and Ricotta's accessories.
    These are turned into Euron at max forge instead of Kathleen, since he's the accessory guy.
    """
    display_name = "Progressive Super Items"
    default = True

class FunItems(Toggle):
    """
    Adds fun, powerful items to the item pool.
    The items are one new arm equipment anyone can equip,
    and four unique accessories that can only be equipped by Laxia, Sahad, Hummel, and Ricotta respectively.
    These are considered for combat logic, they are meant to be powerful 
    and also give Laxia, Sahad, Hummel, and Ricotta items with parity to Mistilteinn and Spirit Ring.
    """
    display_name = "Fun Items"
    default = False

class OctusPathsOpened(Toggle):
    """
    All bridges in Octus start lowered. Bosses and mini-bosses are still present
    but do not need to be defeated to access everywhere in the dungeon.
    Mini-bosses remain an excellent EXP farm.
    """
    display_name = "Octus Paths Opened"
    default = True


class ExtraFlameStones(Range):
    """
    Adds Flame Stones to the item pool (0-10 additional stones).
    There are 7 Flame Stones by default, so 3 additional puts it at a round 10.
    Makes hitting max level more likely without being excessive.
    """
    display_name = "Extra Flame Stones"
    range_start = 0
    range_end = 10
    default = 3


class RecipesWithIngredients(Toggle):
    """
    Grants the player essentially infinite ingredients necessary to cook a dish
    upon obtaining their respective Recipe Book. There's not currently havey logic 
    around ingredient access so it's recommended to use this for things like Mishy.
    The pacing of the rando also generally works better without having to farm ingredients
    and things like the attack/defense recipes are used in battle logic as they're very powerful.
    """
    display_name = "Recipes Come With Ingredients"
    default = True


class NorthSideOpen(Toggle):
    """
    The playthrough will start with the Crystal Checkpoint to Temple Approach unlocked.
    Completing Mt Gendarme is no longer mandatory to access the North Side.
    You may need to explore the North Side while underleveled.
    """
    display_name = "North Side Open"
    default = False


class InfinityMode(Toggle):
    """
    Activates Infinity Mode, a New Game+ that drastically scales up enemy levels.
    The lowest level enemies are in the mid-60s and the highest level is 120.
    It is recommended you upgrade your starting loadout drastically with this on.
    """
    display_name = "Infinity Mode"
    default = False


class ScaleExpItems(Toggle):
    """
    Scales experience reward items (Hermit's Elixir, Bitter Remedy, Sweet Remedy) to attempt
    to make them less rewarding due to experience multiplier options and to smooth out pacing.
    """
    display_name = "Scale Exp Items"
    default = False


# Final Boss Settings
class FinalBoss(Choice):
    """
    Sets which boss(es) will be the final ones.
    If set to both, Theos and Origin fights happen consecutively.
    """
    display_name = "Final Boss"
    option_theos = 0
    option_origin = 1
    option_both = 2
    option_io = 3
    default = 0


class TheosStartPhase(Choice):
    """
    Sets which phase the Theos fight will start in.
    1: Tentacle phase
    2: Circular platform with crystals
    3: Head form
    """
    display_name = "Theos Start Phase"
    option_first = 1
    option_second = 2
    option_final = 3
    default = 1


class OriginCarePackage(Choice):
    """
    Origin is a long fight and higher level than Theos.
    Since the Abyss is skipped in randomizer, this provides balance.
    Lite: A few ripe items and recipes
    Generous: Stacks of ripe items and recipes
    """
    display_name = "Origin Care Package"
    option_none = 0
    option_lite = 1
    option_generous = 2
    default = 0


class OriginStartPhase(Choice):
    """
    Sets which phase the Origin fight starts in.
    1: Mobbing phase
    2: Main boss
    """
    display_name = "Origin Start Phase"
    option_first = 1
    option_second = 2
    default = 2


# Misc Settings
class EssenceKeySanity(Toggle):
    """
    If Former Sanctuary Crypt is on, Essence Key Stones can be placed anywhere
    in the game instead of just within the dungeon itself. If set to on, forces Former Sanctuary Crypt on.
    """
    display_name = "Essence Key Sanity"
    default = False


class StartingCharacterWeights(OptionCounter):
    """
    Set the weight/chance for each starting character.
    Higher values mean more likely to be selected as the starting character.
    Set to 0 to disable a character from being selectable.
    """
    display_name = "Starting Character Weights"
    valid_keys = {"Adol", "Laxia", "Sahad", "Hummel", "Ricotta", "Dana"}
    min = 0
    default = {"Adol": 1, "Laxia": 1, "Sahad": 1, "Hummel": 1, "Ricotta": 1, "Dana": 1}

class DeathLink(Toggle):
    """
    If enabled, players will share death. When one player dies, the other player(s) will also die.
    """
    display_name = "Death Link"
    default = False

class HelperText(Toggle):
    """
    If enabled, this will display additional descriptive text about items.
    This is meant to help with new player onboarding.
    For remote items it will show the information in the client.
    """
    display_name = "Helper Text"
    default = False


@dataclass
class Ys8Options(PerGameCommonOptions):
    # Goal Settings
    final_boss_access: FinalBossAccess
    octus_count_crew_mode: OctusCountCrewMode
    octus_count_psyches_mode: OctusCountPsychesMode
    goal_count_crew_final_boss: GoalCountCrewFinalBoss
    goal_count_psyches_final_boss: GoalCountPsychesFinalBoss
    
    # Shuffle Modifiers
    discovery_sanity: DiscoverySanity
    dungeon_entrance_shuffle: DungeonEntranceShuffle
    shuffle_boss_levels: ShuffleBossLevels
    
    # Progression Placement Modifiers
    jewel_trade_items: JewelTradeItems
    fish_trades: FishTrades
    food_trades: FoodTrades
    map_completion: MapCompletion
    discoveries: Discoveries
    dogi_intercept_rewards: DogiInterceptRewards
    master_kong_rewards: MasterKongRewards
    silvia_progression: SilviaProgression
    mephorash_progression: MephorashProgression
    former_sanctuary_crypt: FormerSanctuaryCrypt
    
    # Pacing Modifiers
    experience_multiplier: ExperienceMultiplier
    additional_intercept_rewards: AdditionalInterceptRewards
    battle_logic: BattleLogic
    progressive_super_items: ProgressiveSuperItems
    fun_items: FunItems
    octus_paths_opened: OctusPathsOpened
    extra_flame_stones: ExtraFlameStones
    recipes_with_ingredients: RecipesWithIngredients
    north_side_open: NorthSideOpen
    infinity_mode: InfinityMode
    scale_exp_items: ScaleExpItems
    
    # Final Boss Settings
    final_boss: FinalBoss
    theos_start_phase: TheosStartPhase
    origin_care_package: OriginCarePackage
    origin_start_phase: OriginStartPhase
    
    # Misc Settings
    essence_key_sanity: EssenceKeySanity
    starting_character_weights: StartingCharacterWeights
    death_link: DeathLink
    helper_text: HelperText

Ys8_option_groups = [
    OptionGroup("Goal Settings", [
        FinalBossAccess,
        OctusCountCrewMode,
        OctusCountPsychesMode,
        GoalCountCrewFinalBoss,
        GoalCountPsychesFinalBoss,
    ]),
    OptionGroup("Shuffle Modifiers", [
        DiscoverySanity,
        DungeonEntranceShuffle,
        ShuffleBossLevels,
    ]),
    OptionGroup("Progression Placement Modifiers", [
        JewelTradeItems,
        FishTrades,
        FoodTrades,
        MapCompletion,
        Discoveries,
        DogiInterceptRewards,
        MasterKongRewards,
        SilviaProgression,
        MephorashProgression,
        FormerSanctuaryCrypt,
    ]),
    OptionGroup("Pacing Modifiers", [
        ExperienceMultiplier,
        AdditionalInterceptRewards,
        BattleLogic,
        ProgressiveSuperItems,
        FunItems,
        OctusPathsOpened,
        ExtraFlameStones,
        RecipesWithIngredients,
        NorthSideOpen,
        InfinityMode,
        ScaleExpItems,
    ]),
    OptionGroup("Final Boss Settings", [
        FinalBoss,
        TheosStartPhase,
        OriginCarePackage,
        OriginStartPhase,
    ]),
    OptionGroup("Misc Settings", [
        EssenceKeySanity,
        StartingCharacterWeights,
        DeathLink,
        HelperText,   
    ]),
]