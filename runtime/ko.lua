-- Korean rendering for the byte-oriented LovePotion 1.0.x runtime.
local K = {}
local graphics = love.graphics
local nativePrint, nativePrintf, nativeDraw = graphics.print, graphics.printf, graphics.draw
local glyphs = require('ko_glyphs')
local ui = require('ko_ui')
local tutorialGlyphs = require('ko_tutorial_glyphs')
local tutorialSheet, tutorialQuads
local sheets, quads = {}, {}
local pattern = '[%z\1-\127\194-\244][\128-\191]*'
local dialog = {key=false, pages={}, page=1, reveal=false, text=''}
local poem = {text=false, pages={}, page=1}

function K.reset()
    dialog={key=false,pages={},page=1,reveal=false,text=''}
    poem={text=false,pages={},page=1}
end

function K.name(value)
    value = tostring(value or '')
    return ui[value] or value
end

function K.ui(value)
    local text = tostring(value or '')
    if ui[text] then return ui[text] end
    local number = text:match('^Save File (%d+)$')
    if number then return '저장 파일 '..number end
    number = text:match('^Save File (%d+) does not exist%.$')
    if number then return '저장 파일 '..number..' 없음' end
    local page, total = text:match('^Page (%d+) of (%d+)$')
    if page then return page..' / '..total end
    local who = text:match('^I would walk home with (.-)%.$')
    if who then return K.name(who)..'와 집에 간다.' end
    return text
end

function K.width(text)
    local width, maximum = 0, 0
    for char in tostring(text):gmatch(pattern) do
        if char == '\n' then maximum=math.max(maximum,width); width=0
        else width=width+(glyphs[char] and glyphs[char][4] or 7) end
    end
    return math.max(width,maximum)
end

