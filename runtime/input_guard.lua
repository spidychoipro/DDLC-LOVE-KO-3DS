-- Modal applets can leave held buttons/touches in the host input state.
-- Resume normal play only after a short input quarantine. Skip additionally
-- requires a fresh X press or a touch which STARTED on the visible Skip button.
local G={modal=false,cooldown=0,frameBlocked=false,suppressed={},previousTouch=false,touchSuppressed=false,xPressed=false,skipTouch=false}
local keys={'a','b','x','y','lbutton','rbutton','start','select','up','down','left','right','cpadup','cpaddown','cpadleft','cpadright'}
local function held(key) return love.keyboard.isDown(key) end
local function captureHeld()
    for _,key in ipairs(keys) do if held(key) then G.suppressed[key]=true end end
end
local function skipRect(x,y) return x and y and x>=237 and x<269 and y>=2 and y<18 end
function G.cancelSkip()
    G.xPressed=false;G.skipTouch=false;autoskip=0
end
function G.suspend()
    G.modal=true;G.cooldown=0;G.frameBlocked=true
    G.cancelSkip();autotimer=0
    captureHeld();G.touchSuppressed=true
end
function G.resume()
    G.modal=false;G.cooldown=.2;G.frameBlocked=true
    G.suppressed={};captureHeld();G.touchSuppressed=true
    G.cancelSkip();autotimer=0;unitimer=0
    myTextStartTime=love.timer.getTime()
end
function G.blocked() return G.modal or G.cooldown>0 or G.frameBlocked end
function G.update(dt,down,x,y)
    G.frameBlocked=G.modal or G.cooldown>0
    if G.frameBlocked then
        captureHeld()
        G.cooldown=math.max(0,G.cooldown-math.min(dt or 0,.05))
        G.cancelSkip();autotimer=0
        if down then G.touchSuppressed=true end
    end
    for key in pairs(G.suppressed) do if not held(key) then G.suppressed[key]=nil end end
    if not held('x') then G.xPressed=false end
    if not down then
        G.touchSuppressed=false;G.skipTouch=false
    elseif not G.previousTouch and not G.touchSuppressed and not G.blocked() then
        G.skipTouch=skipRect(x,y)
    elseif G.skipTouch and not skipRect(x,y) then G.skipTouch=false end
    G.previousTouch=not not down
end
function G.keypressed(key)
    if G.blocked() then G.suppressed[key]=true;return false end
    if G.suppressed[key] then return false end
    if key=='x' then G.xPressed=true end
    return true
end
function G.touchAllowed() return not G.blocked() and not G.touchSuppressed end
function G.skipHeld()
    return not G.blocked() and not G.suppressed.x and G.xPressed and held('x')
end
function G.touchSkip(down,x,y)
    return not G.blocked() and not G.touchSuppressed and G.skipTouch and down and skipRect(x,y)
end
return G
