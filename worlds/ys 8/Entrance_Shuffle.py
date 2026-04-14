from typing import Dict

def dungeon_entrance_shuffle():
    paired_connectors: Dict[str, tuple] = {
        "Water Drop Cave Entrance": ("CIA to WC Entrance", "WC to WC Entrance"),
        "Towering Coral Forest Front Entrance": ("CIA to TCF", "TCF to CIA"),
        "Towering Coral Forest Back Entrance": ("TCF Exit to Meta Area", "TCF Back"),
        "Eroded Valley Front Entrance": ("GRV to EV Front", "EV Front to GRV"),
        "Eroded Valley Back Entrance": ("EV Boss Arena to SB", "EV Back to GRV"),
    }