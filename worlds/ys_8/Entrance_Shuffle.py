from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from . import Ys8World


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DungeonSlot:
    """One enterable region inside a dungeon, paired with its outbound exit."""
    region:    str   # AP region name inside the dungeon
    exit_name: str   # AP exit that leads back to the overworld


@dataclass(frozen=True)
class Dungeon:
    """
    A dungeon that field connectors can lead into.
      Two slots = bidirectional: an isolated connector MUST occupy one slot so
                  the dungeon's second slot keeps it reachable from the world.
      One slot  = unidirectional: no special placement constraints.
    """
    name:            str
    slots:           tuple[DungeonSlot, ...]
    requires_option: str = ""  # options attribute name that must be truthy; "" = always active

    @property
    def is_bidirectional(self) -> bool:
        return len(self.slots) == 2


@dataclass(frozen=True)
class FieldConnector:
    """
    An overworld exit that leads into a shuffled dungeon.

    Flags (all default False/""):
      is_north         – source region is on the north side of the island
      always_isolated  – dead-end area with no other access; MUST land in a
                         bidirectional dungeon regardless of options
      landmark_only    – only reachable via a discovery landmark; behaves as
                         isolated when discovery_sanity is disabled
      requires_option  – options attribute name that must be truthy to include
                         this connector; "" = always active
    """
    exit_name:       str
    source_region:   str
    is_north:        bool = False
    is_garden:       bool = False
    always_isolated: bool = False
    landmark_only:   bool = False
    requires_option: str  = ""


# ---------------------------------------------------------------------------
# Static world data  ← add new areas here; no algorithm changes needed
# ---------------------------------------------------------------------------

DUNGEONS: tuple[Dungeon, ...] = (
    # Bidirectional (2 slots) — order determines bidir_slots key order (TCF, EV, SJ, MG)
    Dungeon("Towering Coral Forest", (
        DungeonSlot("Towering Coral Forest Front",      "TCF NCN Exit"),
        DungeonSlot("Towering Coral Forest After Boss", "TCFAB Meta Exit"),
    )),
    Dungeon("Eroded Valley", (
        DungeonSlot("Eroded Valley Front",      "EVF GRV Exit"),
        DungeonSlot("Eroded Valley After Boss", "EVAB SB Exit"),
    )),
    Dungeon("Schlamm Jungle", (
        DungeonSlot("Schlamm Jungle Front",      "SJF GRVSC Exit"),
        DungeonSlot("Schlamm Jungle After Boss", "SJAB ORC Exit"),
    )),
    Dungeon("Mont Gendarme", (
        DungeonSlot("Mont Gendarme Front",      "MGF PPGE Exit"),
        DungeonSlot("Mont Gendarme After Boss", "MGAB SNA Exit"),
    )),
    Dungeon("Temple of the Great Tree", (
        DungeonSlot("Temple of the Great Tree",             "TGT Entrance Exit"),
        DungeonSlot("Temple of the Great Tree After Boss",  "TGT Garden Exit"),
    )),
    # Unidirectional (1 slot)
    Dungeon("Waterdrop Cave",                (DungeonSlot("Waterdrop Cave",                 "WC Exit"),)),
    Dungeon("East Coast Cave Before Gilkyra",(DungeonSlot("East Coast Cave Before Gilkyra", "ECCBG NCA Exit"),)),
    Dungeon("Silent Tower",                  (DungeonSlot("Silent Tower",                   "STE OST Exit"),)),
    Dungeon("Octus Overlook",                (DungeonSlot("Octus Overlook Entrance",        "OO TGT Exit"),)),
    Dungeon("Former Sanctuary Crypt",        (DungeonSlot("Former Sanctuary Crypt Front",   "FSCF ROEHP Exit"),), requires_option="former_sanctuary_crypt"),
    Dungeon("Baja Tower Lower Floors",       (DungeonSlot("Baja Tower Lower Floors",        "BTLF THBTE Exit"),)),
    Dungeon("Archeozoic Chasm",              (DungeonSlot("Archeozoic Chasm Front",         "ACF BTAC Exit"),)),
    Dungeon("Valley of Kings",               (DungeonSlot("Valley of Kings Before Door",    "VOKBD LMB Exit"),)),
)

