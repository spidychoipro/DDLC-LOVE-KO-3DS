from pathlib import Path
p=Path('work/patched/game/main.lua');s=p.read_text(encoding='utf8')
assert "\tchangeState('load')" in s
s=s.replace("\tchangeState('load')","\tko.init()\n\tchangeState('load')",1)
assert '\nend\n\nfunction love.keypressed(key)' in s
s=s.replace('\nend\n\nfunction love.keypressed(key)','\n\tko.prepareFrame()\nend\n\nfunction love.keypressed(key)',1)
p.write_text(s,encoding='utf8')
