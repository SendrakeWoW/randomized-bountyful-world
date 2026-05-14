-- ============================================================
-- BountyWorld Meta Progression
-- ============================================================
-- Place in: lua_scripts/bountyworld_meta.lua
--
-- Handles:
--   - Lifetime kill/death/run tracking
--   - Safety net bracket (start one below where you died)
--   - Starting level bonus (applied on login)
--   - Achievement tracking and rewards
-- ============================================================

-- ------------------------------------------------------------
-- ACHIEVEMENT IDs
-- These match the DBC IDs directly (1-35)
-- ------------------------------------------------------------
local ACH = {
    -- Milestone
    FIRST_BLOOD       = 1,
    ON_THE_TRAIL      = 2,
    SEASONED_HUNTER   = 3,
    RELENTLESS        = 4,
    VETERAN           = 5,
    LEGEND            = 6,
    ETERNAL_HUNTER    = 7,
    -- Nemesis
    THEY_REMEMBER     = 9,
    GRUDGE_MATCH      = 10,
    OLD_WOUNDS        = 11,
    OBSESSION         = 12,
    RECKONING         = 13,
    AGAINST_ALL_ODDS  = 14,
    MANY_ENEMIES      = 15,
    CLEAN_SLATE       = 16,
    -- Speed & Style
    GHOST             = 17,
    NO_WITNESSES      = 18,
    STUBBORN          = 19,
    BLINDFOLDED       = 20,
    SPEEDRUNNER       = 21,
    -- Exploration
    WANDERER          = 22,
    CARTOGRAPHER      = 23,
    DEEP_CUT          = 24,
    WRONG_HOOD        = 25,
    -- Run Mastery
    SURVIVOR          = 26,
    COMEBACK_KID      = 27,
    BACK_TO_BASICS    = 28,
    ASCENDING         = 29,
    LONG_ROAD         = 30,
    -- Hidden
    HUMBLING          = 31,
    PREDATOR          = 32,
    FULL_CIRCLE       = 33,
    OVERKILL          = 34,
    GHOST_TOWN        = 35,
}

-- Milestone kill thresholds
local MILESTONE_KILLS = {
    [1]  = ACH.FIRST_BLOOD,
    [5]  = ACH.ON_THE_TRAIL,
    [10] = ACH.SEASONED_HUNTER,
    [15] = ACH.RELENTLESS,
    [20] = ACH.VETERAN,
    [25] = ACH.LEGEND,
    [30] = ACH.ETERNAL_HUNTER,
}

-- Achievement names for chat messages
local ACH_NAMES = {
    [ACH.FIRST_BLOOD]      = "First Blood",
    [ACH.ON_THE_TRAIL]     = "On the Trail",
    [ACH.SEASONED_HUNTER]  = "Seasoned Hunter",
    [ACH.RELENTLESS]       = "Relentless",
    [ACH.VETERAN]          = "Veteran of the Hunt",
    [ACH.LEGEND]           = "Legend",
    [ACH.ETERNAL_HUNTER]   = "Eternal Hunter",
    [ACH.THEY_REMEMBER]    = "They Remember You",
    [ACH.GRUDGE_MATCH]     = "Grudge Match",
    [ACH.OLD_WOUNDS]       = "Old Wounds",
    [ACH.OBSESSION]        = "Obsession",
    [ACH.RECKONING]        = "Reckoning",
    [ACH.AGAINST_ALL_ODDS] = "Against All Odds",
    [ACH.MANY_ENEMIES]     = "Many Enemies",
    [ACH.CLEAN_SLATE]      = "Clean Slate",
    [ACH.GHOST]            = "Ghost",
    [ACH.NO_WITNESSES]     = "No Witnesses",
    [ACH.STUBBORN]         = "Stubborn",
    [ACH.BLINDFOLDED]      = "Blindfolded",
    [ACH.SPEEDRUNNER]      = "Speedrunner",
    [ACH.WANDERER]         = "Wanderer",
    [ACH.CARTOGRAPHER]     = "Cartographer",
    [ACH.DEEP_CUT]         = "Deep Cut",
    [ACH.WRONG_HOOD]       = "Wrong Neighbourhood",
    [ACH.SURVIVOR]         = "Survivor",
    [ACH.COMEBACK_KID]     = "Comeback Kid",
    [ACH.BACK_TO_BASICS]   = "Back to Basics",
    [ACH.ASCENDING]        = "Ascending",
    [ACH.LONG_ROAD]        = "The Long Road",
    [ACH.HUMBLING]         = "Humbling",
    [ACH.PREDATOR]         = "Predator",
    [ACH.FULL_CIRCLE]      = "Full Circle",
    [ACH.OVERKILL]         = "Overkill",
    [ACH.GHOST_TOWN]       = "Ghost Town",
}

