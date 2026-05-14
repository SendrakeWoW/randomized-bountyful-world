"""
BountyWorld — DB Lookup Tables
================================
Zone IDs, creature entry IDs, and bracket creature pools.
Used by the DB seeder script to apply the zone shuffle to AzerothCore.

All IDs verified against WoWHead Classic and ClassicDB for vanilla 1.12 / 3.3.5a.

IMPORTANT: Before running the DB seeder, always verify entry IDs:
  SELECT entry, name, ScriptName, rank, minlevel, maxlevel
  FROM creature_template
  WHERE entry IN (<comma separated entries>)
  ORDER BY entry;

Some script-triggered bosses (Gandling, Gahz'rilla) may need special
handling for open-world spawning. Flag these for manual review.
"""

# ---------------------------------------------------------------------------
# ZONE IDs  (AreaTable IDs — creature.zone field in AzerothCore)
# ---------------------------------------------------------------------------

ZONE_IDS = {
    # ── Kalimdor ─────────────────────────────────────────────────────────────
    "Teldrassil":              141,
    "Darkshore":               148,
    "Ashenvale":               331,
    "Stonetalon Mountains":    406,
    "The Barrens":             17,
    "Durotar":                 14,
    "Mulgore":                 215,
    "Dustwallow Marsh":        15,
    "Thousand Needles":        400,
    "Feralas":                 357,
    "Tanaris":                 440,
    "Un'Goro Crater":          490,
    "Silithus":                1377,
    "Felwood":                 361,
    "Moonglade":               493,
    "Winterspring":            618,

    # ── Eastern Kingdoms ─────────────────────────────────────────────────────
    "Elwynn Forest":           12,
    "Westfall":                40,
    "Duskwood":                10,
    "Redridge Mountains":      44,
    "Burning Steppes":         46,
    "Searing Gorge":           51,
    "Blasted Lands":           4,
    "Swamp of Sorrows":        8,
    "Loch Modan":              38,
    "Dun Morogh":              1,
    "Wetlands":                11,
    "Arathi Highlands":        45,
    "Hillsbrad Foothills":     267,
    "Alterac Mountains":       36,
    "Silverpine Forest":       130,
    "Tirisfal Glades":         85,
    "Western Plaguelands":     28,
    "Eastern Plaguelands":     139,
    "The Hinterlands":         47,
}

ZONE_ID_TO_NAME = {v: k for k, v in ZONE_IDS.items()}

MAP_IDS = {
    "Kalimdor":         1,
    "Eastern Kingdoms": 0,
}

ZONE_CONTINENT = {
    "Teldrassil": 1, "Darkshore": 1, "Ashenvale": 1,
    "Stonetalon Mountains": 1, "The Barrens": 1, "Durotar": 1,
    "Mulgore": 1, "Dustwallow Marsh": 1, "Thousand Needles": 1,
    "Feralas": 1, "Tanaris": 1, "Un'Goro Crater": 1,
    "Silithus": 1, "Felwood": 1, "Moonglade": 1, "Winterspring": 1,
    "Elwynn Forest": 0, "Westfall": 0, "Duskwood": 0,
    "Redridge Mountains": 0, "Burning Steppes": 0, "Searing Gorge": 0,
    "Blasted Lands": 0, "Swamp of Sorrows": 0, "Loch Modan": 0,
    "Dun Morogh": 0, "Wetlands": 0, "Arathi Highlands": 0,
    "Hillsbrad Foothills": 0, "Alterac Mountains": 0,
    "Silverpine Forest": 0, "Tirisfal Glades": 0,
    "Western Plaguelands": 0, "Eastern Plaguelands": 0,
    "The Hinterlands": 0,
}

# ---------------------------------------------------------------------------
# BRACKET 7 — DUNGEON BOSS POOL
#
# All named bosses from dungeons level 44+. When a zone is assigned bracket 7,
# every outdoor creature spawn is replaced with bosses from this pool.
# The bounty target is one specific boss chosen at world-generation time.
#
# Dungeons included:
#   Zul'Farrak          (44-54)  —  8 bosses
#   Maraudon            (46-55)  —  8 bosses
#   Sunken Temple       (50-56)  —  7 bosses
#   Blackrock Depths    (52-60)  — 14 bosses
#   Dire Maul East      (55-60)  —  3 bosses
#   Dire Maul West      (55-60)  —  5 bosses
#   Dire Maul North     (55-60)  —  7 bosses
#   LBRS                (55-60)  —  4 bosses
#   UBRS                (55-60)  —  4 bosses
#   Scholomance         (58-60)  —  5 bosses
#   Stratholme          (58-60)  —  5 bosses
#                                  ─────────
#                                  70 bosses total
# ---------------------------------------------------------------------------

DUNGEON_BOSS_POOL = [

    # ── Zul'Farrak (44-54) ──────────────────────────────────────────────────
    {"name": "Theka the Martyr",          "entry": 7272,  "dungeon": "Zul'Farrak",         "level": 44},
    {"name": "Antu'sul",                  "entry": 8127,  "dungeon": "Zul'Farrak",         "level": 45},
    {"name": "Witch Doctor Zum'rah",      "entry": 7271,  "dungeon": "Zul'Farrak",         "level": 44},
    {"name": "Nekrum Gutchewer",          "entry": 7796,  "dungeon": "Zul'Farrak",         "level": 46},
    {"name": "Shadowpriest Sezz'ziz",     "entry": 7275,  "dungeon": "Zul'Farrak",         "level": 46},
    {"name": "Hydromancer Velratha",      "entry": 7795,  "dungeon": "Zul'Farrak",         "level": 46},
    {"name": "Gahz'rilla",               "entry": 7273,  "dungeon": "Zul'Farrak",         "level": 46},
    {"name": "Chief Ukorz Sandscalp",     "entry": 7267,  "dungeon": "Zul'Farrak",         "level": 47},

    # ── Maraudon (46-55) ─────────────────────────────────────────────────────
    {"name": "Lord Vyletongue",           "entry": 12236, "dungeon": "Maraudon",           "level": 46},
    {"name": "Noxxion",                   "entry": 13282, "dungeon": "Maraudon",           "level": 46},
    {"name": "Razorlash",                 "entry": 12258, "dungeon": "Maraudon",           "level": 46},
    {"name": "Celebras the Cursed",       "entry": 12225, "dungeon": "Maraudon",           "level": 47},
    {"name": "Landslide",                 "entry": 12203, "dungeon": "Maraudon",           "level": 47},
    {"name": "Tinkerer Gizlock",          "entry": 13601, "dungeon": "Maraudon",           "level": 48},
    {"name": "Rotgrip",                   "entry": 13596, "dungeon": "Maraudon",           "level": 48},
    {"name": "Princess Theradras",        "entry": 12201, "dungeon": "Maraudon",           "level": 48},

    # ── Sunken Temple / Temple of Atal'Hakkar (50-56) ───────────────────────
    {"name": "Gasher",                    "entry": 5713,  "dungeon": "Sunken Temple",      "level": 49},
    {"name": "Hazzas",                    "entry": 5722,  "dungeon": "Sunken Temple",      "level": 50},
    {"name": "Ogom the Wretched",         "entry": 5711,  "dungeon": "Sunken Temple",      "level": 49},
    {"name": "Jammal'an the Prophet",     "entry": 5710,  "dungeon": "Sunken Temple",      "level": 50},
    {"name": "Morphaz",                   "entry": 5719,  "dungeon": "Sunken Temple",      "level": 50},
    {"name": "Weaver",                    "entry": 5720,  "dungeon": "Sunken Temple",      "level": 50},
    {"name": "Dreamscythe",               "entry": 5721,  "dungeon": "Sunken Temple",      "level": 50},
    {"name": "Avatar of Hakkar",          "entry": 8443,  "dungeon": "Sunken Temple",      "level": 50},

    # ── Blackrock Depths (52-60) ─────────────────────────────────────────────
    {"name": "High Interrogator Gerstahn","entry": 9018,  "dungeon": "Blackrock Depths",   "level": 52},
    {"name": "Lord Roccor",               "entry": 9025,  "dungeon": "Blackrock Depths",   "level": 51},
    {"name": "Houndmaster Grebmar",       "entry": 9319,  "dungeon": "Blackrock Depths",   "level": 52},
    {"name": "Pyromancer Loregrain",      "entry": 9024,  "dungeon": "Blackrock Depths",   "level": 52},
    {"name": "Lord Incendius",            "entry": 9017,  "dungeon": "Blackrock Depths",   "level": 53},
    {"name": "Fineous Darkvire",          "entry": 9056,  "dungeon": "Blackrock Depths",   "level": 53},
    {"name": "Bael'Gar",                  "entry": 9016,  "dungeon": "Blackrock Depths",   "level": 52},
    {"name": "General Angerforge",        "entry": 9033,  "dungeon": "Blackrock Depths",   "level": 55},
    {"name": "Golem Lord Argelmach",      "entry": 8983,  "dungeon": "Blackrock Depths",   "level": 55},
    {"name": "Hurley Blackbreath",        "entry": 9537,  "dungeon": "Blackrock Depths",   "level": 55},
    {"name": "Phalanx",                   "entry": 9502,  "dungeon": "Blackrock Depths",   "level": 55},
    {"name": "Ambassador Flamelash",      "entry": 9156,  "dungeon": "Blackrock Depths",   "level": 55},
    {"name": "Magmus",                    "entry": 9938,  "dungeon": "Blackrock Depths",   "level": 56},
    {"name": "Emperor Dagran Thaurissan", "entry": 9019,  "dungeon": "Blackrock Depths",   "level": 56},

    # ── Dire Maul East (55-60) ───────────────────────────────────────────────
    {"name": "Zevrim Thornhoof",          "entry": 11490, "dungeon": "Dire Maul East",     "level": 57},
    {"name": "Hydrospawn",                "entry": 13280, "dungeon": "Dire Maul East",     "level": 57},
    {"name": "Alzzin the Wildshaper",     "entry": 11492, "dungeon": "Dire Maul East",     "level": 58},

    # ── Dire Maul West (55-60) ───────────────────────────────────────────────
    {"name": "Tendris Warpwood",          "entry": 11489, "dungeon": "Dire Maul West",     "level": 60},
    {"name": "Magister Kalendris",        "entry": 11487, "dungeon": "Dire Maul West",     "level": 60},
    {"name": "Illyanna Ravenoak",         "entry": 11488, "dungeon": "Dire Maul West",     "level": 60},
    {"name": "Immol'thar",                "entry": 11496, "dungeon": "Dire Maul West",     "level": 61},
    {"name": "Prince Tortheldrin",        "entry": 11486, "dungeon": "Dire Maul West",     "level": 61},

    # ── Dire Maul North (55-60) ──────────────────────────────────────────────
    {"name": "Stomper Kreeg",             "entry": 14322, "dungeon": "Dire Maul North",    "level": 59},
    {"name": "Guard Fengus",              "entry": 14321, "dungeon": "Dire Maul North",    "level": 59},
    {"name": "Guard Slip'kik",            "entry": 14323, "dungeon": "Dire Maul North",    "level": 59},
    {"name": "Captain Kromcrush",         "entry": 14325, "dungeon": "Dire Maul North",    "level": 61},
    {"name": "Cho'Rush the Observer",     "entry": 14324, "dungeon": "Dire Maul North",    "level": 60},
    {"name": "King Gordok",               "entry": 11501, "dungeon": "Dire Maul North",    "level": 62},

    # ── Lower Blackrock Spire (55-60) ────────────────────────────────────────
    {"name": "Shadow Hunter Vosh'gajin",  "entry": 9236,  "dungeon": "LBRS",               "level": 58},
    {"name": "War Master Voone",          "entry": 9237,  "dungeon": "LBRS",               "level": 58},
    {"name": "Halycon",                   "entry": 10220, "dungeon": "LBRS",               "level": 59},
    {"name": "Overlord Wyrmthalak",       "entry": 9568,  "dungeon": "LBRS",               "level": 60},

    # ── Upper Blackrock Spire (55-60) ────────────────────────────────────────
    {"name": "Gyth",                      "entry": 10339, "dungeon": "UBRS",               "level": 62},
    {"name": "Warchief Rend Blackhand",   "entry": 10429, "dungeon": "UBRS",               "level": 62},
    {"name": "The Beast",                 "entry": 10430, "dungeon": "UBRS",               "level": 62},
    {"name": "General Drakkisath",        "entry": 10363, "dungeon": "UBRS",               "level": 62},

    # ── Scholomance (58-60) ──────────────────────────────────────────────────
    {"name": "Doctor Theolen Krastinov", "entry": 11261, "dungeon": "Scholomance",         "level": 60},
    {"name": "Lord Alexei Barov",        "entry": 10504, "dungeon": "Scholomance",         "level": 60},
    {"name": "Instructor Malicia",       "entry": 10505, "dungeon": "Scholomance",         "level": 60},
    {"name": "Ras Frostwhisper",         "entry": 10508, "dungeon": "Scholomance",         "level": 62},
    {"name": "Darkmaster Gandling",      "entry": 1853,  "dungeon": "Scholomance",         "level": 61},

    # ── Stratholme (58-60) ───────────────────────────────────────────────────
    {"name": "Magistrate Barthilas",     "entry": 10435, "dungeon": "Stratholme",          "level": 58},
    {"name": "Cannon Master Willey",     "entry": 10997, "dungeon": "Stratholme",          "level": 60},
    {"name": "Timmy the Cruel",          "entry": 10808, "dungeon": "Stratholme",          "level": 58},
    {"name": "Balnazzar",                "entry": 10813, "dungeon": "Stratholme",          "level": 62},
    {"name": "Baron Rivendare",          "entry": 10440, "dungeon": "Stratholme",          "level": 62},
]

