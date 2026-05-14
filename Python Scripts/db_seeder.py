"""
BountyWorld — DB Seeder
========================
Reads the bracket map JSON from zone_shuffle.py and applies creature
replacements to the AzerothCore world database.

For each zone:
  1. Finds all outdoor creature spawns using coordinate bounding boxes
  2. Replaces each spawn's creature entry (id1) with a random creature
     from the bracket's creature pool
  3. Bracket 7 zones get dungeon bosses from DUNGEON_BOSS_POOL instead

Usage:
    python db_seeder.py --json bracket_map_seed12345.json --dry-run
    python db_seeder.py --json bracket_map_seed12345.json --apply

ALWAYS run with --dry-run first to verify the changes before applying.
ALWAYS back up your database before running with --apply:
    mysqldump -u root -p acore_world > backup_before_shuffle.sql
"""

import json
import random
import argparse
import mysql.connector
from db_lookups import (
    ZONE_IDS, BRACKET_CREATURES, DUNGEON_BOSS_POOL,
    BRACKET_7_ALL_ENTRIES, ZONE_CONTINENT, MAP_IDS
)

# ---------------------------------------------------------------------------
# ZONE BOUNDING BOXES
# Format: zone_name: (map_id, min_x, max_x, min_y, max_y)
# Coordinates verified against in-game WoW vanilla map boundaries.
# These are conservative — they stay well within zone borders to avoid
# replacing creatures in neighbouring zones.
#
# WoW coordinate system on Kalimdor/EK:
#   X increases going south, decreases going north
#   Y increases going west, decreases going east
# ---------------------------------------------------------------------------

ZONE_BOUNDS = {
    # ── Kalimdor (map=1) ────────────────────────────────────────────────────
    # Verified against actual DB creature counts - all produce sensible numbers
    "Teldrassil":           (1,  8000, 10500,  -700,  2200),   # 991 creatures
    "Darkshore":            (1,  4500,  7200,  -700,  3000),   # 870 creatures
    "Ashenvale":            (1,  1500,  5000, -4200,  -800),   # 1257 creatures
    "Stonetalon Mountains": (1, -1200,  1800, -3200,  -800),   # 1686 creatures
    "The Barrens":          (1, -1800,  1200, -5000,  -900),   # 2869 creatures
    "Durotar":              (1, -1200,   800, -5600, -3000),   # tightened south only
    "Mulgore":              (1, -2900,  -400, -3000,  -200),   # 1565 creatures
    "Dustwallow Marsh":     (1, -3800, -2600, -4400, -2800),   # 844 creatures
    "Thousand Needles":     (1, -4900, -3800, -5000, -3200),   # 705 creatures
    "Feralas":              (1, -5400, -4900, -4200, -1000),   # 1889 creatures
    "Tanaris":              (1, -8500, -6100, -5200, -3000),   # 1016 creatures
    "Un'Goro Crater":       (1, -7800, -5700, -1800,   800),   # 672 creatures
    "Silithus":             (1, -9400, -7600,   400,  2900),   # 247 creatures
    "Felwood":              (1,  3500,  6600, -1200,  1700),   # 1314 creatures
    "Moonglade":            (1,  5000,  7400,  -700,   800),   # 643 creatures
    "Winterspring":         (1,  5100,  9100, -3500,   200),   # 927 creatures

    # ── Eastern Kingdoms (map=0) ─────────────────────────────────────────────
    "Elwynn Forest":        (0, -9700, -8000,  -900,   700),   # 1804 creatures
    "Westfall":             (0,-11400, -9500, -2100,  -100),   # 970 creatures
    "Duskwood":             (0,-11000, -9000, -3700, -1700),   # 331 creatures
    "Redridge Mountains":   (0, -9500, -8000, -2300,  -700),   # 532 creatures
    "Burning Steppes":      (0, -9000, -7300, -2700, -1200),   # 457 creatures
    "Searing Gorge":        (0, -8200, -6700, -2500,  -800),   # 511 creatures
    "Blasted Lands":        (0,-12000,-10200, -3700, -2100),   # 508 creatures
    "Swamp of Sorrows":     (0,-11000, -9200, -3900, -2400),   # ~710 creatures
    "Loch Modan":           (0, -6300, -4700, -3200, -1500),   # 401 creatures
    "Dun Morogh":           (0, -6600, -4300, -1500,   900),   # 1605 creatures
    "Wetlands":             (0, -4600, -2500, -2300,  -600),   # 713 creatures
    "Arathi Highlands":     (0, -2500,  -200, -3600, -1500),   # 643 creatures
    "Hillsbrad Foothills":  (0,  -600,  1800, -3000,  -800),   # 631 creatures
    "Alterac Mountains":    (0,   200,  2100, -2200,  -500),   # 574 creatures
    "Silverpine Forest":    (0,   400,  1500,  -900,  1500),   # split from Tirisfal at x=1500
    "Tirisfal Glades":      (0,  1500,  4000,  -400,  1600),   # 2028 - Tirisfal starts at x=1500
    "Western Plaguelands":  (0,  2200,  5000, -1500,   500),   # 767 creatures
    "Eastern Plaguelands":  (0,  2400,  5400, -3400,  -900),   # 266 creatures
    "The Hinterlands":      (0,  -700,  2200, -5100, -2700),   # 605 creatures
}

