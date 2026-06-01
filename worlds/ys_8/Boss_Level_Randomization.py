from typing import NamedTuple

class boss(NamedTuple):
    str_threshold: int
    level: int
    boss_id: str
    associated_entrances: list[str] = []
    paired_bosses: list[str] = []
    ordered_paired_bosses: list[str] = [] # used for balanced shuffle to ensure paired bosses are assigned in a specific order

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
    "Gilkyra":              boss(450,   48, 'M0902',    ["East Coast Cave Before Gilkyra"],       ordered_paired_bosses=["Gilkyra", "Pirate Revenant"]),
    "Pirate Revenant":      boss(550,   48, 'B103',     ["East Coast Cave Before Gilkyra"],       ordered_paired_bosses=["Gilkyra", "Pirate Revenant"]),
    "Coelacantos":          boss(580,   51, 'B106',     ["Archeozoic Chasm Front"]),
    "Oceanus":              boss(660,   53, 'B007',     ["Archeozoic Chasm Front"]),
    "Doxa Griel":           boss(700,   58, 'B105',     ["Valley of Kings Before Door"]),
    "Force Garmr":          boss(700,   59, 'M0643',    ["Valley of Kings Before Door"],          ordered_paired_bosses=["Force Garmr", "Basileus"]),
    "Silvia":               boss(750,   60, 'B155',     ["Calm Inlet Area"]),
    "Basileus":             boss(750,   60, 'B005',     ["Valley of Kings Before Door"],          ordered_paired_bosses=["Force Garmr", "Basileus"]),
    "Psyche Hydra":         boss(900,   67, 'B112',     ["Octus Overlook Entrance"],              paired_bosses=["Psyche Minos", "Psyche Nestor", "Psyche Ura"]),
    "Psyche Minos":         boss(920,   70, 'B110',     ["Octus Overlook Entrance"],              paired_bosses=["Psyche Hydra", "Psyche Nestor", "Psyche Ura"]),
    "Psyche Nestor":        boss(940,   73, 'B111',     ["Octus Overlook Entrance"],              paired_bosses=["Psyche Hydra", "Psyche Minos", "Psyche Ura"]),
    "Psyche Ura":           boss(960,   75, 'B008',     ["Octus Overlook Entrance"],              paired_bosses=["Psyche Hydra", "Psyche Minos", "Psyche Nestor"]),
    "Final Boss":           boss(960,   79, 'B020',     ["Octus Overlook Entrance"]),
    "Mephorash":            boss(1000,  80, 'B153',     ["Silent Tower"]),
    "Melaiduma":            boss(1100,  99, 'B170',     ["Former Sanctuary Crypt Front"]),
}

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

def randomize_boss_levels(Ys8World: "Ys8World"):
    if Ys8World.generating_in_ut and len(Ys8World.boss_stats) > 0:
        return

    if Ys8World.options.shuffle_boss_levels == 1:
        randomize_levels_balanced(Ys8World)
    elif Ys8World.options.shuffle_boss_levels == 2:
        randomize_levels_chaotic(Ys8World)
    else:
        Ys8World.boss_stats = boss_list.copy()

def randomize_levels_chaotic(Ys8World, exclude_bosses=None):
    # Ensure we start from the canonical boss list for this world on the world instance
    Ys8World.boss_stats = boss_list.copy()
    exclude_bosses = boss_excludes(Ys8World.options)
    multiworld = Ys8World.multiworld

    # Only shuffle bosses not in exclude_bosses
    boss_names_to_shuffle = [name for name in boss_list.keys() if name not in exclude_bosses]
    boss_stats_list = [boss_list[name] for name in boss_names_to_shuffle]
    multiworld.random.shuffle(boss_stats_list)
    for boss_name in boss_names_to_shuffle:
        stats = boss_stats_list.pop()
        original = boss_list[boss_name]
        Ys8World.boss_stats[boss_name] = boss(stats.str_threshold, stats.level, original.boss_id, original.associated_entrances, original.paired_bosses)
    # For excluded bosses, keep their original stats
    for boss_name in exclude_bosses:
        Ys8World.boss_stats[boss_name] = boss_list[boss_name]
    
    build_boss_level_mapping(Ys8World)

