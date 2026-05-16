from typing import NamedTuple
import json

class boss(NamedTuple):
    str_threshold: int
    level: int
    boss_id: str
    associated_entrances: list[str] = []
    paired_bosses: list[str] = []

boss_stats: dict[str, boss] = {}    

early_entrances = [
    "WC Entrance",
    "NCN TCF Entrance",
    "GRV EVF Entrance",
]

middle_entrances = [
    "GRVSC SJ Entrance",
    "PP MG Entrance",
]

boss_list: dict[str, boss] = {
    "Byfteriza":            boss(10,    5,  'M0111',    ["Waterdrop Cave"]),
    "Avalodragil":          boss(65,    7,  'B150',     ["Calm Inlet Area"]),
    "Serpentus":            boss(87,    13, 'B100',     ["Towering Coral Forest Front", "Towering Coral Forest After Boss"]),
    "Clareon":              boss(90,    14, 'B000',     ["Towering Coral Forest Front", "Towering Coral Forest After Boss"]),
    "Lonbrigius":           boss(200,   20, 'B101B',    ["Eroded Valley Front", "Eroded Valley After Boss"]),
    "Gargantula":           boss(210,   23, 'B001',     ["Eroded Valley Front", "Eroded Valley After Boss"]),
    "Magamandra":           boss(220,   26, 'B102',     ["Schlamm Jungle Front", "Schlamm Jungle After Boss"]),
    "Laspisus":             boss(250,   28, 'B002',     ["Schlamm Jungle Front", "Schlamm Jungle After Boss"]),
    "Kiergaard Weissman":   boss(300,   29, 'B152',     ["Odd Rock Coast"]),
    "Avalodragil 2":        boss(350,   32, 'B154',     ["Mont Gendarme Front", "Mont Gendarme After Boss"]),
    "Giasburn":             boss(400,   35, 'B003',     ["Mont Gendarme Front", "Mont Gendarme After Boss"]),
    "Brachion":             boss(450,   40, 'B006',     ["Temple of the Great Tree"]),
    "Exmetal":              boss(500,   43, 'B104',     ["Baja Tower Lower Floors"]),
    "Carveros":             boss(550,   45, 'B004',     ["Baja Tower Lower Floors"]),
    "Gilkyra":              boss(450,   48, 'M0902',    ["East Coast Cave Before Gilkyra"],                                         ["Pirate Revenant"]),
    "Pirate Revenant":      boss(550,   48, 'B103',     ["East Coast Cave Before Gilkyra"],                                         ["Gilkyra"]),
    "Coelacantos":          boss(580,   51, 'B106',     ["Archeozoic Chasm Front"]),
    "Oceanus":              boss(660,   53, 'B007',     ["Archeozoic Chasm Front"]),
    "Doxa Griel":           boss(700,   58, 'B105',     ["Valley of Kings Before Door"],                                            ["Force Garmr", "Basileus"]),
    "Force Garmr":          boss(700,   59, 'M0643',    ["Valley of Kings Before Door"],                                            ["Doxa Griel", "Basileus"]),
    "Silvia":               boss(750,   60, 'B155',     ["Calm Inlet Area"]),
    "Basileus":             boss(750,   60, 'B005',     ["Valley of Kings Before Door"],                                            ["Doxa Griel", "Force Garmr"]),
    "Psyche Hydra":         boss(900,   67, 'B112',     ["Octus Overlook"],                                                         ["Psyche Minos", "Psyche Nestor", "Psyche Ura"]),
    "Psyche Minos":         boss(920,   70, 'B110',     ["Octus Overlook"],                                                         ["Psyche Hydra", "Psyche Nestor", "Psyche Ura"]),
    "Psyche Nestor":        boss(940,   73, 'B111',     ["Octus Overlook"],                                                         ["Psyche Hydra", "Psyche Minos", "Psyche Ura"]),
    "Psyche Ura":           boss(960,   75, 'B008',     ["Octus Overlook"],                                                         ["Psyche Hydra", "Psyche Minos", "Psyche Nestor"]),
    "Final Boss":           boss(960,   79, 'B020',     ["Octus Overlook"]),
    "Mephorash":            boss(1000,  80, 'B153',     ["Silent Tower"]),
    "Melaiduma":            boss(1100,  99, 'B170',     ["Former Sanctuary Crypt Front"]),
}

boss_stats = boss_list.copy()

