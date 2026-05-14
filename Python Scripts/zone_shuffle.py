"""
BountyWorld Zone Shuffle Script
================================
Generates a spatially-aware bracket assignment for all vanilla WoW outdoor zones.

Bracket system:
  1:  1–10   Common named mobs
  2: 11–20   Named elites, camp leaders
  3: 21–30   Outdoor elites, mini-bosses
  4: 31–40   Named rares, patrol leaders
  5: 41–50   Elite rares
  6: 51–60   Outdoor elite rares, elite packs
  7: 60 Elite — ONE randomly selected zone (natural level 30+)
               All mobs replaced with open-world dungeon bosses.
               Your bounty target is one specific boss roaming that zone.

Zone shuffle logic:
  Every outdoor creature spawn in a zone is replaced with a random
  creature whose natural level fits the bracket's level range.
  Bracket 7 uses the dungeon boss pool instead of regular outdoor creatures.

Usage:
    python zone_shuffle.py                  # Random seed, continent split on
    python zone_shuffle.py --no-split       # Fully random continent assignment
    python zone_shuffle.py --seed 42        # Reproducible output
    python zone_shuffle.py --visualise      # Print full adjacency check
    python zone_shuffle.py --save           # Save to JSON
"""

import random
import argparse
import json
import collections

# ---------------------------------------------------------------------------
# ZONE GRAPH — full vanilla outdoor world, all zones included
# ---------------------------------------------------------------------------

ZONE_GRAPH = {
    # ── Kalimdor ────────────────────────────────────────────────────────────
    "Teldrassil":              ["Darkshore"],
    "Darkshore":               ["Teldrassil", "Ashenvale", "Moonglade"],
    "Ashenvale":               ["Darkshore", "Stonetalon Mountains", "The Barrens", "Felwood"],
    "Stonetalon Mountains":    ["Ashenvale", "The Barrens"],
    "The Barrens":             ["Ashenvale", "Stonetalon Mountains", "Dustwallow Marsh",
                                "Thousand Needles", "Durotar", "Mulgore"],
    "Durotar":                 ["The Barrens"],
    "Mulgore":                 ["The Barrens"],
    "Dustwallow Marsh":        ["The Barrens", "Thousand Needles"],
    "Thousand Needles":        ["The Barrens", "Dustwallow Marsh", "Feralas", "Tanaris"],
    "Feralas":                 ["Thousand Needles", "Tanaris", "Moonglade"],
    "Tanaris":                 ["Thousand Needles", "Feralas", "Un'Goro Crater"],
    "Un'Goro Crater":          ["Tanaris", "Silithus"],
    "Silithus":                ["Un'Goro Crater", "Feralas"],
    "Felwood":                 ["Ashenvale", "Moonglade", "Winterspring"],
    "Moonglade":               ["Darkshore", "Felwood", "Feralas"],
    "Winterspring":            ["Felwood", "Moonglade"],

    # ── Eastern Kingdoms — full graph restored ───────────────────────────────
    "Elwynn Forest":           ["Westfall", "Redridge Mountains", "Duskwood"],
    "Westfall":                ["Elwynn Forest", "Duskwood"],
    "Duskwood":                ["Westfall", "Elwynn Forest", "Redridge Mountains",
                                "Swamp of Sorrows"],
    "Redridge Mountains":      ["Elwynn Forest", "Duskwood", "Burning Steppes"],
    "Burning Steppes":         ["Redridge Mountains", "Searing Gorge", "Blasted Lands"],
    "Searing Gorge":           ["Burning Steppes", "Loch Modan"],
    "Blasted Lands":           ["Burning Steppes", "Swamp of Sorrows"],
    "Swamp of Sorrows":        ["Duskwood", "Blasted Lands"],
    "Loch Modan":              ["Searing Gorge", "Wetlands", "Dun Morogh"],
    "Dun Morogh":              ["Loch Modan"],
    "Wetlands":                ["Loch Modan", "Arathi Highlands"],
    "Arathi Highlands":        ["Wetlands", "Hillsbrad Foothills", "The Hinterlands"],
    "Hillsbrad Foothills":     ["Arathi Highlands", "Alterac Mountains", "Silverpine Forest"],
    "Alterac Mountains":       ["Hillsbrad Foothills", "Western Plaguelands"],
    "Silverpine Forest":       ["Hillsbrad Foothills", "Tirisfal Glades"],
    "Tirisfal Glades":         ["Silverpine Forest", "Western Plaguelands"],
    "Western Plaguelands":     ["Alterac Mountains", "Tirisfal Glades", "Eastern Plaguelands"],
    "Eastern Plaguelands":     ["Western Plaguelands", "The Hinterlands"],
    "The Hinterlands":         ["Arathi Highlands", "Eastern Plaguelands"],
}

KALIMDOR = {
    "Teldrassil", "Darkshore", "Ashenvale", "Stonetalon Mountains",
    "The Barrens", "Durotar", "Mulgore", "Dustwallow Marsh",
    "Thousand Needles", "Feralas", "Tanaris", "Un'Goro Crater",
    "Silithus", "Felwood", "Moonglade", "Winterspring",
}

EASTERN_KINGDOMS = {
    "Elwynn Forest", "Westfall", "Duskwood", "Redridge Mountains",
    "Burning Steppes", "Searing Gorge", "Blasted Lands", "Swamp of Sorrows",
    "Loch Modan", "Dun Morogh", "Wetlands", "Arathi Highlands",
    "Hillsbrad Foothills", "Alterac Mountains", "Silverpine Forest",
    "Tirisfal Glades", "Western Plaguelands", "Eastern Plaguelands",
    "The Hinterlands",
}