# Flat entry ID list for DB queries
BRACKET_7_ALL_ENTRIES = [b["entry"] for b in DUNGEON_BOSS_POOL]

# Grouped by dungeon
DUNGEON_BOSS_POOL_BY_DUNGEON = {}
for _boss in DUNGEON_BOSS_POOL:
    DUNGEON_BOSS_POOL_BY_DUNGEON.setdefault(_boss["dungeon"], []).append(_boss)

# Script-triggered bosses that need special handling
SCRIPT_TRIGGERED_BOSSES = [b["name"] for b in DUNGEON_BOSS_POOL if b.get("note") == "script-triggered"]

# ---------------------------------------------------------------------------
# BRACKET CREATURE POOLS
# Entry IDs per bracket. Expand significantly using the DB query below.
#
#   SELECT entry, name, minlevel, maxlevel
#   FROM creature_template
#   WHERE minlevel >= {min} AND maxlevel <= {max}
#     AND ScriptName = ''
#     AND rank = 0
#     AND type IN (1,2,4,5,7)
#   ORDER BY RAND() LIMIT 50;
# ---------------------------------------------------------------------------

BRACKET_CREATURES = {
    # Bracket 1 — level 1-10 — 253 entries
    1: [
        705,  # Ragged Young Wolf
        707,  # Rockjaw Trogg
        1503,  # Wretched Zombie
        1508,  # Young Scavenger
        1984,  # Young Thistle Boar
        2031,  # Young Nightsaber
        2331,  # Paige Chaddis
        2955,  # Plainstrider
        3098,  # Mottled Boar
        3444,  # Dig Rat
        3680,  # Serpentbloom Snake
        3835,  # Biletoad
        4781,  # Snufflenose Gopher
        5404,  # Black Stallion
        5917,  # Clara Charles
        7507,  # Brown Snake
        7508,  # Black Kingsnake
        7509,  # Crimson Snake
        9699,  # Fire Beetle
        9700,  # Lava Crab
        10577,  # Crypt Scarab
        13338,  # Core Rat
        14361,  # Shen'dralar Wisp
        14496,  # Stormwind Orphan
        14499,  # Horde Orphan
        14869,  # Pygmy Cockatrice
        14884,  # Parasitic Serpent
        15010,  # Jungle Toad
        19163,  # Refugee Kid
        19164,  # Refugee Child
        22314,  # Captive Child
        22379,  # Serpentshrine Parasite
        22480,  # Brown Marmot
        69,  # Diseased Timber Wolf
        704,  # Ragged Timber Wolf
        724,  # Burly Rockjaw Trogg
        1445,  # Jesse Halloran
        1446,  # Regina Halloran
        1447,  # Gimlok Rumdnul
        1504,  # Young Night Web Spider
        1509,  # Ragged Scavenger
        1985,  # Thistle Boar
        2032,  # Mangy Nightsaber
        18651,  # Young Blanchy
        38,  # Defias Thug
        706,  # Frostmane Troll Whelp
        708,  # Small Crag Boar
        946,  # Frostmane Novice
        1354,  # Apprentice Soren
        1505,  # Night Web Spider
        1506,  # Scarlet Convert
        1507,  # Scarlet Initiate
        1513,  # Mangy Duskbat
        1718,  # Rockjaw Raider
        1986,  # Webwood Spider
        2952,  # Bristleback Quilboar
        2953,  # Bristleback Shaman
        2961,  # Mountain Cougar
        2966,  # Battleboar
        3101,  # Vile Familiar
        3124,  # Scorpid Worker
        2954,  # Bristleback Battleboar
        10556,  # Lazy Peon
        30,  # Forest Spider
        94,  # Defias Cutpurse
        103,  # Garrick Padfoot
        113,  # Stonetusk Boar
        475,  # Kobold Tunneler
        525,  # Mangy Wolf
        808,  # Grik'nir the Cold
        1125,  # Crag Boar
        1128,  # Young Black Bear
        1134,  # Young Wendigo
        1199,  # Juvenile Snow Leopard
        1433,  # Corbett Schneider
        1667,  # Meven Korgal
        1688,  # Night Web Matriarch
        1722,  # Andr'e
        1935,  # Tirisfal Farmhand
        1994,  # Githyiss the Vile
        1995,  # Strigid Owl
        1998,  # Webwood Lurker
        2006,  # Gnarlpine Ursa
        2007,  # Gnarlpine Gardener
        2022,  # Timberling
        2042,  # Nightsaber
        2307,  # Caretaker Caice
        2310,  # Jamie Nore
        2315,  # Maquell Ebonwood
        2949,  # Palemane Tanner
        2958,  # Prairie Wolf
        2969,  # Wiry Swoop
        2975,  # Venture Co. Hireling
        3106,  # Pygmy Surf Crawler
        3125,  # Clattering Scorpid
        3128,  # Kul Tiras Sailor
        3183,  # Yarrog Baneshadow
        3229,  # "Squealer" Thornmantle
        3626,  # Jenn Langston
        3627,  # Erich Lohan
        3629,  # David Langston
        8554,  # Chief Sharptusk Thornmantle
        40,  # Kobold Miner
        735,  # Murloc Streamrunner
        1129,  # Black Bear
        1138,  # Snow Tracker Wolf
        1535,  # Scarlet Warrior
          # Tirisfal Farmer
        2008,  # Gnarlpine Warrior
        2152,  # Gnarlpine Ambusher
        2950,  # Palemane Skinner
        2956,  # Adult Plainstrider
        2976,  # Venture Co. Laborer
        3099,  # Dire Mottled Boar
        3103,  # Makrura Clacker
        3104,  # Makrura Shellhide
        3111,  # Razormane Quilboar
        3119,  # Kolkar Drudge
        3122,  # Bloodtalon Taillasher
        3129,  # Kul Tiras Marine
        7235,  # Gnarlpine Mystic
        10805,  # Spotter Klemmy
        15949,  # Thaelis the Hungerer
        476,  # Kobold Geomancer
        524,  # Rockhide Boar
        1120,  # Frostmane Troll
        1127,  # Elder Crag Boar
        1131,  # Winter Wolf
        1196,  # Ice Claw Bear
        1201,  # Snow Leopard
        1536,  # Scarlet Missionary
        1543,  # Vile Fin Puddlejumper
        1922,  # Gray Forest Wolf
        1975,  # Eastvale Lumberjack
        1996,  # Strigid Screecher
        1999,  # Webwood Venomfang
        2009,  # Gnarlpine Shaman
        2010,  # Gnarlpine Defender
        2043,  # Nightsaber Stalker
        2951,  # Palemane Poacher
        2959,  # Prairie Stalker
        2962,  # Windfury Harpy
        2977,  # Venture Co. Taskmaster
        2983,  # The Plains Vision
        2989,  # Bael'dun Digger
        3035,  # Flatland Cougar
        3107,  # Surf Crawler
        3112,  # Razormane Scout
        3115,  # Dustwind Harpy
        3116,  # Dustwind Pillager
        3120,  # Kolkar Outrunner
        3121,  # Durotar Tiger
        3126,  # Armored Scorpid
        3570,  # Cleansed Timberling
        3939,  # Razormane Wolf
        43,  # Mine Spider
        60,  # Ruklar the Trapper
        97,  # Riverpaw Runt
        116,  # Defias Bandit
        583,  # Defias Ambusher
        822,  # Young Forest Bear
        880,  # Erlan Drudgemoor
        1115,  # Rockjaw Skullthumper
        1121,  # Frostmane Snowstrider
        1123,  # Frostmane Headhunter
        1133,  # Starving Winter Wolf
        1211,  # Leper Gnome
        1358,  # Miner Grothor
        1397,  # Frostmane Seer
        1537,  # Scarlet Zealot
        1544,  # Vile Fin Minor Oracle
        1660,  # Scarlet Bodyguard
        1949,  # Servant of Azora
        1997,  # Strigid Hunter
        2000,  # Webwood Silkspinner
        2011,  # Gnarlpine Augur
        2015,  # Bloodfeather Harpy
        2017,  # Bloodfeather Rogue
        2033,  # Elder Nightsaber
        2957,  # Elder Plainstrider
        2963,  # Windfury Wind Witch
        2967,  # Galak Centaur
        2971,  # Taloned Swoop
        2978,  # Venture Co. Worker
        2990,  # Bael'dun Appraiser
        3100,  # Elder Mottled Boar
        3105,  # Makrura Snapclaw
        3113,  # Razormane Dustrunner
        3123,  # Bloodtalon Scythemaw
        3141,  # Makrura Elder
        3192,  # Lieutenant Benedict
        3195,  # Burning Blade Thug
        3206,  # Voodoo Troll
        3207,  # Hexed Troll
        6911,  # Minion of Sethir
        6927,  # Defias Dockworker
        7234,  # Ferocitas the Dream Eater
        10803,  # Rifleman Wheeler
        10804,  # Rifleman Middlecamp
        11690,  # Gnarlpine Instigator
        14868,  # Hornsley
        474,  # Defias Rogue Wizard
        478,  # Riverpaw Outrunner
        732,  # Murloc Lurker
        881,  # Surena Caledon
        1116,  # Rockjaw Ambusher
        1117,  # Rockjaw Bonesnapper
        1122,  # Frostmane Hideskinner
        1124,  # Frostmane Shadowcaster
        1245,  # Kogan Forgestone
        1360,  # Miner Grumnal
        1538,  # Scarlet Friar
        1545,  # Vile Fin Muckdweller
        1555,  # Vicious Night Web Spider
        1662,  # Captain Perrine
        2012,  # Gnarlpine Pathfinder
        2013,  # Gnarlpine Avenger
        2018,  # Bloodfeather Sorceress
        2019,  # Bloodfeather Fury
        2020,  # Bloodfeather Wind Witch
        2029,  # Timberling Mire Beast
        2166,  # Oakenscowl
        2231,  # Pygmy Tide Crawler
        2960,  # Prairie Wolf Alpha
        2964,  # Windfury Sorceress
        2968,  # Galak Outrunner
        2979,  # Venture Co. Supervisor
        3108,  # Encrusted Surf Crawler
        3114,  # Razormane Battleguard
        3117,  # Dustwind Savage
        3127,  # Venomtail Scorpid
        3130,  # Thunder Lizard
        3196,  # Burning Blade Neophyte
        3197,  # Burning Blade Fanatic
        3232,  # Bristleback Interloper
        3566,  # Flatland Prowler
        6123,  # Dark Iron Spy
        6789,  # Thistle Cub
        356,  # Black Wolf
        358,  # Timber Wolf
        359,  # Winter Wolf
        1395,  # Ol' Beasley
        1981,  # Dark Iron Ambusher
        1993,  # Greenpaw
        3204,  # Gazz'uz
        3205,  # Zalazane
        4068,  # Serpent Messenger
        6846,  # Defias Dockmaster
        6866,  # Defias Bodyguard
        7318,  # Rageclaw
        14329,  # Black War Wolf
        15408,  # Spearcrafter Otembe
        15409,  # Old Whitebark
    ],

    # Bracket 2 — level 11-20 — 269 entries
    2: [
        1118,  # Rockjaw Backbreaker
        1161,  # Stonesplinter Trogg
        1162,  # Stonesplinter Scout
        1176,  # Tunnel Rat Forager
        1186,  # Elder Black Bear
        1202,  # Tunnel Rat Kobold
        1664,  # Captain Vachon
        1766,  # Mottled Worg
        1770,  # Moonrage Darkrunner
        1778,  # Ferocious Grizzled Bear
        1961,  # Mangeclaw
        2021,  # Bloodfeather Matriarch
        2190,  # Wild Grell
        2201,  # Greymist Raider
        2321,  # Foreststrider Fledgling
        3058,  # Arra'chea
        3231,  # Corrupted Dreadmaw Crocolisk
        3244,  # Greater Plainstrider
        3254,  # Sunscale Lashtail
        3265,  # Razormane Hunter
        3380,  # Burning Blade Acolyte
        3415,  # Savannah Huntress
        5613,  # Doyo'da
        6093,  # Dead-Tooth Jack
        6390,  # Ulag the Cleaver
        10159,  # Young Moonkin
        15407,  # Chieftain Zul'Marosh
        1174,  # Tunnel Rat Geomancer
        1175,  # Tunnel Rat Digger
        1193,  # Loch Frenzy
        1665,  # Captain Melrache
        1767,  # Vile Fin Shredder
        1779,  # Moonrage Glutton
        1780,  # Moss Stalker
        1797,  # Giant Grizzled Bear
        2039,  # Ursal the Mauler
        2167,  # Blackwood Pathfinder
        2185,  # Darkshore Thresher
        2202,  # Greymist Coastrunner
        2212,  # Deth'ryll Satyr
        2232,  # Tide Crawler
        3203,  # Fizzle Darkstorm
        3243,  # Savannah Highmane
        3246,  # Fleeting Plainstrider
        3266,  # Razormane Defender
        3269,  # Razormane Geomancer
        3272,  # Kolkar Wrangler
        3381,  # Southsea Brigand
        6909,  # Sethir the Ancient
        7319,  # Lady Sathrah
        10160,  # Raging Moonkin
        11816,  # Una Ji'ro
        12138,  # Lunaclaw
        13157,  # Makasgar
        13158,  # Lieutenant Sanders
        13159,  # James Clark
        17673,  # Stinkhorn Striker
        1163,  # Stonesplinter Skullthumper
        1166,  # Stonesplinter Seer
        1184,  # Cliff Lurker
        1188,  # Grizzled Black Bear
        1768,  # Vile Fin Tidehunter
        1781,  # Mist Creeper
        1782,  # Moonrage Darksoul
        1867,  # Dalaran Apprentice
        1891,  # Pyrewood Watcher
        1892,  # Moonrage Watcher
        2203,  # Greymist Seer
        2324,  # Blackwood Windtalker
        3242,  # Zhevra Runner
        3255,  # Sunscale Screecher
        3271,  # Razormane Mystic
        3273,  # Kolkar Stormer
        3285,  # Venture Co. Peon
        3382,  # Southsea Cannoneer
        3695,  # Grimclaw
        4316,  # Kolkar Packhound
        10157,  # Moonkin Oracle
        12320,  # Burning Blade Crusher
        16292,  # Aquantion
        1177,  # Tunnel Rat Surveyor
        1191,  # Mangy Mountain Boar
        1693,  # Loch Crocolisk
        1893,  # Moonrage Sentry
        1896,  # Moonrage Elder
        1912,  # Dalaran Protector
        2069,  # Moonstalker
        2149,  # Dark Iron Raider
        2173,  # Reef Frenzy
        2174,  # Coastal Frenzy
        2204,  # Greymist Netter
        2322,  # Foreststrider
        2540,  # Dalaran Serpent
        3274,  # Kolkar Pack Runner
        3276,  # Witchwing Harpy
        3284,  # Venture Co. Drudger
        3383,  # Southsea Cutthroat
        3384,  # Southsea Privateer
        3425,  # Savannah Prowler
        3533,  # Moonrage Leatherworker
        4263,  # Deepmoss Hatchling
        8236,  # Muck Frenzy
        11713,  # Blackwood Tracker
        11910,  # Grimtotem Ruffian
        11911,  # Grimtotem Mercenary
        12319,  # Burning Blade Toxicologist
        17324,  # Irradiated Wildkin
        1164,  # Stonesplinter Bonesnapper
        1194,  # Mountain Buzzard
        1197,  # Stonesplinter Shaman
        1777,  # Dakk Blunderblast
        1914,  # Dalaran Mage
        1924,  # Moonrage Bloodhowler
        1953,  # Lake Skulker
        1972,  # Grimson the Pale
        2179,  # Stormscale Wave Rider
        2205,  # Greymist Warrior
        2235,  # Reef Crawler
        2361,  # Tamara Armstrong
        2362,  # Hemmit Armstrong
        3241,  # Savannah Patriarch
        3248,  # Barrens Giraffe
        3275,  # Kolkar Marauder
        3277,  # Witchwing Roguefeather
        3282,  # Venture Co. Mercenary
        3438,  # Kreenig Snarlsnout
        3461,  # Oasis Snapjaw
        4008,  # Cliff Stormer
        4127,  # Hecklefang Hyena
        4625,  # Death's Head Ward Keeper
        11912,  # Grimtotem Brute
        11913,  # Grimtotem Sorcerer
        12321,  # Stormscale Toxicologist
        16238,  # Night Elf Ambusher
        1189,  # Black Bear Patriarch
        1192,  # Elder Mountain Boar
        1913,  # Dalaran Warder
        1923,  # Bloodsnout Worg
        1954,  # Elder Lake Skulker
        1957,  # Vile Fin Shorecreeper
        2106,  # Apothecary Berard
        2165,  # Grizzled Thistle Bear
        2168,  # Blackwood Warrior
        2180,  # Stormscale Siren
        2187,  # Elder Darkshore Thresher
        2206,  # Greymist Hunter
        2336,  # Dark Strand Fanatic
        2338,  # Twilight Disciple
        3245,  # Ornery Plainstrider
        3256,  # Sunscale Scytheclaw
        3260,  # Bristleback Water Seeker
        3278,  # Witchwing Slayer
        3283,  # Venture Co. Enforcer
        3417,  # Living Flame
        3471,  # Tinkerer Sniggles
        3475,  # Echeyakee
        4005,  # Deepmoss Creeper
        6492,  # Rift Spawn
        6570,  # Fenwick Thatros
        6606,  # Overseer Glibby
        6787,  # Yelnagi Blackarm
        11714,  # Marosh the Devious
        11915,  # Gogger Rock Keeper
        11917,  # Gogger Geomancer
        16242,  # Tranquillien Scout
        598,  # Defias Miner
        1165,  # Stonesplinter Geomancer
        1185,  # Wood Lurker
        1222,  # Dark Iron Sapper
        1915,  # Dalaran Conjuror
        1955,  # Lake Creeper
        1958,  # Vile Fin Tidecaller
        2169,  # Blackwood Totemic
        2237,  # Moonstalker Sire
        2323,  # Giant Foreststrider
        2339,  # Twilight Thug
        3258,  # Bristleback Hunter
        3279,  # Witchwing Ambusher
        3280,  # Witchwing Windcaller
        3286,  # Venture Co. Overseer
        3416,  # Savannah Matriarch
        3655,  # Mad Magglish
        3990,  # Venture Co. Cutter
        4007,  # Deepmoss Venomspitter
        4071,  # Venture Co. Grinder
        11914,  # Gorehoof the Black
        11918,  # Gogger Stonepounder
        450,  # Defias Renegade Mage
        1167,  # Stonesplinter Digger
        1169,  # Dark Iron Insurgent
        1178,  # Mo'grosh Ogre
        1179,  # Mo'grosh Enforcer
        1181,  # Mo'grosh Shaman
        1888,  # Dalaran Watcher
        1909,  # Vile Fin Lakestalker
        1956,  # Elder Lake Creeper
        2053,  # Haggard Refugee
        2156,  # Cracked Golem
        2158,  # Gravelflint Scout
        2170,  # Blackwood Ursa
        2181,  # Stormscale Myrmidon
        2207,  # Greymist Oracle
        2233,  # Encrusted Tide Crawler
        3240,  # Stormsnout
        3247,  # Thunderhawk Hatchling
        3261,  # Bristleback Thornweaver
        3395,  # Verog the Dervish
        3445,  # Supervisor Lugwizzle
        3463,  # Wandering Barrens Giraffe
        3503,  # Silithid Protector
        3713,  # Wrathtail Wave Rider
        3717,  # Wrathtail Sorceress
        3725,  # Dark Strand Cultist
        3728,  # Dark Strand Adept
        3732,  # Forsaken Seeker
        3733,  # Forsaken Herbalist
        3816,  # Wild Buck
        3989,  # Venture Co. Logger
        4009,  # Raging Cliff Stormer
        4129,  # Hecklefang Snarler
        6020,  # Slimeshell Makrura
        6788,  # Den Mother
        11858,  # Grundig Darkcloud
        1180,  # Mo'grosh Brute
        1183,  # Mo'grosh Mystic
        1224,  # Young Threshadon
        1393,  # Berserk Trogg
        1889,  # Dalaran Wizard
        1908,  # Vile Fin Oracle
        2054,  # Sickly Refugee
        2071,  # Moonstalker Matriarch
        2103,  # Dragonmaw Scout
        2157,  # Stone Behemoth
        2159,  # Gravelflint Bonesnapper
        2171,  # Blackwood Shaman
        2182,  # Stormscale Sorceress
        2208,  # Greymist Tidehunter
        3257,  # Ishamuhale
        3263,  # Bristleback Geomancer
        3396,  # Hezrul Bloodmark
        3454,  # Cannoneer Smythe
        3455,  # Cannoneer Whessan
        3712,  # Wrathtail Razortail
        3715,  # Wrathtail Sea Witch
        3730,  # Dark Strand Excavator
        3737,  # Saltspittle Puddlejumper
        3739,  # Saltspittle Warrior
        3812,  # Clattering Crawler
        3823,  # Ghostpaw Runner
        3988,  # Venture Co. Operator
        3991,  # Venture Co. Deforester
        4001,  # Windshear Tunnel Rat
        4006,  # Deepmoss Webspinner
        4011,  # Young Pridewing
        1437,  # Thomas Booker
        1476,  # Hargin Mundar
        1479,  # Timothy Clark
        1480,  # Caitlin Grassman
        1482,  # Andrea Halloran
        1483,  # Murphy West
        1484,  # Derina Rumdnul
        1947,  # Thule Ravenclaw
        2099,  # Maiden's Virtue Crewman
        3251,  # Silithid Grub
        3393,  # Captain Fairmount
        3452,  # Serena Bloodfeather
        3734,  # Forsaken Thug
        10581,  # Young Arikara
        11920,  # Goggeroc
    ],

    # Bracket 3 — level 21-30 — 277 entries
    3: [
        1008,  # Mosshide Mongrel
        1025,  # Bluegill Puddlejumper
        1111,  # Leech Stalker
        1417,  # Young Wetlands Crocolisk
        2244,  # Syndicate Shadow Mage
        2260,  # Syndicate Rogue
        2332,  # Valdred Moray
        2351,  # Gray Bear
        3252,  # Silithid Swarmer
        3374,  # Bael'dun Excavator
        3780,  # Shadethicket Moss Eater
        3809,  # Ashenvale Bear
        3879,  # Dark Strand Assassin
        3993,  # Venture Co. Machine Smith
        3999,  # Windshear Digger
        4004,  # Windshear Overlord
        4012,  # Pridewing Wyvern
        4040,  # Cave Stalker
        11921,  # Besseleth
        12859,  # Splintertree Raider
        12897,  # Silverwing Warrior
        1009,  # Mosshide Mistweaver
        1010,  # Mosshide Fenrunner
        1020,  # Mottled Raptor
        1026,  # Bluegill Forager
        2120,  # Archmage Ataeric
        2354,  # Vicious Gray Bear
        3375,  # Bael'dun Foreman
        3457,  # Razormane Stalker
        3474,  # Lakota'mani
        3783,  # Shadethicket Raincaller
        3817,  # Shadowhorn Stag
        4002,  # Windshear Stonecutter
        4014,  # Pridewing Consort
        4018,  # Antlered Courser
        4033,  # Charred Stone Spirit
        4264,  # Deepmoss Matriarch
        6141,  # Pridewing Soarer
        7287,  # Foreman Silixiz
        7308,  # Venture Co. Patroller
        12896,  # Silverwing Sentinel
        1011,  # Mosshide Trapper
        1015,  # Highland Raptor
        1028,  # Bluegill Muckdweller
        1034,  # Dragonmaw Raider
        1035,  # Dragonmaw Swamprunner
        1038,  # Dragonmaw Shadowwarder
        1042,  # Red Whelp
        1057,  # Dragonmaw Bonewarder
        1400,  # Wetlands Crocolisk
        2188,  # Deep Sea Threshadon
        2384,  # Starving Mountain Lion
        3249,  # Greater Thunderhawk
        3376,  # Bael'dun Soldier
        3458,  # Razormane Seer
        3736,  # Darkslayer Mordenthal
        3743,  # Foulweald Warrior
        3745,  # Foulweald Pathfinder
        3750,  # Foulweald Totemic
        3781,  # Shadethicket Wood Shaper
        3824,  # Ghostpaw Howler
        3893,  # Forsaken Scout
        3917,  # Befouled Water Elemental
        3921,  # Thistlefur Ursa
        3922,  # Thistlefur Totemic
        3923,  # Thistlefur Den Watcher
        3924,  # Thistlefur Shaman
        3925,  # Thistlefur Avenger
        3926,  # Thistlefur Pathfinder
        4013,  # Pridewing Skyhunter
        4022,  # Bloodfury Harpy
        4025,  # Bloodfury Ambusher
        4032,  # Young Chimaera
        4036,  # Rogue Flame Spirit
        4044,  # Blackened Basilisk
        4051,  # Cenarion Botanist
        4067,  # Twilight Runner
        6132,  # Razorfen Servitor
        6668,  # Lord Cyrik Blackforge
        7307,  # Venture Co. Lookout
        12856,  # Ashenvale Outrunner
        12921,  # Enraged Foulweald
        1012,  # Mosshide Brute
        1016,  # Highland Lashtail
        1021,  # Mottled Screecher
        1027,  # Bluegill Warrior
        1036,  # Dragonmaw Centurion
        1040,  # Fen Creeper
        1043,  # Lost Whelp
        2275,  # Enraged Stanley
        2349,  # Giant Moss Creeper
        3377,  # Bael'dun Rifleman
        3459,  # Razormane Warfrenzy
        3473,  # Owatanka
        3664,  # Ilkrud Magthrull
        3746,  # Foulweald Den Watcher
        3748,  # Foulweald Shaman
        3749,  # Foulweald Ursa
        3820,  # Wildthorn Venomspitter
        4016,  # Fey Dragon
        4019,  # Great Courser
        4026,  # Bloodfury Windcaller
        4034,  # Enraged Stone Spirit
        4037,  # Burning Ravager
        4094,  # Galak Scout
        4096,  # Galak Windchaser
        5409,  # Harvester Swarm
        12860,  # Duriel Moonfire
        1013,  # Mosshide Mystic
        1017,  # Highland Scytheclaw
        1022,  # Mottled Scytheclaw
        1029,  # Bluegill Oracle
        1041,  # Fen Lord
        1069,  # Crimson Whelp
        1413,  # Janey Anship
        1414,  # Lisan Pierce
        1679,  # Avarus Kharag
        2089,  # Giant Wetlands Crocolisk
        2330,  # Karlee Chaddis
        2356,  # Elder Gray Bear
        2449,  # Citizen Wilkes
        3435,  # Lok Orcbane
        3472,  # Washte Pawne
        3782,  # Shadethicket Stone Mover
        3797,  # Cenarion Protector
        3810,  # Elder Ashenvale Bear
        3950,  # Minor Water Guardian
        3986,  # Sarilus Foulborne
        3987,  # Dal Bloodclaw
        4023,  # Bloodfury Roguefeather
        4024,  # Bloodfury Slayer
        4028,  # Charred Ancient
        4031,  # Fledgling Chimaera
        4042,  # Singed Basilisk
        4093,  # Galak Wrangler
        4098,  # Galak Pack Runner
        4112,  # Gravelsnout Vermin
        4117,  # Cloud Serpent
        6913,  # Lost One Rift Traveler
        7779,  # Priestess Tyriona
        10758,  # Grimtotem Bandit
        10760,  # Grimtotem Geomancer
        11979,  # Kim Bridenbecker
        11994,  # Rob Bridenbecker
        1023,  # Mottled Razormaw
        1044,  # Flamesnorting Whelp
        2091,  # Chieftain Nek'rosh
        2348,  # Elder Moss Creeper
        2372,  # Mudsnout Gnoll
        3378,  # Bael'dun Officer
        3815,  # Blink Dragon
        3818,  # Elder Shadowhorn Stag
        3833,  # Cenarion Vindicator
        3919,  # Withered Ancient
        4017,  # Wily Fey Dragon
        4027,  # Bloodfury Storm Witch
        4035,  # Furious Stone Spirit
        4038,  # Burning Destroyer
        4097,  # Galak Stormer
        4099,  # Galak Marauder
        4111,  # Gravelsnout Kobold
        4118,  # Venomous Cloud Serpent
        4248,  # Pesterhide Hyena
        10617,  # Galak Messenger
        10759,  # Grimtotem Stomper
        12918,  # Chief Murgut
        20001,  # Mountain Lion Mother
        1014,  # Mosshide Alpha
        1018,  # Highland Razormaw
        1051,  # Dark Iron Dwarf
        2373,  # Mudsnout Shaman
        2385,  # Feral Mountain Lion
        2503,  # Hillsbrad Foreman
        3476,  # Isha Awak
        3825,  # Ghostpaw Alpha
        3834,  # Crazed Ancient
        3932,  # Bloodtooth Guard
        4029,  # Blackened Ancient
        4041,  # Scorched Basilisk
        4095,  # Galak Mauler
        4114,  # Gravelsnout Forager
        4119,  # Elder Cloud Serpent
        4124,  # Needles Cougar
        6523,  # Dark Iron Rifleman
        10720,  # Galak Assassin
        10757,  # Boiling Elemental
        12759,  # Tideress
        1052,  # Dark Iron Saboteur
        1418,  # Bluegill Raider
        2337,  # Dark Strand Voidcaller
        2344,  # Dun Garok Mountaineer
        2368,  # Daggerspine Shorestalker
        2374,  # Torn Fin Muckdweller
        3804,  # Forsaken Intruder
        3808,  # Forsaken Dark Stalker
        3821,  # Wildthorn Lurker
        4100,  # Screeching Harpy
        4107,  # Highperch Wyvern
        4109,  # Highperch Consort
        4113,  # Gravelsnout Digger
        4120,  # Thundering Boulderkin
        4249,  # Pesterhide Snarler
        6139,  # Highperch Soarer
        6167,  # Chimaera Matriarch
        10756,  # Scalding Elemental
        10761,  # Grimtotem Reaver
        11683,  # Warsong Shaman
        1019,  # Elder Razormaw
        1053,  # Dark Iron Tunneler
        1353,  # Sarltooth
        2345,  # Dun Garok Rifleman
        2346,  # Dun Garok Priest
        2363,  # Apprentice Honeywell
        2370,  # Daggerspine Screamer
        2375,  # Torn Fin Coastrunner
        3791,  # Terrowulf Shadow Weaver
        3806,  # Forsaken Infiltrator
        3807,  # Forsaken Assassin
        3811,  # Giant Ashenvale Bear
        4101,  # Screeching Roguefeather
        4116,  # Gravelsnout Surveyor
        4273,  # Keeper Ordanus
        4661,  # Gelkis Rumbler
        10896,  # Arnak Grimtotem
        11682,  # Warsong Grunt
        1072,  # Roggo Harlbarrow
        1276,  # Mountaineer Brokk
        1277,  # Mountaineer Ganin
        1278,  # Mountaineer Stenn
        1279,  # Mountaineer Flint
        1280,  # Mountaineer Droken
        1281,  # Mountaineer Zaren
        1282,  # Mountaineer Veek
        1283,  # Mountaineer Kalmir
        1329,  # Mountaineer Naarh
        1330,  # Mountaineer Tyraw
        1331,  # Mountaineer Luxst
        1332,  # Mountaineer Morran
        1334,  # Mountaineer Hammerfall
        1335,  # Mountaineer Yuttha
        1336,  # Mountaineer Zwarn
        1337,  # Mountaineer Gwarth
        1338,  # Mountaineer Dalk
        1477,  # Christoph Faral
        1478,  # Aedis Brom
        2105,  # Mountaineer Dokkin
        2305,  # Foreman Bonds
        2335,  # Magistrate Burnside
        2466,  # Mountaineer Grugelm
        2468,  # Mountaineer Thar
        2469,  # Mountaineer Rharen
        2506,  # Mountaineer Harn
        2507,  # Mountaineer Uthan
        2508,  # Mountaineer Wuar
        2509,  # Mountaineer Cragg
        2510,  # Mountaineer Ozmok
        2511,  # Mountaineer Bludd
        2512,  # Mountaineer Roghan
        2513,  # Mountaineer Janha
        2514,  # Mountaineer Modax
        2515,  # Mountaineer Fazgard
        2516,  # Mountaineer Kamdar
        2517,  # Mountaineer Langarr
        2518,  # Mountaineer Swarth
        2524,  # Mountaineer Haggis
        2525,  # Mountaineer Barn
        2526,  # Mountaineer Morlic
        2527,  # Mountaineer Angst
        2528,  # Mountaineer Haggil
        3696,  # Ran Bloodtooth
        3931,  # Shadethicket Oracle
        4104,  # Screeching Windcaller
        4311,  # Holgar Stormaxe
        5042,  # Nurse Lillian
        6575,  # Scarlet Trainee
        12996,  # Mounted Ironforge Mountaineer
        13076,  # Dun Morogh Mountaineer
    ],

    # Bracket 4 — level 31-40 — 285 entries
    4: [
        754,  # Rebel Watchman
        905,  # Sharptooth Frenzy
        1364,  # Balgaras the Foul
        2249,  # Ferocious Yeti
        2271,  # Dalaran Shield Guard
        2371,  # Daggerspine Siren
        2377,  # Torn Fin Tidehunter
        2553,  # Witherbark Shadowcaster
        2575,  # Dark Iron Supplier
        2577,  # Dark Iron Shadowcaster
        2578,  # Young Mesa Buzzard
        2581,  # Dabyrie Militia
        2589,  # Syndicate Mercenary
        4140,  # Scorpid Reaver
        4634,  # Kolkar Mauler
        4635,  # Kolkar Windchaser
        4665,  # Burning Blade Adept
        4666,  # Burning Blade Felsworn
        4728,  # Gritjaw Basilisk
        12676,  # Sharptalon
        20363,  # Caretaker Smithers
        682,  # Stranglethorn Tiger
        775,  # Kurzen's Agent
        937,  # Kurzen Jungle Fighter
        940,  # Kurzen Medicine Man
        976,  # Kurzen War Tiger
        977,  # Kurzen War Panther
        1108,  # Mistvale Gorilla
        2240,  # Syndicate Footpad
        2250,  # Mountain Yeti
        2272,  # Dalaran Theurgist
        2304,  # Captain Ironhill
        2406,  # Mountain Lion
        2440,  # Drunken Footpad
        2554,  # Witherbark Axe Thrower
        2562,  # Boulderfist Ogre
        2563,  # Plains Creeper
        2587,  # Syndicate Pathstalker
        4144,  # Sparkleshell Borer
        4151,  # Saltstone Crystalhide
        4158,  # Salt Flats Vulture
        4636,  # Kolkar Battle Lord
        4637,  # Kolkar Destroyer
        4646,  # Gelkis Outrunner
        4647,  # Gelkis Scout
        4667,  # Burning Blade Shadowmage
        4692,  # Dread Swoop
        4711,  # Slitherblade Naga
        4712,  # Slitherblade Sorceress
        11578,  # Whirlwind Shredder
        587,  # Bloodscalp Warrior
        685,  # Stranglethorn Raptor
        694,  # Bloodscalp Axe Thrower
        697,  # Bloodscalp Shaman
        702,  # Bloodscalp Scavenger
        856,  # Young Lashtail Raptor
        2241,  # Syndicate Thief
        2251,  # Giant Yeti
        2407,  # Hulking Mountain Lion
        2555,  # Witherbark Witch Doctor
        2560,  # Highland Thrasher
        2564,  # Boulderfist Enforcer
        2618,  # Hammerfall Peon
        2628,  # Dalaran Worker
        4139,  # Scorpid Terror
        4479,  # Fardel Dabyrie
        4648,  # Gelkis Stamper
        4649,  # Gelkis Windchaser
        4688,  # Bonepaw Hyena
        4713,  # Slitherblade Warrior
        4726,  # Raging Thunder Lizard
        6238,  # Big Will
        7872,  # Death's Head Cultist
        7873,  # Razorfen Battleguard
        7874,  # Razorfen Thornweaver
        11562,  # Drysnap Crawler
        12976,  # Kolkar Waylayer
        13019,  # Burning Blade Seer
        588,  # Bloodscalp Scout
        595,  # Bloodscalp Hunter
        689,  # Crystal Spine Basilisk
        698,  # Bloodscalp Tiger
        699,  # Bloodscalp Beastmaster
        701,  # Bloodscalp Mystic
        921,  # Venture Co. Lumberjack
        938,  # Kurzen Commando
        941,  # Kurzen Headshrinker
        943,  # Kurzen Wrangler
        1085,  # Elder Stranglethorn Tiger
        1094,  # Venture Co. Miner
        1097,  # Venture Co. Mechanic
        2252,  # Crushridge Ogre
        2358,  # Dalaran Summoner
        2556,  # Witherbark Headhunter
        2579,  # Mesa Buzzard
        2619,  # Hammerfall Grunt
        4143,  # Sparkleshell Snapper
        4150,  # Saltstone Gazer
        4481,  # Marcel Dabyrie
        4651,  # Gelkis Earthcaller
        4697,  # Scorpashi Lasher
        4714,  # Slitherblade Myrmidon
        4718,  # Slitherblade Oracle
        4971,  # Slim's Friend
        11563,  # Drysnap Pincer
        12977,  # Kolkar Ambusher
        686,  # Lashtail Raptor
        815,  # Bookie Herod
        871,  # Saltscale Warrior
        877,  # Saltscale Forager
        879,  # Saltscale Hunter
        1096,  # Venture Co. Geologist
        1151,  # Saltwater Crocolisk
        1152,  # Snapjaw Crocolisk
        2242,  # Syndicate Spy
        2253,  # Crushridge Brute
        2318,  # Argus Shadow Mage
        2319,  # Syndicate Wizard
        2379,  # Caretaker Smithers
        2557,  # Witherbark Shadow Hunter
        2565,  # Giant Plains Creeper
        2566,  # Boulderfist Brute
        2572,  # Drywhisker Kobold
        2590,  # Syndicate Conjuror
        2727,  # Crag Coyote
        2739,  # Shadowforge Tunneler
        2829,  # Starving Buzzard
        2906,  # Dustbelcher Warrior
        4358,  # Mirefin Puddlejumper
        4413,  # Darkfang Spider
        4457,  # Murkgill Forager
        4458,  # Murkgill Hunter
        4461,  # Murkgill Warrior
        4480,  # Kenata Dabyrie
        4545,  # Nag'zehn
        4546,  # Bor'zehn
        4547,  # Tarkreu Shadowstalker
        4652,  # Gelkis Mauler
        4653,  # Gelkis Marauder
        4695,  # Carrion Horror
        4715,  # Slitherblade Razortail
        4719,  # Slitherblade Sea Witch
        4729,  # Hulking Gritjaw Basilisk
        4844,  # Shadowforge Surveyor
        4845,  # Shadowforge Ruffian
        4846,  # Shadowforge Digger
        6013,  # Wayward Buzzard
        6068,  # Warug's Bodyguard
        7175,  # Stonevault Ambusher
        10676,  # Raider Jhash
        10682,  # Raider Kerr
        11577,  # Whirlwind Stormwalker
        597,  # Bloodscalp Berserker
        671,  # Bloodscalp Headhunter
        691,  # Lesser Water Elemental
        854,  # Young Jungle Stalker
        873,  # Saltscale Oracle
        939,  # Kurzen Elite
        942,  # Kurzen Witch Doctor
        1095,  # Venture Co. Workboss
        1142,  # Mosh'Ogg Brute
        1144,  # Mosh'Ogg Witch Doctor
        2243,  # Syndicate Sentry
        2254,  # Crushridge Mauler
        2416,  # Crushridge Plunderer
        2558,  # Witherbark Berserker
        2561,  # Highland Fleshstalker
        2567,  # Boulderfist Magus
        2574,  # Drywhisker Digger
        2588,  # Syndicate Prowler
        2731,  # Ridge Stalker
        2733,  # Apothecary Jorell
        2738,  # Stromgarde Cavalryman
        2740,  # Shadowforge Darkweaver
        4342,  # Drywallow Vicejaw
        4396,  # Mudrock Tortoise
        4400,  # Mudrock Snapjaw
        4411,  # Darkfang Lurker
        4459,  # Murkgill Oracle
        4690,  # Rabid Bonepaw
        4693,  # Dread Flyer
        4716,  # Slitherblade Tidehunter
        4851,  # Stonevault Rockchewer
        4856,  # Stonevault Cave Hunter
        5643,  # Tyranis Malem
        7078,  # Cleft Scorpid
        13737,  # Marandis' Sister
        660,  # Bloodscalp Witch Doctor
        684,  # Shadowmaw Panther
        729,  # Sin'Dall
        772,  # Stranglethorn Tigress
        875,  # Saltscale Tide Lord
        1114,  # Jungle Thunderer
        2245,  # Syndicate Saboteur
        2255,  # Crushridge Mage
        2569,  # Boulderfist Mauler
        2573,  # Drywhisker Surveyor
        2580,  # Elder Mesa Buzzard
        2583,  # Stromgarde Troll Hunter
        2584,  # Stromgarde Defender
        2591,  # Syndicate Magus
        2728,  # Feral Crag Coyote
        2735,  # Lesser Rock Elemental
        2892,  # Stonevault Seer
        2907,  # Dustbelcher Mystic
        2932,  # Magregan Deepshadow
        4355,  # Bloodfen Scytheclaw
        4360,  # Mirefin Warrior
        4377,  # Darkmist Hatchling
        4460,  # Murkgill Lord
        4504,  # Frostmaw
        4654,  # Maraudine Scout
        4655,  # Maraudine Wrangler
        4660,  # Maraudine Bonepaw
        4727,  # Elder Thunder Lizard
        6733,  # Stonevault Basher
        7405,  # Deadly Cleft Scorpid
        814,  # Sergeant Malthus
        978,  # Kurzen Subchief
        979,  # Kurzen Shadow Hunter
        2246,  # Syndicate Assassin
        2256,  # Crushridge Enforcer
        2570,  # Boulderfist Shaman
        2585,  # Stromgarde Vindicator
        2592,  # Rumbling Exile
        2595,  # Daggerspine Raider
        2612,  # Lieutenant Valorcall
        2635,  # Elder Saltwater Crocolisk
        2636,  # Blackwater Deckhand
        2701,  # Dustbelcher Ogre
        2723,  # Stone Golem
        2732,  # Ridge Huntress
        2742,  # Shadowforge Chanter
        2743,  # Shadowforge Warrior
        2760,  # Burning Exile
        2761,  # Cresting Exile
        2762,  # Thundering Exile
        4656,  # Maraudine Mauler
        4657,  # Maraudine Windchaser
        4668,  # Burning Blade Summoner
        4699,  # Scorpashi Venomlash
        4723,  # Foreman Cozzle
        7011,  # Earthen Rocksmasher
        7012,  # Earthen Sculptor
        7076,  # Earthen Guardian
        7077,  # Earthen Hallshaper
        7091,  # Shadowforge Ambusher
        7309,  # Earthen Custodian
        12369,  # Lord Kragaru
        92,  # Rock Elemental
        667,  # Skullsplitter Warrior
        690,  # Cold Eye Basilisk
        696,  # Skullsplitter Axe Thrower
        780,  # Skullsplitter Mystic
        2247,  # Syndicate Enforcer
        2287,  # Crushridge Warmonger
        2571,  # Boulderfist Lord
        2596,  # Daggerspine Sorceress
        2715,  # Dustbelcher Brute
        2729,  # Elder Crag Coyote
        2793,  # Kor'gresh Coldrage
        2893,  # Stonevault Bonesnapper
        4398,  # Mudrock Burrower
        4658,  # Maraudine Stormer
        4659,  # Maraudine Marauder
        4705,  # Burning Blade Invoker
        7396,  # Earthen Stonebreaker
        7397,  # Earthen Stonecarver
        11559,  # Outcast Necromancer
        728,  # Bhag'thera
        813,  # Colonel Kurzen
        2306,  # Baron Vardus
        2421,  # Muckrake
        2737,  # Durtham Greldon
        2773,  # Or'Kalar
        2776,  # Vengeful Surge
        2783,  # Marez Cowl
        2915,  # Hammertoe's Spirit
        5696,  # Gerard Abernathy
        5699,  # Leona Tharpe
        5702,  # Jezelle Pruitt
        5771,  # Jugkar Grim'rod
        5773,  # Jugkar Grim'rod's Image
        8055,  # Thelsamar Mountaineer
        12903,  # Splintertree Guard
    ],

    # Bracket 5 — level 41-50 — 272 entries
    5: [
        669,  # Skullsplitter Hunter
        670,  # Skullsplitter Witch Doctor
        676,  # Venture Co. Surveyor
        709,  # Mosh'Ogg Warmonger
        756,  # Skullsplitter Panther
        782,  # Skullsplitter Scout
        784,  # Skullsplitter Beastmaster
        1511,  # Enraged Silverback Gorilla
        1550,  # Thrashtail Basilisk
        1565,  # Bloodsail Sea Dog
        1653,  # Bloodsail Elder Magus
        2423,  # Lord Aliden Perenolde
        2521,  # Skymane Gorilla
        2522,  # Jaguero Stalker
        2650,  # Witherbark Zealot
        2717,  # Dustbelcher Mauler
        2725,  # Scalding Whelp
        2923,  # Mangy Silvermane
        2944,  # Boss Tho'grun
        4505,  # Bloodsail Deckhand
        5237,  # Gordunni Ogre Mage
        5251,  # Woodpaw Trapper
        5253,  # Woodpaw Brute
        5268,  # Ironfur Bear
        5307,  # Vale Screecher
        5332,  # Hatecrest Wave Rider
        5335,  # Hatecrest Screamer
        5425,  # Starving Blisterpaw
        5618,  # Wastewander Bandit
        7726,  # Grimtotem Naturalist
        8276,  # Soaring Razorbeak
        10696,  # Refuge Pointe Defender
        11778,  # Shadowshard Smasher
        11786,  # Ambereye Reaver
        11788,  # Rock Worm
        675,  # Venture Co. Foreman
        1558,  # Silverback Patriarch
        1559,  # King Mukla
        1713,  # Elder Shadowmaw Panther
        2548,  # Captain Keelhaul
        2549,  # Garr Salthoof
        2550,  # Captain Stillwater
        2651,  # Witherbark Hideskinner
        2718,  # Dustbelcher Shaman
        2730,  # Rabid Crag Coyote
        2736,  # Greater Rock Elemental
        2791,  # Enraged Rock Elemental
        2927,  # Vicious Owlbeast
        2945,  # Murdaloc
        4399,  # Mudrock Borer
        5232,  # Gordunni Brute
        5254,  # Woodpaw Mystic
        5255,  # Woodpaw Reaver
        5260,  # Groddoc Ape
        5331,  # Hatecrest Warrior
        5337,  # Hatecrest Siren
        5402,  # Khan Hratha
        5419,  # Glasshide Basilisk
        5617,  # Wastewander Shadow Mage
        5623,  # Wastewander Assassin
        7725,  # Grimtotem Raider
        8337,  # Dark Iron Steelshifter
        8876,  # Sandfury Acolyte
        11782,  # Ambershard Destroyer
        14123,  # Steeljaw Snapper
        678,  # Mosh'Ogg Mauler
        679,  # Mosh'Ogg Shaman
        710,  # Mosh'Ogg Spellcrafter
        781,  # Skullsplitter Headhunter
        783,  # Skullsplitter Berserker
        1551,  # Ironjaw Basilisk
        1907,  # Naga Explorer
        2257,  # Mug'thol
        2547,  # Ironpatch
        2652,  # Witherbark Venomblood
        2691,  # Highvale Outrunner
        2720,  # Dustbelcher Ogre Mage
        2924,  # Silvermane Wolf
        4405,  # Muckshell Razorclaw
        5234,  # Gordunni Mauler
        5240,  # Gordunni Warlock
        5258,  # Woodpaw Alpha
        5278,  # Sprite Darter
        5287,  # Longtooth Howler
        5292,  # Feral Scar Yeti
        5300,  # Frayfeather Hippogryph
        5328,  # Coast Crawl Deepseer
        5336,  # Hatecrest Sorceress
        5423,  # Scorpid Tail Lasher
        5429,  # Fire Roc
        5615,  # Wastewander Rogue
        5839,  # Dark Iron Geologist
        5856,  # Glassweb Spider
        5860,  # Twilight Dark Shaman
        7727,  # Grimtotem Shaman
        8478,  # Second Mate Shandril
        672,  # Skullsplitter Spiritchaser
        723,  # Mosh'Ogg Butcher
        1490,  # Zanzil Witch Doctor
        1514,  # Mokk the Savage
        2505,  # Saltwater Snapjaw
        2607,  # Prince Galen Trollbane
        2608,  # Commander Amaren
        2653,  # Witherbark Sadist
        2686,  # Witherbark Broodguard
        2692,  # Highvale Scout
        2719,  # Dustbelcher Lord
        2887,  # Prismatic Exile
        2928,  # Primitive Owlbeast
        5236,  # Gordunni Shaman
        5272,  # Grizzled Ironfur Bear
        5295,  # Enraged Feral Scar
        5304,  # Frayfeather Stagwing
        5308,  # Rogue Vale Screecher
        5327,  # Coast Crawl Snapclaw
        5333,  # Hatecrest Serpent Guard
        5334,  # Hatecrest Myrmidon
        5426,  # Blisterpaw Hyena
        5861,  # Twilight Fire Guard
        5862,  # Twilight Geomancer
        7584,  # Wandering Forest Walker
        7788,  # Sandfury Drudge
        7855,  # Southsea Pirate
        7856,  # Southsea Freebooter
        7857,  # Southsea Dock Worker
        7858,  # Southsea Swashbuckler
        7899,  # Treasure Hunting Pirate
        7901,  # Treasure Hunting Swashbuckler
        7902,  # Treasure Hunting Buccaneer
        8637,  # Dark Iron Watchman
        8877,  # Sandfury Zealot
        11276,  # Azshara Sentinel
        13456,  # Noxxion's Spawn
        13696,  # Noxxious Scion
        13736,  # Noxxious Essence
        680,  # Mosh'Ogg Lord
        818,  # Mai'Zoth
        2386,  # Southshore Guard
        2435,  # Southshore Crier
        2639,  # Vilebranch Axe Thrower
        2654,  # Witherbark Caller
        2693,  # Highvale Marksman
        2919,  # Fam'retor Guardian
        2925,  # Silvermane Howler
        4465,  # Vilebranch Warrior
        5239,  # Gordunni Mage-Lord
        5293,  # Hulking Feral Scar
        5305,  # Frayfeather Skystormer
        5420,  # Glasshide Gazer
        5465,  # Land Rager
        5471,  # Dunemaul Ogre
        5850,  # Blazing Elemental
        5853,  # Tempered War Golem
        5857,  # Searing Lava Spider
        5881,  # Cursed Sycamore
        5974,  # Dreadmaul Ogre
        5979,  # Wretched Lost One
        5984,  # Starving Snickerfang
        7401,  # Draenei Refugee
        7805,  # Wastewander Scofflaw
        8151,  # Nijel's Point Guard
        8311,  # Slime Maggot
        8419,  # Twilight Idolater
        8759,  # Mosshoof Runner
        9525,  # Freewind Brave
        10612,  # Guard Wachabe
        17379,  # Stillpine Ancestor Akida
        17391,  # Stillpine Ancestor Coo
        2534,  # Zanzil the Outcast
        2640,  # Vilebranch Witch Doctor
        2641,  # Vilebranch Headhunter
        2659,  # Razorbeak Skylord
        2694,  # Highvale Ranger
        2929,  # Savage Owlbeast
        4466,  # Vilebranch Scalper
        5241,  # Gordunni Warlord
        5296,  # Rage Scar Yeti
        5306,  # Frayfeather Patriarch
        5424,  # Scorpid Dunestalker
        5472,  # Dunemaul Enforcer
        5473,  # Dunemaul Ogre Mage
        5840,  # Dark Iron Steamsmith
        5855,  # Magma Elemental
        5975,  # Dreadmaul Ogre Mage
        5976,  # Dreadmaul Brute
        5988,  # Scorpok Stinger
        6184,  # Timbermaw Pathfinder
        6190,  # Spitelash Warrior
        6375,  # Thunderhead Hippogryph
        7803,  # Scorpid Duneburrower
        7808,  # Marauding Owlbeast
        7847,  # Caliph Scorpidsting
        7848,  # Lurking Feral Scar
        1475,  # Menethil Guard
        2642,  # Vilebranch Shadowcaster
        2643,  # Vilebranch Berserker
        2926,  # Silvermane Stalker
        5276,  # Sprite Dragon
        5288,  # Rabid Longtooth
        5299,  # Ferocious Rage Scar
        5427,  # Rabid Blisterpaw
        5430,  # Searing Roc
        5462,  # Sea Spray
        5474,  # Dunemaul Brute
        5475,  # Dunemaul Warlock
        5481,  # Thistleshrub Dew Collector
        5846,  # Dark Iron Taskmaster
        5852,  # Inferno Elemental
        5858,  # Greater Lava Spider
        5982,  # Black Slayer
        5990,  # Redstone Basilisk
        6185,  # Timbermaw Warrior
        6193,  # Spitelash Screamer
        7809,  # Vilebranch Ambusher
        8136,  # Lord Shalzaru
        8566,  # Dark Iron Lookout
        8762,  # Timberweb Recluse
        8837,  # Muck Splash
        8956,  # Angerclaw Bear
        8959,  # Felpaw Wolf
        9318,  # Incendosaur
        2644,  # Vilebranch Hideskinner
        2645,  # Vilebranch Shadow Hunter
        5274,  # Ironfur Patriarch
        5297,  # Elder Rage Scar
        5362,  # Northspring Harpy
        5363,  # Northspring Roguefeather
        5421,  # Glasshide Petrifier
        5431,  # Surf Glider
        5461,  # Sea Elemental
        5490,  # Gnarled Thistleshrub
        5992,  # Ashmane Boar
        6186,  # Timbermaw Totemic
        6194,  # Spitelash Serpent Guard
        6377,  # Thunderhead Stagwing
        6505,  # Ravasaur
        6509,  # Bloodpetal Lasher
        7097,  # Ironbeak Owl
        7153,  # Deadwood Warrior
        7154,  # Deadwood Gardener
        8319,  # Nightmare Whelp
        9165,  # Fledgling Pterrordax
        12204,  # Spitelash Raider
        2646,  # Vilebranch Blood Drinker
        2647,  # Vilebranch Soul Eater
        5262,  # Groddoc Thunderer
        5364,  # Northspring Slayer
        5366,  # Northspring Windcaller
        5454,  # Hazzali Sandreaver
        5460,  # Centipaar Sandreaver
        5485,  # Thistleshrub Rootshaper
        5985,  # Snickerfang Hyena
        6187,  # Timbermaw Den Watcher
        6506,  # Ravasaur Runner
        6507,  # Ravasaur Hunter
        6511,  # Bloodpetal Thresher
        7155,  # Deadwood Pathfinder
        8760,  # Mosshoof Stag
        8763,  # Mistwing Rogue
        8958,  # Angerclaw Mauler
        8960,  # Felpaw Scavenger
        9162,  # Young Diemetradon
        9683,  # Lar'korwi Mate
        12046,  # Gor'marok the Ravager
        12205,  # Spitelash Witch
        14748,  # Vilebranch Kidnapper
        2621,  # Hammerfall Guardian
        2757,  # Blacklash
        4242,  # Frostsaber Companion
        8154,  # Ghost Walker Brave
        14621,  # Overseer Maltorius
        14734,  # Revantusk Drummer
    ],

    # Bracket 6 — level 51-60 — 347 entries
    6: [
        1815,  # Diseased Black Bear
        5981,  # Portal Seeker
        5991,  # Redstone Crystalhide
        6004,  # Shadowsworn Cultist
        6189,  # Timbermaw Ursa
        6195,  # Spitelash Siren
        6198,  # Blood Elf Surveyor
        6347,  # Young Wavethrasher
        6371,  # Storm Bay Warrior
        6510,  # Bloodpetal Flayer
        6513,  # Un'Goro Stomper
        6527,  # Tar Creeper
        6553,  # Gorishi Reaver
        7034,  # Firegut Ogre Mage
        7047,  # Black Broodling
        7112,  # Jaedenar Cultist
        7115,  # Jaedenar Adept
        8581,  # Blood Elf Defender
        8897,  # Doomforge Craftsman
        8902,  # Shadowforge Citizen
        8957,  # Angerclaw Grizzly
        8961,  # Felpaw Ravager
        9163,  # Diemetradon
        9690,  # Ember Worg
        9878,  # Entropic Beast
        10802,  # Hitah'ya the Keeper
        1821,  # Carrion Lurker
        1823,  # Giant Venom Mist Lurker
        1831,  # Scarlet Hunter
        6005,  # Shadowsworn Thug
        6006,  # Shadowsworn Adept
        6199,  # Blood Elf Reclaimer
        6348,  # Wavethrasher
        6370,  # Makrinni Scrabbler
        6379,  # Thunderhead Patriarch
        6380,  # Thunderhead Consort
        6512,  # Bloodpetal Trapper
        6516,  # Un'Goro Thunderer
        6518,  # Tar Lurker
        7031,  # Obsidian Elemental
        7035,  # Firegut Brute
        7040,  # Black Dragonspawn
        7044,  # Black Drake
        7098,  # Ironbeak Screecher
        7100,  # Warpwood Moss Flayer
        7114,  # Jaedenar Enforcer
        7138,  # Irontree Wanderer
        7139,  # Irontree Stomper
        8761,  # Mosshoof Courser
        8764,  # Mistwing Ravager
        8901,  # Anvilrage Reservist
        9167,  # Frenzied Pterrordax
        9601,  # Treant Spirit
        9691,  # Venomtip Scorpid
        10221,  # Bloodaxe Worg Pup
        10605,  # Scarlet Medic
        10919,  # Shatterspear Troll
        10979,  # Scarlet Hound
        10982,  # Whitewhisker Vermin
        10986,  # Snowblind Harpy
        10987,  # Irondeep Trogg
        10991,  # Wildpaw Gnoll
        11196,  # Shatterspear Drummer
        11443,  # Gordok Ogre-Mage
        11552,  # Timbermaw Mystic
        11553,  # Timbermaw Woodbender
        11603,  # Whitewhisker Digger
        11678,  # Snowblind Ambusher
        12418,  # Gordok Hyena
        13317,  # Coldmine Miner
        13396,  # Irondeep Miner
        1472,  # Morgg Stormshot
        1817,  # Diseased Wolf
        1835,  # Scarlet Invoker
        5666,  # Gunther's Visage
        5977,  # Dreadmaul Mauler
        6007,  # Shadowsworn Enforcer
        6008,  # Shadowsworn Warlock
        6135,  # Arkkoran Clacker
        6136,  # Arkkoran Muckdweller
        6349,  # Great Wavethrasher
        6352,  # Coralshell Lurker
        6519,  # Tar Lord
        6520,  # Scorching Elemental
        7036,  # Thaurissan Spy
        7037,  # Thaurissan Firewalker
        7039,  # War Reaver
        7041,  # Black Wyrmkin
        7045,  # Scalding Drake
        7048,  # Scalding Broodling
        7101,  # Warpwood Shredder
        7118,  # Jaedenar Darkweaver
        7120,  # Jaedenar Warlock
        7132,  # Toxic Horror
        7156,  # Deadwood Den Watcher
        7158,  # Deadwood Shaman
        7442,  # Winterfall Pathfinder
        7444,  # Shardtooth Bear
        7447,  # Fledgling Chillwind
        7450,  # Ragged Owlbeast
        7457,  # Rogue Ice Thistle
        7669,  # Servant of Grol
        8600,  # Plaguebat
        8920,  # Weapon Technician
        9879,  # Entropic Horror
        11440,  # Gordok Enforcer
        11442,  # Gordok Mauler
        11516,  # Timbermaw Warder
        11600,  # Irondeep Shaman
        11604,  # Whitewhisker Geomancer
        11675,  # Snowblind Windcaller
        11837,  # Wildpaw Shaman
        14282,  # Frostwolf Bloodhound
        14283,  # Stormpike Owl
        1824,  # Plague Lurker
        1833,  # Scarlet Knight
        1884,  # Scarlet Lumberjack
        5978,  # Dreadmaul Warlock
        6009,  # Shadowsworn Dreadweaver
        6137,  # Arkkoran Pincer
        6138,  # Arkkoran Oracle
        6350,  # Makrinni Razorclaw
        6351,  # Storm Bay Oracle
        6521,  # Living Blaze
        7038,  # Thaurissan Agent
        7055,  # Blackrock Worg
        7157,  # Deadwood Avenger
        7441,  # Winterfall Totemic
        7451,  # Raging Owlbeast
        7455,  # Winterspring Owl
        7670,  # Servant of Allistarj
        7886,  # Spitelash Enchantress
        8519,  # Blighted Surge
        8601,  # Noxious Plaguebat
        8603,  # Carrion Grub
        8900,  # Doomforge Arcanasmith
        8904,  # Shadowforge Senator
        8915,  # Twilight's Hammer Ambassador
        8977,  # Krom'Grul
        9164,  # Elder Diemetradon
        9176,  # Gor'tesh
        9695,  # Deathlash Scorpid
        10040,  # Gorishi Hive Guard
        10661,  # Spell Eater
        11602,  # Irondeep Skullthumper
        11605,  # Whitewhisker Overseer
        11614,  # Bloodshot
        11735,  # Stonelash Scorpid
        11887,  # Crypt Robber
        13022,  # Whip Lasher
        13080,  # Irondeep Guard
        13087,  # Coldmine Invader
        13096,  # Coldmine Explorer
        13098,  # Irondeep Surveyor
        13099,  # Irondeep Explorer
        13279,  # Discordant Surge
        14460,  # Blazing Invader
        1812,  # Rotting Behemoth
        1816,  # Diseased Grizzly
        1825,  # Giant Plague Lurker
        1826,  # Scarlet Mage
        1827,  # Scarlet Sentinel
        1834,  # Scarlet Paladin
        1883,  # Scarlet Worker
        2802,  # Susan Tillinghast
        7025,  # Blackrock Soldier
        7026,  # Blackrock Sorcerer
        7032,  # Greater Obsidian Elemental
        7049,  # Flamescale Broodling
        7149,  # Withered Protector
        7430,  # Frostsaber Cub
        7440,  # Winterfall Den Watcher
        7443,  # Shardtooth Mauler
        7448,  # Chillwind Chimaera
        7458,  # Ice Thistle Yeti
        8338,  # Dark Iron Marksman
        8408,  # Warlord Krellian
        8520,  # Plague Ravager
        8578,  # Magus Rimtori
        8776,  # Emerald Dragon Whelp
        8980,  # Firegut Captain
        9622,  # U'cha
        9697,  # Giant Ember Worg
        10375,  # Spire Spiderling
        10441,  # Plagued Rat
        10461,  # Plagued Insect
        10510,  # Plagued Slime
        10536,  # Plagued Maggot
        10608,  # Scarlet Priest
        10659,  # Cobalt Whelp
        10660,  # Cobalt Broodling
        10717,  # Temporal Parasite
        10956,  # Naga Siren
        11738,  # Sand Skitterer
        11740,  # Dredge Striker
        11744,  # Dust Stormer
        12047,  # Stormpike Mountaineer
        12048,  # Alliance Sentinel
        12779,  # Archmage Gaiman
        12780,  # Sergeant Major Skyshadow
        14462,  # Thundering Invader
        17068,  # Chief Expeditionary Requisitioner Enkles
        17070,  # Apothecary Quinard
        18727,  # Rarthein
        1813,  # Decaying Horror
        1832,  # Scarlet Magus
        4493,  # Scarlet Avenger
        7027,  # Blackrock Slayer
        7028,  # Blackrock Warlock
        7042,  # Flamescale Dragonspawn
        7046,  # Searscale Drake
        7431,  # Frostsaber
        7439,  # Winterfall Shaman
        7452,  # Crazed Owlbeast
        7459,  # Ice Thistle Matriarch
        7671,  # Servant of Sevine
        8521,  # Blighted Horror
        8602,  # Monstrous Plaguebat
        8605,  # Carrion Devourer
        9462,  # Chieftain Bloodmaw
        9684,  # Lar'korwi
        9698,  # Firetail Scorpid
        10161,  # Rookery Whelp
        10916,  # Winterfall Runner
        11613,  # Huntsman Radley
        11736,  # Stonelash Pincer
        11746,  # Desert Rumbler
        11838,  # Wildpaw Mystic
        11839,  # Wildpaw Brute
        13325,  # Seasoned Mountaineer
        13549,  # Seasoned Coldmine Invader
        13552,  # Seasoned Irondeep Guard
        13555,  # Seasoned Irondeep Surveyor
        14372,  # Winterfall Ambusher
        14458,  # Watery Invader
        3502,  # Ratchet Bruiser
        4494,  # Scarlet Spellbinder
        7043,  # Flamescale Wyrmkin
        7438,  # Winterfall Ursa
        7445,  # Elder Shardtooth
        7449,  # Chillwind Ravager
        7453,  # Moontouched Owlbeast
        7456,  # Winterspring Screecher
        7460,  # Ice Thistle Patriarch
        7668,  # Servant of Razelikh
        8560,  # Mossflayer Scout
        8562,  # Mossflayer Cannibal
        8565,  # Pathstrider
        9517,  # Shadow Lord Fel'dan
        10442,  # Chromatic Whelp
        10678,  # Plagued Hatchling
        10955,  # Summoned Water Elemental
        11611,  # Cavalier Durgen
        11737,  # Stonelash Flayer
        11739,  # Rock Stalker
        11745,  # Cyclone Warrior
        11886,  # Mercutio Filthgorger
        13036,  # Gordok Mastiff
        13160,  # Carrion Swarmer
        13335,  # Veteran Mountaineer
        13540,  # Seasoned Irondeep Explorer
        13543,  # Seasoned Irondeep Raider
        13546,  # Seasoned Coldmine Explorer
        14350,  # Hydroling
        14455,  # Whirling Invader
        15724,  # Drunken Bruiser
        16864,  # Stormwind Infantry
        7433,  # Frostsaber Huntress
        7454,  # Berserk Owlbeast
        8522,  # Plague Monstrosity
        8561,  # Mossflayer Shadowhunter
        8563,  # Woodsman
        9701,  # Spire Scorpid
        10177,  # Spire Scarab
        10807,  # Brumeran
        11677,  # Taskmaster Snivvle
        11747,  # Desert Rager
        11819,  # Jory Zaga
        11840,  # Wildpaw Alpha
        12352,  # Scarlet Trooper
        13078,  # Umi Thorson
        13086,  # Aggi Rumblestomp
        13426,  # Champion Mountaineer
        13541,  # Veteran Irondeep Explorer
        13547,  # Veteran Coldmine Explorer
        13550,  # Veteran Coldmine Invader
        13553,  # Veteran Irondeep Guard
        13556,  # Veteran Irondeep Surveyor
        329,  # Earth Elemental
        1845,  # High Protector Tarsen
        7432,  # Frostsaber Stalker
        7434,  # Frostsaber Pride Watcher
        7446,  # Rabid Shardtooth
        9605,  # Blackrock Raider
        10399,  # Thuzadin Acolyte
        10738,  # High Chief Winterfall
        11723,  # Hive'Ashi Sandstalker
        11728,  # Hive'Zora Reaver
        11730,  # Hive'Regal Ambusher
        13544,  # Veteran Irondeep Raider
        16932,  # Razorfang Hatchling
        603,  # Grimtooth
        1752,  # Caledra Dawnbreeze
        2041,  # Ancient Protector
        3946,  # Velinde Starsong
        9542,  # Franclorn's Spirit
        10741,  # Sian-Rotam
        11054,  # Crimson Rifleman
        11360,  # Zulian Cub
        11368,  # Bloodseeker Bat
        11636,  # Servant of Weldon Barov
        11637,  # Servant of Alexi Barov
        11795,  # Mylentha Riverbend
        11796,  # Bessany Plainswind
        11797,  # Moren Riverbend
        11817,  # Krah'ranik
        11897,  # Duskwing
        12140,  # Guardian of Elune
        12322,  # Quel'Lithien Protector
        13548,  # Champion Coldmine Explorer
        13551,  # Champion Coldmine Invader
        13554,  # Champion Irondeep Guard
        13557,  # Champion Irondeep Surveyor
        14022,  # Corrupted Red Whelp
        14023,  # Corrupted Green Whelp
        14024,  # Corrupted Blue Whelp
        14025,  # Corrupted Bronze Whelp
        14306,  # Eskhandar
        14362,  # Thornling
        14965,  # Frenzied Bloodseeker Bat
        15201,  # Twilight Flamereaver
        15545,  # Cenarion Outrider
        16043,  # Magma Lord Bokk
        16117,  # Plagued Swine
        17023,  # Shadow Council Enforcer
        17410,  # Stillpine Ancestor Vark
        19076,  # High Elf Refugee
        19077,  # Dwarf Refugee
        19120,  # Broken Refugee
        19144,  # Mag'har Refugee
        19150,  # Orc Refugee
        19155,  # Sporeling Refugee
        19162,  # Lost One Refugee
        19170,  # Peasant Refugee
        19455,  # Nurse Judith
        20874,  # Skettis Refugee
        20876,  # Human Refugee
    ],

}