def randomize_levels_chaotic(Ys8World):
    multiworld = Ys8World.multiworld

    boss_stats_list = [stats for stats in boss_list.values()]
    multiworld.random.shuffle(boss_stats_list)
    for boss_name in boss_list.keys():
        stats = boss_stats_list.pop()
        boss_stats[boss_name] = stats

def randomize_levels_balanced(Ys8World):
    multiworld = Ys8World.multiworld
    early_regions = ["Calm Inlet Area"]
    middle_regions = []
    early_boss = []
    middle_boss = []
    later_boss = []

    if Ys8World.options.north_side_open.value or Ys8World.options.discoveries.value:
        early_regions.append("Temple of the Great Tree")
        if Ys8World.options.dungeon_entrance_shuffle.value:
            early_entrances.append("SNA MGAB Entrance")
        else:
            early_regions.append("Mont Gendarme After Boss")

    else:
        middle_regions.append("Temple of the Great Tree")
        if Ys8World.options.dungeon_entrance_shuffle.value:
            middle_entrances.append("SNA MGAB Entrance")
        else:
            middle_regions.append("Mont Gendarme After Boss")

    if Ys8World.options.dungeon_entrance_shuffle.value:
        for entrance, region in Ys8World.dungeon_connections:
            if entrance in early_entrances:
                early_regions.append(region)
            elif entrance in middle_entrances:
                middle_regions.append(region)
    else:
        early_regions.extend(["Calm Inlet Area", "Waterdrop Cave", "Towering Coral Forest Front", "Eroded Valley Front"])
        middle_regions.extend(["Schlamm Jungle Front", "Odd Rock Coast", "Mont Gendarme Front"])
    
    for boss_name, stats in boss_list.items():
        if any(region in early_regions for region in stats.associated_entrances):
            early_boss.append(boss_name)
        elif any(region in middle_regions for region in stats.associated_entrances):
            middle_boss.append(boss_name)
        else:
            later_boss.append(boss_name)

    boss_list_values = list(boss_list.values())
    early_boss_levels = boss_list_values[0:len(early_boss)]
    middle_boss_levels = boss_list_values[len(early_boss):len(early_boss) + len(middle_boss)]
    later_boss_levels = boss_list_values[len(early_boss) + len(middle_boss):]
        
    multiworld.random.shuffle(early_boss_levels)
    multiworld.random.shuffle(middle_boss_levels)
    multiworld.random.shuffle(later_boss_levels)

    def assign_stats_with_pairs(boss_names, stats_pool):
        used_indices = set()
        for boss_name in boss_names:
            # Find next unused stat
            stat_idx = None
            for i in range(len(stats_pool)):
                if i not in used_indices:
                    stat_idx = i
                    break
            
            if stat_idx is None:
                break
            
            new_stats = stats_pool[stat_idx]
            used_indices.add(stat_idx)
            boss_stats[boss_name] = boss(new_stats.str_threshold, new_stats.level, new_stats.boss_id)
            
            # Handle paired bosses - find closest level/str_threshold match from remaining stats
            if boss_list[boss_name].paired_bosses:
                for paired_boss in boss_list[boss_name].paired_bosses:
                    target_level = new_stats.level
                    closest_idx = None
                    closest_diff = float('inf')
                    
                    for i in range(len(stats_pool)):
                        if i not in used_indices:
                            diff = abs(stats_pool[i].level - target_level)
                            if diff < closest_diff:
                                closest_diff = diff
                                closest_idx = i
                    
                    if closest_idx is not None:
                        paired_stats = stats_pool[closest_idx]
                        used_indices.add(closest_idx)
                        boss_stats[paired_boss] = boss(paired_stats.str_threshold, paired_stats.level, paired_stats.boss_id)

    assign_stats_with_pairs(early_boss, early_boss_levels)
    assign_stats_with_pairs(middle_boss, middle_boss_levels)
    assign_stats_with_pairs(later_boss, later_boss_levels)
    
    # Debug output
    debug_output = {
        "tier_distribution": {
            "early_bosses": early_boss,
            "middle_bosses": middle_boss,
            "later_bosses": later_boss,
        },
        "boss_stats": {
            boss_name: {
                "str_threshold": stats.str_threshold,
                "level": stats.level,
                "boss_id": stats.boss_id,
                "associated_entrances": stats.associated_entrances,
                "paired_bosses": stats.paired_bosses,
            }
            for boss_name, stats in boss_stats.items()
        }
    }
    print("\n=== BALANCED BOSS RANDOMIZATION DEBUG ===")
    print(json.dumps(debug_output, indent=2))
    print("=========================================\n")

