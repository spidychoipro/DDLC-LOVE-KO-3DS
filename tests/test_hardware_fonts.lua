package.path='runtime/?.lua;work/patched/game/?.lua;'..package.path
local drawing=false
local uploads=0
local quads=0
local rendered=0
local function graphicsStub()
 return {print=function()end,printf=function()end,setColor=function()end,rectangle=function()end,
 newImage=function(path)
  assert(not drawing,'GPU texture upload from draw callback: '..path)
  uploads=uploads+1;return {setFilter=function()end}
 end,
 newQuad=function()
  assert(not drawing,'Quad allocation from draw callback')
  quads=quads+1;return {}
 end,
 draw=function()rendered=rendered+1 end}
end
love={graphics=graphicsStub()}
local baseline=loadfile('../../DDLC-LOVE-KO-0.2.6/GitHub-ready/runtime/ko.lua')
if baseline then
 baseline();drawing=true
 local ok,err=pcall(love.graphics.print,'두근두근 문예부의 비공식 3DS 포트입니다.',8,66)
 assert(not ok and tostring(err):find('GPU texture upload from draw callback',1,true),'Must reproduce original first-Korean-draw hazard')
 drawing=false
end
love.graphics=graphicsStub();local K=assert(loadfile('runtime/ko.lua'))()
K.init();local initialUploads=uploads
K.prepare('힣');local preparedUploads=uploads;local preparedQuads=quads
chapter=0;cl=10016;player='힣';ct='';state='newgame';poem_enabled=false
K.prepareFrame()
drawing=true
love.graphics.print('두근두근 문예부의 비공식 3DS 포트입니다.',8,66)
love.graphics.print('힣',8,80)
K.drawPoemTutorial(255,{})
drawing=false
assert(uploads==preparedUploads and quads==preparedQuads and rendered>0,'Drawing must only use prepared GPU objects')
local config=require('ko_font_config');assert(config.size==256)
assert(config.base_pages*config.size*config.size*4<=2*1024*1024,'Initial font texture budget must stay under 2 MiB')
print('PASS: first-Korean-draw hazard reproduced; all font uploads/quad creation outside draw; first warning/name/tutorial render without GPU allocations')