# Connector order matters for seed parity:
#   1. Normal free exits (matches original multi_connector_exits list order)
#   2. always_isolated  (appended after free, matching original single_connector_exits)
#   3. landmark_only    (appended last, matching original DISCOVERY_DEPENDENT_EXITS extend)
CONNECTORS: tuple[FieldConnector, ...] = (
    FieldConnector("WC Entrance",           "Calm Inlet Area"),
    FieldConnector("NCN TCF Entrance",      "Nameless Coast North"),
    FieldConnector("GRV EVF Entrance",      "Great River Valley Area"),
    FieldConnector("GRVSC SJ Entrance",     "Great River Valley South Camp"),
    FieldConnector("PP MG Entrance",        "Primordial Passage Gendarme Entrance"),
    FieldConnector("SNA MGAB Entrance",     "Seiren North Access",                      is_north=True),
    FieldConnector("AC Entrance",           "Bridge to Archeozoic Chasm",               is_north=True),
    FieldConnector("FSC Entrance",          "Ruins of Eternia Hidden Passage",          is_north=True, requires_option="former_sanctuary_crypt"),
    FieldConnector("BTLF Entrance",         "Towal Highway Baja Tower Entrance",        is_north=True),
    FieldConnector("LMB VOKBD Entrance",    "Lodinia Marshlands Back",                  is_north=True),
    FieldConnector("TGT Entrance",          "Temple of the Great Tree Entrance",        is_north=True),
    FieldConnector("TGT Garden Entrance",   "Temple of the Great Tree Garden Entrance", is_garden=True),
    FieldConnector("OO Entrance",           "Temple of the Great Tree Garden",          is_garden=True),
    FieldConnector("ST Entrance",           "Silent Tower Entrance"),
    FieldConnector("NCA ECCBG Entrance",    "Nostalgia Cape Area"),
    # always_isolated — dead-end; never enters free_exits
    FieldConnector("ORC SJ Entrance",       "Odd Rock Coast",                    always_isolated=True),
    # landmark_only — isolated without discovery_sanity; at end so free_exits
    # list comp appends them last when discovery_sanity is on (matching original .extend())
    FieldConnector("Meta TCF Entrance",     "Metavolicalis Area",                landmark_only=True),
    FieldConnector("SB EV Entrance",        "Sunrise Beach",                     landmark_only=True),
)

# Lookup tables derived from the above — no manual maintenance needed.
_DUNGEON_EXIT:     dict[str, str] = {s.region:    s.exit_name    for d in DUNGEONS   for s in d.slots}
_CONNECTOR_SOURCE: dict[str, str] = {c.exit_name: c.source_region for c in CONNECTORS}

# ---------------------------------------------------------------------------


def _assign(world, exit_name: str, dungeon_region: str, connections: dict) -> None:
    """Record one exit→dungeon assignment and add it to the spoiler log."""
    connections[exit_name] = dungeon_region
    world.entrance_spoiler.append(f"{exit_name}=>{dungeon_region}")


