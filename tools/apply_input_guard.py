from pathlib import Path
import shutil
G=Path('work/patched/game')
shutil.copyfile('runtime/input_guard.lua',G/'input_guard.lua')
p=G/'main.lua';s=p.read_text(encoding='utf8')
s=s.replace("native_nameentry = require 'native_nameentry'","input_guard = require 'input_guard'\nnative_nameentry = require 'native_nameentry'",1)
s=s.replace('function love.update(dt)','function love.update(dt)\n\tdt = math.min(dt, 0.1)',1)
s=s.replace('\t--this acts as love.mousepressed', '''\tinput_guard.update(dt,mouseDown,mouseX,mouseY)
\tif not input_guard.touchAllowed() then
\t\tmousereleased = mouseDown and 1 or nil
\t\tmouseDown = false
\tend
\t--this acts as love.mousepressed''',1)
s=s.replace('function love.keypressed(key)','function love.keypressed(key)\n\tif not input_guard.keypressed(key) then return end',1)
s=s.replace('function love.update(dt)', 'function love.update(dt)\n\tnative_nameentry.update()',1)
s=s.replace('\nend\n\nfunction love.update(dt)', '\n\tnative_nameentry.sceneDrawn()\nend\n\nfunction love.update(dt)',1)
p.write_text(s,encoding='utf8')
p=G/'states/game.lua' ;s=p.read_text(encoding='utf8')
a=s.index('\t--skipping');b=s.index('\tif menu_enabled == false and cl ~= 666 then',a)
s=s[:a]+'''\t-- Skip must be deliberate, fresh input after returning from the keyboard.
\tlocal canSkip = state == 'game' and not menu_enabled and not poem_enabled and not event_enabled and not input_guard.blocked()
\tif canSkip and (input_guard.skipHeld() or input_guard.touchSkip(mouseDown,mouseX,mouseY)) then
\t\tif autoskip < 1 then autoskip = 1 end
\telse
\t\tautoskip = 0
\t\tif not canSkip then input_guard.cancelSkip() end
\tend
\t
'''+s[b:]
s=s.replace("game_keypressed('a')","love.keypressed('a')",1)
p.write_text(s,encoding='utf8')
p=G/'menu.lua';s=p.read_text(encoding='utf8').replace('function menu_enable(m)','function menu_enable(m)\n\tinput_guard.cancelSkip()\n\tautotimer = 0',1);p.write_text(s,encoding='utf8')
p=G/'resources.lua';s=p.read_text(encoding='utf8')
s=s.replace('function audioUpdate(audiox, forceload) --audio changes', 'function audioUpdate(audiox, forceload) --audio changes\n\tif native_nameentry.queueAudio(audiox) then return end',1)
s=s.replace('\tstate = cstate\nend', '''\tstate = cstate
\tif cstate == 'game' and (x == 1 or x == 2 or x == 'autoload') then
\t\tko.reset()
\t\tinput_guard.resume()
\t\tif x == 1 then
\t\t\t-- Initialize the opening scene before the first post-keyboard draw.
\t\t\txaload = 0
\t\t\tscriptCheck()
\t\t\ttimerCheck()
\t\t\tc_disp = {'','','',''}
\t\t\tinput_guard.resume()
\t\tend
\tend
end''',1)
p.write_text(s,encoding='utf8')

# Keep native timer functions intact: the bundled engine expects native APIs.
# Limit elapsed time only where the game consumes it.
for p in G.rglob('*.lua'):
    s=p.read_text(encoding='utf8')
    if 'love.timer.getDelta()' in s:
        p.write_text(s.replace('love.timer.getDelta()', 'math.min(love.timer.getDelta(), 0.1)'),encoding='utf8')
