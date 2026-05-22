from typing import NamedTuple
import json

class boss(NamedTuple):
    str_threshold: int
    level: int
    boss_id: str
    associated_entrances: list[str] = []
    paired_bosses: list[str] = []
    ordered_paired_bosses: list[str] = [] # used for balanced shuffle to ensure paired bosses are assigned in a specific order

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

# associated_entrances is the entrance region nearest the boss, ordered paired bosses change their arrangement base on which boss is encountered first in the shuffle.
# paired_bosses keep their original list order when encounter in the shuffle.
boss_list: dict[str, boss] = {
    "Byfteriza":            boss(10,    5,  'M0111',    ["Waterdrop Cave"]),
    "Avalodragil":          boss(65,    7,  'B150',     ["Calm Inlet Area"]),
    "Serpentus":            boss(87,    13, 'B100',     ["Towering Coral Forest Front"],          ordered_paired_bosses=["Serpentus","Clareon"]),
    "Clareon":              boss(90,    14, 'B000',     ["Towering Coral Forest After Boss"],     ordered_paired_bosses=["Clareon", "Serpentus"]),
    "Lonbrigius":           boss(200,   20, 'B101B',    ["Eroded Valley After Boss"],             ordered_paired_bosses=["Lonbrigius", "Gargantula"]),
    "Gargantula":           boss(210,   23, 'B001',     ["Eroded Valley Front"],                  ordered_paired_bosses=["Gargantula", "Lonbrigius"]),
    "Magamandra":           boss(220,   26, 'B102',     ["Schlamm Jungle Front"],                 ordered_paired_bosses=["Magamandra", "Laspisus"]),
    "Laspisus":             boss(250,   28, 'B002',     ["Schlamm Jungle After Boss"],            ordered_paired_bosses=["Laspisus", "Magamandra"]),
    "Kiergaard Weissman":   boss(300,   29, 'B152',     ["Odd Rock Coast"]),
    "Avalodragil 2":        boss(350,   32, 'B154',     ["Mont Gendarme Front"],                  ordered_paired_bosses=["Avalodragil 2", "Giasburn"]),
    "Giasburn":             boss(400,   35, 'B003',     ["Mont Gendarme After Boss"],             ordered_paired_bosses=["Giasburn", "Avalodragil 2"]),
    "Brachion":             boss(450,   40, 'B006',     ["Temple of the Great Tree", 
                                                         "Temple of the Great Tree After Boss"]),
    "Exmetal":              boss(500,   43, 'B104',     ["Baja Tower Lower Floors"]),
    "Carveros":             boss(550,   45, 'B004',     ["Baja Tower Lower Floors"]),
    "Gilkyra":              boss(450,   48, 'M0902',    ["East Coast Cave Before Gilkyra"],       paired_bosses=["Pirate Revenant"]),
    "Pirate Revenant":      boss(550,   48, 'B103',     ["East Coast Cave Before Gilkyra"],       paired_bosses=["Gilkyra"]),
    "Coelacantos":          boss(580,   51, 'B106',     ["Archeozoic Chasm Front"]),
    "Oceanus":              boss(660,   53, 'B007',     ["Archeozoic Chasm Front"]),
    "Doxa Griel":           boss(700,   58, 'B105',     ["Valley of Kings Before Door"],          paired_bosses=["Force Garmr", "Basileus"]),
    "Force Garmr":          boss(700,   59, 'M0643',    ["Valley of Kings Before Door"],          paired_bosses=["Doxa Griel", "Basileus"]),
    "Silvia":               boss(750,   60, 'B155',     ["Calm Inlet Area"]),
    "Basileus":             boss(750,   60, 'B005',     ["Valley of Kings Before Door"],          paired_bosses=["Doxa Griel", "Force Garmr"]),
    "Psyche Hydra":         boss(900,   67, 'B112',     ["Octus Overlook Entrance"],              paired_bosses=["Psyche Minos", "Psyche Nestor", "Psyche Ura"]),
    "Psyche Minos":         boss(920,   70, 'B110',     ["Octus Overlook Entrance"],              paired_bosses=["Psyche Hydra", "Psyche Nestor", "Psyche Ura"]),
    "Psyche Nestor":        boss(940,   73, 'B111',     ["Octus Overlook Entrance"],              paired_bosses=["Psyche Hydra", "Psyche Minos", "Psyche Ura"]),
    "Psyche Ura":           boss(960,   75, 'B008',     ["Octus Overlook Entrance"],              paired_bosses=["Psyche Hydra", "Psyche Minos", "Psyche Nestor"]),
    "Final Boss":           boss(960,   79, 'B020',     ["Octus Overlook Entrance"]),
    "Mephorash":            boss(1000,  80, 'B153',     ["Silent Tower"]),
    "Melaiduma":            boss(1100,  99, 'B170',     ["Former Sanctuary Crypt Front"]),
}

boss_stats = boss_list.copy()

def boss_excludes(options):
    exclude_bosses = []
    boss_option_dict = {
        "Melaiduma": options.former_sanctuary_crypt.value == 0,
        "Mephorash": options.mephorash_progression.value == 0,
        "Silvia": options.silvia_progression.value == 0,
        "Psyche Hydra": options.final_boss_access == 2,
        "Psyche Minos": options.final_boss_access == 2,
        "Psyche Nestor": options.final_boss_access == 2,
        "Psyche Ura": options.final_boss_access == 2,
    }
    for boss_name, option_condition in boss_option_dict.items():
        if option_condition:
            exclude_bosses.append(boss_name)
    exclude_bosses.append("Final Boss")
    
    return exclude_bosses

