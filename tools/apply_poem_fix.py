from pathlib import Path
G=Path('work/patched/game')
p=G/'states/poemgame.lua';s=p.read_text(encoding='utf8')
s=s.replace("\t\tpoemtime = lg.newImage('images/gui/poemgame/poemtime.png')", "\t\tpoemtime = nil -- Tutorial is rendered with Korean text.",1)
assert "lg.draw(poemtime,0,0)" in s
s=s.replace('lg.draw(poemtime,0,0)','ko.drawPoemTutorial(alpha)',1)
p.write_text(s,encoding='utf8')
p=G/'resources.lua';s=p.read_text(encoding='utf8')
s=s.replace('function changeState(cstate,x)',"function changeState(cstate,x)\n\tlocal returningFromPoem = state == 'poemgame' and cstate == 'game' and x == 3",1)
s=s.replace("\t\tcl = cl + 2\n\telseif cstate == 'game' and x == 'autoload'", "\t\tcl = cl + 2\n\t\tif returningFromPoem then\n\t\t\tbg1 = 'black'; cg1 = ''; bgch = nil; bgch2 = nil; cgch = nil\n\t\tend\n\telseif cstate == 'game' and x == 'autoload'",1)
s=s.replace("(x == 1 or x == 2 or x == 'autoload')", "(x == 1 or x == 2 or x == 'autoload' or returningFromPoem)",1)
s=s.replace('\t\tif x == 1 then\n\t\t\t-- Initialize', '\t\tif x == 1 or returningFromPoem then\n\t\t\t-- Initialize',1)
s=s.replace("\t\t\ttimerCheck()\n\t\t\tc_disp", "\t\t\ttimerCheck()\n\t\t\tif returningFromPoem then bgch2 = nil end\n\t\t\tc_disp",1)
p.write_text(s,encoding='utf8')
