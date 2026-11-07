from pathlib import Path
G=Path('work/patched/game')
for name in ['menu.lua','states/game.lua','states/splash.lua','states/poemgame.lua','states/poem_special.lua']:
    p=G/name;s=p.read_text(encoding='utf8')
    assert 'lg.draw(background_Image, posX, posY)' in s,name
    p.write_text(s.replace('lg.draw(background_Image, posX, posY)','ko.drawBackground()'),encoding='utf8')

# The old native loader expands NPOT images without clearing the unused GPU
# buffer. Emit an exact power-of-two RGBA texture with no unwritten padding.
from PIL import Image
p=G/'images/bg/menu_bg.png'
with Image.open(p) as original:
    assert original.size==(552,528),original.size
    original.convert('RGBA').crop((0,0,512,512)).save(p)
p=G/'states/load.lua';s=p.read_text(encoding='utf8')
needle="background_Image = lg.newImage('images/bg/menu_bg.png')"
assert needle in s
s=s.replace(needle,needle+"\n\t\tbackground_Image:setFilter('nearest','nearest')",1)
p.write_text(s,encoding='utf8')