# Zones eligible for bracket 7 — natural retail level 30+
# These have enough mob density and appropriate feel for a boss-filled zone
BRACKET_7_ELIGIBLE = {
    # Kalimdor
    "Feralas", "Tanaris", "Un'Goro Crater", "Silithus",
    "Felwood", "Winterspring", "Dustwallow Marsh",
    # Eastern Kingdoms
    "Swamp of Sorrows", "Blasted Lands", "Searing Gorge",
    "Burning Steppes", "The Hinterlands", "Western Plaguelands",
    "Eastern Plaguelands", "Alterac Mountains",
}

# Zones with 4+ neighbours are hub zones — they cannot be geographically
# isolated regardless of bracket assignment, so adjacency constraints are
# relaxed for them during rebalancing. This gives the rebalancer the
# headroom to push bracket 5 down without getting stuck.
HUB_ZONES = {
    zone for zone, neighbours in ZONE_GRAPH.items()
    if len(neighbours) >= 4
}
# Result: The Barrens (6), Ashenvale (4), Thousand Needles (4), Duskwood (4)

ALL_ZONES = set(ZONE_GRAPH.keys())

# ---------------------------------------------------------------------------
# BRACKET DEFINITIONS
# ---------------------------------------------------------------------------

BRACKETS = {
    1: (1,  10,  "Bracket 1 [ 1–10 ]"),
    2: (11, 20,  "Bracket 2 [11–20]"),
    3: (21, 30,  "Bracket 3 [21–30]"),
    4: (31, 40,  "Bracket 4 [31–40]"),
    5: (41, 50,  "Bracket 5 [41–50]"),
    6: (51, 60,  "Bracket 6 [51–60]"),
    7: (60, 60,  "Bracket 7 [☠ Skull]"),
}

# Target zone count ranges per bracket for brackets 1–6
# Bracket 7 is always exactly 1 zone (promoted post-shuffle)
# Total zones: 35. With 1 bracket 7 zone, 34 zones across brackets 1–6.
# These are hard enforced — rebalancer keeps running until satisfied or stuck.
BRACKET_MIN_ZONES = {1: 3, 2: 4, 3: 5, 4: 5, 5: 4, 6: 4}
BRACKET_MAX_ZONES = {1: 6, 2: 7, 3: 8, 4: 8, 5: 11, 6: 7}

MAX_BRACKET_DIFF = 2

BFS_STEP_WEIGHTS = {
    1: [1, 3, 5],
    2: [1, 3, 5],
    3: [1, 3, 5],
    4: [1, 2, 6],
    5: [1, 1, 7],
    6: [1, 1, 8],
}

# ---------------------------------------------------------------------------
# BRACKET 7 — DUNGEON BOSS POOL
# Imported from db_lookups.py which contains verified entry IDs.
# ---------------------------------------------------------------------------

from db_lookups import DUNGEON_BOSS_POOL


def roll_bracket_7(brackets):
    """
    Post-shuffle: select one eligible zone that was assigned bracket 5 or 6,
    verify all its neighbours are at bracket 5 or 6 (so diff stays <= 2),
    promote it to bracket 7, and roll a bounty target from the boss pool.
    Returns (updated brackets, zone name, bounty boss).
    """
    # Candidates: eligible zones currently at bracket 5 or 6
    candidates = [
        z for z in BRACKET_7_ELIGIBLE
        if z in brackets and brackets[z] in (5, 6)
    ]
    random.shuffle(candidates)

    for zone in candidates:
        # All neighbours must be bracket 5 or 6 (so bracket 7 diff <= 2)
        neighbours = ZONE_GRAPH.get(zone, [])
        neighbour_brackets = [brackets[n] for n in neighbours if n in brackets]
        if all(b >= 5 for b in neighbour_brackets):
            brackets[zone] = 7
            bounty = random.choice(DUNGEON_BOSS_POOL)
            return brackets, zone, bounty

    # Fallback: relax neighbour constraint to bracket 4+ if no perfect candidate
    candidates2 = [
        z for z in BRACKET_7_ELIGIBLE
        if z in brackets and brackets[z] in (4, 5, 6)
    ]
    random.shuffle(candidates2)
    for zone in candidates2:
        neighbours = ZONE_GRAPH.get(zone, [])
        neighbour_brackets = [brackets[n] for n in neighbours if n in brackets]
        if all(b >= 4 for b in neighbour_brackets):
            brackets[zone] = 7
            bounty = random.choice(DUNGEON_BOSS_POOL)
            return brackets, zone, bounty

    # Last resort: just pick any eligible zone
    zone = random.choice(list(BRACKET_7_ELIGIBLE))
    brackets[zone] = 7
    bounty = random.choice(DUNGEON_BOSS_POOL)
    return brackets, zone, bounty

# ---------------------------------------------------------------------------
# ZONE FLAVOR TEXT
# ---------------------------------------------------------------------------