# ---------------------------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("BountyWorld DB Lookup Tables")
    print(f"  Zones mapped:          {len(ZONE_IDS)}")
    print(f"  Bracket 7 boss pool:   {len(DUNGEON_BOSS_POOL)} bosses across "
          f"{len(DUNGEON_BOSS_POOL_BY_DUNGEON)} dungeons")
    total = sum(len(v) for v in BRACKET_CREATURES.values())
    print(f"  Bracket creature pool: {total} entries across 6 brackets")
    print()

    ranges = [(1,10),(11,20),(21,30),(31,40),(41,50),(51,60)]
    for b, (mn, mx) in enumerate(ranges, 1):
        print(f"  Bracket {b} [{mn:2d}–{mx}]:  {len(BRACKET_CREATURES[b])} creatures")

    print()
    print("  Bracket 7 pool by dungeon:")
    for dungeon, bosses in DUNGEON_BOSS_POOL_BY_DUNGEON.items():
        lvl_min = min(b["level"] for b in bosses)
        lvl_max = max(b["level"] for b in bosses)
        print(f"    {dungeon:<30} {len(bosses):2d} bosses  (lvl {lvl_min}–{lvl_max})")

    print()
    if SCRIPT_TRIGGERED_BOSSES:
        print("  ⚠ Script-triggered bosses (verify open-world spawnability):")
        for name in SCRIPT_TRIGGERED_BOSSES:
            print(f"    - {name}")
        print()

    print("  Verification SQL:")
    entries = ",".join(str(b["entry"]) for b in DUNGEON_BOSS_POOL)
    print(f"    SELECT entry, name, ScriptName, rank")
    print(f"    FROM creature_template")
    print(f"    WHERE entry IN ({entries})")
    print(f"    ORDER BY entry;")

