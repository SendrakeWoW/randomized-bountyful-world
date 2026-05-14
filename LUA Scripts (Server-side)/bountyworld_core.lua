-- ============================================================
-- BountyWorld Core
-- ============================================================
-- Schema:
--   bountyworld_run     : guid, current_bracket, run_active, seed
--   bountyworld_bounties: guid, bracket, bounty_entry, bounty_name,
--                         bounty_zone, killed, assigned_at
-- ============================================================

-- ------------------------------------------------------------
-- CONFIG
-- ------------------------------------------------------------
local CURRENT_SEED    = 12345
local B7_ZONE         = "Alterac Mountains"
local B7_BOUNTY_ENTRY = 7796
local B7_BOUNTY_NAME  = "Nekrum Gutchewer"

-- Bracket level caps for clean clear detection
local BRACKET_LEVEL_CAP = {
    [1]=10, [2]=20, [3]=30, [4]=40, [5]=50, [6]=60, [7]=60
}

-- Gold reward per bracket (in copper: 1g = 10000)
local BRACKET_GOLD = {
    [1]=100000, [2]=200000, [3]=300000,
    [4]=400000, [5]=500000, [6]=600000, [7]=1000000
}

-- Hunter's Medallion item IDs per clean clear tier
local MEDALLION_ITEMS = {
    [1]=700001, [2]=700002, [3]=700003, [4]=700004,
    [5]=700005, [6]=700006, [7]=700007
}

-- XP bonus per clean clear (5% = 0.05)
local XP_BONUS_PER_CLEAR = 0.05

-- Kalimdor zones (Horde continent)
local KALIMDOR_ZONES = {
    ["Teldrassil"]=true, ["Darkshore"]=true, ["Ashenvale"]=true,
    ["Stonetalon Mountains"]=true, ["The Barrens"]=true, ["Durotar"]=true,
    ["Mulgore"]=true, ["Dustwallow Marsh"]=true, ["Thousand Needles"]=true,
    ["Feralas"]=true, ["Tanaris"]=true, ["Un'Goro Crater"]=true,
    ["Silithus"]=true, ["Felwood"]=true, ["Moonglade"]=true, ["Winterspring"]=true,
}

-- Eastern Kingdoms zones (Alliance continent)
local EK_ZONES = {
    ["Elwynn Forest"]=true, ["Westfall"]=true, ["Duskwood"]=true,
    ["Redridge Mountains"]=true, ["Burning Steppes"]=true, ["Searing Gorge"]=true,
    ["Blasted Lands"]=true, ["Swamp of Sorrows"]=true, ["Loch Modan"]=true,
    ["Dun Morogh"]=true, ["Wetlands"]=true, ["Arathi Highlands"]=true,
    ["Hillsbrad Foothills"]=true, ["Alterac Mountains"]=true,
    ["Silverpine Forest"]=true, ["Tirisfal Glades"]=true,
    ["Western Plaguelands"]=true, ["Eastern Plaguelands"]=true, ["The Hinterlands"]=true,
}

-- Number of bounties per bracket
local BRACKET_BOUNTY_COUNT = {
    [1]=2, [2]=3, [3]=3, [4]=4, [5]=5, [6]=5, [7]=1
}

-- Hint reveal times in seconds
local HINT_1_DELAY = 600   -- 10 min: flavor text
local HINT_2_DELAY = 1500  -- 25 min: zone name

local BRACKET_FLAVOR = {
    [1] = "Rumor has it your targets lurk in a low-level region...",
    [2] = "Your bounties have been spotted in a zone of modest danger...",
    [3] = "Travelers warn of your targets in lands of growing peril...",
    [4] = "Your quarry commands dangerous territory...",
    [5] = "Your targets roam a zone that breaks unprepared adventurers...",
    [6] = "Only the most seasoned hunters survive where your bounties wait...",
    [7] = "The skull zone pulses with dark energy. Your final target awaits.",
}

-- Colors
local C_GOLD   = "|cffFFD700"
local C_RED    = "|cffFF4444"
local C_GREEN  = "|cff44FF44"
local C_SILVER = "|cffC0C0C0"
local C_RESET  = "|r"
local PREFIX   = C_GOLD .. "[BountyWorld]" .. C_RESET .. " "

