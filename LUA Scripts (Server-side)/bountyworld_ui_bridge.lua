-- ============================================================
-- BountyWorld UI Bridge (server side)
-- ============================================================
-- Pushes run data, stats, and achievements to the client addon
-- Place in: lua_scripts/bountyworld_ui_bridge.lua
-- ============================================================

local ADDON_PREFIX = "BWUI"

local function SendUIData(player)
    local guid      = player:GetGUIDLow()
    local accountId = player:GetAccountId()

    -- Run data
    local runQ = CharDBQuery(string.format(
        "SELECT current_bracket, run_active "
     .. "FROM bountyworld_run WHERE guid = %d", guid))

    if runQ then
        local bracket = runQ:GetUInt8(0)
        local active  = runQ:GetUInt8(1)

        -- Get bounties for this bracket
        local bQ = CharDBQuery(string.format(
            "SELECT bounty_entry, bounty_name, bounty_zone, killed "
         .. "FROM bountyworld_bounties WHERE guid = %d AND bracket = %d "
         .. "ORDER BY bounty_entry", guid, bracket))

        local bountyParts = {}
        if bQ then
            repeat
                local entry  = bQ:GetUInt32(0)
                local name   = string.gsub(bQ:GetString(1), " ", "_")
                local zone   = string.gsub(bQ:GetString(2), " ", "_")
                local killed = bQ:GetUInt8(3)
                table.insert(bountyParts, entry .. "," .. name .. "," .. zone .. "," .. killed)
            until not bQ:NextRow()
        end

        -- Send run state
        player:SendAddonMessage(ADDON_PREFIX,
            string.format("RUN:%d:%d:%s", bracket, active,
                table.concat(bountyParts, "|")),
            18, player)
    end

    -- Stats
    local metaQ = CharDBQuery(string.format(
        "SELECT lifetime_kills, lifetime_deaths, lifetime_runs, "
     .. "achievements, starting_level_bonus, safety_net_bracket "
     .. "FROM bountyworld_meta WHERE account_id = %d", accountId))

    if metaQ then
        player:SendAddonMessage(ADDON_PREFIX,
            string.format("STATS:%d:%d:%d:%d:%d:%d",
                metaQ:GetUInt32(0), metaQ:GetUInt32(1), metaQ:GetUInt32(2),
                metaQ:GetUInt32(3), metaQ:GetUInt8(4),  metaQ:GetUInt8(5)),
            18, player)
    else
        -- No meta row (fresh reset) — send zeroes
        player:SendAddonMessage(ADDON_PREFIX, "STATS:0:0:0:0:0:0", 18, player)
    end

    -- Also send empty achievements on reset
    local achQ = CharDBQuery(string.format(
        "SELECT COUNT(*) FROM bountyworld_achievements WHERE account_id = %d", accountId))
    if not achQ or achQ:GetUInt32(0) == 0 then
        player:SendAddonMessage(ADDON_PREFIX, "ACH:", 18, player)
    end

    -- Achievements
    local achQ = CharDBQuery(string.format(
        "SELECT achievement_id FROM bountyworld_achievements "
     .. "WHERE account_id = %d ORDER BY achievement_id", accountId))

    if achQ then
        local ids = {}
        repeat
            table.insert(ids, tostring(achQ:GetUInt16(0)))
        until not achQ:NextRow()
        player:SendAddonMessage(ADDON_PREFIX, "ACH:" .. table.concat(ids, ","), 18, player)
    else
        player:SendAddonMessage(ADDON_PREFIX, "ACH:", 18, player)
    end
end

-- Expose globally so core and meta scripts can trigger refreshes
function BW_SendUIData(player)
    SendUIData(player)
end

local function OnLogin(event, player)
    -- Small delay to let bounty assignment complete before sending UI data
    local guid = player:GetGUID()
    CreateLuaEvent(function()
        local p = GetPlayerByGUID(guid)
        if p then SendUIData(p) end
    end, 1000, 1)
end

RegisterPlayerEvent(3, OnLogin)