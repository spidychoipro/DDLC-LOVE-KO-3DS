from pathlib import Path
import shutil

G=Path('work/patched/game')
runtime=Path('runtime') if Path('runtime').is_dir() else G
for name in ['hangul_input.lua','nameinput.lua']:
    if (runtime/name).resolve()!=(G/name).resolve():shutil.copyfile(runtime/name,G/name)
p=G/'main.lua';s=p.read_text(encoding='utf8')
if "nameinput = require 'nameinput'" not in s:
    s=s.replace("ko = require 'ko'","ko = require 'ko'\nnameinput = require 'nameinput'")
    s=s.replace("\tif event_enabled then\n\t\tevent_draw()", "\tif nameinput.active then nameinput.draw();return end\n\tif event_enabled then\n\t\tevent_draw()",1)
    s=s.replace('\t--this acts as love.mousepressed', '''\tif nameinput.active then
\t\tif mouseDown and mousereleased ~= 1 then
\t\t\tmousereleased = 1
\t\t\tnameinput.touch(mouseX,mouseY)
\t\telseif not mouseDown then mousereleased = nil end
\t\treturn
\tend
\t--this acts as love.mousepressed''',1)
    s=s.replace('function love.keypressed(key)','function love.keypressed(key)\n\tif nameinput.active then nameinput.keypressed(key);return end',1)
    s=s.replace('function love.textinput(text)','function love.textinput(text)\n\tif nameinput.active then nameinput.systemText(text);return end',1)
s=s.replace('v0.3.1 KO-test1','v0.3.1 KO-test2')
p.write_text(s,encoding='utf8')
p=G/'menu.lua';s=p.read_text(encoding='utf8')
if 'nameinput.open()' not in s:
    a=s.index('\t\t--set player name to MC if not on 3DS');b=s.index('\t\telseif m_selected == 3 then',a)
    s=s[:a]+'''\t\tif m_selected == 2 then --new game
\t\t\tnameinput.open()
\t\t\tmenu_previous = nil
\t\t\t
'''+s[b:]
p.write_text(s,encoding='utf8')
(G/'conf.lua').write_text("function love.conf(t)\n t.identity = 'DDLC-3DS-KO'\nend\n",encoding='utf8')
p=G/'states/load.lua';s=p.read_text(encoding='utf8').replace('LovePotion/DDLC-3DS/','LovePotion/DDLC-3DS-KO/').replace('LOVE\\\\DDLC-3DS\\\\','LOVE\\\\DDLC-3DS-KO\\\\');p.write_text(s,encoding='utf8')
