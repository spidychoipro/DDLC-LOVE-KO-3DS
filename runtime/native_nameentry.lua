-- Delegate typing/composition to Nintendo 3DS's system software keyboard.
-- No game-drawn keyboard or custom Hangul IME is used.
local N={pending=false,notice=nil,loadingAudio=false,drawReady=false,waitingForScene=false,nextAudio=nil}
local guard=require('input_guard')
local function clearAudioDelay()
    N.loadingAudio=false;N.drawReady=false;N.waitingForScene=false;N.nextAudio=nil
end
function N.queueAudio(track)
    if not N.loadingAudio then return false end
    N.nextAudio=track;audio1=track
    return true
end
function N.sceneDrawn()
    if N.waitingForScene and state=='game' then N.drawReady=true end
end
function N.update()
    if not N.waitingForScene or not N.drawReady then return end
    local track=N.nextAudio or '0'
    clearAudioDelay()
    audioUpdate(track,true)
    guard.resume()
end
function N.open()
    N.pending=true;N.notice=nil
    -- Clear DSP buffers before the modal applet and synchronous scene loads.
    -- Streamed music starts again only after the first complete scene draw.
    if ddlct then ddlct:stop() end
    if sfx1 then sfx1:stop() end
    if sfx2 then sfx2:stop() end
    audio1='0'
    N.loadingAudio=true;N.drawReady=false;N.waitingForScene=false;N.nextAudio='0'
    guard.suspend()
    love.keyboard.setTextInput(true)
    guard.resume()
end
local function invalid(message)
    clearAudioDelay()
    N.notice=message;changeState('title');menu_enable('dialog');menutext=message;menu_previous='title'
    return false
end
function N.submit(text)
    if not N.pending then return false end
    N.pending=false
    guard.resume()
    if type(text)~='string' or text=='' then clearAudioDelay();changeState('title');return false end
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
    N.waitingForScene=N.loadingAudio
    return true
end
function N.closeNotice()
    if not N.notice then return false end
    N.notice=nil;changeState('title');return true
end
return N
