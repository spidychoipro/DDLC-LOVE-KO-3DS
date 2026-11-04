from pathlib import Path
import re,json,collections,difflib
PAT=re.compile(r'^\s*(?:(s|n|y|m|mc|ny)(?:\s+\w+)*)?\s*"((?:[^"\\]|\\.)*)"\s*(?:with .*)?$')
def clean(s):
 return s.replace('\\"','"').replace('\\\'','\'').replace('\\n','\n').replace('\\\\','\\')
allgroups=[];mapping={};conflicts=[]
for p in Path('work/english').glob('script*.rpy'):
 ns=json.loads(Path('work/kr-ast',p.stem+'.json').read_text(encoding='utf8'))
 labels={n['name'] for n in ns if n['type']=='Label' and not n['name'].startswith('_')}
 es=collections.defaultdict(list);label=''
 for l in p.read_text(encoding='utf8').splitlines():
  if (m:=re.match(r'\s*label (\w+)',l)) and m[1] in labels:label=m[1]
  if (m:=PAT.match(l)) and not m[2].startswith(('images/','yuri 3y')):es[label].append((m[1] or 'bl',clean(m[2])))
 ks=collections.defaultdict(list);label=''
 for n in sorted(ns,key=lambda n:n.get('linenumber',0)):
  if n['type']=='Label' and n['name'] in labels:label=n['name']
  if n['type']=='Say':ks[label].append((n.get('who') or 'bl',n['what']))
 for label,eng in es.items():
  kor=ks[label]
  er=[];kr=[]
  for seq,out in [(eng,er),(kor,kr)]:
   for who,s in seq:
    if not out or out[-1][0]!=who:out.append((who,[]))
    out[-1][1].append(s)
  # Runs of a single speaker provide anchors even where translation merges sentences.
  sm=difflib.SequenceMatcher(None,[x[0] for x in er],[x[0] for x in kr],autojunk=False)
  for op,a,b,c,d in sm.get_opcodes():
   if op!='equal':
    allgroups.append({'file':p.stem,'label':label,'english':er[a:b],'korean':kr[c:d],'kind':'speaker mismatch'});continue
   for (_,ee),(_,kk) in zip(er[a:b],kr[c:d]):
    if len(ee)==len(kk):pairs=zip(ee,kk)
    else:
     idx=len(allgroups);allgroups.append({'file':p.stem,'label':label,'english':ee,'korean':kk,'kind':'length mismatch'})
     continue
    for e,k in pairs:
     if e in mapping and mapping[e]!=k:conflicts.append(e)
     else:mapping[e]=k
Path('work/alignment-review.json').write_text(json.dumps(allgroups,ensure_ascii=False,indent=2),encoding='utf8')
Path('work/mapping.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf8')
print('mapped',len(mapping),'review groups',len(allgroups),'conflicts',len(set(conflicts)))
print(collections.Counter(x['kind'] for x in allgroups))
