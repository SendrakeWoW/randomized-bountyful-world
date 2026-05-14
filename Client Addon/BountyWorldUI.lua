-- BountyWorld UI Addon
-- Interface/AddOns/BountyWorldUI/BountyWorldUI.lua

local ADDON_NAME   = "BountyWorldUI"
local ADDON_PREFIX = "BWUI"

BountyWorldUIData = BountyWorldUIData or {
    run          = {},
    achievements = {},
    stats        = {},
}

-- Achievement definitions
local ALL_ACHIEVEMENTS = {
    {id=1,  name="First Blood",          desc="Kill your first bounty target",              cat="Milestone"},
    {id=2,  name="On the Trail",         desc="Kill 5 bounty targets",                      cat="Milestone"},
    {id=3,  name="Seasoned Hunter",      desc="Kill 10 bounty targets",                     cat="Milestone"},
    {id=4,  name="Relentless",           desc="Kill 15 bounty targets",                     cat="Milestone"},
    {id=5,  name="Veteran of the Hunt",  desc="Kill 20 bounty targets",                     cat="Milestone"},
    {id=6,  name="Legend",               desc="Kill 25 bounty targets",                     cat="Milestone"},
    {id=7,  name="Eternal Hunter",       desc="Kill 30 bounty targets",                     cat="Milestone"},
    {id=9,  name="They Remember You",    desc="Die to a bounty target",                     cat="Nemesis"},
    {id=10, name="Grudge Match",         desc="Die to same bounty twice",                   cat="Nemesis"},
    {id=11, name="Old Wounds",           desc="Die to same bounty three times",             cat="Nemesis"},
    {id=12, name="Obsession",            desc="Die to same bounty five times",              cat="Nemesis"},
    {id=13, name="Reckoning",            desc="Kill your first Nemesis",                    cat="Nemesis"},
    {id=14, name="Against All Odds",     desc="Kill Nemesis that killed you 5+ times",      cat="Nemesis"},
    {id=15, name="Many Enemies",         desc="Have 3 active Nemeses",                      cat="Nemesis"},
    {id=16, name="Clean Slate",          desc="Kill 5 Nemeses in one run",                  cat="Nemesis"},
    {id=17, name="Ghost",                desc="Kill bounty within 10 min",                  cat="Style"},
    {id=18, name="No Witnesses",         desc="Kill bounty without taking damage",           cat="Style"},
    {id=19, name="Stubborn",             desc="Kill bounty without hints",                  cat="Style"},
    {id=20, name="Blindfolded",          desc="Complete run using zero hints",               cat="Style"},
    {id=21, name="Speedrunner",          desc="Complete brackets 1-3 in 2 hours",           cat="Style"},
    {id=22, name="Wanderer",             desc="Enter 10 zones in one run",                  cat="Exploration"},
    {id=23, name="Cartographer",         desc="Enter every zone in one run",                cat="Exploration"},
    {id=24, name="Deep Cut",             desc="Reach bracket 5 without dying",              cat="Exploration"},
    {id=25, name="Wrong Neighbourhood",  desc="Enter bracket 5 zone on bracket 1",          cat="Exploration"},
    {id=26, name="Survivor",             desc="Complete run without dying",                  cat="Mastery"},
    {id=27, name="Comeback Kid",         desc="Start from safety net, reach bracket 5",     cat="Mastery"},
    {id=28, name="Back to Basics",       desc="Start bracket 1 despite safety net",         cat="Mastery"},
    {id=29, name="Ascending",            desc="Beat personal best 3 runs in a row",         cat="Mastery"},
    {id=30, name="The Long Road",        desc="10 hours total playtime",                    cat="Mastery"},
    {id=31, name="Humbling",             desc="Be killed by a critter",                     cat="Hidden", hidden=true},
    {id=32, name="Predator",             desc="Bounty dead on arrival",                     cat="Hidden", hidden=true},
    {id=33, name="Full Circle",          desc="Kill Nemesis before it's assigned",          cat="Hidden", hidden=true},
    {id=34, name="Overkill",             desc="Kill bounty in one hit at 10x health",       cat="Hidden", hidden=true},
    {id=35, name="Ghost Town",           desc="Bracket 1 killing only bounty",              cat="Hidden", hidden=true},
}

