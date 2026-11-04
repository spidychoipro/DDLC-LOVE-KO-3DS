package.path='runtime/?.lua;work/patched/game/?.lua;'..package.path
local opens,saves=0,0
love={keyboard={setTextInput=function(enabled) assert(enabled==true);opens=opens+1 end}}
function savepersistent() saves=saves+1 end
function changeState(value,arg) state=value;mode=arg end
function menu_enable(value) menu_type=value end
local N=require('native_nameentry')
for _,name in ipairs({'김민수','Alex','한글ABC','하늘','John Kim'}) do
    N.open();assert(N.pending)
    assert(N.submit(name));assert(player==name and state=='game' and mode==1 and not N.pending)
end
assert(opens==5 and saves==5)
assert(not N.submit('중복 콜백') and saves==5)
local previous=player
N.open();assert(not N.submit(''));assert(player==previous and state=='title')
N.open();assert(not N.submit(string.rep('가',13)));assert(N.notice and menu_type=='dialog' and saves==5)
assert(N.closeNotice() and not N.notice and state=='title')
N.open();assert(not N.submit("bad'name"));assert(saves==5)
N.open();assert(N.submit('  한글  '));assert(player=='한글' and saves==6)
local fontLoaded,glyphs=pcall(require,'ko_glyphs')
if fontLoaded then
    for n=0xAC00,0xD7A3 do
        local c=string.char(224+math.floor(n/4096),128+math.floor(n/64)%64,128+n%64)
        assert(glyphs[c],n)
    end
end
print('PASS: direct system keyboard, Korean/English/mixed names, final syllable, cancel, validation, duplicate callback'..(fontLoaded and ', 11172 Hangul glyphs' or ''))