-- ------------------------------------------------------------
-- ZONE BOUNDS (for bounty picking)
-- ------------------------------------------------------------
local ZONE_BOUNDS = {
    ["Teldrassil"]           = {1,  8000, 10500,  -700,  2200},
    ["Darkshore"]            = {1,  4500,  7200,  -700,  3000},
    ["Ashenvale"]            = {1,  1500,  5000, -4200,  -800},
    ["Stonetalon Mountains"] = {1, -1200,  1800, -3200,  -800},
    ["The Barrens"]          = {1, -1800,  1200, -5000,  -900},
    ["Durotar"]              = {1, -1200,   800, -5600, -3000},
    ["Mulgore"]              = {1, -2900,  -400, -3000,  -200},
    ["Dustwallow Marsh"]     = {1, -3800, -2600, -4400, -2800},
    ["Thousand Needles"]     = {1, -4900, -3800, -5000, -3200},
    ["Feralas"]              = {1, -5400, -4900, -4200, -1000},
    ["Tanaris"]              = {1, -8500, -6100, -5200, -3000},
    ["Un'Goro Crater"]       = {1, -7800, -5700, -1800,   800},
    ["Silithus"]             = {1, -9400, -7600,   400,  2900},
    ["Felwood"]              = {1,  3500,  6600, -1200,  1700},
    ["Moonglade"]            = {1,  5000,  7400,  -700,   800},
    ["Winterspring"]         = {1,  5100,  9100, -3500,   200},
    ["Elwynn Forest"]        = {0, -9700, -8000,  -900,   700},
    ["Westfall"]             = {0,-11400, -9500, -2100,  -100},
    ["Duskwood"]             = {0,-11000, -9000, -3700, -1700},
    ["Redridge Mountains"]   = {0, -9500, -8000, -2300,  -700},
    ["Burning Steppes"]      = {0, -9000, -7300, -2700, -1200},
    ["Searing Gorge"]        = {0, -8200, -6700, -2500,  -800},
    ["Blasted Lands"]        = {0,-12000,-10200, -3700, -2100},
    ["Swamp of Sorrows"]     = {0,-11000, -9200, -3900, -2400},
    ["Loch Modan"]           = {0, -6300, -4700, -3200, -1500},
    ["Dun Morogh"]           = {0, -6600, -4300, -1500,   900},
    ["Wetlands"]             = {0, -4600, -2500, -2300,  -600},
    ["Arathi Highlands"]     = {0, -2500,  -200, -3600, -1500},
    ["Hillsbrad Foothills"]  = {0,  -600,  1800, -3000,  -800},
    ["Alterac Mountains"]    = {0,   200,  2100, -2200,  -500},
    ["Silverpine Forest"]    = {0,   400,  1500,  -900,  1500},
    ["Tirisfal Glades"]      = {0,  1500,  4000,  -400,  1600},
    ["Western Plaguelands"]  = {0,  2200,  5000, -1500,   500},
    ["Eastern Plaguelands"]  = {0,  2400,  5400, -3400,  -900},
    ["The Hinterlands"]      = {0,  -700,  2200, -5100, -2700},
}

-- ------------------------------------------------------------
-- SQL ESCAPE
-- ------------------------------------------------------------
local function EscapeSQL(str)
    return string.gsub(tostring(str or ""), "'", "''")
end

-- ------------------------------------------------------------
-- HELPERS
-- ------------------------------------------------------------
local function Msg(player, text)
    player:SendBroadcastMessage(PREFIX .. text)
end

-- ------------------------------------------------------------
-- RUN DATA
-- ------------------------------------------------------------
local function GetRunData(player)
    local guid = player:GetGUIDLow()
    local q = CharDBQuery(string.format(
        "SELECT current_bracket, run_active, seed, clean_clears "
     .. "FROM bountyworld_run WHERE guid = %d", guid))
    if not q then return nil end
    return {
        bracket      = q:GetUInt8(0),
        run_active   = q:GetUInt8(1),
        seed         = q:GetUInt32(2),
        clean_clears = q:GetUInt8(3),
    }