-- Colors
local C = {
    gold   = {1.0,  0.84, 0.0},
    white  = {1.0,  1.0,  1.0},
    gray   = {0.5,  0.5,  0.5},
    green  = {0.2,  0.9,  0.2},
    red    = {0.9,  0.2,  0.2},
    dim    = {0.3,  0.3,  0.35},
    border = {0.6,  0.5,  0.1,  1.0},
    bracket = {
        [1]={0.0, 1.0, 0.0},
        [2]={0.4, 0.9, 0.0},
        [3]={1.0, 0.9, 0.0},
        [4]={1.0, 0.55,0.0},
        [5]={1.0, 0.25,0.0},
        [6]={1.0, 0.0, 0.0},
        [7]={0.6, 0.0, 1.0},
    },
}

-- ── Main Frame ────────────────────────────────────────────────────────────────
local frame = CreateFrame("Frame", "BountyWorldUIFrame", UIParent)
frame:SetSize(440, 520)
frame:SetPoint("CENTER")
frame:SetFrameStrata("DIALOG")
frame:SetMovable(true)
frame:EnableMouse(true)
frame:RegisterForDrag("LeftButton")
frame:SetScript("OnDragStart", frame.StartMoving)
frame:SetScript("OnDragStop", frame.StopMovingOrSizing)
frame:Hide()

local bg = frame:CreateTexture(nil, "BACKGROUND")
bg:SetAllPoints()
bg:SetTexture("Interface\\Buttons\\WHITE8X8")
bg:SetVertexColor(0.05, 0.05, 0.08, 0.95)

-- Border
for _, side in ipairs({"TOP","BOTTOM","LEFT","RIGHT"}) do
    local t = frame:CreateTexture(nil, "OVERLAY")
    t:SetTexture("Interface\\Buttons\\WHITE8X8")
    t:SetVertexColor(0.6, 0.5, 0.1, 1)
    if side == "TOP" or side == "BOTTOM" then
        t:SetSize(440, 1)
    else
        t:SetSize(1, 520)
    end
    t:SetPoint(side)
end

-- Title
local titleBg = frame:CreateTexture(nil, "BACKGROUND")
titleBg:SetSize(440, 32)
titleBg:SetPoint("TOP")
titleBg:SetTexture("Interface\\Buttons\\WHITE8X8")
titleBg:SetVertexColor(0.08, 0.06, 0.02, 1)

local titleText = frame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
titleText:SetPoint("TOPLEFT", frame, "TOPLEFT", 12, -9)
titleText:SetText("|cffFFD700BOUNTY WORLD|r")
titleText:SetFont("Fonts\\FRIZQT__.TTF", 14, "OUTLINE")

local closeBtn = CreateFrame("Button", nil, frame, "UIPanelCloseButton")
closeBtn:SetSize(24, 24)
closeBtn:SetPoint("TOPRIGHT", -4, -4)
closeBtn:SetScript("OnClick", function() frame:Hide() end)

-- ── Tabs ──────────────────────────────────────────────────────────────────────
local tabs = {}
local tabPanels = {}
local activeTab = 1
local TAB_NAMES = {"Run", "Achievements", "Stats"}

local function ShowTab(idx)
    activeTab = idx
    for i = 1, #TAB_NAMES do
        if i == idx then
            tabPanels[i]:Show()
            tabs[i].bg:SetVertexColor(0.15, 0.12, 0.03, 1)
            tabs[i].text:SetTextColor(C.gold[1], C.gold[2], C.gold[3])
        else
            tabPanels[i]:Hide()
            tabs[i].bg:SetVertexColor(0.08, 0.08, 0.12, 1)
            tabs[i].text:SetTextColor(C.gray[1], C.gray[2], C.gray[3])
        end
    end
end

