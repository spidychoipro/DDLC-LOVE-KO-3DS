from pathlib import Path
import re,json
import sys
G=Path(sys.argv[1]) if len(sys.argv)>1 else Path('work/patched/game')
S=re.compile(r'''"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\[\[.*?\]\]''',re.S)
def argend(s,pos):
 depth=0;i=pos
 while i<len(s):
  m=S.match(s,i)
  if m:i=m.end();continue
  if s[i]=='(':depth+=1
  elif s[i]==')':
   if depth==0:return i
   depth-=1
  elif s[i]==',' and depth==0:return i
  i+=1
 return i
rows=[];total=0;exceptions=[]
for f in G.rglob('*.lua'):
 if f.name in ['ko_glyphs.lua','ko_ui.lua']:continue
 s=f.read_text(encoding='utf8')
 pat=re.compile(r'''\bcw\s*\(\s*['"][^'"]+['"]\s*,\s*|(?m:^\s*(?:bl|mc|s|n|y|m))\s*\(\s*''')
 spans=[(m.start(),m.end()) for m in S.finditer(s)]
 for m in pat.finditer(s):
  if any(a<=m.start()<b for a,b in spans):continue
  expr=s[m.end():argend(s,m.end())];total+=1
  text=' '.join(q[0][2:-2] if q[0].startswith('[[') else q[0][1:-1] for q in S.finditer(expr))
  clean=re.sub(r'https?://[^ ]+|\b(?:DDLC|New|CFW|Nintendo|DS|Monika|Sayori|Yuri|Natsuki|KO|Beta|characters|SNS)\b|@lilmonix3','',text,flags=re.ASCII)
  if re.search(r'[A-Za-z]{3}',text) and not re.search(r'[A-Za-z]{3}',clean):exceptions.append({'file':f.relative_to(G).as_posix(),'line':s.count('\n',0,m.start())+1,'text':text})
  if re.search(r'[A-Za-z]{3}',clean):rows.append({'file':f.relative_to(G).as_posix(),'line':s.count('\n',0,m.start())+1,'text':text})
Path('work/dialogue-english-audit.json').write_text(json.dumps({'dialogue_calls':total,'ordinary_english_candidates':rows,'proper_name_or_path_exceptions':exceptions},ensure_ascii=False,indent=2),encoding='utf8')
print('Dialogue calls:',total,'Ordinary English candidates:',len(rows))
for x in rows:print(x['file'],x['line'],repr(x['text'][:180]))

if rows: raise SystemExit("Untranslated ordinary dialogue remains; see work/dialogue-english-audit.json")
