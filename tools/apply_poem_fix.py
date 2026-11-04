from pathlib import Path
G=Path('work/patched/game')
# Compile a small native font atlas at the original tutorial text size.
import json
from PIL import Image,ImageDraw,ImageFont
font=ImageFont.truetype('work/kr-unpacked/gui/font/Aller_Rg.ttf',8)
text='시를 써 볼 시간이에요!좋아하는 부원이 좋아할 단어를 고르세요.여러분의 시를 가장 좋아하는 부원과는좋은 일이 생길지도 몰라요!확인'
chars=sorted(set(text));atlas=Image.new('RGBA',(256,256),(255,255,255,0));draw=ImageDraw.Draw(atlas);glyphs={}
for i,c in enumerate(chars):
    x=i%16*16;y=i//16*16
    draw.text((x,y-1),c,font=font,fill='white')
    glyphs[c]=[1,x,y,max(1,round(font.getlength(c)))]
atlas.save(G/'fonts/ko_tutorial.png')
(G/'ko_tutorial_glyphs.lua').write_text('return {\n'+''.join('['+json.dumps(c,ensure_ascii=False)+']={'+','.join(map(str,g))+'},\n' for c,g in glyphs.items())+'}\n',encoding='utf8')
p=G/'states/poemgame.lua';s=p.read_text(encoding='utf8')
assert "lg.draw(poemtime,0,0)" in s
s=s.replace('lg.draw(poemtime,0,0)','ko.drawPoemTutorial(alpha,poemtime)',1)
p.write_text(s,encoding='utf8')
p=G/'resources.lua';s=p.read_text(encoding='utf8')
s=s.replace('function changeState(cstate,x)',"function changeState(cstate,x)\n\tlocal returningFromPoem = state == 'poemgame' and cstate == 'game' and x == 3",1)
s=s.replace("\t\tcl = cl + 2\n\telseif cstate == 'game' and x == 'autoload'", "\t\tcl = cl + 2\n\t\tif returningFromPoem then\n\t\t\tbg1 = 'black'; cg1 = ''; bgch = nil; bgch2 = nil; cgch = nil\n\t\tend\n\telseif cstate == 'game' and x == 'autoload'",1)
s=s.replace("(x == 1 or x == 2 or x == 'autoload')", "(x == 1 or x == 2 or x == 'autoload' or returningFromPoem)",1)
s=s.replace('\t\tif x == 1 then\n\t\t\t-- Initialize', '\t\tif x == 1 or returningFromPoem then\n\t\t\t-- Initialize',1)
s=s.replace("\t\t\ttimerCheck()\n\t\t\tc_disp", "\t\t\ttimerCheck()\n\t\t\tif returningFromPoem then bgch2 = nil end\n\t\t\tc_disp",1)
p.write_text(s,encoding='utf8')
