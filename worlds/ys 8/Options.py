from dataclasses import dataclass
from typing import Tuple
from schema import And, Schema
from typing import Any, Dict
from Options import (
    Choice,
    DefaultOnToggle,
    LocationSet,
    OptionCounter,
    OptionError,
    OptionGroup,
    OptionSet,
    PerGameCommonOptions,
    Range,
    Toggle,
    Visibility,
)

class FinalBossAccess(Choice):
    """
    Sets the goal for when the teleport to the final boss inside the Selection Sphere will become active.
    """
    display_name = "Final Boss Access"
    option_find_crew = 0
    option_seiren_escape = 1

@dataclass
class Ys8Options(PerGameCommonOptions):
    final_boss_access: FinalBossAccess

Ys8_option_groups = [
    OptionGroup("Goal", [
        FinalBossAccess,
    ])
]

Ys8_option_presets: Dict[str, Dict[str, Any]] = {
    #Default
    "Defaults":{
        "final_boss_access": FinalBossAccess.option_find_crew,
    }
}