end

local function SaveRunData(player, data)
    local guid = player:GetGUIDLow()
    CharDBExecute(string.format(
        "REPLACE INTO bountyworld_run (guid, current_bracket, run_active, seed, clean_clears) "
     .. "VALUES (%d, %d, %d, %d, %d)",
        guid, data.bracket, data.run_active, data.seed,
        data.clean_clears or 0))
end

-- ------------------------------------------------------------
-- BOUNTY DATA
-- ------------------------------------------------------------
local function GetBounties(player, bracket)
    local guid = player:GetGUIDLow()
    local q = CharDBQuery(string.format(
        "SELECT bounty_entry, bounty_name, bounty_zone, killed "
     .. "FROM bountyworld_bounties "
     .. "WHERE guid = %d AND bracket = %d "
     .. "ORDER BY bounty_entry",
        guid, bracket))
    if not q then return {} end
    local bounties = {}
    repeat
        table.insert(bounties, {
            entry  = q:GetUInt32(0),
            name   = q:GetString(1),
            zone   = q:GetString(2),
            killed = q:GetUInt8(3),
        })
    until not q:NextRow()
    return bounties
end

local function AllBountiesKilled(player, bracket)
    local guid = player:GetGUIDLow()
    local q = CharDBQuery(string.format(
        "SELECT COUNT(*) FROM bountyworld_bounties "
     .. "WHERE guid = %d AND bracket = %d AND killed = 0",
        guid, bracket))
    if not q then return false end
    return q:GetUInt32(0) == 0
end

local function MarkBountyKilled(player, bracket, entry)
    local guid = player:GetGUIDLow()
    CharDBExecute(string.format(
        "UPDATE bountyworld_bounties SET killed = 1 "
     .. "WHERE guid = %d AND bracket = %d AND bounty_entry = %d",
        guid, bracket, entry))
end

local function ClearBounties(player, bracket)
    local guid = player:GetGUIDLow()
    CharDBExecute(string.format(
        "DELETE FROM bountyworld_bounties WHERE guid = %d AND bracket = %d",
        guid, bracket))
end

-- ------------------------------------------------------------
-- ZONE HELPERS
-- ------------------------------------------------------------
local function GetZonesForBracket(bracket, player)
    local zones = {}
    local q = CharDBQuery(string.format(
        "SELECT zone_name FROM bountyworld_bracket_zones "
     .. "WHERE seed = %d AND bracket = %d",
        CURRENT_SEED, bracket))
    if not q then return zones end

    repeat
        table.insert(zones, q:GetString(0))
    until not q:NextRow()

    -- Brackets 1-2: restrict to home continent
    -- Brackets 3-4: prefer home continent but allow away
    -- Brackets 5+: no restriction
    if bracket <= 2 and player then
        local faction = player:GetTeam()  -- 0=Alliance, 1=Horde
        local home = (faction == 1) and KALIMDOR_ZONES or EK_ZONES
        local filtered = {}
        for _, z in ipairs(zones) do
            if home[z] then table.insert(filtered, z) end
        end
        if #filtered > 0 then return filtered end
        -- Fallback to all zones if none on home continent
    end

    return zones
end

