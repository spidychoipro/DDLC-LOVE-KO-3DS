from pathlib import Path
import sys,json
sys.path.insert(0,str(Path('work/pylibs').resolve()))
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
g=Path('work/patched/game')
existing=set()
for line in (g/'ko_glyphs.lua').read_text(encoding='utf8').splitlines():
    if line.startswith('['):existing.add(json.JSONDecoder().raw_decode(line[1:])[0])
for p in g.rglob('*.lua'):
    if p.name!='ko_glyphs.lua':existing.update(p.read_text(encoding='utf8'))
base=sorted(c for c in existing if c>=' ')
allchars=base+[chr(n) for n in range(0xAC00,0xD7A4) if chr(n) not in existing]
fontpath='work/kr-unpacked/gui/font/Aller_Rg.ttf'
font=ImageFont.truetype(fontpath,12);cmap=TTFont(fontpath).getBestCmap()
missing=[c for c in allchars if ord(c) not in cmap]
assert not missing,missing
atlas_size=256
columns=atlas_size//16
per_page=columns*columns
base_pages=(len(base)+per_page-1)//per_page
glyphs={}
for page,offset in enumerate(range(0,len(allchars),per_page),1):
    im=Image.new('RGBA',(atlas_size,atlas_size),(255,255,255,0));draw=ImageDraw.Draw(im)
    for i,c in enumerate(allchars[offset:offset+per_page]):
        x=(i%columns)*16;y=(i//columns)*16
        draw.text((x,y-2),c,font=font,fill='white')
        glyphs[c]=[page,x,y,max(1,round(font.getlength(c)))]
    im.save(g/'fonts'/f'ko{page}.png')
(g/'ko_glyphs.lua').write_text('return {\n'+''.join('['+json.dumps(c,ensure_ascii=False)+']={'+','.join(map(str,v))+'},\n' for c,v in glyphs.items())+'}\n',encoding='utf8')
print('Glyphs:',len(glyphs),'atlas pages:',page,'Hangul syllables:',11172)

(g/'ko_font_config.lua').write_text('return {size='+str(atlas_size)+',base_pages='+str(base_pages)+',pages='+str(page)+'}\n',encoding='utf8')
print('Initial font texture bytes:',base_pages*atlas_size*atlas_size*4)
