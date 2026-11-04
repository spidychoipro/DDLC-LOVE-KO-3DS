from pathlib import Path
import json,re,sys,shutil
sys.path.insert(0,str(Path('work/pylibs').resolve()))
from PIL import Image,ImageDraw,ImageFont
G=Path('work/patched/game')
ui={
'Sayori':'사요리','Natsuki':'나츠키','Yuri':'유리','Monika':'모니카','Nat & Yuri':'나츠키와 유리',
'New Game':'새 게임','Load Game':'불러오기','Save Game':'저장하기','Settings':'설정','Help':'도움말','Quit':'종료','Return':'돌아가기',
'Main Menu':'시작 화면','Game Menu':'게임 메뉴','Yes':'예','No':'아니요','Yes.':'예.','No.':'아니요.','OK':'확인',
'Menu':'메뉴','Auto':'자동','Skip':'넘김','Auto-Forward On':'자동 진행 중','Skipping':'넘기는 중','Skipping >':'넘기는 중 >','Skipping >>':'넘기는 중 >>','Skipping >>>':'넘기는 중 >>>',
'Textbox Location':'대사창 위치','Text Speed':'글자 속도','Auto-Forward Time':'자동 진행 간격','Show Date&Time':'날짜와 시간','Characters':'캐릭터','Save Settings':'설정 저장','Char. Animations':'캐릭터 움직임','Top Screen':'위 화면','Bottom Screen':'아래 화면',
'Delete monika.chr':'monika.chr 삭제','Delete natsuki.chr':'natsuki.chr 삭제','Delete sayori.chr':'sayori.chr 삭제','Delete yuri.chr':'yuri.chr 삭제','Restore all':'모두 복구',
'I agree.':'동의합니다.','I do not agree.':'동의하지 않습니다.','Natsuki.':'나츠키.','Yuri.':'유리.','Monika.':'모니카.','Sayori...':'사요리…','Help me, Sayori!!':'도와줘, 사요리!!',
'I would still walk home with Sayori.':'그래도 사요리와 집에 간다.','I love you.':'사랑해.','You\'ll always be my dearest friend.':'넌 언제까지나 내 소중한 친구야.',
'Are you sure you want to quit the game?':'게임을 종료할까요?',
'Are you sure you want to return to the main menu?\nThis will lose unsaved progress.':'시작 화면으로 돌아갈까요?\n저장하지 않은 진행 상황은 사라집니다.',
'Press (<) and (>) to change settings.':'좌우 버튼으로 설정을 바꿉니다.',
'Key Bindings:':'버튼 안내:',
'A, L Trigger - Advances through the game,':'A, L: 대사 진행 / 다음 쪽',
'activates menu choices':'선택 항목 확인',
'B - Exit Menu, AutoForward On/Off':'B: 메뉴 닫기 / 자동 진행',
'X - (Menu) Previous Page, (Hold) Skip':'X: 이전 쪽 / 누르는 동안 넘기기',
'Y - (Menu) Next Page, Enter Game Menu':'Y: 다음 쪽 / 게임 메뉴 열기',
'Managing files: Go to Settings > Characters':'파일 관리: 설정 > 캐릭터',
'Deleting save data: Delete everything in here':'저장 초기화: 아래 폴더를 백업 후 삭제',
}
ui.update(json.loads(Path('work/menu-translations.json').read_text(encoding='utf8')))
# Character identifiers used by script branches stay English; only drawing changes.
(G/'ko_ui.lua').write_text('return {\n'+''.join('['+json.dumps(k,ensure_ascii=False)+']='+json.dumps(v,ensure_ascii=False)+',\n' for k,v in ui.items())+'}\n',encoding='utf8')
shutil.copyfile('work/ko.lua',G/'ko.lua')

p=G/'main.lua';s=p.read_text(encoding='utf8').replace("require 'draw'","require 'draw'\nko = require 'ko'")
s=s.replace("dversion = 'v0.3.1'","dversion = 'v0.3.1 KO-test1'")
start=s.index('function love.keypressed(key)');end=s.index('\nend',start)
chunk=s[start:end]
chunk=chunk.replace("if menu_enabled ~= true then", "if (key == 'a' or key == 'lbutton') and not menu_enabled and (state == 'game' or state == 'newgame') and ko.advance() then return end\n\tif menu_enabled ~= true then")
s=s[:start]+chunk+s[end:];p.write_text(s,encoding='utf8')