for i, name in ipairs(TAB_NAMES) do
    local tw = 440 / #TAB_NAMES
    local tab = CreateFrame("Button", nil, frame)
    tab:SetSize(tw - 2, 28)
    tab:SetPoint("TOPLEFT", frame, "TOPLEFT", (i-1)*tw + 1, -32)

    local tabBg = tab:CreateTexture(nil, "BACKGROUND")
    tabBg:SetAllPoints()
    tabBg:SetTexture("Interface\\Buttons\\WHITE8X8")
    tabBg:SetVertexColor(0.08, 0.08, 0.12, 1)
    tab.bg = tabBg

    local tabText = tab:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    tabText:SetPoint("CENTER")
    tabText:SetText(name)
    tabText:SetFont("Fonts\\FRIZQT__.TTF", 11, "OUTLINE")
    tab.text = tabText

    local idx = i
    tab:SetScript("OnClick", function() ShowTab(idx) end)
    tabs[i] = tab

    local panel = CreateFrame("Frame", nil, frame)
    panel:SetSize(440, 455)
    panel:SetPoint("TOPLEFT", frame, "TOPLEFT", 0, -65)
    tabPanels[i] = panel
end

ShowTab(1)

-- ── TAB 1: RUN ────────────────────────────────────────────────────────────────
local runPanel = tabPanels[1]

local function AddLabel(parent, text, x, y, font, r, g, b)
    local fs = parent:CreateFontString(nil, "OVERLAY", font or "GameFontNormalSmall")
    fs:SetPoint("TOPLEFT", parent, "TOPLEFT", x, y)
    fs:SetText(text)
    if r then fs:SetTextColor(r, g, b) end
    return fs
end

local function MakeField(parent, label, y)
    local lbl = AddLabel(parent, label, 20, y, "GameFontNormalSmall", unpack(C.gray))
    local val = AddLabel(parent, "--", 160, y, "GameFontNormal", unpack(C.white))
    return val
end

AddLabel(runPanel, "ACTIVE BOUNTIES", 20, -12, "GameFontNormal", unpack(C.gold))

local runBracket = MakeField(runPanel, "Bracket", -35)
local runStatus  = MakeField(runPanel, "Run Status", -52)
local runProgress = AddLabel(runPanel, "", 20, -72, "GameFontNormalSmall", unpack(C.gray))

-- Separator
local sep1 = runPanel:CreateTexture(nil, "ARTWORK")
sep1:SetTexture("Interface\\Buttons\\WHITE8X8")
sep1:SetVertexColor(0.6, 0.5, 0.1, 0.3)
sep1:SetSize(400, 1)
sep1:SetPoint("TOPLEFT", runPanel, "TOPLEFT", 20, -82)

AddLabel(runPanel, "TARGETS", 20, -90, "GameFontNormalSmall", unpack(C.gray))

-- Pre-create 7 bounty rows
local MAX_BOUNTIES = 7
local bountyRows = {}
for i = 1, MAX_BOUNTIES do
    local row = CreateFrame("Frame", nil, runPanel)
    row:SetSize(400, 34)
    row:SetPoint("TOPLEFT", runPanel, "TOPLEFT", 10, -105 - (i-1)*36)

    local num = row:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    num:SetPoint("TOPLEFT", row, "TOPLEFT", 4, -2)
    num:SetText(tostring(i) .. ".")
    row.num = num

    local name = row:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    name:SetPoint("TOPLEFT", row, "TOPLEFT", 22, -2)
    name:SetText("")
    row.name = name

    local zone = row:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    zone:SetPoint("TOPLEFT", row, "TOPLEFT", 22, -18)
    zone:SetText("")
    row.zone = zone

    row:Hide()
    bountyRows[i] = row
end