-- Colors
local C_GOLD   = "|cffFFD700"
local C_GREEN  = "|cff44FF44"
local C_SILVER = "|cffC0C0C0"
local C_RESET  = "|r"
local PREFIX   = C_GOLD .. "[BountyWorld]" .. C_RESET .. " "

local function Msg(player, text)
    player:SendBroadcastMessage(PREFIX .. text)
end

-- ------------------------------------------------------------
-- META DATA
-- ------------------------------------------------------------

local function GetMeta(player)
    local accountId = player:GetAccountId()
    local q = CharDBQuery(string.format(
        "SELECT lifetime_kills, lifetime_deaths, lifetime_runs, "
     .. "safety_net_bracket, starting_level_bonus, achievements, total_playtime "
     .. "FROM bountyworld_meta WHERE account_id = %d", accountId))
    if not q then
        CharDBExecute(string.format(
            "INSERT INTO bountyworld_meta (account_id) VALUES (%d)", accountId))
        return {
            kills         = 0,
            deaths        = 0,
            runs          = 0,
            safety_bracket= 0,
            level_bonus   = 0,
            achievements  = 0,
            playtime      = 0,
        }
    end
    return {
        kills          = q:GetUInt32(0),
        deaths         = q:GetUInt32(1),
        runs           = q:GetUInt32(2),
        safety_bracket = q:GetUInt8(3),
        level_bonus    = q:GetUInt8(4),
        achievements   = q:GetUInt32(5),
        playtime       = q:GetUInt32(6),
    }
end

local function SaveMeta(player, meta)
    local accountId = player:GetAccountId()
    CharDBExecute(string.format(
        "REPLACE INTO bountyworld_meta "
     .. "(account_id, lifetime_kills, lifetime_deaths, lifetime_runs, "
     .. " safety_net_bracket, starting_level_bonus, achievements, total_playtime) "
     .. "VALUES (%d, %d, %d, %d, %d, %d, %d, %d)",
        accountId,
        meta.kills,
        meta.deaths,
        meta.runs,
        meta.safety_bracket,
        meta.level_bonus,
        meta.achievements,
        meta.playtime))
end

-- ------------------------------------------------------------
-- ACHIEVEMENT SYSTEM
-- ------------------------------------------------------------

local function HasAchievement(player, ach_id)
    local accountId = player:GetAccountId()
    local q = CharDBQuery(string.format(
        "SELECT 1 FROM bountyworld_achievements "
     .. "WHERE account_id = %d AND achievement_id = %d",
        accountId, ach_id))
    return q ~= nil
end