def dungeon_entrance_shuffle(world) -> None:
    # If we are generating in Universal Tracker, it may already have locations saved for us
    if world.generating_in_ut and world.dungeon_connections is not None:
        return

    rng     = world.multiworld.random
    options = world.options

    discovery_off = not options.discovery_sanity.value

    # Filter out entries whose required option is disabled.
    active_connectors = [c for c in CONNECTORS if not c.requires_option or getattr(options, c.requires_option).value]
    active_dungeons   = [d for d in DUNGEONS   if not d.requires_option or getattr(options, d.requires_option).value]

    # --- Build mutable slot pools ---
    bidir_slots: dict[str, list[str]] = {
        d.name: [s.region for s in d.slots]
        for d in active_dungeons if d.is_bidirectional
    }
    uni_slots: list[str] = [d.slots[0].region for d in active_dungeons if not d.is_bidirectional]

    # --- Derive working exit lists from connector properties ---
    # always_isolated first, then landmark_only (when discovery is off) —
    # preserves original order: ["ORC SJ", "Meta TCF", "SB EV"]
    isolated_exits: list[str] = (
        [c.exit_name for c in active_connectors if c.always_isolated] +
        [c.exit_name for c in active_connectors if c.landmark_only and discovery_off]
    )
    # Non-special connectors in tuple order; landmark_only connectors appear at
    # end of the tuple so they're naturally appended last when discovery is on —
    # matching original multi_connector_exits + .extend(DISCOVERY_DEPENDENT_EXITS)
    free_exits: list[str] = [
        c.exit_name for c in active_connectors
        if not c.always_isolated and not (c.landmark_only and discovery_off)
    ]
    north_exits: list[str] = [c.exit_name for c in active_connectors if c.is_north]

    connections: dict[str, str] = {}

    # === Phase 1: Place isolated exits into unique bidirectional dungeons ===
    # Each gets its OWN dungeon — sharing one would form an isolated cluster
    # cut off from the rest of the world.
    bidir_keys = list(bidir_slots.keys())
    rng.shuffle(bidir_keys)
    for exit_name in isolated_exits:
        dungeon = bidir_keys.pop()
        slot    = rng.choice(bidir_slots[dungeon])
        bidir_slots[dungeon].remove(slot)
        _assign(world, exit_name, slot, connections)

    # === Phase 2: Guarantee connectivity bridges (when required) ===
    # Each entry: (active: bool, flagged_exits: list[str]).
    # When active, one flagged exit and one non-flagged exit are forced into the
    # same bidirectional dungeon so both groups remain mutually reachable.
    # To bridge a new region: append (condition, region_exits_list) below.
    bridges: list[tuple[bool, list[str]]] = [
        (discovery_off and not options.north_side_open.value, north_exits),
    ]
    active_bridges = [(cond, exits) for cond, exits in bridges if cond]
    if active_bridges:
        rng.shuffle(free_exits)
    for _, flagged_exits in active_bridges:
        bridge_dungeon = next(d for d in bidir_slots if len(bidir_slots[d]) >= 2)

        slot_a = rng.choice(bidir_slots[bridge_dungeon])
        bidir_slots[bridge_dungeon].remove(slot_a)
        flagged_pick = rng.choice([e for e in flagged_exits if e not in connections])
        _assign(world, flagged_pick, slot_a, connections)

        slot_b = rng.choice(bidir_slots[bridge_dungeon])
        bidir_slots[bridge_dungeon].remove(slot_b)
        other_pick = next(e for e in free_exits if e not in connections and e not in flagged_exits)
        _assign(world, other_pick, slot_b, connections)

    # === Phase 3: Assign all remaining exits to remaining slots ===
    remaining_slots: list[str] = [slot for slots in bidir_slots.values() for slot in slots]
    remaining_slots.extend(uni_slots)
    rng.shuffle(remaining_slots)

    for exit_name in free_exits:
        if exit_name in connections:
            continue
        try:
            _assign(world, exit_name, remaining_slots.pop(), connections)
        except IndexError:
            print(f"Failed on exit: {exit_name}")
            for line in world.entrance_spoiler:
                print(line)
            raise

    # === Build the bidirectional connection table ===
    # Each forward assignment (exit → dungeon region) implies a reverse assignment
    # (dungeon's outbound exit → the overworld region the connector came from).
    world.dungeon_connections = dict(connections)
    for exit_name, dungeon_region in connections.items():
        world.dungeon_connections[_DUNGEON_EXIT[dungeon_region]] = _CONNECTOR_SOURCE[exit_name]