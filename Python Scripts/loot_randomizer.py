"""
BountyWorld Loot Randomizer
============================
Randomly shuffles creature loot tables globally.
Every creature entry gets another random creature's loot table assigned.
Quest loot is never touched.

Usage:
    python loot_randomizer.py --dry-run --password acore
    python loot_randomizer.py --apply --password acore
    python loot_randomizer.py --restore --password acore
"""

import random
import argparse
import mysql.connector


def connect(host, port, user, password, database):
    return mysql.connector.connect(
        host=host, port=port, user=user, password=password,
        database=database, autocommit=False
    )


def backup_loot_table(cursor):
    """Create a backup of creature_loot_template before randomizing."""
    print("  Creating backup table creature_loot_template_bw_backup...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS creature_loot_template_bw_backup
        LIKE creature_loot_template
    """)
    cursor.execute("""
        SELECT COUNT(*) FROM creature_loot_template_bw_backup
    """)
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"  Backup already exists ({count} rows) — skipping backup creation.")
        return False
    cursor.execute("""
        INSERT INTO creature_loot_template_bw_backup
        SELECT * FROM creature_loot_template
    """)
    cursor.execute("SELECT COUNT(*) FROM creature_loot_template_bw_backup")
    count = cursor.fetchone()[0]
    print(f"  Backup created: {count} rows.")
    return True


def restore_loot_table(cursor):
    """Restore from backup."""
    cursor.execute("""
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_schema = 'acore_world'
        AND table_name = 'creature_loot_template_bw_backup'
    """)
    if cursor.fetchone()[0] == 0:
        print("  No backup table found. Run with --apply first.")
        return False

    print("  Restoring creature_loot_template from backup...")
    cursor.execute("DELETE FROM creature_loot_template")
    cursor.execute("""
        INSERT INTO creature_loot_template
        SELECT * FROM creature_loot_template_bw_backup
    """)
    cursor.execute("SELECT COUNT(*) FROM creature_loot_template")
    print(f"  Restored: {cursor.rowcount} rows written.")
    return True


def get_loot_entries(cursor):
    """
    Get all creature entries that have non-quest loot.
    Returns list of entry IDs that have at least one non-quest item drop.
    """
    cursor.execute("""
        SELECT DISTINCT Entry
        FROM creature_loot_template
        WHERE QuestRequired = 0
        AND Item > 0
        AND Reference = 0
        ORDER BY Entry
    """)
    return [row[0] for row in cursor.fetchall()]


def randomize_loot(cursor, seed_val, dry_run=True):
    """
    For each creature entry, assign a random other entry's loot table.
    Quest drops are preserved. Only non-quest direct item drops are shuffled.
    """
    rng = random.Random(seed_val)

    print("  Fetching all loot entries...")
    entries = get_loot_entries(cursor)
    print(f"  Found {len(entries)} creature entries with non-quest loot")

    # Create a shuffled mapping: entry -> new_source_entry
    shuffled = list(entries)
    rng.shuffle(shuffled)
    remap = dict(zip(entries, shuffled))

    # Count how many will actually change
    changed = sum(1 for k, v in remap.items() if k != v)
    print(f"  {changed} entries will get a different loot table")
    print(f"  {len(entries) - changed} entries happen to map to themselves")

    if dry_run:
        # Show a sample of the remapping
        print("\n  Sample remappings (first 10):")
        for old, new in list(remap.items())[:10]:
            if old != new:
                print(f"    Entry {old} will drop loot from entry {new}")
        return remap

    print("\n  Applying loot remapping...")

    # Strategy: for each entry, replace its non-quest direct item rows
    # with the rows from its assigned source entry
    # We do this in two passes to avoid conflicts:
    # Pass 1: delete all non-quest direct item rows for all entries
    # Pass 2: insert the remapped rows

    print("  Pass 1: Collecting remapped loot data...")
    new_rows = []
    for target_entry, source_entry in remap.items():
        if target_entry == source_entry:
            continue

        # Get source loot rows
        cursor.execute("""
            SELECT Item, Reference, Chance, QuestRequired,
                   LootMode, GroupId, MinCount, MaxCount, Comment
            FROM creature_loot_template
            WHERE Entry = %s
            AND QuestRequired = 0
            AND Item > 0
            AND Reference = 0
        """, (source_entry,))
        rows = cursor.fetchall()

        for row in rows:
            new_rows.append((target_entry,) + row)

    print(f"  Pass 2: Deleting {len(entries)} entries' non-quest direct loot...")
    cursor.execute("""
        DELETE FROM creature_loot_template
        WHERE Entry IN ({})
        AND QuestRequired = 0
        AND Item > 0
        AND Reference = 0
    """.format(','.join(str(e) for e in entries)))

    print(f"  Pass 3: Inserting {len(new_rows)} remapped loot rows...")
    if new_rows:
        cursor.executemany("""
            INSERT INTO creature_loot_template
            (Entry, Item, Reference, Chance, QuestRequired,
             LootMode, GroupId, MinCount, MaxCount, Comment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, new_rows)

    return remap


def main():
    parser = argparse.ArgumentParser(description="BountyWorld Loot Randomizer")
    parser.add_argument("--dry-run",  action="store_true", default=True)
    parser.add_argument("--apply",    action="store_true")
    parser.add_argument("--restore",  action="store_true")
    parser.add_argument("--seed",     type=int, default=12345)
    parser.add_argument("--host",     default="127.0.0.1")
    parser.add_argument("--port",     type=int, default=3306)
    parser.add_argument("--user",     default="acore")
    parser.add_argument("--password", default="acore")
    args = parser.parse_args()

    dry_run = not args.apply and not args.restore

    conn   = connect(args.host, args.port, args.user, args.password, "acore_world")
    cursor = conn.cursor()

    if args.restore:
        print("\n  BountyWorld Loot Randomizer — RESTORE")
        print("  ======================================")
        if restore_loot_table(cursor):
            conn.commit()
            print("  Restore complete. Restart worldserver to apply.")
        cursor.close()
        conn.close()
        return

    mode = "DRY RUN" if dry_run else "APPLYING"
    print(f"\n  BountyWorld Loot Randomizer — {mode}")
    print(f"  Seed: {args.seed}")
    print("  ======================================\n")

    if not dry_run:
        print("  Backing up loot table...")
        backup_loot_table(cursor)
        conn.commit()

    randomize_loot(cursor, args.seed, dry_run=dry_run)

    if not dry_run:
        print("\n  Committing...")
        conn.commit()
        print("  Done! Restart worldserver to see changes.")
        print("  To restore original loot: python loot_randomizer.py --restore --password acore")
    else:
        print("\n  Dry run complete. Run with --apply to apply.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()