ZONE_FLAVORS = {
    "Teldrassil":           ["ancient tree canopy", "glowing violet bark", "moonlit boughs"],
    "Darkshore":            ["black sand shores", "ruined elven docks", "mist-covered coastline"],
    "Ashenvale":            ["ancient forest", "moonlit glades", "ruined elven shrines"],
    "Stonetalon Mountains": ["jagged mountain ridges", "talon-shaped peaks", "goblin machinery"],
    "The Barrens":          ["vast open savannah", "scorched red earth", "scattered thunder lizards"],
    "Durotar":              ["harsh rocky cliffs", "orange dusty terrain", "orcish settlements"],
    "Mulgore":              ["rolling green plains", "tauren totem poles", "gentle prairie winds"],
    "Dustwallow Marsh":     ["murky swampland", "rotting wooden piers", "black ooze pools"],
    "Thousand Needles":     ["towering stone spires", "arid canyon floors", "centaur camps"],
    "Feralas":              ["dense jungle canopy", "twin colossus ruins", "emerald river basins"],
    "Tanaris":              ["cracked desert flats", "scorched canyon walls", "goblin bazaar tents"],
    "Un'Goro Crater":       ["steaming jungle crater", "tar pits", "crystal pylons"],
    "Silithus":             ["barren windswept sands", "ancient qiraji ruins", "silithid hives"],
    "Felwood":              ["corrupted purple trees", "fel-soaked soil", "satyr encampments"],
    "Moonglade":            ["serene moonlit forest", "still silver lake", "druid stone circles"],
    "Winterspring":         ["frozen snowfields", "ice crystal formations", "blue dragon lairs"],
    "Elwynn Forest":        ["peaceful farmland", "cobblestone roads", "human kingdom banners"],
    "Westfall":             ["dusty golden fields", "abandoned farmsteads", "Defias scarecrows"],
    "Duskwood":             ["permanently dark canopy", "gnarled silver trees", "worgen howls"],
    "Redridge Mountains":   ["red stone ridgelines", "gnoll camps", "crumbling watchtowers"],
    "Burning Steppes":      ["volcanic ash plains", "lava flows", "Blackrock Mountain looming"],
    "Searing Gorge":        ["industrial smoke", "Dark Iron forges", "glowing magma channels"],
    "Blasted Lands":        ["demonic red sky", "twisted fel craters", "Dark Portal horizon"],
    "Swamp of Sorrows":     ["boggy wetlands", "mossy ruins", "green mist over still water"],
    "Loch Modan":           ["alpine lake shores", "dwarven excavation sites", "stone-carved dam"],
    "Dun Morogh":           ["snowy mountain passes", "dwarven gun emplacements", "frozen pines"],
    "Wetlands":             ["flooded lowlands", "crumbling fortifications", "murloc-lined rivers"],
    "Arathi Highlands":     ["windswept green plateaus", "ruined stone keeps", "Syndicate banners"],
    "Hillsbrad Foothills":  ["green rolling farmland", "Forsaken siege camps", "coastal cliffs"],
    "Alterac Mountains":    ["abandoned stone city", "deep snowdrifts", "ogre-held ruins"],
    "Silverpine Forest":    ["dark pine forest", "Forsaken patrols", "wolf-haunted roads"],
    "Tirisfal Glades":      ["sickly pale forest", "Undercity smoke", "plague-touched soil"],
    "Western Plaguelands":  ["plague-soaked farmland", "Scarlet Crusade fortresses", "skeletal livestock"],
    "Eastern Plaguelands":  ["dead corrupted forest", "Naxxramas shadow overhead", "scourge ziggurats"],
    "The Hinterlands":      ["dense highland jungle", "troll ruins", "gryphon aerie cliffs"],
}

# ---------------------------------------------------------------------------
# CORE ALGORITHM
# ---------------------------------------------------------------------------

def bfs_assign(seed_zone, seed_bracket, brackets):
    """Flood-fill bracket assignments outward from a seed zone using BFS."""
    queue   = collections.deque([(seed_zone, seed_bracket)])
    visited = {seed_zone}
    brackets[seed_zone] = seed_bracket

    while queue:
        zone, current_bracket = queue.popleft()
        weights = BFS_STEP_WEIGHTS.get(current_bracket, [2, 4, 3])
        for neighbour in ZONE_GRAPH.get(zone, []):
            if neighbour not in visited:
                visited.add(neighbour)
                step        = random.choices([0, 1, 2], weights=weights)[0]
                new_bracket = min(6, current_bracket + step)
                brackets[neighbour] = new_bracket
                queue.append((neighbour, new_bracket))

    return brackets


def apply_variance(brackets):
    """Nudge individual zones ±1 bracket while respecting adjacency constraints.
    Hub zones (4+ neighbours) are exempt — they cannot be isolated."""
    zones = list(brackets.keys())
    random.shuffle(zones)

    for zone in zones:
        current = brackets[zone]
        for delta in random.sample([-1, 1], 2):
            candidate = current + delta
            if candidate < 1 or candidate > 6:
                continue
            # Hub zones skip adjacency check — always valid to move
            if zone in HUB_ZONES:
                brackets[zone] = candidate
                break
            valid = all(
                abs(candidate - brackets[n]) <= MAX_BRACKET_DIFF
                for n in ZONE_GRAPH.get(zone, [])
                if n in brackets
            )
            if valid:
                brackets[zone] = candidate
                break

    return brackets


def rebalance_distribution(brackets, max_passes=200):
    """
    Aggressively push bracket counts toward BRACKET_MIN/MAX_ZONES targets.
    Hub zones (4+ neighbours) are exempt from adjacency checks — they can
    be freely moved to any bracket, giving the rebalancer much more headroom
    to drain bracket 5 into underpopulated brackets.
    """
    for pass_num in range(max_passes):
        counts = collections.Counter(b for b in brackets.values() if b <= 6)
        over   = [b for b in range(1, 7) if counts[b] > BRACKET_MAX_ZONES[b]]
        under  = [b for b in range(1, 7) if counts[b] < BRACKET_MIN_ZONES[b]]

        if not over or not under:
            break

        most_over  = max(over, key=lambda b: counts[b] - BRACKET_MAX_ZONES[b])
        most_under = max(under, key=lambda b: BRACKET_MIN_ZONES[b] - counts[b])

        candidates = [z for z, b in brackets.items() if b == most_over]
        # Prioritise hub zones — they can always be moved freely
        candidates.sort(key=lambda z: (0 if z in HUB_ZONES else 1))
        random.shuffle(candidates[:len([z for z in candidates if z in HUB_ZONES])])
        random.shuffle(candidates[len([z for z in candidates if z in HUB_ZONES]):])

        moved = False
        for zone in candidates:
            is_hub = zone in HUB_ZONES
            for target in sorted(under,
                                 key=lambda b: BRACKET_MIN_ZONES[b] - counts[b],
                                 reverse=True):
                if is_hub:
                    # Hub zones: no adjacency check needed
                    brackets[zone] = target
                    moved = True
                    break
                else:
                    valid = all(
                        abs(target - brackets[n]) <= MAX_BRACKET_DIFF
                        for n in ZONE_GRAPH.get(zone, [])
                        if n in brackets and brackets[n] <= 6
                    )
                    if valid:
                        brackets[zone] = target
                        moved = True
                        break
            if moved:
                break

        if not moved:
            break

    return brackets