# ---------------------------------------------------------------------------
# DB CONNECTION
# ---------------------------------------------------------------------------

def connect(host, port, user, password, database):
    return mysql.connector.connect(
        host=host, port=port,
        user=user, password=password,
        database=database,
        autocommit=False
    )

# ---------------------------------------------------------------------------
# CORE SEEDER LOGIC
# ---------------------------------------------------------------------------

def get_creatures_in_zone(cursor, zone_name, is_bracket_7=False, claimed_guids=None):
    """
    Fetch all creature GUIDs for a zone using the zoneId field.
    Accurate - no bounding box overlaps possible.
    """
    from db_lookups import ZONE_IDS
    zone_id = ZONE_IDS.get(zone_name)

    if not zone_id:
        print(f"    No zone ID found for {zone_name}")
        return []

    cursor.execute("""
        SELECT c.guid, c.id1, ct.name, ct.minlevel, ct.maxlevel
        FROM creature c
        JOIN creature_template ct ON c.id1 = ct.entry
        WHERE c.zoneId = %s
          AND ct.npcflag = 0
          AND ct.unit_class != 0
          AND ct.type IN (1,2,4,5,7,8)
          AND ct.minlevel > 0
          AND (ct.ScriptName = '' OR ct.ScriptName IS NULL)
          AND ct.faction NOT IN (
              35, 36, 12, 14, 21, 22, 150, 534,
              890, 914, 1014, 1015, 1074, 1375, 1376,
              1634, 1635, 1638, 1639
          )
          AND ct.name NOT LIKE '%Refugee%'
          AND ct.name NOT LIKE '%Civilian%'
          AND ct.name NOT LIKE '%Peasant%'
          AND ct.name NOT LIKE '%Orphan%'
          AND ct.name NOT LIKE '%Dummy%'
          AND ct.name NOT LIKE '%Trigger%'
          AND ct.name NOT LIKE '%Invisible%'
          AND ct.name NOT LIKE '%Farmhand%'
          AND ct.name NOT LIKE '%Farmer%'
          AND ct.name NOT LIKE 'Guard %%'
          AND ct.name NOT LIKE '%Wisp%'
          AND ct.name NOT LIKE '%Kid%'
          AND ct.name NOT LIKE '%Child%'
          AND ct.name NOT LIKE '%Baby%'
          AND ct.name NOT LIKE '%Survivor%'
          AND ct.name NOT LIKE '%Explorer%'
          AND ct.name NOT LIKE '%Surveyor%'
          AND ct.name NOT LIKE '%Requisition%'
          AND ct.name NOT LIKE '%Expeditionary%'
          AND ct.name NOT LIKE '%Sickly%'
          AND ct.name NOT LIKE '%Invasion%'
          AND ct.name NOT LIKE '%finder%'
          AND ct.name NOT LIKE '%Minion%'
          AND ct.name NOT LIKE '%Invasion%'
          AND ct.name NOT LIKE 'Scourge%'
        ORDER BY c.guid
    """, (zone_id,))

    return cursor.fetchall()


def get_replacement_pool(bracket, zone_name, b7_zone, validated_pools=None):
    """
    Return the list of entry IDs to use as replacements for this zone.
    Bracket 7 skull zone uses dungeon bosses.
    Any other zone assigned bracket 7 falls back to bracket 6 pool.
    """
    if zone_name == b7_zone:
        return BRACKET_7_ALL_ENTRIES
    if bracket == 7:
        bracket = 6
    pools = validated_pools if validated_pools else BRACKET_CREATURES
    return pools.get(bracket, [])


# Names to exclude from pool even if they passed DB filter
POOL_NAME_EXCLUSIONS = {
    'Farmer', 'Farmhand', 'Civilian', 'Peasant', 'Refugee', 'Orphan',
    'Child', 'Baby', 'Kid', 'Wisp', 'Dummy', 'Trigger', 'Survivor',
    'Explorer', 'Requisition', 'Expeditionary',
}

