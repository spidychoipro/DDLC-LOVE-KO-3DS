package.path='runtime/?.lua;work/patched/game/?.lua;'..package.path
local H=require('hangul_input')
local function characters(s)
 local out={};for c in s:gmatch('[\194-\244][\128-\191]*') do out[#out+1]=c end;return out
end
local function typeText(jamo)
 local h=H.new();for _,c in ipairs(characters(jamo)) do assert(h:feed(c)) end;return h
end
local samples={
 {'ㅎㅏㄴㄱㅡㄹ','한글'},{'ㄱㅣㅁㅁㅣㄴㅅㅜ','김민수'},
 {'ㄱㅏㄱㅏ','가가'},{'ㄱㅏㅂㅅㅣ','갑시'},{'ㄱㅏㅂㅅㅇㅣ','값이'},
 {'ㄷㅏㄹㄱㅇㅣ','닭이'},{'ㅂㅏㄹㅂㅏ','발바'},{'ㄱㅗㅏㄴ','관'},
 {'ㅇㅜㅓㄴ','원'},{'ㅎㅗㅣ','회'},{'ㄱㄱㅗㅊ','꽃'},{'ㅆㅣ','씨'},
}
for _,sample in ipairs(samples) do assert(typeText(sample[1]):text()==sample[2],sample[1]) end
local h=typeText('ㄱㅏㅂㅅ');h:backspace();assert(h:text()=='갑');h:backspace();assert(h:text()=='가');h:backspace();assert(h:text()=='ㄱ');h:backspace();assert(h:text()=='')
h=H.new('한글');h:backspace();assert(h:text()=='한')
h=H.new(string.rep('가',12));assert(not h:feed('ㄱ'));assert(h:text()==string.rep('가',12))
local ls=characters('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')
local vs=characters('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
local ts={'','ㄱ','ㄲ','ㄱㅅ','ㄴ','ㄴㅈ','ㄴㅎ','ㄷ','ㄹ','ㄹㄱ','ㄹㅁ','ㄹㅂ','ㄹㅅ','ㄹㅌ','ㄹㅍ','ㄹㅎ','ㅁ','ㅂ','ㅂㅅ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'}
local fontLoaded,glyphs=pcall(require,'ko_glyphs')
local total=0
for l,a in ipairs(ls) do for v,b in ipairs(vs) do for t,c in ipairs(ts) do
 local cp=0xAC00+((l-1)*21+v-1)*28+t-1
 local expected=string.char(224+math.floor(cp/4096),128+math.floor(cp/64)%64,128+cp%64)
 assert(typeText(a..b..c):text()==expected,cp)
 if fontLoaded then assert(glyphs[expected],cp) end
 total=total+1
end end end
print('PASS: '..total..' Hangul syllables, '..(fontLoaded and 'font coverage, ' or '(font coverage requires a local build), ')..' resyllabification, compound vowels/finals, backspace, name length')
