from pathlib import Path
G=Path('work/patched/game')
for name in ['menu.lua','states/game.lua','states/splash.lua','states/poemgame.lua','states/poem_special.lua']:
    p=G/name;s=p.read_text(encoding='utf8')
    assert 'lg.draw(background_Image, posX, posY)' in s,name
    p.write_text(s.replace('lg.draw(background_Image, posX, posY)','ko.drawBackground()'),encoding='utf8')