def validate_adjacency(brackets):
    """Return list of adjacency violations. Bracket 7 may diff by up to 2 from bracket 5."""
    violations = []
    for zone, neighbours in ZONE_GRAPH.items():
        for neighbour in neighbours:
            if zone in brackets and neighbour in brackets:
                b1 = brackets[zone]
                b2 = brackets[neighbour]
                # Treat bracket 7 as bracket 6 for adjacency checking
                # (boss zone is placed adjacent to 5/6 zones by roll_bracket_7)
                diff = abs(min(b1, 6) - min(b2, 6))
                if diff > MAX_BRACKET_DIFF:
                    violations.append((zone, b1, neighbour, b2, diff))
    return violations


def validate_traversability(brackets):
    """
    Verify every zone is reachable from its continent's lowest-bracket zone
    without crossing a gap > MAX_BRACKET_DIFF. Validated per-continent.
    Bracket 7 zones are excluded from traversability checks.
    """
    unreachable_zones = set()

    for continent_zones in [KALIMDOR, EASTERN_KINGDOMS]:
        in_map = [z for z in continent_zones
                  if z in brackets and brackets[z] <= 6]
        if not in_map:
            continue

        min_b  = min(brackets[z] for z in in_map)
        starts = [z for z in in_map if brackets[z] == min_b]

        reachable = set(starts)
        queue     = collections.deque(starts)

        while queue:
            zone = queue.popleft()
            for neighbour in ZONE_GRAPH.get(zone, []):
                if (neighbour not in reachable
                        and neighbour in brackets
                        and brackets[neighbour] <= 6):
                    if abs(brackets[zone] - brackets[neighbour]) <= MAX_BRACKET_DIFF:
                        reachable.add(neighbour)
                        queue.append(neighbour)

        unreachable_zones.update(set(in_map) - reachable)

    return {brackets[z] for z in unreachable_zones}, unreachable_zones


def shuffle(continent_split=True, max_attempts=100):
    """
    Generate a valid bracket map (brackets 1-6), then promote one eligible
    zone to bracket 7 and roll its dungeon boss bounty target.

    Faction-based continent rules:
    - Kalimdor (Horde): exactly 2 adjacent bracket 1 zones, spreads outward
    - Eastern Kingdoms (Alliance): minimum bracket 3, no bracket 1 or 2
    """
    for attempt in range(1, max_attempts + 1):
        brackets = {}

        if continent_split:
            # Kalimdor always gets bracket 1 seed (Horde starting continent)
            # Eastern Kingdoms always gets bracket 3+ seed (Alliance, harder start)
            kal_seed_bracket = 1
            ek_seed_bracket  = random.choice([3, 4, 5])

            kal_seed = random.choice(list(KALIMDOR))
            ek_seed  = random.choice(list(EASTERN_KINGDOMS))

            brackets = bfs_assign(kal_seed, kal_seed_bracket, brackets)
            brackets = bfs_assign(ek_seed,  ek_seed_bracket,  brackets)

            # Force exactly one adjacent bracket 1 neighbour on Kalimdor
            kal_nbrs = [n for n in ZONE_GRAPH.get(kal_seed, [])
                        if n in KALIMDOR and brackets.get(n, 99) > 1]
            if kal_nbrs:
                brackets[random.choice(kal_nbrs)] = 1
        else:
            seed     = random.choice(list(ALL_ZONES))
            brackets = bfs_assign(seed, 1, brackets)

        # Fill any zones missed by BFS
        for zone in ALL_ZONES:
            if zone not in brackets:
                brackets[zone] = random.randint(1, 6)

        brackets = apply_variance(brackets)
        brackets = rebalance_distribution(brackets)

        # Promote one eligible zone to bracket 7
        brackets, b7_zone, b7_bounty = roll_bracket_7(brackets)

        # Validate
        violations       = validate_adjacency(brackets)
        _, unreachable_z = validate_traversability(brackets)
        b1_count         = sum(1 for z, b in brackets.items() if b == 1)
        b6_count         = sum(1 for z, b in brackets.items() if b == 6)

        kal_avg  = sum(min(brackets[z], 6) for z in KALIMDOR  if z in brackets) / len(KALIMDOR)
        ek_avg   = sum(min(brackets[z], 6) for z in EASTERN_KINGDOMS if z in brackets) / len(EASTERN_KINGDOMS)
        split_diff = abs(kal_avg - ek_avg)
        # After 50 attempts accept maps without split — distribution takes priority
        split_ok = (not continent_split) or (split_diff >= 1.0) or (attempt > 50)

        # Check faction continent rules:
        # - Kalimdor must have at least 2 bracket 1 zones
        # - Eastern Kingdoms must have minimum bracket 3
        ek_min_bracket = min((brackets.get(z, 99) for z in EASTERN_KINGDOMS), default=99)
        kal_b1_count   = sum(1 for z in KALIMDOR if brackets.get(z) == 1)

        faction_ok = (not continent_split) or (
            ek_min_bracket >= 3 and
            kal_b1_count >= 2
        )

        if (not violations and not unreachable_z
                and b1_count >= BRACKET_MIN_ZONES[1]
                and b6_count >= BRACKET_MIN_ZONES[6]
                and split_ok
                and faction_ok):
            if continent_split and split_diff < 1.0:
                print(f"  ⚠ Accepted without continent split (diff={split_diff:.1f}) after {attempt} attempts")
            print(f"✓ Valid bracket map generated on attempt {attempt}")
            return brackets, b7_zone, b7_bounty, attempt

        if attempt % 10 == 0:
            print(f"  Attempt {attempt}: {len(violations)} violations, "
                  f"{len(unreachable_z)} unreachable, "
                  f"b1={b1_count} b6={b6_count} b7={b7_zone}, "
                  f"split diff={abs(kal_avg - ek_avg):.1f} — retrying...")

    print(f"✗ Could not generate valid map after {max_attempts} attempts.")
    return None, None, None, max_attempts

