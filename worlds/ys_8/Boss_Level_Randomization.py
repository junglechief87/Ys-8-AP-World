from typing import NamedTuple

class boss(NamedTuple):
    str_threshold: int
    level: int
    associated_entrances: list[str] = []

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
    "Byfteriza":            boss(10,    5,  ["Waterdrop Cave"]),
    "Avalodragil":          boss(65,    7,  ["Calm Inlet Area"]),
    "Serpentus":            boss(87,    13, ["Towering Coral Forest Front", "Towering Coral Forest After Boss"]),
    "Clareon":              boss(90,    14, ["Towering Coral Forest Front", "Towering Coral Forest After Boss"]),
    "Lonbrigius":           boss(200,   20, ["Eroded Valley Front", "Eroded Valley After Boss"]),
    "Gargantula":           boss(210,   23, ["Eroded Valley Front", "Eroded Valley After Boss"]),
    "Magamandra":           boss(220,   26, ["Schlamm Jungle Front", "Schlamm Jungle After Boss"]),
    "Laspisus":             boss(250,   28, ["Schlamm Jungle Front", "Schlamm Jungle After Boss"]),
    "Kiergaard Weissman":   boss(300,   29, ["Odd Rock Coast"]),
    "Avalodragil 2":        boss(350,   32, ["Mont Gendarme Front", "Mont Gendarme After Boss"]),
    "Giasburn":             boss(400,   35, ["Mont Gendarme Front", "Mont Gendarme After Boss"]),
    "Brachion":             boss(450,   40, ["Temple of the Great Tree"]),
    "Exmetal":              boss(500,   43, ["Baja Tower Lower Floors"]),
    "Carveros":             boss(550,   45, ["Baja Tower Lower Floors"]),
    "Gilkyra":              boss(450,   48, ["East Coast Cave Before Gilkyra"]),
    "Pirate Revenant":      boss(550,   48, ["East Coast Cave Before Gilkyra"]),
    "Coelacantos":          boss(580,   51, ["Archeozoic Chasm Front"]),
    "Oceanus":              boss(660,   53, ["Archeozoic Chasm Front"]),
    "Doxa Griel":           boss(700,   58, ["Valley of Kings Before Door"]),
    "Force Garmr":          boss(700,   59, ["Valley of Kings Before Door"]),
    "Silvia":               boss(750,   60, ["Calm Inlet Area"]),
    "Basileus":             boss(750,   60, ["Valley of Kings Before Door"]),
    "Psyche Hydra":         boss(900,   67, ["Octus Overlook"]),
    "Psyche Minos":         boss(920,   70, ["Octus Overlook"]),
    "Psyche Nestor":        boss(940,   73, ["Octus Overlook"]),
    "Psyche Ura":           boss(960,   75, ["Octus Overlook"]),
    "Final Boss":           boss(960,   79, ["Octus Overlook"]),
    "Mephorash":            boss(1000,  80, ["Silent Tower"]),
    "Melaiduma":            boss(1100,  99, ["Former Sanctuary Crypt Front"]),
}

boss_stats = boss_list.copy()

def randomize_levels_chaotic(Ys8World):
    boss_stats_list = [stats for stats in boss_list.values()]
    Ys8World.random.shuffle(boss_stats_list)
    for boss_name in boss_list.keys():
        stats = boss_stats_list.pop()
        boss_stats[boss_name] = stats

def randomize_levels_balanced(Ys8World):
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
        
    Ys8World.random.shuffle(early_boss_levels)
    Ys8World.random.shuffle(middle_boss_levels)
    Ys8World.random.shuffle(later_boss_levels)

    for boss_name in early_boss:
        new_stats = early_boss_levels.pop(0)
        boss_stats[boss_name] = boss(new_stats.str_threshold, new_stats.level)

    for boss_name in middle_boss:
        new_stats = middle_boss_levels.pop(0)
        boss_stats[boss_name] = boss(new_stats.str_threshold, new_stats.level)

    for boss_name in later_boss:
        new_stats = later_boss_levels.pop(0)
        boss_stats[boss_name] = boss(new_stats.str_threshold, new_stats.level)

