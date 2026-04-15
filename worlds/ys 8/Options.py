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
    Seiren Escape: Find three specific items: Seiren Nautical Chart, Ship Blueprints, and Mistilteinn.
    Release the Psyches: Defeat the specified number of Wardens of Evolution (out of up to 6 possible).
    Untouchable: Reach the bottom of Former Sanctuary Crypt and defeat Melaiduma. Forces Former Sanctuary Crypt on.
    """
    display_name = "Final Boss Access"
    option_find_crew = 0
    option_seiren_escape = 1
    option_release_the_psyches = 2
    option_untouchable = 3
    default = 0


class GoalCountCrewMode(Range):
    """
    For Find Crew mode: Sets the number of castaways required to open Octus Overlook Entrance
    and unlock access to the Tree of Origin, a powerful grinding location.
    """
    display_name = "Goal Count to Open Octus (Find Crew)"
    range_start = 1
    range_end = 28
    default = 16


class GoalCountPsychesMode(Range):
    """
    For Release the Psyches mode: Sets the number of Wardens of Evolution required to defeat
    to open Octus Overlook Entrance and unlock access to the Tree of Origin.
    """
    display_name = "Goal Count to Open Octus (Release the Psyches)"
    range_start = 1
    range_end = 6
    default = 2


class GoalCountCrewFinalBoss(Range):
    """
    For Find Crew mode: Sets the number of castaways required to access the final boss.
    """
    display_name = "Goal Count to Access Final Boss (Find Crew)"
    range_start = 1
    range_end = 28
    default = 20


class GoalCountPsychesFinalBoss(Range):
    """
    For Release the Psyches mode: Sets the number of Wardens of Evolution required to defeat
    to access the final boss.
    """
    display_name = "Goal Count to Access Final Boss (Release the Psyches)"
    range_start = 1
    range_end = 6
    default = 4


# Shuffle Modifiers
class DiscoverySanity(Toggle):
    """
    Puts the landmarks in the item pool. Finding a landmark unlocks the ability to warp to it on the map.
    This drastically changes logic and movement around the world.
    """
    display_name = "Discovery-Sanity"
    default = False


class DungeonEntranceShuffle(Toggle):
    """
    Shuffles the entrances to dungeon maps. The entrance to one dungeon may lead to another.
    East Coast Cave is treated as the entrance for Pirate Ship Eleftheria with this setting on.
    """
    display_name = "Dungeon Entrance Shuffle"
    default = False


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
    Dogi does not need to have joined the village.
    Intercepts are now unlocked via T's Memos found in the world.
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
    Mephorash is the highest level optional fight in the game
    and the Silent Tower is a high requirement location.
    """
    display_name = "Mephorash Progression"
    default = False


class FormerSanctuaryCrypt(Toggle):
    """
    Sets whether Former Sanctuary Crypt is added to the item pool.
    If turned off, the dungeon is closed.
    All essence keystones are placed within the dungeon unless Essence Key Sanity is on.
    """
    display_name = "Former Sanctuary Crypt"
    default = False


# Pacing Modifiers
class ExperienceMultiplier(Range):
    """
    Divides character's min and max Exp values allowing for quicker leveling.
    A multiplier of 3 provides well-balanced pacing.
    """
    display_name = "Experience Multiplier"
    range_start = 1
    range_end = 10
    default = 3


class AdditionalInterceptRewards(Toggle):
    """
    Causes intercepts to give out up to four additional rewards after returning
    to Castaway Village post-intercept.
    """
    display_name = "Additional Intercept Rewards"
    default = False


class BattleLogic(Toggle):
    """
    Attempts to smooth combat pacing by guaranteeing the player always has access
    to some amount of strength for each boss.
    Highly recommended to be left on, especially for Inferno difficulty.
    """
    display_name = "Battle Logic"
    default = True

class ScaledEncounters(Toggle):
    """
    Scales the levels of forced encounters and bosses based on when they appear in the seed.
    """
    display_name = "Scaled Encounters"
    default = False

