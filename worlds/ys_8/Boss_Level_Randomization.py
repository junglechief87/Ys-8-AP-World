from typing import NamedTuple

class boss(NamedTuple):
    str_threshold: int
    level: int

boss_stats: dict[str, boss] = {}    

boss_list: dict[str, boss] = {
    "Byfteriza": boss(10, 5),
    "Avalodragil": boss(65, 7),
    "Serpentus": boss(87, 13),
    "Clareon": boss(90, 14),
    "Lonbrigius": boss(200, 20),
    "Gargantula": boss(210, 23),
    "Magamandra": boss(220, 26),
    "Laspisus": boss(250, 28),
    "Kiergaard Weissman": boss(300, 29),
    "Avalodragil 2": boss(350, 32),
    "Giasburn": boss(400, 35),
    "Brachion": boss(450, 40),
    "Exmetal": boss(500, 43),
    "Carveros": boss(550, 45),
    "Gilkyra": boss(450, 48),
    "Pirate Revenant": boss(550, 48),
    "Coelacantos": boss(580, 51),
    "Oceanus": boss(660, 53),
    "Doxa Griel": boss(700, 58),
    "Force Garmr": boss(700, 59),
    "Silvia": boss(750, 60),
    "Basileus": boss(750, 60),
    "Octus": boss(700, 60),
    "Psyche Hydra": boss(900, 67),
    "Psyche Minos": boss(920, 70),
    "Psyche Nestor": boss(940, 73),
    "Psyche Ura": boss(960, 75),
    "Final Boss": boss(960, 79),
    "Mephorash": boss(1000, 80),
    "FSC First Barrier": boss(1000, 50),
    "Melaiduma": boss(1100, 99),
}

boss_stats = boss_list.copy()

def randomize_levels_chaotic(Ys8World):
    boss_stats_list = [stats for stats in boss_list.values()]
    Ys8World.random.shuffle(boss_stats_list)
    for boss_name in boss_list.keys():
        stats = boss_stats_list.pop()
        boss_stats[boss_name] = stats