def randomize_levels_chaotic(Ys8World, exclude_bosses=None):
    exclude_bosses = boss_excludes(Ys8World.options)
    multiworld = Ys8World.multiworld

    # Only shuffle bosses not in exclude_bosses
    boss_names_to_shuffle = [name for name in boss_list.keys() if name not in exclude_bosses]
    boss_stats_list = [boss_list[name] for name in boss_names_to_shuffle]
    multiworld.random.shuffle(boss_stats_list)
    for boss_name in boss_names_to_shuffle:
        stats = boss_stats_list.pop()
        original = boss_list[boss_name]
        boss_stats[boss_name] = boss(stats.str_threshold, stats.level, original.boss_id, original.associated_entrances, original.paired_bosses)
    # For excluded bosses, keep their original stats
    for boss_name in exclude_bosses:
        boss_stats[boss_name] = boss_list[boss_name]
    
    build_boss_level_mapping(Ys8World)

def randomize_levels_balanced(Ys8World):
    multiworld = Ys8World.multiworld
    early_regions = []
    middle_regions = []
    early_boss = []
    middle_boss = []
    later_boss = []

    if Ys8World.options.north_side_open.value or Ys8World.options.discoveries.value:
        if Ys8World.options.dungeon_entrance_shuffle.value:
            early_entrances.append("SNA MGAB Entrance")
            early_entrances.append("TGT Entrance")
        else:
            early_regions.append("Mont Gendarme After Boss")
            early_regions.append("Temple of the Great Tree")

    else:
        if Ys8World.options.dungeon_entrance_shuffle.value:
            early_entrances.append("SNA MGAB Entrance")
            early_entrances.append("TGT Entrance")
        else:
            middle_regions.append("Mont Gendarme After Boss")
            middle_regions.append("Temple of the Great Tree")

    if Ys8World.options.dungeon_entrance_shuffle.value:
        for entrance, region in Ys8World.dungeon_connections.items():
            if entrance in early_entrances:
                early_regions.append(region)
            elif entrance in middle_entrances:
                middle_regions.append(region)
        early_regions.append("Calm Inlet Area")
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

    exclude_bosses = boss_excludes(Ys8World.options)
    early_boss = [b for b in early_boss if b not in exclude_bosses]
    middle_boss = [b for b in middle_boss if b not in exclude_bosses]
    later_boss = [b for b in later_boss if b not in exclude_bosses]


    def build_assignment_list(boss_names, exclude_bosses):
        assignment = []
        for boss_name in boss_names:
            if boss_name in exclude_bosses or boss_name in assignment:
                continue
            if boss_list[boss_name].paired_bosses:
                for paired in boss_list[boss_name].paired_bosses:
                    if paired not in exclude_bosses and paired not in assignment:
                        assignment.append(paired)
            if boss_list[boss_name].ordered_paired_bosses:
                for paired in boss_list[boss_name].ordered_paired_bosses:
                    if paired not in exclude_bosses and paired not in assignment:
                        assignment.append(paired)
            assignment.append(boss_name)
        return assignment

    early_assignment = build_assignment_list(early_boss, exclude_bosses)
    middle_assignment = build_assignment_list(middle_boss, exclude_bosses)
    later_assignment = build_assignment_list(later_boss, exclude_bosses)

    sorted_stats = sorted(boss_list.values(), key=lambda x: x.level)
    early_boss_levels = sorted_stats[:len(early_assignment)]
    middle_boss_levels = sorted_stats[len(early_assignment):len(early_assignment)+len(middle_assignment)]
    later_boss_levels = sorted_stats[len(early_assignment)+len(middle_assignment):len(early_assignment)+
                                     len(middle_assignment)+len(later_assignment)]

    multiworld.random.shuffle(early_boss)
    multiworld.random.shuffle(middle_boss)
    multiworld.random.shuffle(later_boss)

    def assign_stats_with_pairs(boss_names, stats_pool):
        sorted_boss_stats = sorted(stats_pool, key=lambda x: x.level)
        sorted_boss_names = []
        assigned = set()
        
        # build assingment order
        for boss_name in boss_names:
            if boss_name in exclude_bosses or boss_name in sorted_boss_names:
                continue
            if boss_list[boss_name].paired_bosses:
                paired_boss_list = [boss_name]
                for paired in boss_list[boss_name].paired_bosses:
                    if boss_name in exclude_bosses:
                        continue
                    paired_boss_list.append(paired)
                paired_boss_list_sorted = sorted(paired_boss_list, key=lambda name: list(boss_list.keys()).index(name))
                sorted_boss_names.extend(paired_boss_list_sorted)
            elif boss_list[boss_name].ordered_paired_bosses:
                for paired in boss_list[boss_name].ordered_paired_bosses:
                    if paired in exclude_bosses:
                        continue
                    sorted_boss_names.append(paired)
            sorted_boss_names.append(boss_name)
        
        for boss_name in sorted_boss_names:
            if boss_name in assigned or boss_name in exclude_bosses:
                continue
            stats = sorted_boss_stats.pop(0)
            boss_stats[boss_name] = boss(stats.str_threshold, stats.level, 
                                         boss_list[boss_name].boss_id, boss_list[boss_name].associated_entrances, 
                                         boss_list[boss_name].paired_bosses)
            assigned.add(boss_name)
            
    assign_stats_with_pairs(early_boss, early_boss_levels)
    assign_stats_with_pairs(middle_boss, middle_boss_levels)
    assign_stats_with_pairs(later_boss, later_boss_levels)

    for boss_name in exclude_bosses:
        boss_stats[boss_name] = boss_list[boss_name]
    
    build_boss_level_mapping(Ys8World)

def build_boss_level_mapping(Ys8World):
    Ys8World.boss_levels = {boss_name: {"level": stats.level, "boss_id": stats.boss_id} for boss_name, stats in boss_stats.items()} 
