# BountyWorld - BETA Version 1.0

A singleplayer roguelite gamemode for World of Warcraft 3.3.5a built on [AzerothCore](https://www.azerothcore.org/).
You play in 3.3.5a, so WOTLK, but only the Vanilla zones are shuffled!

The 35 vanilla zones are shuffled into 7 difficulty brackets. Named bounty targets are assigned across the world — hunt them down, survive, and advance. Die and your run resets. Clear all brackets to achieve true victory.

---
## Known bugs / problems
- Some higher level mobs gets filtered and not reset. These are quest-mobs and scripted mobs. This leads to some zones being VERY dangerous for lower levels and some spawn-points impossible to get out from. This can be fixed during playtime by having a macro with ".gm on" keybound. A permanent solutions is in progress.
---

## Features

- **Zone Shuffle** — 35 zones randomly assigned to 7 brackets (1–10, 11–20, 21–30, 31–40, 41–50, 51–60, Skull). Continent balance: Kalimdor always has bracket 1 zones, EK has bracket 3+.
- **Creature Seeder** — Every outdoor mob in each zone replaced with bracket-appropriate creatures. Strict filtering prevents scripted creatures, and event mobs from being replaced.
- **Multi-Bounty System** — 2–5 named bounty targets per bracket. Kill them all to advance. Hint system reveals location after 10 and 25 minutes.
- **Clean Clear Bonus** — Kill all bounties in a bracket while at or under the bracket's level cap: receive gold, a Hunter's Medallion (escalating neck item), and stacking 5% XP bonus.
- **Faction-Based Spawning** — New characters teleport to a safe inn in a bracket 1 zone on their home continent.
- **Continent-Restricted Bounties** — Bracket 1–2 bounties only spawn on the player's home continent. Bracket 3+ opens up both continents.
- **Random Loot** — Every creature's loot table globally shuffled. A level 5 wolf might drop Ragnaros gear.
- **Safety Net** — Die in bracket X and your next run starts at bracket X–1.
- **Meta Progression** — Lifetime kills, deaths, runs, and 35 achievements tracked account-wide.
- **BountyWorld UI** — In-game addon with Run, Achievements, and Stats tabs. Minimap button and `/bw` slash command.
- **Zone Report** — Dark-themed HTML report showing top creatures per zone, tabbed by zone, generated from live DB data.
- **AHBot Compatible** — Works alongside mod-ah-bot for a functional auction house economy.

---

## Requirements

- [AzerothCore](https://www.azerothcore.org/) 3.3.5a
- [mod-ale](https://github.com/azerothcore/mod-ale) (ALE Lua Engine)
- [mod-progression-system](https://github.com/azerothcore/mod-progression-system) set to Phase 1
- [mod-solo-lfg](https://github.com/azerothcore/mod-solo-lfg) (optional but recommended)
- Python 3.8+ with `mysql-connector-python` (`pip install mysql-connector-python`)
- MySQL 8.x

---

## File Reference

### Python Scripts

| File | Description |
|------|-------------|
| `zone_shuffle.py` | Core shuffle algorithm. Assigns 35 zones to 7 brackets with faction continent constraints. Generates bracket map JSON, optional HTML zone report, and visualisation. |
| `db_lookups.py` | Static data tables: zone IDs, zone adjacency graph, continent sets, bracket creature pools, dungeon boss pool, zone spawn coordinates (innkeeper positions). |
| `db_seeder.py` | Reads bracket map JSON and replaces outdoor creature spawns in each zone with bracket-appropriate creatures. Validates pools against live DB to exclude event/quest NPCs. |
| `bw_populate.py` | Reads bracket map JSON and writes zone→bracket assignments to `bountyworld_bracket_zones` table in `acore_characters`. |
| `loot_randomizer.py` | Globally shuffles `creature_loot_template`. Every creature gets another creature's loot. Quest loot untouched. Supports `--dry-run`, `--apply`, and `--restore`. |

### SQL Files

| File | Description |
|------|-------------|
| `bountyworld_items.sql` | Creates 7 Hunter's Medallion neck items (entries 700001–700007) in `acore_world.item_template`. Escalating stats from epic (bracket 1) to legendary (bracket 7). |
| `bountyworld_achievements.sql` | Creates the `bountyworld_achievements` table and inserts all 35 achievement definitions in `acore_characters`. |

### Lua Scripts (Server-side, ALE)

Place these in your worldserver's `lua_scripts/` directory.

| File | Description |
|------|-------------|
| `bountyworld_core.lua` | Main bounty system. Handles bounty assignment, kill detection, bracket advancement, hint system, safety net, clean clear detection, and all `bw` chat commands. |
| `bountyworld_meta.lua` | Account-wide meta progression. Tracks lifetime stats, achievements, safety net bracket, and starting level bonus. Handles faction-based teleport to bracket 1 zone on first login. |
| `bountyworld_ui_bridge.lua` | Sends run data, stats, and achievement data to the client addon via `SendAddonMessage` on login and after bounty events. |

### Client Addon

Place the `BountyWorldUI/` folder in `Interface/AddOns/`.

| File | Description |
|------|-------------|
| `BountyWorldUI/BountyWorldUI.lua` | Client addon. Three tabs: Run (active bounties with zones and kill progress), Achievements (all 35, earned/unearned), Stats (lifetime totals and milestones). Minimap button and `/bw` command. |
| `BountyWorldUI/BountyWorldUI.toc` | Addon table of contents file. |

---

## Database Tables

All tables created in `acore_characters`:

| Table | Description |
|-------|-------------|
| `bountyworld_run` | Per-character run state: current bracket, active status, seed, clean clear count. |
| `bountyworld_bounties` | Active bounty targets per character: entry ID, name, zone, killed status. |
| `bountyworld_bracket_zones` | Zone→bracket assignments for the current seed. Written by `bw_populate.py`. |
| `bountyworld_meta` | Account-wide stats: lifetime kills, deaths, runs, safety net bracket, XP bonus, achievements bitmask. |
| `bountyworld_achievements` | Per-account achievement earn timestamps. |

---

## Installation

### 0. Install the requirements and AzerothCore!
Do this as normal from their online guide. A fresh install is needed and dont forget to backup files if you ever want to play the original.

### 1. Database Setup

Run the following SQL files against your MySQL instance:

```sql
source bountyworld_items.sql
source bountyworld_achievements.sql
```

Create the character DB tables:

```sql
USE acore_characters;

CREATE TABLE IF NOT EXISTS bountyworld_run (
    guid INT UNSIGNED NOT NULL PRIMARY KEY,
    current_bracket TINYINT UNSIGNED NOT NULL DEFAULT 1,
    run_active TINYINT UNSIGNED NOT NULL DEFAULT 0,
    seed INT UNSIGNED NOT NULL DEFAULT 0,
    clean_clears TINYINT UNSIGNED NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS bountyworld_bounties (
    guid INT UNSIGNED NOT NULL,
    bracket TINYINT UNSIGNED NOT NULL,
    bounty_entry INT UNSIGNED NOT NULL,
    bounty_name VARCHAR(100) NOT NULL,
    bounty_zone VARCHAR(100) NOT NULL,
    killed TINYINT UNSIGNED NOT NULL DEFAULT 0,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (guid, bracket, bounty_entry)
);

CREATE TABLE IF NOT EXISTS bountyworld_bracket_zones (
    seed INT UNSIGNED NOT NULL,
    zone_name VARCHAR(100) NOT NULL,
    bracket TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (seed, zone_name)
);

CREATE TABLE IF NOT EXISTS bountyworld_meta (
    account_id INT UNSIGNED NOT NULL PRIMARY KEY,
    lifetime_kills INT UNSIGNED NOT NULL DEFAULT 0,
    lifetime_deaths INT UNSIGNED NOT NULL DEFAULT 0,
    lifetime_runs INT UNSIGNED NOT NULL DEFAULT 0,
    safety_net_bracket TINYINT UNSIGNED NOT NULL DEFAULT 1,
    starting_level_bonus TINYINT UNSIGNED NOT NULL DEFAULT 0,
    achievements BIGINT UNSIGNED NOT NULL DEFAULT 0,
    total_playtime INT UNSIGNED NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS bountyworld_achievements (
    account_id INT UNSIGNED NOT NULL,
    achievement_id INT UNSIGNED NOT NULL,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (account_id, achievement_id)
);
```

### 2. Generate a Bracket Map

```bash
python zone_shuffle.py --seed 12345 --save
```

This generates `bracket_map_seed12345.json`.

### 3. Populate Bracket Zones

```bash
python bw_populate.py --json bracket_map_seed12345.json --password YOUR_PASSWORD
```

### 4. Restore Vanilla Creatures

```powershell
Get-Content "path/to/AzerothCore/data/sql/base/db_world/creature.sql" | mysql -u root -p --max_allowed_packet=512M acore_world
```

### 5. Populate zoneId Fields

Start the worldserver, with the config line "Calculate.Creature.Zone.Area.Data = 1" in worldserver.conf, wait for the `AC>` prompt, then stop it. This populates the `zoneId` field on all creature spawns which the seeder requires.

### 6. Seed Creatures

```bash
python db_seeder.py --json bracket_map_seed12345.json --apply --password YOUR_PASSWORD
```

### 7. Randomize Loot

```bash
python loot_randomizer.py --apply --seed 12345 --password YOUR_PASSWORD
```

### 8. Clear Respawn Cache

```sql
TRUNCATE TABLE acore_characters.creature_respawn;
```

### 9. Install Lua Scripts

Copy the four Lua files to your worldserver's `lua_scripts/` directory. Reload with `.reload eluna` or restart the worldserver.

### 10. Install Client Addon

Copy `BountyWorldUI/` to your WoW client's `Interface/AddOns/` directory.

---

## Reshuffle Workflow

To generate a completely new shuffle (e.g. seed 99999):

1. Restore vanilla creatures (step 4 above)
2. `python zone_shuffle.py --seed 99999 --save`
3. `python bw_populate.py --json bracket_map_seed99999.json --password YOUR_PASSWORD`
4. Start worldserver → wait for `AC>` → stop
5. `python db_seeder.py --json bracket_map_seed99999.json --apply --password YOUR_PASSWORD`
6. `TRUNCATE TABLE acore_characters.creature_respawn;`
7. `python loot_randomizer.py --apply --seed 99999 --password YOUR_PASSWORD`
8. Update `CURRENT_SEED` in `bountyworld_core.lua` to `99999`
9. `.reload eluna` or restart worldserver
10. `bw fullreset` on all characters

---

## In-Game Commands

All commands are typed in the **say** chat channel.

| Command | Description |
|---------|-------------|
| `bw hint` | Request a hint for your current bounty targets. First hint after 10 min gives flavor text, after 25 min reveals the zone. |
| `bw status` | Show current bracket, bounty progress, and kill count. |
| `bw info` | *(GM)* Show detailed run data. |
| `bw zones` | *(GM)* List all zone bracket assignments for current seed. |
| `bw reset` | *(GM)* Reset current run and start fresh at bracket 1. |
| `bw fullreset` | *(GM)* Full account reset including meta progression and achievements. |

---

## Zone Report

Generate a dark-themed HTML report showing the top 5 creatures per zone after seeding:

```bash
python zone_shuffle.py --seed 12345 --report --json bracket_map_seed12345.json --password YOUR_PASSWORD
```

Opens automatically in your browser. Zones are tabbed in the sidebar, color-coded by bracket.

---

## Bracket System

| Bracket | Level Range | Notes |
|---------|-------------|-------|
| 1 | 1–10 | Kalimdor only (Horde) / EK only (Alliance) |
| 2 | 11–20 | Home continent only |
| 3 | 21–30 | Both continents |
| 4 | 31–40 | Both continents |
| 5 | 41–50 | Both continents |
| 6 | 51–60 | Both continents |
| 7 ☠ | 60 Elite | Single skull zone, all mobs replaced with dungeon bosses |

Clean clear (kill all bounties at or under level cap) rewards: gold, Hunter's Medallion neck item, +5% XP bonus stacking per bracket.

---

## Credits

Built on [AzerothCore](https://www.azerothcore.org/) with [mod-ale](https://github.com/azerothcore/mod-ale).
Huge shoutout to [UncleChimpuss](https://www.youtube.com/@UncleChimpuss) for the idea for randomized mobs!