local function AwardAchievement(player, ach_id)
    if HasAchievement(player, ach_id) then return false end

    local accountId = player:GetAccountId()

    -- Record in our meta DB
    CharDBExecute(string.format(
        "INSERT IGNORE INTO bountyworld_achievements (account_id, achievement_id, earned_at) "
     .. "VALUES (%d, %d, %d)",
        accountId, ach_id, os.time()))

    CharDBExecute(string.format(
        "UPDATE bountyworld_meta SET achievements = achievements + 1 WHERE account_id = %d",
        accountId))

    -- Write to character_achievement so it shows in the achievement panel
    local db_id = 9000 + ach_id
    local char_guid = player:GetGUIDLow()
    CharDBExecute(string.format(
        "INSERT IGNORE INTO character_achievement (guid, achievement, date) VALUES (%d, %d, %d)",
        char_guid, db_id, os.time()))

    local name = ACH_NAMES[ach_id] or ("Achievement #" .. ach_id)
    Msg(player, C_GOLD .. "Achievement Unlocked: [" .. name .. "]" .. C_RESET)

    return true
end

-- ------------------------------------------------------------
-- REWARDS
-- ------------------------------------------------------------

local function ApplyLevelBonus(player, bonus)
    if bonus <= 0 then return end
    local current = player:GetLevel()
    local target  = current + bonus
    if target > 60 then target = 60 end
    if target > current then
        player:SetLevel(target)
        Msg(player, C_GREEN .. "Meta reward: Started at level " .. target
            .. " (+" .. bonus .. " from achievements)" .. C_RESET)
    end
end

local function ApplyMilestoneReward(player, ach_id, meta)
    if ach_id == ACH.VETERAN then
        Msg(player, C_SILVER .. "Reward: Title - The Hunter. +5% XP passive." .. C_RESET)
    elseif ach_id == ACH.ETERNAL_HUNTER then
        Msg(player, C_SILVER .. "Reward: Title - The Eternal. Gear quality improves." .. C_RESET)
    end
    return meta
end

-- ------------------------------------------------------------
-- KILL HANDLER (called from bountyworld_core.lua on bounty kill)
-- ------------------------------------------------------------

function BW_OnBountyKilled(player, bracket)
    local meta = GetMeta(player)
    meta.kills = meta.kills + 1
    SaveMeta(player, meta)

    -- Check milestone achievements
    local ach = MILESTONE_KILLS[meta.kills]
    if ach then
        if AwardAchievement(player, ach) then
            meta = ApplyMilestoneReward(player, ach, meta)
            SaveMeta(player, meta)
        end
    end

    -- Prestige tier — every 5 kills after 30
    if meta.kills > 30 and meta.kills % 5 == 0 then
        local tier = math.floor((meta.kills - 30) / 5)
        Msg(player, C_GOLD .. "Prestige: Hunter " .. tier .. "!" .. C_RESET)
    end

    -- Deep Cut — reach bracket 5 without dying this run
    -- (tracked via run deaths, checked externally)
end

-- ------------------------------------------------------------
-- DEATH HANDLER (called from bountyworld_core.lua on death)
-- ------------------------------------------------------------

function BW_OnPlayerDied(player, bracket)
    local meta = GetMeta(player)
    meta.deaths  = meta.deaths + 1
    meta.runs    = meta.runs + 1

    -- Safety net: next run starts one bracket below where player died
    local safety = bracket - 1
    if safety < 0 then safety = 0 end
    meta.safety_bracket = safety

    -- They Remember You — first death to a bounty target
    if meta.deaths == 1 then
        AwardAchievement(player, ACH.THEY_REMEMBER)
    end

    SaveMeta(player, meta)

    Msg(player, C_SILVER .. "Lifetime kills: " .. meta.kills
        .. " | Deaths: " .. meta.deaths .. C_RESET)
    if safety > 0 then
        Msg(player, C_SILVER .. "Safety net: Next run starts at bracket "
            .. safety .. C_RESET)
    end
end

-- ------------------------------------------------------------
-- LOGIN HANDLER — apply safety net and level bonus
-- ------------------------------------------------------------


