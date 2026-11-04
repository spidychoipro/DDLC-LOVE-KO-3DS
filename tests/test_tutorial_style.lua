package.path='runtime/?.lua;work/patched/game/?.lua;'..package.path
local original={original=true}
local backgroundDrawn=false
local rects={}
local glyphDraws=0
love={graphics={}}
local g=love.graphics
g.print=function()end;g.printf=function()end;g.setColor=function()end
g.rectangle=function(mode,x,y,w,h)
 assert(mode=='fill' and x>=106 and y>=71 and x+w<=294 and y+h<=168,'Text masks must stay inside original small panel')
 rects[#rects+1]={x,y,w,h}
end
g.newImage=function(path)
 assert(path=='fonts/ko_tutorial.png','Tutorial should use its native-size small font')
 return {setFilter=function()end}
end
g.newQuad=function(x,y,w,h,sw,sh)
 assert(sw==256 and sh==256 and x>=0 and y>=0 and x+w<=sw and y+h<=sh)
 return {quad=true}
end
g.draw=function(...)
 local a={...}
 if a[1]==original then
  assert(not backgroundDrawn and a[2]==0 and a[3]==0 and #a==3,'Original overlay must be drawn unchanged')
  backgroundDrawn=true
 else
  assert(backgroundDrawn and a[2].quad and #a==4,'Use native-size glyph quads without scaled overload')
  assert(a[3]>=110 and a[3]<=290 and a[4]>=82 and a[4]<=157,'Text must remain in original panel')
  glyphDraws=glyphDraws+1
 end
end
local K=require('ko');K.drawPoemTutorial(255,original)
assert(backgroundDrawn and #rects==3 and glyphDraws>60)
print('PASS: original overlay reused, small-panel geometry retained, outlined confirmation, native-size glyph drawing')