local function UpdateRunTab()
    for i = 1, MAX_BOUNTIES do
        bountyRows[i]:Hide()
    end

    local r = BountyWorldUIData.run
    if not r or not r.bracket then
        runBracket:SetText("|cffFF4444No active run|r")
        runStatus:SetText("--")
        runProgress:SetText("")
        return
    end

    local bc = C.bracket[r.bracket] or C.white
    runBracket:SetText(string.format("|cff%02x%02x%02xBracket %d|r",
        bc[1]*255, bc[2]*255, bc[3]*255, r.bracket))
    runStatus:SetText(r.run_active == 1 and "|cff44FF44Active|r" or "|cffFF4444Inactive|r")

    local bounties = r.bounties or {}
    local killed = 0
    for _, b in ipairs(bounties) do
        if b.killed == 1 then killed = killed + 1 end
    end
    runProgress:SetText("Progress: " .. killed .. "/" .. #bounties .. " killed")

    for i, b in ipairs(bounties) do
        if i > MAX_BOUNTIES then break end
        local row = bountyRows[i]
        local isKilled = b.killed == 1

        if isKilled then
            row.num:SetTextColor(C.green[1], C.green[2], C.green[3])
            row.name:SetText("|cff44FF44" .. (b.name or "?") .. " [KILLED]|r")
            row.zone:SetText("|cff555555" .. (b.zone or "") .. "|r")
        else
            row.num:SetTextColor(C.gold[1], C.gold[2], C.gold[3])
            row.name:SetText("|cffFFD700" .. (b.name or "?") .. "|r")
            row.zone:SetText("|cff888888" .. (b.zone or "Unknown") .. "|r")
        end
        row:Show()
    end
end

-- ── TAB 2: ACHIEVEMENTS ───────────────────────────────────────────────────────
local achPanel = tabPanels[2]

local achScroll = CreateFrame("ScrollFrame", "BWAchScroll", achPanel, "UIPanelScrollFrameTemplate")
achScroll:SetSize(410, 430)
achScroll:SetPoint("TOPLEFT", achPanel, "TOPLEFT", 8, -8)

local achContent = CreateFrame("Frame", nil, achScroll)
achContent:SetSize(390, 1400)
achScroll:SetScrollChild(achContent)

local achFontStrings = {}

local function UpdateAchievements()
    -- Hide all previously created font strings
    for _, fs in ipairs(achFontStrings) do
        fs:Hide()
    end
    achFontStrings = {}

    local earned = BountyWorldUIData.achievements or {}
    local earnedSet = {}
    for _, id in ipairs(earned) do earnedSet[id] = true end

    local currentCat = nil
    local y = -8

    for _, ach in ipairs(ALL_ACHIEVEMENTS) do
        -- Category header
        if ach.cat ~= currentCat then
            currentCat = ach.cat
            local catLabel = achContent:CreateFontString(nil, "OVERLAY", "GameFontNormal")
            table.insert(achFontStrings, catLabel)
            catLabel:SetPoint("TOPLEFT", achContent, "TOPLEFT", 8, y)
            catLabel:SetText(string.upper(currentCat))
            catLabel:SetTextColor(C.gold[1], C.gold[2], C.gold[3])
            catLabel:SetFont("Fonts\\FRIZQT__.TTF", 10, "OUTLINE")
            y = y - 20
        end

        local isEarned = earnedSet[ach.id]
        local isHidden = ach.hidden and not isEarned

        local icon = achContent:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
        table.insert(achFontStrings, icon)
        icon:SetPoint("TOPLEFT", achContent, "TOPLEFT", 10, y - 6)
        if isEarned then
            icon:SetText("|cff44FF44+|r")
        elseif isHidden then
            icon:SetText("|cff555555?|r")
        else
            icon:SetText("|cff444444o|r")
        end

        local nameLabel = achContent:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
        table.insert(achFontStrings, nameLabel)
        nameLabel:SetPoint("TOPLEFT", achContent, "TOPLEFT", 26, y - 2)
        if isHidden then
            nameLabel:SetText("|cff555555???|r")
        elseif isEarned then
            nameLabel:SetText("|cffFFD700" .. ach.name .. "|r")
        else
            nameLabel:SetText("|cffAAAAAA" .. ach.name .. "|r")
        end

        local descLabel = achContent:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
        table.insert(achFontStrings, descLabel)
        descLabel:SetPoint("TOPLEFT", achContent, "TOPLEFT", 26, y - 16)
        if isHidden then
            descLabel:SetText("|cff333333Hidden achievement|r")
        else
            descLabel:SetText("|cff666666" .. ach.desc .. "|r")
        end

        y = y - 36
    end

    achContent:SetHeight(math.abs(y) + 20)
end

-- ── TAB 3: STATS ─────────────────────────────────────────────────────────────
local statsPanel = tabPanels[3]

local function MakeStatField(label, y)
    local lbl = AddLabel(statsPanel, label, 20, y, "GameFontNormalSmall", unpack(C.gray))
    local val = AddLabel(statsPanel, "--", 220, y, "GameFontNormal", unpack(C.white))
    return val
end

AddLabel(statsPanel, "LIFETIME STATS", 20, -12, "GameFontNormal", unpack(C.gold))

local statKills    = MakeStatField("Bounties killed",     -35)
local statDeaths   = MakeStatField("Deaths",              -52)
local statRuns     = MakeStatField("Runs completed",      -69)
local statAch      = MakeStatField("Achievements",        -86)
local statBonus    = MakeStatField("Level bonus",         -103)

local sep2 = statsPanel:CreateTexture(nil, "ARTWORK")
sep2:SetTexture("Interface\\Buttons\\WHITE8X8")
sep2:SetVertexColor(0.6, 0.5, 0.1, 0.3)
sep2:SetSize(400, 1)
sep2:SetPoint("TOPLEFT", statsPanel, "TOPLEFT", 20, -118)

AddLabel(statsPanel, "CURRENT META", 20, -128, "GameFontNormal", unpack(C.gold))
local statSafety   = MakeStatField("Safety net bracket",  -151)
local statNextRun  = MakeStatField("Next run starts at",  -168)

local sep3 = statsPanel:CreateTexture(nil, "ARTWORK")
sep3:SetTexture("Interface\\Buttons\\WHITE8X8")
sep3:SetVertexColor(0.6, 0.5, 0.1, 0.3)
sep3:SetSize(400, 1)
sep3:SetPoint("TOPLEFT", statsPanel, "TOPLEFT", 20, -188)

AddLabel(statsPanel, "MILESTONE PROGRESS", 20, -198, "GameFontNormal", unpack(C.gold))

local milestones = {
    {kills=1,  label="First Blood"},
    {kills=5,  label="On the Trail"},
    {kills=10, label="Seasoned Hunter"},
    {kills=15, label="Relentless"},
    {kills=20, label="Veteran of the Hunt"},
    {kills=25, label="Legend"},
    {kills=30, label="Eternal Hunter"},
}

local milestoneLabels = {}
for i, m in ipairs(milestones) do
    local y = -215 - (i-1)*18
    local killLbl = AddLabel(statsPanel, m.kills .. " kills", 25, y, "GameFontNormalSmall", unpack(C.gray))
    local nameLbl = AddLabel(statsPanel, m.label,             95, y, "GameFontNormalSmall", unpack(C.dim))
    milestoneLabels[i] = {killLbl, nameLbl, kills=m.kills}
end

local function UpdateStatsTab()
    local s = BountyWorldUIData.stats
    if not s or not s.kills then
        statKills:SetText("--") ; statDeaths:SetText("--")
        statRuns:SetText("--")  ; statAch:SetText("--")
        statBonus:SetText("--") ; statSafety:SetText("--")
        statNextRun:SetText("--")
        return
    end

    statKills:SetText(tostring(s.kills or 0))
    statDeaths:SetText(tostring(s.deaths or 0))
    statRuns:SetText(tostring(s.runs or 0))
    statAch:SetText(tostring(s.achievements or 0) .. " / 35")
    statBonus:SetText("+" .. tostring(s.level_bonus or 0) .. " levels")

    local safety = s.safety_bracket or 0
    statSafety:SetText(safety > 0 and ("Bracket " .. safety) or "None")
    statNextRun:SetText(safety > 0 and ("Bracket " .. safety) or "Bracket 1")

    local kills = s.kills or 0
    for _, m in ipairs(milestoneLabels) do
        local done = kills >= m.kills
        m[1]:SetTextColor(done and C.green[1] or C.gray[1],
                          done and C.green[2] or C.gray[2],
                          done and C.green[3] or C.gray[3])
        m[2]:SetTextColor(done and C.gold[1] or C.dim[1],
                          done and C.gold[2] or C.dim[2],
                          done and C.gold[3] or C.dim[3])
    end
end

-- ── Addon message handler ─────────────────────────────────────────────────────
local function OnAddonMessage(prefix, message)
    if prefix ~= ADDON_PREFIX then return end
    local msgType = string.match(message, "^(%u+):")
    local payload = string.match(message, "^%u+:(.*)")
    if not msgType then return end

    if msgType == "RUN" then
        local bracket, active, bountiesStr = string.match(payload, "^(%d+):(%d+):(.*)")
        if bracket then
            local bounties = {}
            if bountiesStr and bountiesStr ~= "" then
                for part in string.gmatch(bountiesStr, "[^|]+") do
                    local e, n, z, k = string.match(part, "^(%d+),([^,]+),([^,]+),(%d+)$")
                    if e then
                        table.insert(bounties, {
                            entry  = tonumber(e),
                            name   = string.gsub(n, "_", " "),
                            zone   = string.gsub(z, "_", " "),
                            killed = tonumber(k),
                        })
                    end
                end
            end
            BountyWorldUIData.run = {
                bracket    = tonumber(bracket),
                run_active = tonumber(active),
                bounties   = bounties,
            }
            UpdateRunTab()
        end

    elseif msgType == "STATS" then
        local k, d, r, a, l, s = string.match(payload, "^(%d+):(%d+):(%d+):(%d+):(%d+):(%d+)")
        if k then
            BountyWorldUIData.stats = {
                kills=tonumber(k), deaths=tonumber(d), runs=tonumber(r),
                achievements=tonumber(a), level_bonus=tonumber(l),
                safety_bracket=tonumber(s),
            }
            UpdateStatsTab()
        end

    elseif msgType == "ACH" then
        local ids = {}
        for id in string.gmatch(payload, "%d+") do
            table.insert(ids, tonumber(id))
        end
        BountyWorldUIData.achievements = ids
        UpdateAchievements()
    end
end

-- ── Event frame ───────────────────────────────────────────────────────────────
local eventFrame = CreateFrame("Frame", "BountyWorldUIEvents")
eventFrame:RegisterEvent("ADDON_LOADED")
eventFrame:RegisterEvent("CHAT_MSG_ADDON")
eventFrame:SetScript("OnEvent", function(self, event, ...)
    if event == "ADDON_LOADED" then
        local name = ...
        if name == ADDON_NAME then
            if RegisterAddonMessagePrefix then
                RegisterAddonMessagePrefix(ADDON_PREFIX)
            end
            UpdateRunTab()
            UpdateAchievements()
            UpdateStatsTab()
        end
    elseif event == "CHAT_MSG_ADDON" then
        local pfx, msg = ...
        OnAddonMessage(pfx, msg)
    end
end)

WorldMapFrame:HookScript("OnShow", function()
    -- reserved for map integration
end)

-- ── Minimap button ────────────────────────────────────────────────────────────
local minimapBtn = CreateFrame("Button", "BWMinimapButton", UIParent)
minimapBtn:SetSize(28, 28)
minimapBtn:SetFrameStrata("HIGH")
minimapBtn:SetPoint("TOPRIGHT", Minimap, "TOPRIGHT", -5, -5)

local minimapBg = minimapBtn:CreateTexture(nil, "BACKGROUND")
minimapBg:SetAllPoints()
minimapBg:SetTexture("Interface\\Buttons\\WHITE8X8")
minimapBg:SetVertexColor(0.5, 0.35, 0.0, 1)

local minimapText = minimapBtn:CreateFontString(nil, "OVERLAY")
minimapText:SetPoint("CENTER")
minimapText:SetFont("Fonts\\FRIZQT__.TTF", 10, "OUTLINE")
minimapText:SetText("BW")
minimapText:SetTextColor(1, 1, 1)

minimapBtn:SetScript("OnClick", function()
    if frame:IsShown() then frame:Hide() else frame:Show() end
end)
minimapBtn:SetScript("OnEnter", function()
    GameTooltip:SetOwner(minimapBtn, "ANCHOR_LEFT")
    GameTooltip:SetText("BountyWorld")
    GameTooltip:AddLine("Click to open", 1, 1, 1)
    GameTooltip:Show()
end)
minimapBtn:SetScript("OnLeave", function() GameTooltip:Hide() end)

-- ── Slash commands ────────────────────────────────────────────────────────────
SLASH_BOUNTYWORLD1 = "/bw"
SLASH_BOUNTYWORLD2 = "/bountyworld"
SlashCmdList["BOUNTYWORLD"] = function(msg)
    local sub = string.lower(msg or "")
    if sub == "run" then ShowTab(1)
    elseif sub == "achievements" or sub == "ach" then ShowTab(2)
    elseif sub == "stats" then ShowTab(3)
    end
    if frame:IsShown() and msg == "" then frame:Hide()
    else frame:Show() end
end

print("|cffFFD700[BountyWorld]|r UI loaded. /bw to open.")