p=G/'scripts/script.lua';s=p.read_text(encoding='utf8')
s=s.replace("ct = 'Sayori'","ct = '사요리'").replace("ct = 'Natsuki'","ct = '나츠키'").replace("ct = 'Yuri'","ct = '유리'").replace("ct = 'Monika'","ct = '모니카'").replace("ct = 'Nat & Yuri'","ct = '나츠키와 유리'")
s=s.replace('\t--text drip for scripts','\tstext = ko.page(stext)\n\t--text drip for scripts')
a=s.index('\t--word wrap');b=s.index('\tif tag then',a)
s=s[:a]+"\tslen = string.len(textx)\n\tc_disp = {}\n\tlocal lines = {}\n\tfor line in (textx..'\\n'):gmatch('(.-)\\n') do lines[#lines+1]=line end\n\tfor i=1,4 do c_disp[i]=lines[i] or '' end\n\n"+s[b:]
s=s.replace('scriptJump(cl+1)','if not ko.autoPage() then scriptJump(cl+1) end',1)
p.write_text(s,encoding='utf8')
p=G/'draw.lua';s=p.read_text(encoding='utf8')
a=s.index('function dripText(');b=s.index('\nend',a)+4
s=s[:a]+"function dripText(text,charactersPerSecond,startTime)\n\treturn ko.drip(text,charactersPerSecond or 100,startTime)\nend"+s[b:]
a=s.index('function drawPoem()');b=s.index('\nend',a)+4
s=s[:a]+"function drawPoem()\n\tko.drawPoem()\nend"+s[b:]
p.write_text(s,encoding='utf8')
p=G/'menu.lua';s=p.read_text(encoding='utf8')
s=s.replace('font:getWidth(choices[i])','ko.width(ko.ui(choices[i]))').replace('font:getWidth(itemnames[i])','ko.width(ko.ui(itemnames[i]))')
p.write_text(s,encoding='utf8')

# Translate the five intentionally corrupted dialogue expressions without
# changing their glitch generators or event timing.
fixes={
'script-ch23.lua':[("Monika lifts the foil from ","모니카는 "),("'s tray and takes a cupcake.","의 쟁반에서 포일을 걷고 컵케익을 집는다.")],
'script-exclusives2-natsuki.lua':[("don't judge a bookkkkkkkkkkkkkkkkk kkkkk kk","겉만 보고 판단하지 마아아아아아아아아 아아아 아아")],
'script-exclusives2-yuri.lua':[("my whole body gets incredibly ","제 온몸이 엄청나게 "),('"Will"..space(60)','"그렇게"..space(60)')],
'script-poemresponses2.lua':[("In case you couldn't tell, the poem is about ","혹시 모르실까 봐 말하는 건데, 이 시는 ")],
}
for name,rs in fixes.items():
    p=G/'scripts'/name;s=p.read_text(encoding='utf8')
    for a,b in rs:s=s.replace(a,b)
    p.write_text(s,encoding='utf8')

# Keep atlas dimensions within the old 3DS runtime's 1024 texture limit.
chars=set(chr(i) for i in range(32,127))
for p in G.rglob('*.lua'):
    if p.name!='ko_glyphs.lua':chars.update(p.read_text(encoding='utf8'))
chars=sorted(c for c in chars if c>=' ' and c not in '\r\n\t')
font=ImageFont.truetype('work/kr-unpacked/gui/font/Aller_Rg.ttf',12)
glyphs={};missing=[]
from fontTools.ttLib import TTFont
cmap=TTFont('work/kr-unpacked/gui/font/Aller_Rg.ttf').getBestCmap()
for page,offset in enumerate(range(0,len(chars),1024),1):
    im=Image.new('RGBA',(512,512),(255,255,255,0));draw=ImageDraw.Draw(im)
    for index,c in enumerate(chars[offset:offset+1024]):
        x=(index%32)*16;y=(index//32)*16
        if ord(c) not in cmap:missing.append(c)
        draw.text((x,y-2),c,font=font,fill='white')
        advance=max(1,round(font.getlength(c)))
        glyphs[c]=[page,x,y,advance]
    im.save(G/'fonts'/f'ko{page}.png')
(G/'ko_glyphs.lua').write_text('return {\n'+''.join('['+json.dumps(c,ensure_ascii=False)+']={'+','.join(map(str,v))+'},\n' for c,v in glyphs.items())+'}\n',encoding='utf8')
Path('work/font-report.json').write_text(json.dumps({'glyphs':len(chars),'pages':page,'missing':missing},ensure_ascii=False,indent=2),encoding='utf8')
print('Glyphs',len(chars),'pages',page,'missing',missing)
