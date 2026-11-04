-- Korean rendering for the byte-oriented LovePotion 1.0.x runtime.
local K = {}
local graphics = love.graphics
local nativePrint, nativePrintf, nativeDraw = graphics.print, graphics.printf, graphics.draw
local glyphs = require('ko_glyphs')
local ui = require('ko_ui')
local sheets, quads = {}, {}
local pattern = '[%z\1-\127\194-\244][\128-\191]*'
local dialog = {key=false, pages={}, page=1, reveal=false, text=''}
local poem = {text=false, pages={}, page=1}

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

return K
