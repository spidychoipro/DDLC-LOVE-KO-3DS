-- Delegate typing/composition to Nintendo 3DS's system software keyboard.
-- No game-drawn keyboard or custom Hangul IME is used.
local N={pending=false,notice=nil}
function N.open()
    N.pending=true;N.notice=nil
    love.keyboard.setTextInput(true)
end
local function invalid(message)
    N.notice=message;changeState('title');menu_enable('dialog');menutext=message;menu_previous='title'
    return false
end
function N.submit(text)
    if not N.pending then return false end
    N.pending=false
    if type(text)~='string' or text=='' then changeState('title');return false end
    text=text:gsub('^%s+',''):gsub('%s+$','')
    if text=='' then return invalid('이름을 입력해 주세요.') end
    local count=0
    for _ in text:gmatch('[%z\1-\127\194-\244][\128-\191]*') do count=count+1 end
    if count>12 then return invalid('이름은 열두 글자까지 입력할 수 있습니다.') end
    if text:find("['\\%z\1-\31\127]") then
        return invalid('이름에는 따옴표·역슬래시·제어 문자를 쓸 수 없습니다.')
    end
    -- Preserve the complete UTF-8 string returned by the system keyboard.
    player=text;savepersistent();cl=1;changeState('game',1)
    return true
end
function N.closeNotice()
    if not N.notice then return false end
    N.notice=nil;changeState('title');return true
end
return N