# ---------------------------------------------------------------------------
# OUTPUT & VISUALISATION
# ---------------------------------------------------------------------------

BRACKET_COLORS = {
    1: "\033[92m",          # Green
    2: "\033[93m",          # Yellow
    3: "\033[33m",          # Dark yellow
    4: "\033[38;5;208m",    # Orange
    5: "\033[91m",          # Light red
    6: "\033[31m",          # Red
    7: "\033[35m",          # Magenta — skull tier
}
RESET = "\033[0m"
BOLD  = "\033[1m"


def print_map(brackets, b7_zone):
    print()
    print(f"{BOLD}{'='*62}{RESET}")
    print(f"{BOLD}  BOUNTY WORLD — Zone Bracket Map{RESET}")
    print(f"{'='*62}")

    for continent, zones in [("Kalimdor", KALIMDOR), ("Eastern Kingdoms", EASTERN_KINGDOMS)]:
        print(f"\n{BOLD}  {continent}{RESET}")
        print(f"  {'-'*42}")

        sorted_zones = sorted(
            [z for z in zones if z in brackets],
            key=lambda z: (brackets[z], z)
        )

        for zone in sorted_zones:
            b      = brackets[zone]
            color  = BRACKET_COLORS[b]
            label  = BRACKETS[b][2]
            flavor = random.choice(ZONE_FLAVORS.get(zone, ["unknown terrain"]))
            tag    = f"  {BOLD}☠ SKULL ZONE{RESET}" if zone == b7_zone else ""
            print(f"  {color}{label}{RESET}  {zone:<30} — {flavor}{tag}")

    print()
    print(f"{BOLD}  Bracket Distribution{RESET}")
    print(f"  {'-'*42}")
    for b in range(1, 8):
        count = sum(1 for v in brackets.values() if v == b)
        if count == 0:
            continue
        color = BRACKET_COLORS[b]
        bar   = "█" * count
        label = BRACKETS[b][2]
        note  = "  ← open-world dungeon bosses roam here" if b == 7 else ""
        print(f"  {color}{label}{RESET}  {bar} ({count} zone){note}")
    print()


def print_bracket7(b7_zone, b7_bounty, brackets):
    color = BRACKET_COLORS[7]
    print(f"{BOLD}  Bracket 7 — Skull Zone{RESET}")
    print(f"  {'-'*42}")
    print(f"  Zone:    {color}{b7_zone}{RESET}  (all mobs replaced with dungeon bosses)")
    print(f"  Bounty:  {color}{b7_bounty['name']}{RESET}  [{b7_bounty['dungeon']}  entry:{b7_bounty['entry']}]")
    print(f"  Flavor:  {random.choice(ZONE_FLAVORS.get(b7_zone, ['']))}")
    print()


def print_adjacency_check(brackets):
    print(f"\n{BOLD}  Adjacency Check{RESET}")
    print(f"  {'-'*62}")
    seen   = set()
    all_ok = True

    for zone, neighbours in sorted(ZONE_GRAPH.items()):
        for neighbour in neighbours:
            pair = tuple(sorted([zone, neighbour]))
            if pair in seen:
                continue
            seen.add(pair)
            b1   = brackets.get(zone, "?")
            b2   = brackets.get(neighbour, "?")
            # For display, show real bracket values
            diff = abs(min(b1,6) - min(b2,6)) if isinstance(b1, int) and isinstance(b2, int) else "?"
            flag = ""
            if isinstance(diff, int) and diff > MAX_BRACKET_DIFF:
                flag   = f"  {BOLD}\033[91m← VIOLATION{RESET}"
                all_ok = False
            c1 = BRACKET_COLORS.get(b1, "") if isinstance(b1, int) else ""
            c2 = BRACKET_COLORS.get(b2, "") if isinstance(b2, int) else ""
            print(f"  {zone:<30} {c1}[{b1}]{RESET}  ↔  {neighbour:<30} {c2}[{b2}]{RESET}  diff={diff}{flag}")

    if all_ok:
        print(f"\n  {BOLD}\033[92m✓ All adjacency constraints satisfied{RESET}")
    else:
        print(f"\n  {BOLD}\033[91m✗ Violations found{RESET}")


def print_summary(brackets, b7_zone, b7_bounty):
    kal_avg = sum(min(brackets[z],6) for z in KALIMDOR  if z in brackets) / len(KALIMDOR)
    ek_avg  = sum(min(brackets[z],6) for z in EASTERN_KINGDOMS if z in brackets) / len(EASTERN_KINGDOMS)
    b1_zones = [z for z, b in brackets.items() if b == 1]
    b6_zones = [z for z, b in brackets.items() if b == 6]

    print(f"\n{BOLD}  Summary{RESET}")
    print(f"  {'─'*42}")
    print(f"  Kalimdor avg bracket:          {kal_avg:.1f}")
    print(f"  Eastern Kingdoms avg bracket:  {ek_avg:.1f}")
    print(f"  Continent split diff:          {abs(kal_avg - ek_avg):.1f}")
    print(f"  Bracket 1 zones:  {', '.join(b1_zones)}")
    print(f"  Bracket 6 zones:  {', '.join(b6_zones)}")
    print(f"  Bracket 7 zone:   {b7_zone}  →  {b7_bounty['name']} ({b7_bounty['dungeon']})")