def build_zone_species(pool):
    # Pure random selection from pool - no weighting
    # zoneId approach gives accurate zone data so no need to force a primary species
    pool_copy = list(pool)
    random.shuffle(pool_copy)
    return pool_copy, pool_copy[0] if pool_copy else None



def cleanup_overlevel_creatures(cursor, zone_name, bracket, dry_run=True):
    """
    After seeding, delete vanilla creatures whose level exceeds the bracket cap.
    These are creatures that survived the replacement filter (wrong faction, type, etc.)
    but are still too high level for the zone's assigned bracket.
    We preserve: type 10 (triggers/objects), guards, friendly NPCs (faction 35).
    """
    from db_lookups import ZONE_IDS
    zone_id = ZONE_IDS.get(zone_name)
    if not zone_id:
        return 0

    # Bracket level caps (max level allowed in this bracket)
    BRACKET_CAPS = {1:12, 2:22, 3:32, 4:42, 5:52, 6:62, 7:65}
    level_cap = BRACKET_CAPS.get(bracket, 65)

    # Find GUIDs of overlevel creatures to remove
    cursor.execute("""
        SELECT c.guid, ct.name, ct.minlevel, ct.faction, ct.type
        FROM creature c
        JOIN creature_template ct ON c.id1 = ct.entry
        WHERE c.zoneId = %s
          AND ct.minlevel > %s
          AND ct.type != 10
          AND ct.npcflag = 0
          AND ct.name NOT LIKE 'Guard %%'
          AND ct.name NOT LIKE '%%Guard%%'
          AND ct.faction NOT IN (35, 36, 469, 1610, 1629, 1638, 1639)
    """, (zone_id, level_cap))

    rows = cursor.fetchall()
    if not rows:
        return 0

    if not dry_run:
        guids = [r[0] for r in rows]
        cursor.execute(
            "DELETE FROM creature WHERE guid IN ({})".format(
                ','.join(str(g) for g in guids)
            )
        )

    return len(rows)

def seed_zone(cursor, zone_name, bracket, b7_zone, dry_run=True, claimed_guids=None, validated_pools=None):
    if claimed_guids is None:
        claimed_guids = set()
    if claimed_guids is None:
        claimed_guids = set()
    is_bracket_7 = (zone_name == b7_zone)
    creatures = get_creatures_in_zone(cursor, zone_name, is_bracket_7=is_bracket_7, claimed_guids=claimed_guids)
    pool = get_replacement_pool(bracket, zone_name, b7_zone, validated_pools)

    if not pool:
        print(f"  No pool for bracket {bracket} - skipping {zone_name}")
        return 0, len(creatures)

    if not creatures:
        print(f"  No creatures found in {zone_name}")
        return 0, 0

    weighted_pool, primary = build_zone_species(pool)

    replaced = 0
    for guid, old_id, name, minlevel, maxlevel in creatures:
        new_entry = random.choice(weighted_pool)
        if not dry_run:
            cursor.execute(
                "UPDATE creature SET id1 = %s WHERE guid = %s",
                (new_entry, guid)
            )
        replaced += 1

    print(f"           -> {replaced} replaced  (primary species: entry {primary})")

    for guid, _, _, _, _ in creatures:
        claimed_guids.add(guid)

    # Mark all processed GUIDs as claimed
    for guid, _, _, _, _ in creatures:
        claimed_guids.add(guid)

    return replaced, 0