def randomize_levels_balanced(Ys8World):
    # Ensure we start from the canonical boss list for this world on the world instance
    Ys8World.boss_stats = boss_list.copy()
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


    def build_assignment_list(boss_names, exclude_bosses, used_bosses):
        assignment = []
        for boss_name in boss_names:
            if boss_name in exclude_bosses or \
               boss_name in assignment or \
               boss_name in used_bosses:
                continue
            elif boss_list[boss_name].paired_bosses:
                assignment.append(boss_name)
                for paired in boss_list[boss_name].paired_bosses:
                    if paired not in exclude_bosses and \
                       paired not in assignment and \
                       paired not in used_bosses:
                        assignment.append(paired)
            elif boss_list[boss_name].ordered_paired_bosses:
                for paired in boss_list[boss_name].ordered_paired_bosses:
                    if paired not in exclude_bosses and \
                       paired not in assignment and \
                       paired not in used_bosses:
                        assignment.append(paired)
            else:
                assignment.append(boss_name)
        
        used_bosses.extend(assignment)
        return assignment,used_bosses
    
    used_bosses = []
    early_assignment, used_bosses = build_assignment_list(early_boss, exclude_bosses, used_bosses)
    middle_assignment, used_bosses = build_assignment_list(middle_boss, exclude_bosses, used_bosses)
    later_assignment, used_bosses = build_assignment_list(later_boss, exclude_bosses, used_bosses)

    sorted_stats = sorted(boss_list.values(), key=lambda x: x.level)
    early_boss_levels = sorted_stats[:len(early_assignment)]
    middle_boss_levels = sorted_stats[len(early_assignment):len(early_assignment)+len(middle_assignment)]
    later_boss_levels = sorted_stats[len(early_assignment)+len(middle_assignment):len(early_assignment)+
                                     len(middle_assignment)+len(later_assignment)]

    def assign_stats_with_pairs(boss_names, stats_pool):
        multiworld.random.shuffle(stats_pool)
        assigned = set()
        def assign_boss_stats(boss_name, stats):
            Ys8World.boss_stats[boss_name] = boss(stats.str_threshold, stats.level, 
                                                 boss_list[boss_name].boss_id, boss_list[boss_name].associated_entrances, 
                                                 boss_list[boss_name].paired_bosses)
            assigned.add(boss_name)
        
        for boss_name in boss_names:
            if boss_name in assigned:
                continue
            # If the bosses are an ordered pair we sort the remaining stats pool by level and assign in order
            # then reshuffle the remaining pool. This keeps the levels close and in a specific order but still random.
            if Ys8World.boss_stats[boss_name].ordered_paired_bosses:
                stats_pool = sorted(stats_pool, key=lambda x: x.level)
                for paired in Ys8World.boss_stats[boss_name].ordered_paired_bosses:
                    if paired in assigned:
                        continue
                    assign_boss_stats(paired, stats_pool.pop(0))
                multiworld.random.shuffle(stats_pool)
            # If the bosses are an unordered pair we sort the stats pool gather our boss list
            # then shuffle the list. This keeps the levels close but not perfectly ordered.
            elif Ys8World.boss_stats[boss_name].paired_bosses:
                stats_pool = sorted(stats_pool, key=lambda x: x.level)
                paired_bosses = Ys8World.boss_stats[boss_name].paired_bosses.copy()
                paired_bosses.append(boss_name)
                multiworld.random.shuffle(paired_bosses)
                for paired in paired_bosses:
                    if paired in assigned:
                        continue
                    assign_boss_stats(paired, stats_pool.pop(0))
            else:
                assign_boss_stats(boss_name, stats_pool.pop(0))

    assign_stats_with_pairs(early_assignment, early_boss_levels)
    assign_stats_with_pairs(middle_assignment, middle_boss_levels)
    assign_stats_with_pairs(later_assignment, later_boss_levels)

    for boss_name in exclude_bosses:
        Ys8World.boss_stats[boss_name] = boss_list[boss_name]
    
    build_boss_level_mapping(Ys8World)

def build_boss_level_mapping(Ys8World):
    Ys8World.boss_levels = {boss_name: {"level": stats.level, "boss_id": stats.boss_id} for boss_name, stats in Ys8World.boss_stats.items()}

def ut_build_boss_stats(Ys8World: "Ys8World", boss_levels: dict[str, int]):
    id_to_stats = {b.boss_id: b for b in boss_list.values()}

    Ys8World.boss_stats = dict()
    for name, level in boss_levels.items():
        stat = id_to_stats.get(level)
        if stat is not None:
            Ys8World.boss_stats[name] = stat
        else: # Missing boss. Try to recover by getting the normal stats, and if that fails just use Byfteriza.
            Ys8World.boss_stats[name] = boss_levels.get(name, boss_levels["Byfteriza"])

    build_boss_level_mapping(Ys8World)