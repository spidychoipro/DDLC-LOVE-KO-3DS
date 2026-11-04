-- Hangul composition without relying on the console or emulator's IME.
local H = {}
local function chars(s)
    local out={}
    for c in s:gmatch('[%z\1-\127\194-\244][\128-\191]*') do out[#out+1]=c end
    return out
end
local initials=chars('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')
local vowels=chars('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
local finals=chars('ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ')
local li,vi,ti={},{},{}
for i,c in ipairs(initials) do li[c]=i-1 end
for i,c in ipairs(vowels) do vi[c]=i-1 end
for i,c in ipairs(finals) do ti[c]=i end
local double={['ㄱㄱ']='ㄲ',['ㄷㄷ']='ㄸ',['ㅂㅂ']='ㅃ',['ㅅㅅ']='ㅆ',['ㅈㅈ']='ㅉ'}
local compoundV={['ㅗㅏ']='ㅘ',['ㅗㅐ']='ㅙ',['ㅗㅣ']='ㅚ',['ㅜㅓ']='ㅝ',['ㅜㅔ']='ㅞ',['ㅜㅣ']='ㅟ',['ㅡㅣ']='ㅢ',['ㅘㅣ']='ㅙ',['ㅝㅣ']='ㅞ'}
local compoundT={['ㄱㅅ']='ㄳ',['ㄴㅈ']='ㄵ',['ㄴㅎ']='ㄶ',['ㄹㄱ']='ㄺ',['ㄹㅁ']='ㄻ',['ㄹㅂ']='ㄼ',['ㄹㅅ']='ㄽ',['ㄹㅌ']='ㄾ',['ㄹㅍ']='ㄿ',['ㄹㅎ']='ㅀ',['ㅂㅅ']='ㅄ',['ㄱㄱ']='ㄲ',['ㅅㅅ']='ㅆ'}
local splitT={}
for pair,value in pairs(compoundT) do
    if value~='ㄲ' and value~='ㅆ' then splitT[value]=chars(pair) end
end
local function encode(n)
    return string.char(224+math.floor(n/4096),128+math.floor(n/64)%64,128+n%64)
end
function H.new(text)
    return setmetatable({done=text or '',l=nil,v=nil,t=nil,history={}},{__index=H})
end
function H:pending()
    if self.l and self.v then
        return encode(44032+(li[self.l]*21+vi[self.v])*28+(self.t and ti[self.t] or 0))
    end
    return self.l or self.v or ''
end
function H:text() return self.done..self:pending() end
function H:commit()
    self.done=self.done..self:pending();self.l=nil;self.v=nil;self.t=nil
end
function H:feed(c)
    local before={self.done,self.l,self.v,self.t}
    self.history[#self.history+1]=before
    if vi[c] then
        if self.l and self.v and self.t then
            local split=splitT[self.t]
            local onset=split and split[2] or self.t
            self.t=split and split[1] or nil
            self:commit();self.l=onset;self.v=c
        elseif self.v then
            local joined=compoundV[self.v..c]
            if joined then self.v=joined else self:commit();self.v=c end
        else self.v=c end
    elseif li[c] then
        if self.l and self.v then
            if not self.t and ti[c] then self.t=c
            elseif self.t and compoundT[self.t..c] then self.t=compoundT[self.t..c]
            else self:commit();self.l=c end
        elseif self.l then
            if double[self.l..c] then self.l=double[self.l..c]
            else self:commit();self.l=c end
        else self:commit();self.l=c end
    else self:commit();self.done=self.done..c end
    if #chars(self:text())>12 then
        self.done,self.l,self.v,self.t=before[1],before[2],before[3],before[4]
        self.history[#self.history]=nil;return false
    end
    return true
end
function H:backspace()
    local before=self.history[#self.history]
    if before then
        self.history[#self.history]=nil
        self.done,self.l,self.v,self.t=before[1],before[2],before[3],before[4]
    else
        local text=chars(self:text());text[#text]=nil
        self.done=table.concat(text);self.l=nil;self.v=nil;self.t=nil
    end
end
return H
