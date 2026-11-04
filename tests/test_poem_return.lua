local function exercise(path,expectReady,previous)
 local chunk=loadfile(path)
 if not chunk then return false end
 local nativeRequire=require
 require=function()return {}end
 love={timer={getDelta=function()return 1/60 end,getTime=function()return 1 end}}
 lg={newImage=function(path)return {path=path}end}
 chunk()
 state=previous or 'poemgame';cl=346;chapter=1;audio1='4';bg1='old-bedroom';cg1=''
 bgch={path='old-bedroom'};bgch2={path='old-notebook'};menu_enabled=false
 persistent={ptr=0,chr={m=1,s=1}};poemwinner={[1]='Sayori'}
 unitimer=0;uniduration=.3;autoskip=0;player='테스트'
 function unloadAll()end
 function hideAll()end
 function loadAll()end
 function audioUpdate(track)audio1=track end
 function updateMonika()end
 function cw(who,text)ct=who;c_disp={text}end
 ko={reset=function()end};input_guard={resume=function()unitimer=0;autotimer=0;autoskip=0 end}
 assert(loadfile('work/patched/game/scripts/script-ch1.lua'))()
 function scriptCheck()ch1script()end
 changeState('game',3)
 assert(cl==348,'Poem return must keep the next chapter line')
 if expectReady then
  assert(bgch.path=='images/bg/club.png','Next scene background must be ready before drawing')
  assert(bgch2==nil,'Previous scene/notebook must not overlay the new scene')
  assert(c_disp[1]=='' and ct=='m','Old dialogue and speaker must not flash')
 else assert(bgch.path=='images/bg/old-bedroom.png','Baseline should reproduce the stale first frame') end
 require=nativeRequire
 return true
end
local built=loadfile('work/patched/game/resources.lua')
if built then
 assert(exercise('work/3ds/game/resources.lua',false))
 assert(exercise('work/patched/game/resources.lua',true))
 assert(exercise('work/patched/game/resources.lua',false,'game'))
 print('PASS: stale poem-return frame reproduced; actual next-chapter script primed before draw; other chapter transitions preserved')
end
