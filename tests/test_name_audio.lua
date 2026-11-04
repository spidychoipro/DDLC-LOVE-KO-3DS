package.path='runtime/?.lua;work/patched/game/?.lua;'..package.path
local stopped=0
local created={}
local phase='title'
love={timer={getTime=function()return 0 end},keyboard={isDown=function()return false end},audio={}}
local function stream(track)
 return {stop=function()stopped=stopped+1 end,setLooping=function()end,play=function()end}
end
love.audio.newSource=function(path,kind)
 assert(phase~='keyboard' and phase~='loading' and phase~='drawing','No stream creation during modal input or scene loading')
 created[#created+1]=path
 return stream(path)
end
local N=require('native_nameentry');native_nameentry=N
local resource=loadfile('work/patched/game/resources.lua')
if resource then resource() end
if not resource then
 -- Module-only CI still checks the gate; local builds exercise actual audioUpdate.
 function audioUpdate(track,force)
  if N.queueAudio(track) then return end
  audio1=track
  if track~='0' and track~='' then love.audio.newSource('audio/bgm/'..track..'.ogg','stream'):play() end
 end
end
function savepersistent()end
function menu_enable()end
function changeState(value,mode)
 state=value
 if value=='title' then phase='title';audioUpdate('1')
 else
  phase='loading'
  audioUpdate(audio1,true)
  audioUpdate('2')
 end
end
love.keyboard.setTextInput=function(enabled)
 assert(enabled and stopped>=1,'Title stream must stop before opening keyboard')
 assert(N.loadingAudio)
 phase='keyboard'
end
state='title';audio1='1';ddlct=stream('1')
N.open();assert(#created==0)
N.submit('한글ABC');assert(state=='game' and N.waitingForScene)
assert(#created==0,'Music must stay off while scene assets are loading')
N.update();assert(#created==0,'Update before first draw must not start music')
phase='drawing';N.sceneDrawn();assert(#created==0,'Drawing only signals readiness')
phase='game';N.update()
assert(#created==1 and created[1]=='audio/bgm/2.ogg','Only final scene music starts after drawing')
assert(not N.loadingAudio and not N.waitingForScene)
N.update();N.sceneDrawn();N.update();assert(#created==1,'Do not restart music every frame')
N.open();N.submit('');assert(state=='title' and not N.loadingAudio)
assert(#created==2 and created[2]=='audio/bgm/1.ogg','Cancel must restore title music')
N.open();N.submit(string.rep('가',13));assert(state=='title' and not N.loadingAudio)
assert(#created==3 and created[3]=='audio/bgm/1.ogg','Invalid input must restore title music')
print('PASS: stop before keyboard, no music during scene loading, start final track after first draw, cancel/invalid title recovery')