-- ── Spawn coordinates per zone ──────────────────────────────────────────────
-- (map, x, y, z, orientation)
local ZONE_SPAWNS = {
    -- Kalimdor (Horde)
    ["Durotar"]              = {1,  340.362, -4686.29,   16.541, 0.0},
    ["Dustwallow Marsh"]     = {1,-3616.13,  -4470.82,   14.329, 0.0},
    ["The Barrens"]          = {1, -407.123, -2645.22,   96.306, 0.0},
    ["Mulgore"]              = {1,-2365.37,   -347.31,   -8.874, 0.0},
    ["Ashenvale"]            = {1, 2781.16,   -432.997, 116.665, 0.0},
    ["Stonetalon Mountains"] = {1, 2729.88,   1498.14,  237.593, 0.0},
    ["Darkshore"]            = {1, 6406.51,    515.367,    8.726, 0.0},
    ["Teldrassil"]           = {1, 9802.21,    982.608, 1313.98,  0.0},
    ["Thousand Needles"]     = {1,-5477.85,  -2460.43,   89.369, 0.0},
    ["Feralas"]              = {1,-4460.1,     242.722,   39.191, 0.0},
    ["Tanaris"]              = {1,-7158.96,  -3841.61,    8.848, 0.0},
    ["Winterspring"]         = {1, 6695.15,  -4673.04,  721.650, 0.0},
    ["Felwood"]              = {1, 3796.96,  -2135.69,  210.565, 0.0},
    ["Moonglade"]            = {1, 7923.832, -2635.349, 492.689, 0.0},
    ["Un'Goro Crater"]       = {1,-6117.564, -1344.658,-179.329, 0.0},
    ["Silithus"]             = {1,-6864.242,   705.133,  43.580, 0.0},
    -- Eastern Kingdoms (Alliance)
    ["Elwynn Forest"]        = {0,-9462.66,     16.192,  57.046, 0.0},
    ["Westfall"]             = {0,-10653.4,   1166.52,   34.565, 0.0},
    ["Duskwood"]             = {0,-10516.0,  -1161.21,   28.116, 0.0},
    ["Redridge Mountains"]   = {0,-9223.98,  -2157.12,   64.017, 0.0},
    ["Wetlands"]             = {0,-3827.93,   -831.901,  10.091, 0.0},
    ["Loch Modan"]           = {0,-5377.91,  -2973.91,  323.252, 0.0},
    ["Dun Morogh"]           = {0,-5601.6,    -531.203, 399.737, 0.0},
    ["Arathi Highlands"]     = {0, -912.374, -3524.92,   72.768, 0.0},
    ["Hillsbrad Foothills"]  = {0, -857.096,  -570.751,  11.165, 0.0},
    ["Silverpine Forest"]    = {0,  510.916,  1636.47,  126.027, 0.0},
    ["Tirisfal Glades"]      = {0, 2269.51,    244.944,  34.340, 0.0},
    ["The Hinterlands"]      = {0,  399.725, -2119.74,  131.664, 0.0},
    ["Swamp of Sorrows"]     = {0,-10487.3,  -3258.84,   21.113, 0.0},
    ["Burning Steppes"]      = {0,-8371.9,   -3051.95,  124.126, 0.0},
    ["Searing Gorge"]        = {0,-7276.75,  -1857.01,  159.448, 0.0},
    ["Blasted Lands"]        = {0,-11817.3,  -3437.1,   -30.917, 0.0},
    ["Alterac Mountains"]    = {0,  -16.326, -1628.55,   38.915, 0.0},
    ["Western Plaguelands"]  = {0,  902.236, -2617.66,   33.517, 0.0},
    ["Eastern Plaguelands"]  = {0, 1380.44,  -5778.2,    56.917, 0.0},
}

-- Kalimdor and EK zone sets for continent filtering
local KALIMDOR_ZONES = {
    ["Teldrassil"]=true, ["Darkshore"]=true, ["Ashenvale"]=true,
    ["Stonetalon Mountains"]=true, ["The Barrens"]=true, ["Durotar"]=true,
    ["Mulgore"]=true, ["Dustwallow Marsh"]=true, ["Thousand Needles"]=true,
    ["Feralas"]=true, ["Tanaris"]=true, ["Un'Goro Crater"]=true,
    ["Silithus"]=true, ["Felwood"]=true, ["Moonglade"]=true, ["Winterspring"]=true,
}