def run_seeder(bracket_map, b7_zone, b7_bounty, db_config, dry_run=True):
    """
    Main seeder — iterates all zones in the bracket map and applies
    creature replacements using zoneId for accurate zone targeting.
    """
    conn   = connect(**db_config)
    cursor = conn.cursor()

    print()
    print("=" * 60)
    print(f"  BountyWorld DB Seeder — {'DRY RUN' if dry_run else 'APPLYING CHANGES'}")
    print("=" * 60)
    print()

    # Validate bracket pools against creature_template
    print("  Validating bracket pools...")
    cursor.execute("""
        SELECT entry FROM creature_template
        WHERE npcflag = 0
        AND unit_class != 0
        AND type IN (1,2,4,5,7,8)
        AND minlevel > 1
        AND maxlevel > 1
        AND (maxlevel - minlevel) <= 15
        AND (ScriptName = '' OR ScriptName IS NULL)
        AND faction NOT IN (
            35, 36, 12, 14, 21, 22, 150, 534,
            890, 914, 1014, 1015, 1074, 1375, 1376,
            1634, 1635, 1638, 1639
        )
        AND name NOT LIKE '%Child%'
        AND name NOT LIKE '%Wisp%'
        AND name NOT LIKE '%Farmhand%'
        AND name NOT LIKE '%Refugee%'
        AND name NOT LIKE '%Orphan%'
        AND name NOT LIKE '%Credit%'
        AND name NOT LIKE '%Stalker%'
        AND name NOT LIKE '%Trigger%'
        AND name NOT LIKE '%Dummy%'
        AND name NOT LIKE '%Minion%'
        AND name NOT LIKE '%Invasion%'
        AND name NOT LIKE 'Scourge%%'
        AND name NOT LIKE '%Surveyor%'
        AND name NOT LIKE '%Explorer%'
        AND name NOT LIKE '%finder%'
        AND name NOT LIKE '%Spy %%'
        AND name NOT LIKE '%Captive%'
        AND name NOT LIKE '%Prisoner%'
        AND name NOT LIKE '%Civilian%'
        AND name NOT LIKE '%Peasant%'
        AND name NOT LIKE '%Farmer%'
        AND name NOT LIKE '%Sickly%'
    """)
    valid_entries = set(r[0] for r in cursor.fetchall())

    from db_lookups import BRACKET_CREATURES as _BC
    validated_pools = {
        b: [e for e in pool if e in valid_entries]
        for b, pool in _BC.items()
    }
    print("  Pool sizes: " + ", ".join(f"B{b}:{len(p)}" for b, p in sorted(validated_pools.items())))
    print()

    total_replaced = 0
    total_skipped  = 0
    claimed_guids  = set()

    # Sort zones by bracket (skull zone first)
    sorted_zones = sorted(bracket_map.items(), key=lambda x: (0 if x[0] == b7_zone else x[1]))

    for zone_name, bracket in sorted_zones:
        skull = " SKULL" if zone_name == b7_zone else ""
        print(f"  Bracket {bracket}  {zone_name}{skull}")

        replaced, skipped = seed_zone(
            cursor, zone_name, bracket, b7_zone,
            dry_run=dry_run, claimed_guids=claimed_guids,
            validated_pools=validated_pools
        )

        cleaned = cleanup_overlevel_creatures(cursor, zone_name, bracket, dry_run=dry_run)
        if cleaned > 0:
            print(f"           \u2192 {cleaned} overlevel vanilla creatures removed")

        total_replaced += replaced
        total_skipped  += skipped
        print(f"           \u2192 {replaced} creatures replaced, {skipped} skipped")

    print()
    print(f"  Total replaced: {total_replaced}")
    print(f"  Total skipped:  {total_skipped}")
    print()

    if not dry_run:
        print("  Committing changes to database...")
        conn.commit()
        print("  \u2713 Done. Restart your worldserver for changes to take effect.")
    else:
        print("  Dry run complete \u2014 no changes written.")
        print("  Run with --apply to apply changes.")

    print()
    print(f"  Bracket 7 Skull Zone: {b7_zone}")
    print(f"  Bounty Target:        {b7_bounty['name']} ({b7_bounty['dungeon']})")
    print()

    cursor.close()
    conn.close()


def reset_from_backup(backup_file, db_config, dry_run=True):
    """
    Restore original creature entries from a backup JSON created during
    a previous seeder run. Not yet implemented — use mysqldump backup.
    """
    print("Reset from backup not yet implemented.")
    print("Restore your database using:")
    print("  mysql -u root -p acore_world < backup_before_shuffle.sql")

# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="BountyWorld DB Seeder")
    parser.add_argument("--json",     required=True,
                        help="Bracket map JSON file from zone_shuffle.py")
    parser.add_argument("--dry-run",  action="store_true", default=True,
                        help="Preview changes without writing to DB (default)")
    parser.add_argument("--apply",    action="store_true",
                        help="Actually apply changes to the database")
    parser.add_argument("--host",     default="127.0.0.1")
    parser.add_argument("--port",     type=int, default=3306)
    parser.add_argument("--user",     default="acore")
    parser.add_argument("--password", default="acore")
    parser.add_argument("--database", default="acore_world")
    args = parser.parse_args()

    dry_run = not args.apply

    # Load bracket map
    with open(args.json, "r") as f:
        data = json.load(f)

    bracket_map = data["brackets"]
    b7_zone     = data["bracket_7_zone"]
    b7_bounty   = data["bracket_7_bounty"]
    seed_val    = data["seed"]

    print(f"  Loaded bracket map — seed {seed_val}")
    print(f"  Zones: {len(bracket_map)}")
    print(f"  Bracket 7 zone: {b7_zone} → {b7_bounty['name']}")

    db_config = {
        "host":     args.host,
        "port":     args.port,
        "user":     args.user,
        "password": args.password,
        "database": args.database,
    }

    run_seeder(bracket_map, b7_zone, b7_bounty, db_config, dry_run=dry_run)


if __name__ == "__main__":
    main()