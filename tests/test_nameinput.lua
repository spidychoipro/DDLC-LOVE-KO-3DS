package.path='runtime/?.lua;work/patched/game/?.lua;'..package.path
love={keyboard={setTextInput=function() end}}
local saved=0
function savepersistent() saved=saved+1 end
function changeState(s,x) state=s;mode=x end
player=''
local N=require('nameinput')
N.open();assert(N.active)
for c in ('ㅎㅏㄴㄱㅡㄹ'):gmatch('[\194-\244][\128-\191]*') do N.editor:feed(c) end
-- Confirm while the final syllable is still being composed.
N.keypressed('y');assert(player=='한글' and saved==1 and state=='game' and mode==1 and not N.active)
player='';N.open();N.finish();assert(N.active and saved==1)
N.systemText('붙여넣기');N.finish();assert(player=='붙여넣기' and saved==2)
N.open();N.systemText("bad'name");N.finish();assert(N.active and saved==2)
N.open();N.systemText(string.rep('가',13));N.finish();assert(N.active and saved==2)
player='';N.open();N.touch(145,80);N.touch(240,80);N.touch(50,80);assert(N.editor:text()=='한')
N.touch(80,185);assert(player=='한' and saved==3)
print('PASS: touch input, complete final syllable on confirm, empty/invalid names, UTF-8 paste, persistence callback')
