local N={active=false}
local Hangul=require('hangul_input')
local items={}
local rows={'ㅂㅈㄷㄱㅅㅛㅕㅑㅐㅔ','ㅁㄴㅇㄹㅎㅗㅓㅏㅣ','ㅋㅌㅊㅍㅠㅜㅡ'}
local shift={['ㅂ']='ㅃ',['ㅈ']='ㅉ',['ㄷ']='ㄸ',['ㄱ']='ㄲ',['ㅅ']='ㅆ',['ㅐ']='ㅒ',['ㅔ']='ㅖ'}
for r,row in ipairs(rows) do
    local col=0
    for c in row:gmatch('[\194-\244][\128-\191]*') do
        items[#items+1]={label=c,x=5+(r-1)*10+col*31,y=42+(r-1)*30,w=29,h=27,row=r,char=c};col=col+1
    end
end
local function button(label,x,y,w,row,action)
    items[#items+1]={label=label,x=x,y=y,w=w,h=27,row=row,action=action}
end
button('쌍자음',5,137,59,4,'shift')
button('띄어쓰기',67,137,80,4,'space')
button('지우기',150,137,64,4,'erase')
button('시스템',217,137,97,4,'system')
button('완료',5,174,152,5,'confirm')
button('취소',161,174,153,5,'cancel')

function N.open()
    N.editor=Hangul.new(player or '');N.selected=1;N.shift=false;N.error='';N.active=true
end
function N.finish()
    local text=N.editor:text():gsub('^%s+',''):gsub('%s+$','')
    if text=='' then N.error='이름을 입력해 주세요.';return end
    local count=0
    for _ in text:gmatch('[%z\1-\127\194-\244][\128-\191]*') do count=count+1 end
    if count>12 then N.error='이름은 열두 글자까지 입력할 수 있습니다.';return end
    if text:find("['\\\r\n]") then N.error='따옴표와 역슬래시는 쓸 수 없습니다.';return end
    N.active=false
    player=text;savepersistent();cl=1;changeState('game',1)
end
function N.systemText(text)
    -- The system keyboard returns a complete string. Keep the custom keyboard
    -- open so the user can check and explicitly confirm the result.
    if text and text~='' then N.editor=Hangul.new(text) end
end
local function selectItem()
    local item=items[N.selected];N.error=''
    if item.char then
        if not N.editor:feed(N.shift and (shift[item.char] or item.char) or item.char) then N.error='이름은 열두 글자까지 입력할 수 있습니다.' end
        N.shift=false
    elseif item.action=='erase' then N.editor:backspace()
    elseif item.action=='shift' then N.shift=not N.shift
    elseif item.action=='space' then N.editor:feed(' ')
    elseif item.action=='system' then love.keyboard.setTextInput(true)
    elseif item.action=='confirm' then N.finish()
    elseif item.action=='cancel' then N.active=false;changeState('title') end
end
function N.keypressed(key)
    if key=='a' or key=='lbutton' then selectItem()
    elseif key=='b' then N.editor:backspace()
    elseif key=='x' then N.shift=not N.shift
    elseif key=='y' or key=='start' then N.finish()
    elseif key=='up' or key=='down' then
        local current=items[N.selected]
        local row=((current.row-1+(key=='down' and 1 or -1))%5)+1
        local best,distance=nil,math.huge
        for i,item in ipairs(items) do
            local d=math.abs(item.x+item.w/2-current.x-current.w/2)
            if item.row==row and d<distance then best=i;distance=d end
        end
        N.selected=best or N.selected
    elseif key=='left' or key=='right' then
        local current=items[N.selected];local same={};local at=1
        for i,item in ipairs(items) do
            if item.row==current.row then same[#same+1]=i;if i==N.selected then at=#same end end
        end
        N.selected=same[((at-1+(key=='right' and 1 or -1))%#same)+1]
    end
end
function N.touch(x,y)
    for i,item in ipairs(items) do
        if x>=item.x and x<item.x+item.w and y>=item.y and y<item.y+item.h then
            N.selected=i;selectItem();return
        end
    end
end
function N.draw()
    drawTopScreen();lg.setColor(32,23,35);lg.rectangle('fill',0,0,400,240)
    lg.setColor(255,255,255);lg.printf('이름을 입력해 주세요',10,25,380,'center')
    lg.setColor(255,220,239);lg.rectangle('fill',20,65,360,47)
    lg.setColor(30,20,30);lg.printf(N.editor:text()..'|',26,80,348,'center')
    lg.setColor(255,255,255);lg.printf(N.error,20,130,360,'center')
    lg.printf('아래 화면의 자판을 터치하거나\n십자키와 A 버튼으로 입력하세요.',20,175,360,'center')
    drawBottomScreen();lg.setColor(255,239,248);lg.rectangle('fill',0,0,320,240)
    lg.setColor(50,30,45);lg.print('한글 이름 입력',8,8)
    for i,item in ipairs(items) do
        if i==N.selected then lg.setColor(225,119,181) else lg.setColor(255,202,231) end
        lg.rectangle('fill',item.x,item.y,item.w,item.h)
        lg.setColor(30,20,30)
        local label=item.char and N.shift and (shift[item.char] or item.char) or item.label
        lg.printf(label,item.x,item.y+6,item.w,'center')
    end
    lg.setColor(50,30,45);lg.printf('A 선택  B 지움  X 쌍자음  Y 완료\n시스템: 영문 입력 또는 붙여넣기',5,209,310,'center')
end
return N
