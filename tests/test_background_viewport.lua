package.path='runtime/?.lua;work/patched/game/?.lua;'..package.path
local drawing=false
local created=0
local lastDraw
love={graphics={print=function()end,printf=function()end,
newQuad=function(x,y,w,h,sw,sh)
 assert(not drawing,'Quad allocation during drawing')
 assert(x>=1 and y>=1 and x+w<=sw and y+h<=sh,'Crop must stay inside decoded pixels')
 created=created+1;return {x=x,y=y,w=w,h=h}
end,
draw=function(image,q,x,y) lastDraw={image,q,x,y} end}}
local K=require('ko')
background_Image={};posX=-40;posY=0
for frame=1,1600 do
 posX=posX-.25;posY=posY-.25
 if posX<=-80 then posX=0 end
 if posY<=-80 then posY=0 end
 K.prepareBackground();local before=created
 drawing=true;K.drawBackground();drawing=false
 assert(created==before and lastDraw[3]==0 and lastDraw[4]==0)
 assert(lastDraw[2].w==400 and lastDraw[2].h==240)
 assert(lastDraw[2].x==1-math.floor(posX) and lastDraw[2].y==1-math.floor(posY))
end
local cached=created
for frame=1,320 do
 posX=posX-.25;posY=posY-.25
 if posX<=-80 then posX=0 end
 if posY<=-80 then posY=0 end
 K.prepareBackground();K.drawBackground()
end
assert(created==cached,'Repeated scroll cycles must reuse quads')
print('PASS: 1920 background frames, integral viewport inside image, no negative screen vertices, cached quads outside draw')
