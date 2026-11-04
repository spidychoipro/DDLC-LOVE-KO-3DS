from pathlib import Path
import json,re,ast,sys
sys.path.insert(0,str(Path('work/pylibs').resolve()))
from PIL import Image
G=Path('work/patched/game')

# The port divides long poems into script steps. Distribute the Korean poem
# across those same steps instead of leaving English fragments or placeholders.
data={}
for node in ast.parse(Path('work/poems-source.txt').read_text(encoding='utf8')).body:
    if isinstance(node,ast.Assign) and isinstance(node.value,ast.Call) and getattr(node.value.func,'id','')=='Poem':
        fields={k.arg:ast.literal_eval(k.value) for k in node.value.keywords}
        data[node.targets[0].id]=re.sub(r'\{[^}]*\}','',fields.get('title','')+'\n\n'+fields.get('text',''))
p=G/'scripts/poems.lua';s=p.read_text(encoding='utf8')
pattern=re.compile(r"(poemname == '([^']+)' then\s*poemtext = )(\[\[.*?\]\]|\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')",re.S)
groups={}
for m in pattern.finditer(s):groups.setdefault(m[2].split('-')[0],[]).append(m[2])
parts={}
for base,names in groups.items():
    if base not in data:continue
    lines=data[base].strip().splitlines()
    # Retain paragraph breaks, but avoid a string of entirely blank pages.
    compact=[];blanks=0
    for line in lines:
        blanks=blanks+1 if not line.strip() else 0
        if blanks<=3:compact.append(line)
    step=max(1,(len(compact)+len(names)-1)//len(names))
    for i,name in enumerate(names):parts[name]='\n'.join(compact[i*step:(i+1)*step]) or '…'
s=pattern.sub(lambda m:m[1]+json.dumps(parts[m[2]],ensure_ascii=False) if m[2] in parts else m[0],s)
p.write_text(s,encoding='utf8')

# Original Korean patch artwork: fit to both screens without cropping the text.
out=G/'images/ko_special';out.mkdir(exist_ok=True)
source=Path('work/kr-unpacked/images/poem_special')
for f in source.glob('*.png'):
    im=Image.open(f).convert('RGBA')
    scale=min(0.5,400/im.width,480/im.height)
    im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    top=im.crop((0,0,im.width,min(240,im.height)));top.save(out/(f.stem+'_top.png'))
    if im.height>240:
        bottom=im.crop((0,240,im.width,im.height))
        if bottom.width>320:bottom=bottom.resize((320,round(bottom.height*320/bottom.width)),Image.Resampling.LANCZOS)
        bottom.save(out/(f.stem+'_bottom.png'))
    else:Image.new('RGBA',(8,8),(0,0,0,0)).save(out/(f.stem+'_bottom.png'))
p=G/'states/poem_special.lua';s=p.read_text(encoding='utf8')
a=s.index('\tif p_number == 1 then');b=s.index("\tstate = 'poem_special'",a)
s=s[:a]+'''\tlocal name = 'poem_special'..p_number
\tif p_number == 5 or p_number == 7 then name=name..'a'
\telseif p_number == 12 then name='poem_end'
\telseif p_number == 13 then name='poem_end_clearall' end
\tpoemsp.name=name
\tpoemsp.topimg=lg.newImage('images/ko_special/'..name..'_top.png')
\tpoemsp.bottomimg=lg.newImage('images/ko_special/'..name..'_bottom.png')
\tpoemsp.topX=(400-poemsp.topimg:getWidth())/2
\tpoemsp.bottomX=(320-poemsp.bottomimg:getWidth())/2
'''+s[b:]
for n in [5,7]:
    s=s.replace("poemsp.topimg = lg.newImage('images/poem_special/poem_special"+str(n)+"b.png')", "poemsp.topimg = lg.newImage('images/ko_special/poem_special"+str(n)+"b_top.png')\n\t\t\tpoemsp.bottomimg = lg.newImage('images/ko_special/poem_special"+str(n)+"b_bottom.png')")
s=s.replace('Error: Script file is missing or corrupt.\\nPlease reinstall the game.','오류: 스크립트가 없거나 손상되었습니다.\\n게임을 다시 설치해 주세요.')
p.write_text(s,encoding='utf8')

# Remaining short UI strings, including the original port's splash messages.
ui={
'This game is not suitable for children':'이 게임에는 어린이에게 부적합한 내용과',
'  or those who are easily disturbed.':'충격적인 장면이 포함되어 있습니다.',
'You are my sunshine,\\nMy only sunshine':'너는 내 햇살,\\n나만의 햇살',
'I missed you.':'보고 싶었어.','Play with me':'나랑 놀자',
"It's just a game, mostly.":'대부분은 그냥 게임이야.',
'This game is not suitable for children\\nor those who are easily disturbed?':'이 게임은 어린이나\\n충격에 민감한 분께 부적합할까요?',
'I have granted kids to hell':'아이들을 지옥으로 보냈어',
'It was only partially your fault.':'전부 네 잘못은 아니었어.',
'This game is not suitable for children\\nor those who are easily dismembered.':'이 게임은 어린이나\\n쉽게 조각나는 분께 부적합합니다.',
"Don't forget to backup Monika's character file.":'모니카의 캐릭터 파일을 백업하는 걸 잊지 마.',
'Now everyone can be happy.':'이제 모두 행복할 수 있어.',
}
p=G/'states/splash.lua';s=p.read_text(encoding='utf8')
for old,new in sorted(ui.items(),key=lambda item:len(item[0]),reverse=True):s=s.replace(old,new)
p.write_text(s,encoding='utf8')
p=G/'main.lua';s=p.read_text(encoding='utf8').replace("v0.3.1 KO-test2","KO 0.2.6-beta").replace("dvertype = 'Release'","dvertype = 'Beta'")
p.write_text(s,encoding='utf8')
print('Polished',len(parts),'poem fragments and',len(list(source.glob('*.png'))),'Korean special-poem images')
