package.path='runtime/?.lua;work/patched/game/?.lua;'..package.path
local time=0
local drawn=0
love={timer={getTime=function() return time end},graphics={}}
local g=love.graphics
g.print=function() end
g.printf=function() end
g.draw=function() drawn=drawn+1 end
g.newImage=function() return {setFilter=function() end} end
g.newQuad=function(x,y,w,h,sw,sh)
 assert(x>=0 and y>=0 and x+w<=sw and y+h<=sh)
 return {}
end
g.setColor=function() end
g.rectangle=function() end
ko=require('ko');ko.init()
chapter=0;cl=1;unitimer=1;uniduration=.3
textbox_enabled=true;menu_enabled=false;poem_enabled=false
myTextStartTime=0
local original='저 멀리서 성가신 여자아이가 주변 사람들 시선은 아랑곳하지 않은 채 팔을 허공에 흔들며 달려온다.'
local lines=ko.wrap(original,304)
for _,line in ipairs(lines) do assert(ko.width(line)<=304) end
assert(table.concat(lines,'')==original)
local page=ko.page('한글')
time=.1;assert(ko.drip(page,10,0)=='한')
assert(ko.advance())
assert(ko.drip(page,10,0)=='한글')
assert(not ko.advance())
cl=2;time=0
page=ko.page(string.rep('한',150))
assert(#page>0)
assert(ko.advance());assert(ko.advance())
unitimer=1
local second=ko.page('unused')
assert(second~=page)
g.print('한글 출력 테스트',0,0)
assert(drawn>0)
assert(ko.ui('I would walk home with Yuri.')=='유리와 집에 간다.')
assert(ko.ui('Save File 4')=='저장 파일 4')
poem_enabled=true;poemtext=string.rep('한글 시\n',40)
ko.drawPoem();assert(ko.advance())
print('PASS: UTF-8 reveal, 304px wrapping, dialogue pagination, poem pagination, atlas bounds, menu display')