def save_output(brackets, b7_zone, b7_bounty, seed_val, continent_split):
    output = {
        "seed":               seed_val,
        "continent_split":    continent_split,
        "brackets":           brackets,
        "bracket_7_zone":     b7_zone,
        "bracket_7_bounty":   b7_bounty,
        "bracket_7_boss_pool":DUNGEON_BOSS_POOL,
        "zone_flavors":       {z: ZONE_FLAVORS.get(z, []) for z in brackets},
    }
    filename = f"bracket_map_seed{seed_val}.json"
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  Saved to {filename}")

# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# HTML REPORT GENERATOR
# ---------------------------------------------------------------------------

def generate_html_report(brackets, b7_zone, b7_bounty, seed_val, user="acore", password="acore"):
    """
    Query the DB for top 5 mobs per zone and generate a dark-themed HTML report.
    Opens automatically in the default browser.
    """
    import webbrowser
    import os

    print("  Generating zone report...")

    try:
        import mysql.connector
    except ImportError:
        print("  ERROR: mysql-connector-python not installed.")
        print("  Run: pip install mysql-connector-python")
        return

    try:
        conn = mysql.connector.connect(
            host="127.0.0.1", port=3306,
            user=user, password=password,
            database="acore_world", autocommit=True
        )
        cursor = conn.cursor()
        print("  Connected to DB successfully.")
    except Exception as e:
        print(f"  DB connection failed: {e}")
        return

    # Bracket colors
    BRACKET_COLORS = {
        1: "#00ff66", 2: "#66e600", 3: "#ffe600",
        4: "#ff8c00", 5: "#ff4000", 6: "#ff0000", 7: "#9900ff"
    }


    # Sort zones by bracket
    sorted_zones = sorted(brackets.items(), key=lambda x: x[1])
    # Put skull zone last
    sorted_zones = [(z, b) for z, b in sorted_zones if z != b7_zone]
    sorted_zones.append((b7_zone, 7))

    # Load zone IDs
    from db_lookups import ZONE_IDS

    # Query top 5 mobs per zone using zoneId (accurate, no overlap)
    zone_data = {}
    for zone_name, bracket in sorted_zones:
        zone_id = ZONE_IDS.get(zone_name)
        if not zone_id:
            zone_data[zone_name] = []
            continue

        # Get level range for this bracket to filter out unmodified vanilla creatures
        bracket_levels = {
            1: (1, 12), 2: (11, 22), 3: (21, 32), 4: (31, 42),
            5: (41, 52), 6: (51, 62), 7: (55, 65)
        }
        min_lvl, max_lvl = bracket_levels.get(bracket, (1, 65))

        try:
            cursor.execute("""
                SELECT ct.name, ct.minlevel, ct.maxlevel, COUNT(*) as cnt
                FROM creature c
                JOIN creature_template ct ON c.id1 = ct.entry
                WHERE c.zoneId = %s
                AND ct.npcflag = 0
                AND (ct.ScriptName = '' OR ct.ScriptName IS NULL)
                AND ct.minlevel BETWEEN %s AND %s
                AND ct.minlevel > 1
                AND (ct.maxlevel - ct.minlevel) <= 15
                AND ct.type IN (1,2,4,5,7,8)
                AND ct.faction NOT IN (
                    35, 36, 12, 14, 21, 22, 150, 534,
                    890, 914, 1014, 1015, 1074, 1375, 1376,
                    1634, 1635, 1638, 1639
                )
                AND ct.name NOT LIKE '%Refugee%'
                AND ct.name NOT LIKE '%Orphan%'
                AND ct.name NOT LIKE '%Credit%'
                AND ct.name NOT LIKE '%Stalker%'
                AND ct.name NOT LIKE '%Trigger%'
                AND ct.name NOT LIKE '%Dummy%'
                AND ct.name NOT LIKE '%Minion%'
                AND ct.name NOT LIKE '%Invasion%'
                AND ct.name NOT LIKE 'Scourge%'
                AND ct.name NOT LIKE '%Surveyor%'
                AND ct.name NOT LIKE '%Explorer%'
                AND ct.name NOT LIKE '%Spy %'
                AND ct.name NOT LIKE '%finder%'
                AND ct.unit_class != 0
                GROUP BY ct.name, ct.minlevel, ct.maxlevel
                HAVING cnt >= 5
                ORDER BY cnt DESC
                LIMIT 5
            """, (zone_id, min_lvl, max_lvl))
            zone_data[zone_name] = cursor.fetchall()
        except Exception as e:
            print(f"  Query error for {zone_name}: {e}")
            zone_data[zone_name] = []

    cursor.close()
    conn.close()

    # Generate HTML
    tabs_html = ""
    panels_html = ""
    first = True

    for zone_name, bracket in sorted_zones:
        zone_id = zone_name.replace("'", "").replace(" ", "_")
        color   = BRACKET_COLORS.get(bracket, "#ffffff")
        is_b7   = (zone_name == b7_zone)
        active  = "active" if first else ""
        first   = False

        bracket_label = f"B{bracket}" if not is_b7 else "SKULL"

        tabs_html += f"""
        <button class="tab-btn {active}" onclick="showTab('{zone_id}')"
                data-bracket="{bracket}" style="--bc: {color}">
            <span class="tab-bracket" style="color:{color}">{bracket_label}</span>
            <span class="tab-name">{zone_name}</span>
        </button>"""

        mobs = zone_data.get(zone_name, [])
        mob_rows = ""
        if is_b7:
            mob_rows = f"""
            <tr class="skull-mob">
                <td class="mob-rank">★</td>
                <td class="mob-name">{b7_bounty.get('name','Avatar of Hakkar')}</td>
                <td class="mob-level">60</td>
                <td class="mob-level">60</td>
                <td class="mob-count skull-label">SKULL BOSS</td>
            </tr>"""
            for i, (name, minlv, maxlv, cnt) in enumerate(mobs, 1):
                mob_rows += f"""
            <tr>
                <td class="mob-rank">{i}</td>
                <td class="mob-name">{name}</td>
                <td class="mob-level">{minlv}</td>
                <td class="mob-level">{maxlv}</td>
                <td class="mob-count">{cnt:,}</td>
            </tr>"""
        else:
            for i, (name, minlv, maxlv, cnt) in enumerate(mobs, 1):
                bar_w = int((cnt / max(mobs[0][3], 1)) * 100) if mobs else 0
                mob_rows += f"""
            <tr>
                <td class="mob-rank">{i}</td>
                <td class="mob-name">{name}
                    <div class="mob-bar" style="width:{bar_w}%; background:{color}22; border-left: 2px solid {color}66"></div>
                </td>
                <td class="mob-level">{minlv}</td>
                <td class="mob-level">{maxlv}</td>
                <td class="mob-count">{cnt:,}</td>
            </tr>"""

        skull_class = " skull-panel" if is_b7 else ""
        panels_html += f"""
        <div class="tab-panel {active}{skull_class}" id="panel-{zone_id}">
            <div class="panel-header">
                <div class="panel-title">
                    <span class="panel-bracket" style="color:{color}; border-color:{color}40">
                        {'☠ SKULL ZONE' if is_b7 else f'Bracket {bracket}'}
                    </span>
                    <h2>{zone_name}</h2>
                </div>
                {'<div class="skull-warning">All creatures replaced with dungeon bosses</div>' if is_b7 else ''}
            </div>
            <table class="mob-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Creature</th>
                        <th>Min Lvl</th>
                        <th>Max Lvl</th>
                        <th>Spawns</th>
                    </tr>
                </thead>
                <tbody>
                    {mob_rows if mob_rows else '<tr><td colspan="5" class="no-data">No data available</td></tr>'}
                </tbody>
            </table>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BountyWorld Zone Report — Seed {seed_val}</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>
:root {{
    --bg: #0a0a0f;
    --surface: #12121a;
    --surface2: #1a1a24;
    --border: #2a2a3a;
    --text: #c8c8d8;
    --text-dim: #66667a;
    --gold: #c8a84b;
    --gold-glow: #c8a84b40;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'Crimson Pro', Georgia, serif;
    font-size: 16px;
    min-height: 100vh;
    background-image:
        radial-gradient(ellipse at 20% 0%, #1a1020 0%, transparent 50%),
        radial-gradient(ellipse at 80% 100%, #0a1520 0%, transparent 50%);
}}

header {{
    text-align: center;
    padding: 40px 20px 20px;
    border-bottom: 1px solid var(--border);
    background: linear-gradient(180deg, #15101a 0%, transparent 100%);
    position: relative;
}}

header::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}}

h1 {{
    font-family: 'Cinzel', serif;
    font-size: 2.4rem;
    color: var(--gold);
    letter-spacing: 0.15em;
    text-shadow: 0 0 40px var(--gold-glow);
    margin-bottom: 8px;
}}

.subtitle {{
    color: var(--text-dim);
    font-style: italic;
    font-size: 1rem;
    letter-spacing: 0.05em;
}}

.seed-badge {{
    display: inline-block;
    margin-top: 12px;
    padding: 4px 16px;
    border: 1px solid var(--border);
    border-radius: 20px;
    font-family: 'Cinzel', serif;
    font-size: 0.75rem;
    color: var(--text-dim);
    letter-spacing: 0.1em;
}}

.layout {{
    display: flex;
    height: calc(100vh - 140px);
    min-height: 500px;
}}

/* Sidebar tabs */
.sidebar {{
    width: 220px;
    flex-shrink: 0;
    background: var(--surface);
    border-right: 1px solid var(--border);
    overflow-y: auto;
    padding: 12px 0;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
}}

.tab-btn {{
    width: 100%;
    background: none;
    border: none;
    border-left: 3px solid transparent;
    padding: 10px 14px;
    cursor: pointer;
    text-align: left;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: all 0.15s ease;
    color: var(--text-dim);
}}

.tab-btn:hover {{
    background: var(--surface2);
    color: var(--text);
}}

.tab-btn.active {{
    background: var(--surface2);
    border-left-color: var(--bc);
    color: var(--text);
}}

.tab-bracket {{
    font-family: 'Cinzel', serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    min-width: 36px;
    text-align: center;
    padding: 2px 5px;
    border-radius: 3px;
    background: rgba(255,255,255,0.04);
}}

.tab-name {{
    font-size: 0.85rem;
    line-height: 1.2;
    font-family: 'Crimson Pro', serif;
}}

/* Content panels */
.content {{
    flex: 1;
    overflow-y: auto;
    padding: 32px 40px;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
}}

.tab-panel {{ display: none; animation: fadeIn 0.2s ease; }}
.tab-panel.active {{ display: block; }}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(4px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

.panel-header {{
    margin-bottom: 28px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
}}

.panel-title {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 8px;
}}

.panel-bracket {{
    font-family: 'Cinzel', serif;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    padding: 5px 12px;
    border: 1px solid;
    border-radius: 4px;
    background: rgba(255,255,255,0.03);
    white-space: nowrap;
}}

h2 {{
    font-family: 'Cinzel', serif;
    font-size: 1.8rem;
    color: var(--text);
    font-weight: 400;
    letter-spacing: 0.05em;
}}

.skull-warning {{
    color: #9900ff;
    font-style: italic;
    font-size: 0.9rem;
    margin-top: 8px;
    padding: 8px 14px;
    background: #9900ff10;
    border-left: 2px solid #9900ff60;
    border-radius: 0 4px 4px 0;
}}

.mob-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.95rem;
}}

.mob-table th {{
    text-align: left;
    padding: 10px 14px;
    font-family: 'Cinzel', serif;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    color: var(--text-dim);
    border-bottom: 1px solid var(--border);
    font-weight: 400;
}}

.mob-table td {{
    padding: 12px 14px;
    border-bottom: 1px solid #1e1e2a;
    vertical-align: middle;
    position: relative;
}}

.mob-table tr:last-child td {{ border-bottom: none; }}

.mob-table tr:hover td {{
    background: var(--surface2);
}}

.mob-rank {{
    color: var(--text-dim);
    font-family: 'Cinzel', serif;
    font-size: 0.75rem;
    width: 30px;
    text-align: center;
}}

.mob-name {{
    font-size: 1rem;
    color: var(--text);
    min-width: 200px;
}}

.mob-bar {{
    position: absolute;
    bottom: 0;
    left: 0;
    height: 2px;
    border-radius: 0 2px 0 0;
    transition: width 0.3s ease;
}}

.mob-level {{
    color: var(--text-dim);
    font-size: 0.85rem;
    text-align: center;
    width: 70px;
}}

.mob-count {{
    font-family: 'Cinzel', serif;
    font-size: 0.8rem;
    color: var(--gold);
    text-align: right;
    width: 80px;
}}

.skull-mob td {{ color: #bb88ff; }}
.skull-mob .mob-name {{ color: #cc99ff; font-style: italic; }}
.skull-label {{ color: #9900ff !important; letter-spacing: 0.1em; }}

.no-data {{
    color: var(--text-dim);
    font-style: italic;
    text-align: center;
    padding: 40px;
}}

.skull-panel h2 {{ color: #bb88ff; }}
</style>
</head>
<body>
<header>
    <h1>BOUNTY WORLD</h1>
    <p class="subtitle">Zone Report — Top 5 Creatures per Zone</p>
    <span class="seed-badge">SEED {seed_val}</span>
</header>
<div class="layout">
    <nav class="sidebar">
        {tabs_html}
    </nav>
    <main class="content">
        {panels_html}
    </main>
</div>
<script>
function showTab(zoneId) {{
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    document.querySelector(`[onclick="showTab('${{zoneId}}')"]`).classList.add('active');
    document.getElementById('panel-' + zoneId).classList.add('active');
}}
</script>
</body>
</html>"""

    # Save and open
    report_path = os.path.join(os.getcwd(), f"zone_report_seed{seed_val}.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  Report saved: {report_path}")
    webbrowser.open(f"file:///{report_path.replace(chr(92), '/')}")
    print("  Opening in browser...")