# ============================================================
# Zone spawn points — safe landing coordinates per zone
# (map, x, y, z, orientation)
# Town centers, quest hubs, flight master locations
# ============================================================
ZONE_SPAWN_POINTS = {
    # Kalimdor — from innkeeper positions (verified safe)
    "Durotar":              (1,  340.362, -4686.29,   16.541, 0.0),  # Razor Hill inn
    "Dustwallow Marsh":     (1,-3616.13,  -4470.82,   14.329, 0.0),  # Theramore inn
    "The Barrens":          (1, -407.123, -2645.22,   96.306, 0.0),  # Crossroads inn
    "Mulgore":              (1,-2365.37,   -347.31,   -8.874, 0.0),  # Bloodhoof Village inn
    "Ashenvale":            (1, 2781.16,   -432.997, 116.665, 0.0),  # Astranaar inn
    "Stonetalon Mountains": (1, 2729.88,   1498.14,  237.593, 0.0),  # Stonetalon Peak inn
    "Darkshore":            (1, 6406.51,    515.367,    8.726, 0.0), # Auberdine inn
    "Teldrassil":           (1, 9802.21,    982.608, 1313.98,  0.0), # Darnassus inn
    "Thousand Needles":     (1,-5477.85,  -2460.43,   89.369, 0.0),  # Freewind Post inn
    "Feralas":              (1,-4460.1,     242.722,   39.191, 0.0), # Camp Mojache inn
    "Tanaris":              (1,-7158.96,  -3841.61,    8.848, 0.0),  # Gadgetzan inn
    "Winterspring":         (1, 6695.15,  -4673.04,  721.650, 0.0),  # Everlook inn
    "Felwood":              (1, 3796.96,  -2135.69,  210.565, 0.0),  # Talonbranch Glade
    "Moonglade":            (1, 7923.832, -2635.349, 492.689, 0.0),  # Lake Elune'ara (GPS)
    "Un'Goro Crater":       (1,-6117.564, -1344.658,-179.329, 0.0),  # Waygate area (GPS)
    "Silithus":             (1,-6864.242,   705.133,  43.580, 0.0),  # Cenarion Hold (GPS)
    # Eastern Kingdoms — from innkeeper positions (verified safe)
    "Elwynn Forest":        (0,-9462.66,     16.192,  57.046, 0.0),  # Goldshire inn
    "Westfall":             (0,-10653.4,   1166.52,   34.565, 0.0),  # Sentinel Hill inn
    "Duskwood":             (0,-10516.0,  -1161.21,   28.116, 0.0),  # Darkshire inn
    "Redridge Mountains":   (0,-9223.98,  -2157.12,   64.017, 0.0),  # Lakeshire inn
    "Wetlands":             (0,-3827.93,   -831.901,  10.091, 0.0),  # Menethil Harbor inn
    "Loch Modan":           (0,-5377.91,  -2973.91,  323.252, 0.0),  # Thelsamar inn
    "Dun Morogh":           (0,-5601.6,    -531.203, 399.737, 0.0),  # Kharanos inn
    "Arathi Highlands":     (0, -912.374, -3524.92,   72.768, 0.0),  # Refuge Pointe inn
    "Hillsbrad Foothills":  (0, -857.096,  -570.751,  11.165, 0.0),  # Southshore inn
    "Silverpine Forest":    (0,  510.916,  1636.47,  126.027, 0.0),  # The Sepulcher inn
    "Tirisfal Glades":      (0, 2269.51,    244.944,  34.340, 0.0),  # Brill inn
    "The Hinterlands":      (0,  399.725, -2119.74,  131.664, 0.0),  # Aerie Peak inn
    "Swamp of Sorrows":     (0,-10487.3,  -3258.84,   21.113, 0.0),  # Stonard inn
    "Burning Steppes":      (0,-8371.9,   -3051.95,  124.126, 0.0),  # Morgan's Vigil
    "Searing Gorge":        (0,-7276.75,  -1857.01,  159.448, 0.0),  # Thorium Point
    "Blasted Lands":        (0,-11817.3,  -3437.1,   -30.917, 0.0),  # Nethergarde Keep
    "Alterac Mountains":    (0,  -16.326, -1628.55,   38.915, 0.0),  # Alterac ruins
    "Western Plaguelands":  (0,  902.236, -2617.66,   33.517, 0.0),  # Chillwind Camp
    "Eastern Plaguelands":  (0, 1380.44,  -5778.2,    56.917, 0.0),  # Light's Hope
}