-- ------------------------------------------------------------
-- BOUNTY PICKER
-- ------------------------------------------------------------
local function PickBountyForZone(zone, exclude_entries)
    local bounds = ZONE_BOUNDS[zone]
    if not bounds then return nil end

    local map_id = bounds[1]
    local min_x  = bounds[2]
    local max_x  = bounds[3]
    local min_y  = bounds[4]
    local max_y  = bounds[5]

    local exclude_clause = ""
    if exclude_entries and #exclude_entries > 0 then
        exclude_clause = "AND c.id1 NOT IN (" .. table.concat(exclude_entries, ",") .. ") "
    end

    local q = WorldDBQuery(string.format(
        "SELECT c.id1, ct.name, COUNT(*) as cnt "
     .. "FROM creature c "
     .. "JOIN creature_template ct ON c.id1 = ct.entry "
     .. "WHERE c.map = %d "
     .. "AND c.position_x BETWEEN %d AND %d "
     .. "AND c.position_y BETWEEN %d AND %d "
     .. "AND ct.npcflag = 0 "
     .. "AND (ct.ScriptName = '' OR ct.ScriptName IS NULL) "
     .. "AND ct.subname IS NULL "
     .. "%s"
     .. "GROUP BY c.id1, ct.name "
     .. "ORDER BY cnt DESC LIMIT 5",
        map_id, min_x, max_x, min_y, max_y, exclude_clause))

    if not q then return nil end

    local candidates = {}
    repeat
        table.insert(candidates, {
            entry = q:GetUInt32(0),
            name  = q:GetString(1),
            count = q:GetUInt32(2),
        })
    until not q:NextRow()

    if #candidates == 0 then return nil end
    local pick = candidates[math.random(#candidates)]
    return {entry=pick.entry, name=pick.name, zone=zone}
end

local function AssignBounties(player, bracket)
    -- Check safety net
    if bracket == 1 and BW_GetSafetyBracket then
        local safety = BW_GetSafetyBracket(player)
        if safety > 1 then bracket = safety end
    end

    ClearBounties(player, bracket)

    if bracket == 7 then
        -- Skull zone: single dungeon boss bounty
        local guid = player:GetGUIDLow()
        CharDBExecute(string.format(
            "INSERT INTO bountyworld_bounties "
         .. "(guid, bracket, bounty_entry, bounty_name, bounty_zone, killed, assigned_at) "
         .. "VALUES (%d, 7, %d, '%s', '%s', 0, %d)",
            guid, B7_BOUNTY_ENTRY,
            EscapeSQL(B7_BOUNTY_NAME),
            EscapeSQL(B7_ZONE),
            os.time()))

        local data = {bracket=7, run_active=1, seed=CURRENT_SEED}
        SaveRunData(player, data)

        Msg(player, "Bracket 7 - SKULL ZONE")
        Msg(player, C_RED .. "Target: " .. B7_BOUNTY_NAME .. " in " .. B7_ZONE .. C_RESET)
        return
    end

    local zones = GetZonesForBracket(bracket, player)
    if #zones == 0 then
        Msg(player, C_RED .. "Error: No zones for bracket " .. bracket .. C_RESET)
        return
    end

    -- Shuffle zones
    for i = #zones, 2, -1 do
        local j = math.random(i)
        zones[i], zones[j] = zones[j], zones[i]
    end

    local count    = BRACKET_BOUNTY_COUNT[bracket] or 2
    local assigned = 0
    local used_entries = {}
    local guid = player:GetGUIDLow()
    local zone_idx = 1

    local assigned_bounties = {}
    while assigned < count do
        local zone = zones[zone_idx]
        if not zone then break end

        local bounty = PickBountyForZone(zone, used_entries)
        if bounty then
            table.insert(used_entries, bounty.entry)
            table.insert(assigned_bounties, bounty)
            CharDBExecute(string.format(
                "INSERT INTO bountyworld_bounties "
             .. "(guid, bracket, bounty_entry, bounty_name, bounty_zone, killed, assigned_at) "
             .. "VALUES (%d, %d, %d, '%s', '%s', 0, %d)",
                guid, bracket, bounty.entry,
                EscapeSQL(bounty.name),
                EscapeSQL(bounty.zone),
                os.time()))
            assigned = assigned + 1
        end

        zone_idx = zone_idx + 1
        if zone_idx > #zones then break end
    end

    local data = {bracket=bracket, run_active=1, seed=CURRENT_SEED}
    SaveRunData(player, data)

    Msg(player, "Bracket " .. bracket .. " - " .. assigned .. " bounties assigned!")
    for i, b in ipairs(assigned_bounties) do
        Msg(player, C_GOLD .. i .. ". " .. b.name .. C_RESET
            .. " - " .. C_RED .. "Location: Unknown" .. C_RESET)
    end
    Msg(player, "Say \"bw hint\" for hints.")
end

-- ------------------------------------------------------------
-- HINT SYSTEM
-- ------------------------------------------------------------
local hint_timers = {}

local function StartHintTimer(player, bracket)
    hint_timers[player:GetGUIDLow()] = {
        start_time = os.time(),
        bracket    = bracket,
    }
end

local function GetHintText(player, bracket)
    local guid  = player:GetGUIDLow()
    local timer = hint_timers[guid]
    if not timer then
        StartHintTimer(player, bracket)
        timer = hint_timers[guid]
    end

    local elapsed = os.time() - timer.start_time

    if elapsed < HINT_1_DELAY then
        local remaining = HINT_1_DELAY - elapsed
        local mins = math.floor(remaining / 60)
        local secs = remaining % 60
        return string.format("Next hint in %d:%02d - %s",
            mins, secs, BRACKET_FLAVOR[bracket] or "")
    end

    local bounties = GetBounties(player, bracket)
    if elapsed < HINT_2_DELAY then
        local lines = {}
        for _, b in ipairs(bounties) do
            if b.killed == 0 then
                table.insert(lines, C_GOLD .. b.name .. C_RESET
                    .. " - Continent revealed")
            end
        end
        return table.concat(lines, "\n")
    end

    -- Full hint: zone revealed
    local lines = {}
    for _, b in ipairs(bounties) do
        if b.killed == 0 then
            table.insert(lines, C_GOLD .. b.name .. C_RESET
                .. " - " .. C_GOLD .. b.zone .. C_RESET)
        end
    end
    return table.concat(lines, "\n")
end

-- ------------------------------------------------------------
-- LOGIN
-- ------------------------------------------------------------
local function OnLogin(event, player)
    local data = GetRunData(player)

    if not data or data.run_active == 0 then
        Msg(player, "Welcome to BountyWorld! Starting your run...")
        AssignBounties(player, 1)
    else
        local bracket  = data.bracket
        local bounties = GetBounties(player, bracket)
        local killed   = 0
        for _, b in ipairs(bounties) do
            if b.killed == 1 then killed = killed + 1 end
        end

        Msg(player, "Welcome back, hunter.")
        Msg(player, "Bracket " .. bracket .. " - "
            .. killed .. "/" .. #bounties .. " bounties killed")

        for i, b in ipairs(bounties) do
            if b.killed == 0 then
                Msg(player, C_GOLD .. i .. ". " .. b.name .. C_RESET
                    .. " - " .. C_RED .. "Unknown" .. C_RESET)
            else
                Msg(player, C_GREEN .. i .. ". " .. b.name .. " [KILLED]" .. C_RESET)
            end
        end

        StartHintTimer(player, bracket)
    end
end

-- ------------------------------------------------------------
-- KILL DETECTION
-- ------------------------------------------------------------
local function OnCreatureKill(event, player, creature)
    local data = GetRunData(player)
    if not data or data.run_active == 0 then return end

    local killed_entry = creature:GetEntry()
    local bracket      = data.bracket

    -- Check if killed creature is one of our bounties
    local bounties = GetBounties(player, bracket)
    local found    = false
    for _, b in ipairs(bounties) do
        if b.entry == killed_entry and b.killed == 0 then
            found = true
            break
        end
    end
    if not found then return end

    -- Mark it killed
    MarkBountyKilled(player, bracket, killed_entry)
    Msg(player, C_GREEN .. "BOUNTY KILLED!" .. C_RESET
        .. " " .. creature:GetName())

    -- Update meta
    if BW_OnBountyKilled then BW_OnBountyKilled(player, bracket) end

    -- Count remaining in memory (don't re-query DB since MarkBountyKilled is async)
    local remaining = 0
    for _, b in ipairs(bounties) do
        if b.entry ~= killed_entry and b.killed == 0 then
            remaining = remaining + 1
        end
    end

    if remaining == 0 then
        -- Check for clean clear BEFORE advancing bracket
        local playerLevel = player:GetLevel()
        local levelCap    = BRACKET_LEVEL_CAP[bracket] or 60
        local isClean     = (playerLevel <= levelCap)

        if isClean then
            -- Award clean clear bonuses
            local clears = (data.clean_clears or 0) + 1
            data.clean_clears = clears

            -- Gold reward
            local gold = BRACKET_GOLD[bracket] or 100000
            player:ModifyMoney(gold)

            -- Medallion item — remove old one, give new tier
            local oldItem = MEDALLION_ITEMS[clears - 1]
            if oldItem then
                player:RemoveItem(oldItem, 1)
            end
            local newItem = MEDALLION_ITEMS[clears]
            if newItem then
                player:AddItem(newItem, 1)
            end

            Msg(player, C_GOLD .. "CLEAN CLEAR! Bracket " .. bracket
                .. " cleared at level " .. playerLevel .. "/" .. levelCap .. "!" .. C_RESET)
            Msg(player, C_SILVER .. "Rewards: " .. (gold/10000) .. "g + Hunter's Medallion "
                .. (clears) .. " + 5% XP bonus stacking!" .. C_RESET)
        end

        local next_bracket = bracket + 1
        if next_bracket > 7 then
            Msg(player, C_GOLD .. "* TRUE VICTORY! You cleared all brackets! *" .. C_RESET)
            data.run_active = 0
            SaveRunData(player, data)
        else
            Msg(player, C_GOLD .. "All bounties killed! Advancing to bracket "
                .. next_bracket .. "!" .. C_RESET)
            hint_timers[player:GetGUIDLow()] = nil
            AssignBounties(player, next_bracket)
        end
    else
        Msg(player, C_SILVER .. remaining .. " bounties remaining in bracket "
            .. bracket .. C_RESET)
    end

    -- Give bonus XP for clean clear stacks
    if data.clean_clears and data.clean_clears > 0 then
        local baseXP = creature:GetMaxHealth()  -- rough XP approximation
        local bonus  = math.floor(baseXP * XP_BONUS_PER_CLEAR * data.clean_clears)
        if bonus > 0 then
            player:GiveXP(bonus, nil)
        end
    end

    -- Push UI update
    if BW_SendUIData then
        local guid = player:GetGUID()
        CreateLuaEvent(function()
            local p = GetPlayerByGUID(guid)
            if p then BW_SendUIData(p) end
        end, 500, 1)
    end
end

-- ------------------------------------------------------------
-- DEATH
-- ------------------------------------------------------------
local function OnPlayerKilledByCreature(event, killer, player)
    local data = GetRunData(player)
    if not data or data.run_active == 0 then return end

    Msg(player, C_RED .. "You have fallen. Your run is over." .. C_RESET)
    Msg(player, C_SILVER .. "You reached bracket " .. data.bracket .. C_RESET)

    data.run_active = 0
    SaveRunData(player, data)
    hint_timers[player:GetGUIDLow()] = nil

    if BW_OnPlayerDied then BW_OnPlayerDied(player, data.bracket) end

    if BW_SendUIData then
        local guid = player:GetGUID()
        CreateLuaEvent(function()
            local p = GetPlayerByGUID(guid)
            if p then BW_SendUIData(p) end
        end, 500, 1)
    end
end

-- ------------------------------------------------------------
-- CHAT COMMANDS
-- ------------------------------------------------------------
local function OnChat(event, player, msg, msgType, lang)
    local lower = string.lower(msg)
    if not string.match(lower, "^bw") then return end

    local sub = string.match(lower, "^bw%s*(%S*)") or ""
    local data = GetRunData(player)

    if sub == "hint" then
        if not data or data.run_active == 0 then
            Msg(player, "No active run.")
        else
            Msg(player, GetHintText(player, data.bracket))
        end

    elseif sub == "status" then
        if not data or data.run_active == 0 then
            Msg(player, "No active run.")
        else
            local bounties = GetBounties(player, data.bracket)
            Msg(player, "Bracket: " .. data.bracket)
            for i, b in ipairs(bounties) do
                local status = b.killed == 1
                    and (C_GREEN .. "[KILLED]" .. C_RESET)
                    or  (C_RED   .. "[ALIVE]"  .. C_RESET)
                Msg(player, i .. ". " .. C_GOLD .. b.name .. C_RESET
                    .. " - " .. b.zone .. " " .. status)
            end
        end

    elseif sub == "info" then
        if not player:IsGM() then Msg(player, "GM only.") return false end
        if not data then Msg(player, "No run data.") return false end
        local bounties = GetBounties(player, data.bracket)
        Msg(player, "------- Bounty Info -------")
        Msg(player, "Bracket: " .. data.bracket)
        for i, b in ipairs(bounties) do
            Msg(player, i .. ". Entry:" .. b.entry
                .. " " .. b.name .. " in " .. b.zone
                .. (b.killed == 1 and " [KILLED]" or ""))
            local zq = WorldDBQuery(string.format(
                "SELECT COUNT(*) FROM creature WHERE id1 = %d", b.entry))
            if zq then
                Msg(player, "   Spawns in world: " .. zq:GetUInt32(0))
            end
        end
        Msg(player, "---------------------------------")

    elseif sub == "zones" then
        if not player:IsGM() then Msg(player, "GM only.") return false end
        local activeSeed = (data and data.seed and data.seed > 0) and data.seed or CURRENT_SEED
        local q = CharDBQuery(string.format(
            "SELECT zone_name, bracket FROM bountyworld_bracket_zones "
         .. "WHERE seed = %d ORDER BY bracket, zone_name", activeSeed))
        if not q then
            Msg(player, "No zone data for seed " .. activeSeed)
            return false
        end
        local colors = {[1]="|cff00FF00",[2]="|cff66E600",[3]="|cffFFE600",
                        [4]="|cffFF8C00",[5]="|cffFF4000",[6]="|cffFF0000",[7]="|cff9900FF"}
        Msg(player, "--- Zone Brackets (seed " .. activeSeed .. ") ---")
        repeat
            local zone    = q:GetString(0)
            local bracket = q:GetUInt8(1)
            local col     = colors[bracket] or C_SILVER
            Msg(player, col .. "B" .. bracket .. "|r  " .. zone)
        until not q:NextRow()

    elseif sub == "reset" then
        if not player:IsGM() then Msg(player, "GM only.") return false end
        local guid = player:GetGUIDLow()
        CharDBExecute(string.format("DELETE FROM bountyworld_run WHERE guid = %d", guid))
        CharDBExecute(string.format("DELETE FROM bountyworld_bounties WHERE guid = %d", guid))
        hint_timers[guid] = nil
        Msg(player, "Run reset. Assigning fresh bracket 1 bounty...")
        AssignBounties(player, 1)
        if BW_SendUIData then
            local pguid = player:GetGUID()
            CreateLuaEvent(function()
                local p = GetPlayerByGUID(pguid)
                if p then BW_SendUIData(p) end
            end, 500, 1)
        end

    elseif sub == "fullreset" then
        if not player:IsGM() then Msg(player, "GM only.") return false end
        local guid      = player:GetGUIDLow()
        local accountId = player:GetAccountId()
        CharDBExecute(string.format("DELETE FROM bountyworld_run WHERE guid = %d", guid))
        CharDBExecute(string.format("DELETE FROM bountyworld_bounties WHERE guid = %d", guid))
        CharDBExecute(string.format("DELETE FROM bountyworld_meta WHERE account_id = %d", accountId))
        CharDBExecute(string.format("DELETE FROM bountyworld_achievements WHERE account_id = %d", accountId))
        CharDBExecute(string.format(
            "DELETE FROM character_achievement WHERE guid = %d AND achievement BETWEEN 9001 AND 9035", guid))
        hint_timers[guid] = nil
        Msg(player, "|cffFF4444Full reset complete.|r")
        Msg(player, "Assigning fresh bracket 1 bounty...")
        AssignBounties(player, 1)
        if BW_SendUIData then
            local pguid = player:GetGUID()
            CreateLuaEvent(function()
                local p = GetPlayerByGUID(pguid)
                if p then BW_SendUIData(p) end
            end, 500, 1)
        end

    else
        Msg(player, "Commands: bw hint | bw status | bw info | bw zones | bw reset | bw fullreset")
    end

    return false
end

-- ------------------------------------------------------------
-- REGISTER EVENTS
-- ------------------------------------------------------------
RegisterPlayerEvent(3,  OnLogin)
RegisterPlayerEvent(7,  OnCreatureKill)
RegisterPlayerEvent(8,  OnPlayerKilledByCreature)
RegisterPlayerEvent(18, OnChat)