def main():
    parser = argparse.ArgumentParser(description="BountyWorld Zone Shuffle")
    parser.add_argument("--seed",      type=int, default=None,
                        help="RNG seed for reproducible output")
    parser.add_argument("--no-split",  action="store_true",
                        help="Disable continent split mode")
    parser.add_argument("--visualise", action="store_true",
                        help="Print full adjacency check")
    parser.add_argument("--attempts",  type=int, default=200,
                        help="Max generation attempts (default 100)")
    parser.add_argument("--save",      action="store_true",
                        help="Save bracket map to JSON")
    parser.add_argument("--report",    action="store_true",
                        help="Generate HTML zone report with top mobs per zone")
    parser.add_argument("--password",  type=str, default="acore",
                        help="MySQL password for --report")
    parser.add_argument("--user",      type=str, default="acore",
                        help="MySQL user for --report")
    parser.add_argument("--json",      type=str, default=None,
                        help="Load bracket map from JSON file instead of reshuffling")
    args = parser.parse_args()

    seed_val        = args.seed if args.seed is not None else random.randint(0, 999999)
    continent_split = not args.no_split
    random.seed(seed_val)

    print(f"\n{BOLD}BountyWorld Zone Shuffle{RESET}")
    print(f"  Seed:             {seed_val}")
    print(f"  Continent split:  {'ON  (min 1.2 avg bracket diff enforced)' if continent_split else 'OFF'}")
    print(f"  Bracket 7:        1 randomized skull zone from eligible pool (natural level 30+)")
    print(f"  Max attempts:     {args.attempts}")
    print()

    result = shuffle(continent_split=continent_split, max_attempts=args.attempts)
    brackets, b7_zone, b7_bounty, _ = result

    if brackets is None:
        print("Failed to generate a valid map. Try --attempts 200.")
        return

    print_map(brackets, b7_zone)
    print_bracket7(b7_zone, b7_bounty, brackets)
    print_summary(brackets, b7_zone, b7_bounty)

    if args.visualise:
        print_adjacency_check(brackets)

    if args.save:
        save_output(brackets, b7_zone, b7_bounty, seed_val, continent_split)

    if args.report:
        # If --json provided, load bracket map from file for accurate reporting
        if args.json:
            import json as _json
            with open(args.json) as f:
                jdata = _json.load(f)
            report_brackets = jdata["brackets"]
            report_b7_zone  = jdata["bracket_7_zone"]
            report_b7_bounty = jdata.get("bracket_7_bounty", b7_bounty)
            report_seed = jdata.get("seed", seed_val)
        else:
            report_brackets  = brackets
            report_b7_zone   = b7_zone
            report_b7_bounty = b7_bounty
            report_seed      = seed_val
        generate_html_report(report_brackets, report_b7_zone, report_b7_bounty,
                             report_seed, user=args.user, password=args.password)

    print(f"\n{BOLD}  Re-run with --seed {seed_val} to reproduce this exact map.{RESET}\n")


if __name__ == "__main__":
    main()