function BW_TeleportToStart(player, faction)
    -- faction: 0=Alliance (EK), 1=Horde (Kalimdor)
    local home_continent = (faction == 1) and KALIMDOR_ZONES or nil

    -- Get bracket 1 zones from DB
    local guid = player:GetGUIDLow()
    local seedQ = CharDBQuery(string.format(
        "SELECT seed FROM bountyworld_run WHERE guid = %d", guid))
    local seed = seedQ and seedQ:GetUInt32(0) or 12345

    local q = CharDBQuery(string.format(
        "SELECT zone_name FROM bountyworld_bracket_zones "
     .. "WHERE seed = %d AND bracket = 1", seed))

    if not q then
        Msg(player, C_SILVER .. "No bracket map found — staying in starting area." .. C_RESET)
        return
    end

    -- Collect bracket 1 zones on home continent
    local valid_zones = {}
    repeat
        local zone = q:GetString(0)
        if home_continent == nil or home_continent[zone] then
            if ZONE_SPAWNS[zone] then
                table.insert(valid_zones, zone)
            end
        end
    until not q:NextRow()

    if #valid_zones == 0 then
        Msg(player, C_SILVER .. "No suitable starting zone found." .. C_RESET)
        return
    end

    -- Pick random bracket 1 zone
    local chosen = valid_zones[math.random(#valid_zones)]
    local sp = ZONE_SPAWNS[chosen]
    player:Teleport(sp[1], sp[2], sp[3], sp[4], sp[5])
    Msg(player, C_GOLD .. "Welcome to BountyWorld! Starting in: "
        .. chosen .. C_RESET)
end

local function OnLogin(event, player)
    local meta = GetMeta(player)
    if not meta then return end

    -- Bracket minimum levels
    local BRACKET_MIN_LEVEL = {
        [0]=1, [1]=1, [2]=11, [3]=21, [4]=31, [5]=41, [6]=51, [7]=60
    }

    -- Apply safety net starting level
    -- Safety bracket is one below where player died, so start at that bracket's min level
    local safety = meta.safety_bracket or 0
    local baseLevel = BRACKET_MIN_LEVEL[safety] or 1

    if player:GetLevel() == 1 then
        if baseLevel > 1 then
            player:SetLevel(baseLevel)
            Msg(player, C_GREEN .. "Safety net: Starting at bracket "
                .. safety .. " (level " .. baseLevel .. ")" .. C_RESET)
        end

        -- Teleport to a bracket 1 zone on the player's faction continent
        -- Faction: 469=Alliance, 67=Horde
        local faction = player:GetTeam()  -- 0=Alliance, 1=Horde
        BW_TeleportToStart(player, faction)
    end

    -- Safety net bracket reminder
    if safety > 0 then
        Msg(player, C_SILVER .. "Safety net active: Starting at bracket "
            .. safety .. C_RESET)
    end

    -- Lifetime stats reminder
    if meta.kills > 0 then
        Msg(player, C_SILVER .. "Lifetime bounties: " .. meta.kills
            .. " | Achievements: " .. meta.achievements .. C_RESET)
    end
end

-- ------------------------------------------------------------
-- EXPOSE META READ FOR CORE SCRIPT
-- ------------------------------------------------------------

function BW_GetSafetyBracket(player)
    local meta = GetMeta(player)
    return meta.safety_bracket or 0
end

function BW_GetLifetimeKills(player)
    local meta = GetMeta(player)
    return meta.kills or 0
end

-- ------------------------------------------------------------
-- REGISTER EVENTS
-- ------------------------------------------------------------

RegisterPlayerEvent(3, OnLogin)  -- PLAYER_EVENT_ON_LOGIN