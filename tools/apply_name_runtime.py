from pathlib import Path
import shutil

G=Path('work/patched/game')
shutil.copyfile('runtime/native_nameentry.lua',G/'native_nameentry.lua')
p=G/'main.lua';s=p.read_text(encoding='utf8')
s=s.replace("ko = require 'ko'","ko = require 'ko'\nnative_nameentry = require 'native_nameentry'",1)
a=s.index('function love.textinput(text)');b=s.index('\nfunction game_quit()',a)
s=s[:a]+'function love.textinput(text)\n\tnative_nameentry.submit(text)\nend\n'+s[b:]
s=s.replace('v0.3.1 KO-test1','v0.3.1 KO-test2')
p.write_text(s,encoding='utf8')
p=G/'menu.lua';s=p.read_text(encoding='utf8')
a=s.index('\t\t--set player name to MC if not on 3DS');b=s.index('\t\telseif m_selected == 3 then',a)
s=s[:a]+'''\t\tif m_selected == 2 then --new game: open the system keyboard directly
\t\t\tnative_nameentry.open()
\t\t\tmenu_previous = nil
\t\t\t
'''+s[b:]
s=s.replace('function menu_confirm()','function menu_confirm()\n\tif native_nameentry.closeNotice() then return end',1)
s=s.replace('function menu_keypressed(key)',"function menu_keypressed(key)\n\tif key == 'b' and native_nameentry.closeNotice() then return end",1)
p.write_text(s,encoding='utf8')
(G/'conf.lua').write_text("function love.conf(t)\n t.identity = 'DDLC-3DS-KO'\nend\n",encoding='utf8')
p=G/'states/load.lua';s=p.read_text(encoding='utf8').replace('LovePotion/DDLC-3DS/','LovePotion/DDLC-3DS-KO/').replace('LOVE\\\\DDLC-3DS\\\\','LOVE\\\\DDLC-3DS-KO\\\\');p.write_text(s,encoding='utf8')
