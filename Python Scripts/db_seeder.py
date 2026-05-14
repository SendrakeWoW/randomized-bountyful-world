"""
BountyWorld DB Seeder
=====================
Replaces outdoor creature spawns with bracket-appropriate creatures
using zoneId for accurate zone targeting (no bounding box overlaps).

Usage:
    python db_seeder.py --json bracket_map_seed12345.json --dry-run --password acore
    python db_seeder.py --json bracket_map_seed12345.json --apply --password acore
"""

import random
import argparse
import json
import mysql.connector

from db_lookups import (
    BRACKET_CREATURES, DUNGEON_BOSS_POOL, BRACKET_7_ALL_ENTRIES, ZONE_IDS
)

# Build dungeon boss entry set for exclusion from regular pools
BOSS_ENTRIES = set(b['entry'] for b in DUNGEON_BOSS_POOL if 'entry' in b)


def connect(host, port, user, password, database):
    return mysql.connector.connect(
        host=host, port=port, user=user, password=password,
        database=database, autocommit=False
    )


def get_creatures_in_zone(cursor, zone_name, is_bracket_7=False):
    """Fetch all replaceable creature GUIDs for a zone using zoneId."""
    zone_id = ZONE_IDS.get(zone_name)
    if not zone_id:
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
          AND ct.name NOT LIKE '%Captive%'
          AND ct.name NOT LIKE '%Prisoner%'
          AND ct.name NOT LIKE '%Spy %%'
          AND ct.name NOT LIKE '%Credit%'
          AND ct.name NOT LIKE 'Scourge%%'
        ORDER BY c.guid
    """, (zone_id,))

    return cursor.fetchall()


def get_replacement_pool(bracket, zone_name, b7_zone, validated_pools):
    """Return the creature pool for this zone's bracket."""
    if zone_name == b7_zone:
        return BRACKET_7_ALL_ENTRIES
    if bracket == 7:
        bracket = 6
    return validated_pools.get(bracket, [])


def seed_zone(cursor, zone_name, bracket, b7_zone, dry_run, validated_pools):
    """Replace all creatures in a zone with bracket-appropriate ones."""
    creatures = get_creatures_in_zone(cursor, zone_name, is_bracket_7=(zone_name == b7_zone))

    if not creatures:
        print(f"  No creatures found in {zone_name}")
        return 0, 0

    pool = get_replacement_pool(bracket, zone_name, b7_zone, validated_pools)
    if not pool:
        print(f"  No pool for bracket {bracket} — skipping {zone_name}")
        return 0, len(creatures)

    primary = random.choice(pool)
    replaced = 0

    for guid, old_id, name, minlevel, maxlevel in creatures:
        new_entry = random.choice(pool)
        if not dry_run:
            cursor.execute(
                "UPDATE creature SET id1 = %s WHERE guid = %s",
                (new_entry, guid)
            )
        replaced += 1

    print(f"           -> {replaced} replaced  (primary species: entry {primary})")
    return replaced, 0


def validate_pools(cursor):
    """Filter bracket pools to only include valid hostile outdoor creatures."""
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
          AND name NOT LIKE '%Farmhand%'
    """)
    valid = set(r[0] for r in cursor.fetchall())

    result = {}
    for bracket, pool in BRACKET_CREATURES.items():
        filtered = [e for e in pool if e in valid and e not in BOSS_ENTRIES]
        result[bracket] = filtered

    print("  Pool sizes: " + ", ".join(
        f"B{b}:{len(p)}" for b, p in sorted(result.items())
    ))
    return result


def run_seeder(bracket_map, b7_zone, b7_bounty, db_config, dry_run=True):
    conn   = connect(**db_config)
    cursor = conn.cursor()

    print()
    print("=" * 60)
    mode = "DRY RUN" if dry_run else "APPLYING CHANGES"
    print(f"  BountyWorld DB Seeder — {mode}")
    print("=" * 60)
    print()

    print("  Validating bracket pools...")
    validated_pools = validate_pools(cursor)
    print()

    total_replaced = 0
    total_skipped  = 0

    # Skull zone first, then brackets 1-6
    sorted_zones = sorted(
        bracket_map.items(),
        key=lambda x: (0 if x[0] == b7_zone else x[1])
    )

    for zone_name, bracket in sorted_zones:
        skull = " SKULL" if zone_name == b7_zone else ""
        print(f"  Bracket {bracket}  {zone_name}{skull}")

        replaced, skipped = seed_zone(
            cursor, zone_name, bracket, b7_zone,
            dry_run=dry_run,
            validated_pools=validated_pools
        )

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


def main():
    parser = argparse.ArgumentParser(description="BountyWorld DB Seeder")
    parser.add_argument("--json",     required=True, help="Bracket map JSON file")
    parser.add_argument("--dry-run",  action="store_true", default=True)
    parser.add_argument("--apply",    action="store_true")
    parser.add_argument("--seed",     type=int, default=None)
    parser.add_argument("--host",     default="127.0.0.1")
    parser.add_argument("--port",     type=int, default=3306)
    parser.add_argument("--user",     default="acore")
    parser.add_argument("--password", default="acore")
    args = parser.parse_args()

    dry_run = not args.apply

    with open(args.json) as f:
        data = json.load(f)

    bracket_map = data["brackets"]
    b7_zone     = data["bracket_7_zone"]
    b7_bounty   = data["bracket_7_bounty"]
    seed_val    = data.get("seed", args.seed or 0)

    random.seed(seed_val)

    print()
    print(f"  Loaded bracket map \u2014 seed {seed_val}")
    print(f"  Zones: {len(bracket_map)}")
    print(f"  Bracket 7 zone: {b7_zone} \u2192 {b7_bounty['name']}")

    db_config = {
        "host":     args.host,
        "port":     args.port,
        "user":     args.user,
        "password": args.password,
        "database": "acore_world",
    }

    run_seeder(bracket_map, b7_zone, b7_bounty, db_config, dry_run=dry_run)


if __name__ == "__main__":
    main()