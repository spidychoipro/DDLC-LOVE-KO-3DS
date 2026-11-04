package.path='runtime/?.lua;work/patched/game/?.lua;'..package.path
local down={};local now=0
love={keyboard={isDown=function(k)return down[k] or false end},timer={getTime=function()return now end,getDelta=function()return 30 end}}
local guard=require('input_guard');input_guard=guard
local function tick(touch,x,y,dt)
    dt=dt or 1/60;now=now+dt;guard.update(dt,touch or false,x or 0,y or 0)
end
down.x=true;down.b=true;autotimer=3;autoskip=2
guard.suspend();assert(guard.blocked() and autotimer==0 and autoskip==0)
assert(not guard.keypressed('a'))
guard.resume()
-- A huge dt from the blocking native applet must not exhaust quarantine.
tick(true,245,8,30);assert(guard.blocked())
for i=1,60 do tick(true,245,8);assert(not guard.skipHeld() and not guard.touchSkip(true,245,8)) end
assert(not guard.keypressed('x') and not guard.keypressed('b'))
assert(guard.keypressed('a')) -- stale X must not lock out unrelated manual input
down.x=false;down.b=false;tick(false)
assert(not guard.skipHeld())
down.x=true;assert(guard.keypressed('x'));tick(false);assert(guard.skipHeld())
down.x=false;tick(false);assert(not guard.skipHeld())
tick(true,20,100);tick(true,245,8);assert(not guard.touchSkip(true,245,8))
tick(false);tick(true,245,225);assert(not guard.touchSkip(true,245,225))
tick(false);tick(true,245,8);assert(guard.touchSkip(true,245,8))
tick(true,20,100);assert(not guard.touchSkip(true,245,8));tick(false)

-- Exercise the actual upstream and patched game update loops when available.
local old=loadfile('work/3ds/game/states/game.lua')
local patched=loadfile('work/patched/game/states/game.lua')
if old and patched then
    function scriptCheck() end
    function timerCheck() end
    function collectgarbage() end
    settings={autospd=4};global_os='Horizon';event_enabled=false;poem_enabled=false
    menu_enabled=false;state='game';bgch2=nil;audio1='2';mouseX=0;mouseY=0;mouseDown=false
    down.x=true;autotimer=0;autoskip=0;cl=1
    old();for i=1,40 do updateGame(1/60) end
    assert(cl>1,'Baseline must reproduce held-X auto skip')
    local baseline=cl
    patched();cl=1;guard.resume()
    for i=1,600 do
        tick(true,245,8);mouseDown=guard.touchAllowed() and true or false
        updateGame(1/60)
    end
    assert(cl==1 and autoskip==0 and autotimer==0,'Post-keyboard idle must preserve line 1')
    down.x=false;tick(false);mouseDown=false
    down.x=true;assert(guard.keypressed('x'))
    for i=1,12 do tick(false);updateGame(1/60) end
    assert(cl>1,'Fresh deliberate X must still skip')
    down.x=false;tick(false);local stopped=cl
    for i=1,120 do tick(false);updateGame(1/60) end
    assert(cl==stopped and autoskip==0,'Releasing X must immediately stop skipping')
    down.x=true;guard.keypressed('x');menu_enabled=true
    for i=1,20 do tick(false);updateGame(1/60) end
    assert(cl==stopped and autoskip==0,'Menus must not leave skip active')
    -- Check the actual main.lua key dispatcher too: a stale B from name
    -- entry must not enable automatic progression, while a fresh B still can.
    local entry=loadfile('work/patched/game/main.lua')
    if entry then
        local originalRequire=require
        local native=originalRequire('native_nameentry')
        require=function(name)
            if name=='input_guard' then return guard end
            if name=='native_nameentry' then return native end
            if name=='ko' then return {advance=function()return false end} end
            return true
        end
        local nativeDelta=love.timer.getDelta
        entry();require=originalRequire
        assert(love.timer.getDelta==nativeDelta,'Do not replace the engine native timer function')
        assert(love.timer.getDelta()==30,'Native timer must remain unmodified')
        menu_enabled=false;state='game';sfx1={play=function()end}
        down.x=false;down.b=true;guard.resume()
        love.keypressed('b');assert(autotimer==0)
        for i=1,60 do tick(false) end
        love.keypressed('b');assert(autotimer==0,'Stale B must not enable auto-forward')
        down.b=false;tick(false);down.b=true
        love.keypressed('b');assert(autotimer>0,'Fresh deliberate B must retain auto-forward')
        down.b=false;guard.resume();for i=1,60 do tick(false) end
        cl=1;unitimer=1;uniduration=.3;love.keypressed('a');assert(cl==2,'Fresh manual A must advance one line')
        print('PASS: actual main.lua dispatcher rejects stale B, accepts fresh B and single manual A')
    end
    print('PASS: baseline reproduced (line '..baseline..'); patched 600-frame modal return, deliberate skip, release and menu isolation')
end
print('PASS: modal quarantine, stale held keys, fresh X, touch origin, invisible lower strip, long dt')

local resource=io.open('work/patched/game/resources.lua','r')
if resource then
 local source=resource:read('*a');resource:close()
 assert(source:find('local dt = math.min(love.timer.getDelta(), 0.1)',1,true),'Cap delta at its game call site')
end
print('PASS: native timer identity preserved; elapsed time capped in game code')