class ProgressiveSuperWeapons(Toggle):
    """
    Both the Mistilteinn and Spirit Ring are in the pools.
    Players find Broken Mistilteinn or Broken Spirit Ring instead.
    Speaking with Kathleen after maxing the forge will fix the broken weapon.
    """
    display_name = "Progressive Super Weapons"
    default = True


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
    Adds Flame Stones to the item pool (1-10 additional stones).
    There are 7 Flame Stones by default, so 3 additional puts it at a round 10.
    Makes hitting max level more likely without being excessive.
    """
    display_name = "Extra Flame Stones"
    range_start = 1
    range_end = 10
    default = 3


class RecipesWithIngredients(Toggle):
    """
    Grants the player all ingredients necessary to cook a dish
    upon obtaining their respective Recipe Book.
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
    Scales experience reward items (Hermit's Elixir and Bitter Remedy) with the
    Experience Multiplier setting. For example, with a 3.0x multiplier, a Hermit's
    Elixir check becomes 3 Bitter Remedy.
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
    default = 0


class TheosStartPhase(Choice):
    """
    Sets which phase the Theos fight will start in.
    1: Normal mode
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
    in the game instead of just within the dungeon itself.
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


@dataclass
class Ys8Options(PerGameCommonOptions):
    # Goal Settings
    final_boss_access: FinalBossAccess
    goal_count_crew_mode: GoalCountCrewMode
    goal_count_psyches_mode: GoalCountPsychesMode
    goal_count_crew_final_boss: GoalCountCrewFinalBoss
    goal_count_psyches_final_boss: GoalCountPsychesFinalBoss
    
    # Shuffle Modifiers
    discovery_sanity: DiscoverySanity
    dungeon_entrance_shuffle: DungeonEntranceShuffle
    
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
    scaled_encounters: ScaledEncounters
    progressive_super_weapons: ProgressiveSuperWeapons
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


Ys8_option_groups = [
    OptionGroup("Goal Settings", [
        FinalBossAccess,
        GoalCountCrewMode,
        GoalCountPsychesMode,
        GoalCountCrewFinalBoss,
        GoalCountPsychesFinalBoss,
    ]),
    OptionGroup("Shuffle Modifiers", [
        DiscoverySanity,
        DungeonEntranceShuffle,
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
        ScaledEncounters,
        ProgressiveSuperWeapons,
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
    ]),
]

Ys8_option_presets: Dict[str, Dict[str, Any]] = {
    "Defaults": {
        "final_boss_access": FinalBossAccess.option_find_crew,
        "goal_count_crew_mode": 16,
        "goal_count_psyches_mode": 2,
        "goal_count_crew_final_boss": 20,
        "goal_count_psyches_final_boss": 3,
        "discovery_sanity": False,
        "dungeon_entrance_shuffle": False,
        "jewel_trade_items": JewelTradeItems.option_up_to_10_jewels,
        "fish_trades": FishTrades.option_6,
        "food_trades": FoodTrades.option_6,
        "map_completion": MapCompletion.option_60_percent,
        "discoveries": Discoveries.option_all,
        "dogi_intercept_rewards": True,
        "master_kong_rewards": False,
        "silvia_progression": False,
        "mephorash_progression": False,
        "former_sanctuary_crypt": False,
        "experience_multiplier": 3,
        "additional_intercept_rewards": False,
        "battle_logic": True,
        "scaled_encounters": False,
        "progressive_super_weapons": True,
        "octus_paths_opened": True,
        "extra_flame_stones": 3,
        "recipes_with_ingredients": True,
        "north_side_open": False,
        "infinity_mode": False,
        "scale_exp_items": False,
        "final_boss": FinalBoss.option_theos,
        "theos_start_phase": TheosStartPhase.option_first,
        "origin_care_package": OriginCarePackage.option_none,
        "origin_start_phase": OriginStartPhase.option_second,
        "essence_key_sanity": False,
        "starting_character_weights": {"Adol": 1, "Laxia": 1, "Sahad": 1, "Hummel": 1, "Ricotta": 1, "Dana": 1},
    }
}