function K.wrap(text, limit)
    local lines, line, width = {}, '', 0
    for char in tostring(text):gmatch(pattern) do
        local advance = glyphs[char] and glyphs[char][4] or 7
        if char=='\n' then
            lines[#lines+1]=line; line=''; width=0
        else
            if width+advance>limit and line~='' then
                lines[#lines+1]=line; line=''; width=0
            end
            if char~=' ' or line~='' then line=line..char; width=width+advance end
        end
    end
    lines[#lines+1]=line
    return lines
end

local function paginate(text,width,height)
    local lines=K.wrap(text,width)
    local pages={}
    for i=1,#lines,height do
        local page={}
        for j=i,math.min(i+height-1,#lines) do page[#page+1]=lines[j] end
        pages[#pages+1]=table.concat(page,'\n')
    end
    return pages
end

function K.page(text)
    local key=tostring(chapter)..':'..tostring(cl)
    if key~=dialog.key then
        dialog={key=key,pages=paginate(text,304,4),page=1,reveal=false,text=''}
    end
    return dialog.pages[dialog.page] or text
end

function K.drip(text,speed,start)
    if dialog.reveal then dialog.text=text; return text end
    local count=math.max(0,math.floor((love.timer.getTime()-start)*speed))
    local out={}
    for char in text:gmatch(pattern) do
        if #out>=count then break end
        out[#out+1]=char
    end
    dialog.text=table.concat(out)
    return dialog.text
end

local function nextPage()
    if dialog.page<#dialog.pages then
        dialog.page=dialog.page+1;dialog.reveal=false
        myTextStartTime=love.timer.getTime(); unitimer=0
        return true
    end
    return false
end

function K.autoPage()
    return nextPage()
end

function K.advance()
    if menu_enabled then return false end
    if poem_enabled and poem.text==poemtext and poem.page<#poem.pages then
        poem.page=poem.page+1;unitimer=0;return true
    end
    local key=tostring(chapter)..':'..tostring(cl)
    if not textbox_enabled or dialog.key~=key then return false end
    if unitimer and unitimer<uniduration then return true end
    if dialog.text~=(dialog.pages[dialog.page] or '') and not dialog.reveal then
        dialog.reveal=true;return true
    end
    return nextPage()
end

function K.drawPoem()
    if poem.text~=poemtext then
        poem={text=poemtext,pages=paginate(poemtext or '',306,16),page=1}
    end
    if poembg then graphics.draw(poembg,40,0)
    else graphics.setColor(243,243,243);graphics.rectangle('fill',40,0,320,240) end
    graphics.setColor(0,0,0)
    graphics.print(poem.pages[poem.page] or '',45,6)
    graphics.print(tostring(poem.page)..' / '..#poem.pages..'  A: 다음',45,222)
end

local function render(text,x,y)
    local origin=x
    for char in text:gmatch(pattern) do
        if char=='\n' then x=origin;y=y+14
        else
            local g=glyphs[char] or glyphs['?']
            if g then
                if char~=' ' then
                    if not sheets[g[1]] then
                        sheets[g[1]]=graphics.newImage('fonts/ko'..g[1]..'.png')
                        sheets[g[1]]:setFilter('nearest','nearest')
                    end
                    if not quads[char] then quads[char]=graphics.newQuad(g[2],g[3],16,16,512,512) end
                    nativeDraw(sheets[g[1]],quads[char],x,y)
                end
                x=x+g[4]
            end
        end
    end
end

function graphics.print(text,x,y,...)
    text=K.ui(text)
    if text:find('[\128-\255]') then render(text,x or 0,y or 0)
    else nativePrint(text,x,y,...) end
end

function graphics.printf(text,x,y,limit,align,...)
    text=K.ui(text)
    if not text:find('[\128-\255]') then return nativePrintf(text,x,y,limit,align,...) end
    local lines=K.wrap(text,limit)
    for i,line in ipairs(lines) do
        local offset=0
        if align=='center' then offset=(limit-K.width(line))/2
        elseif align=='right' then offset=limit-K.width(line) end
        render(line,x+offset,y+(i-1)*14)
    end
end

-- Reuse the original 400x240 overlay, including the translucent surround,
-- pink frame and original small-panel geometry. Replace text areas only.
local function tutorialWidth(text)
    local width=0
    for char in text:gmatch(pattern) do width=width+(tutorialGlyphs[char] and tutorialGlyphs[char][4] or 4) end
    return width
end
local function tutorialText(text,x,y)
    if not tutorialSheet then
        tutorialSheet=graphics.newImage('fonts/ko_tutorial.png')
        tutorialSheet:setFilter('nearest','nearest');tutorialQuads={}
    end
    for char in text:gmatch(pattern) do
        local g=tutorialGlyphs[char]
        if g then
            if char~=' ' then
                if not tutorialQuads[char] then tutorialQuads[char]=graphics.newQuad(g[2],g[3],16,16,256,256) end
                nativeDraw(tutorialSheet,tutorialQuads[char],x,y)
            end
            x=x+g[4]
        end
    end
end
function K.drawPoemTutorial(alpha,original)
    graphics.setColor(255,255,255,alpha)
    graphics.draw(original,0,0)
    graphics.setColor(253,229,244,alpha)
    graphics.rectangle('fill',112,82,176,16)
    graphics.rectangle('fill',111,102,178,34)
    graphics.rectangle('fill',190,142,20,15)
    local function centered(text,y)
        tutorialText(text,200-tutorialWidth(text)/2,y)
    end
    graphics.setColor(55,45,51,alpha)
    centered('시를 써 볼 시간이에요!',86)
    centered('좋아하는 부원이 좋아할 단어를 고르세요.',105)
    centered('여러분의 시를 가장 좋아하는 부원과는',115)
    centered('좋은 일이 생길지도 몰라요!',125)
    graphics.setColor(190,89,154,alpha)
    for dy=-1,1 do for dx=-1,1 do
        if dx~=0 or dy~=0 then tutorialText('확인',200-tutorialWidth('확인')/2+dx,146+dy) end
    end end
    graphics.setColor(255,255,255,alpha)
    centered('확인',146)
end

return K
