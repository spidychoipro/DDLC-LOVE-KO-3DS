from pathlib import Path
import re, json, shutil, ast, sys, difflib, bisect
sys.path.insert(0, str(Path('work/pylibs').resolve()))
from PIL import Image, ImageDraw, ImageFont

ROOT = Path('work/patched')
GAME = ROOT / 'game'
shutil.copytree('work/3ds', ROOT, dirs_exist_ok=True)
MP = json.loads(Path('work/mapping.json').read_text(encoding='utf8'))
STR = re.compile(r""""(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'""")
def decode(s):
    return re.sub(r'\\(.)', lambda m: {'n':'\n','r':'\r','t':'\t'}.get(m[1],m[1]), s[1:-1])
def quote(s):
    return json.dumps(s, ensure_ascii=False)
def plain(s):
    return re.sub(r'\{[^}]*\}', '', s).replace('[[','[')
def norm(s):
    return re.sub(r'\s+', ' ', plain(s)).strip()
LOOK = {norm(k): plain(v) for k,v in MP.items()}
def loose(s):return re.sub(r'[^\w\[\]]','',norm(s).lower())
LOOSE = {loose(k):v for k,v in LOOK.items()}
EXTRA = json.loads(Path('work/extra-translations.json').read_text(encoding='utf8')) if Path('work/extra-translations.json').exists() else {}
LOOK.update(EXTRA)
VARS = {'player':'player','ch2_winner':'ch2_winner','ch4_name':'savevalue',
        'currentname':'currentname','unfairto':'unfairto','currentuser':'currentuser',
        'gtext':'gtext','persistent.yuri_kill':'persistent.yuri_kill','basedir':'basedir','s_name':'s_name','savevalue':'savevalue','gtext10':'gtext10','gtext24':'gtext24','gtext80':'gtext80','gtext200':'gtext200'}
def template(expr):
    parts=[]; end=0
    for m in STR.finditer(expr):
        gap=expr[end:m.start()].strip().strip('.').strip()
        if gap:
            for v in gap.split('..'):
                v=v.strip()
                if v not in VARS:return None
                parts.append('['+('ch4_name' if v=='savevalue' else v)+']')
        parts.append(decode(m[0]));end=m.end()
    gap=expr[end:].strip().strip('.').strip()
    if gap:
        for v in gap.split('..'):
            v=v.strip()
            if v not in VARS:return None
            parts.append('['+('ch4_name' if v=='savevalue' else v)+']')
    return ''.join(parts) if parts else None
def expression(s):
    parts=[];end=0
    for m in re.finditer(r'\[([\w.]+)\]',s):
        if m[1] not in VARS:continue
        parts.append(quote(s[end:m.start()]));parts.append('ko.name('+VARS[m[1]]+')' if m[1]!='player' else 'player');end=m.end()
    parts.append(quote(s[end:]))
    return ' .. '.join(parts)
def arg_end(s,start):
    depth=0;i=start
    while i<len(s):
        if s[i] in "\"'":
            m=STR.match(s,i)
            if not m:return len(s)
            i=m.end();continue
        if s[i]=='(':depth+=1
        elif s[i]==')':
            if depth==0:return i
            depth-=1
        elif s[i]==',' and depth==0:return i
        i+=1
    return i

report=[]; counts={}
for p in GAME.rglob('*.lua'):
    if p.name in ['script.lua','poems.lua','poemwords.lua']:continue
    s=p.read_text(encoding='utf8'); edits=[];n=0
    spans=[(m.start(),m.end()) for m in STR.finditer(s)]
    starts=[a for a,b in spans]
    for m in re.finditer(r"\bcw\s*\(\s*(['\"])(?:[^'\"]+)\1\s*,\s*|(?m:^\s*(?:bl|mc|s|n|y|m))\s*(?:\(\s*|(?=['\"]))",s):
        start=m.end()
        si=bisect.bisect_right(starts,m.start())-1
        if si>=0 and spans[si][0]<=m.start()<spans[si][1]:continue
        if s[m.start():m.end()].rstrip().endswith(('"',"'")) and not s[m.start():].startswith('cw'):continue
        if start>=len(s):continue
        if s[start] not in "\"'":continue
        if not STR.match(s,start):continue
        shorthand=s[m.start():m.end()].strip() in ['bl','mc','s','n','y','m']
        if shorthand:
            end=STR.match(s,start).end()
        else:end=arg_end(s,start)
        src=s[start:end];t=template(src)
        if t is None:
            report.append({'file':str(p.relative_to(GAME)),'source':src,'reason':'expression'});continue
        k=LOOK.get(norm(t),LOOSE.get(loose(t)))
        if k is None:
            matches=difflib.get_close_matches(norm(t),LOOK,n=1,cutoff=.94)
            if matches and re.findall(r'\[[^]]+\]',matches[0])==re.findall(r'\[[^]]+\]',t):k=LOOK[matches[0]]
        if k is None:
            if re.search('[A-Za-z]{3}',t):report.append({'file':str(p.relative_to(GAME)),'source':src,'text':t,'reason':'unmatched'})
            continue
        replacement=expression(k)
        edits.append((start,end,'('+replacement+')' if shorthand else replacement));n+=1
    for a,b,t in reversed(edits):s=s[:a]+t+s[b:]
    p.write_text(s,encoding='utf8');counts[str(p.relative_to(GAME))]=n

# Preserve the original word scores and replace only the displayed words.
words=[]
for line in Path('work/kr-unpacked/poemwords.txt').read_text(encoding='utf8-sig').splitlines():
    row=line.strip().split(',')
    if len(row)==4 and row[1].strip().isdigit():words.append(row)
p=GAME/'scripts/poemwords.lua'
p.write_text('function poemwords()\nwordlist = {\n'+''.join('{'+quote(w)+','+','.join(v)+'},\n' for w,*v in words)+'}\nend\n',encoding='utf8')

# Parse literal poem data without executing the downloaded Python code.
poems={}
tree=ast.parse(Path('work/poems-source.txt').read_text(encoding='utf8'))
for node in tree.body:
    if isinstance(node,ast.Assign) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='Poem':
        fields={k.arg:ast.literal_eval(k.value) for k in node.value.keywords}
        poems[node.targets[0].id]=plain(fields.get('title','')+'\n\n'+fields.get('text',''))
p=GAME/'scripts/poems.lua';s=p.read_text(encoding='utf8')
pat=re.compile(r"(poemname == '([^']+)' then\s*poemtext = )\[\[(.*?)\]\]",re.S)
def replace_poem(m):
    name=m[2];base=name.split('-')[0]
    if base not in poems:return m[0]
    # The old port splits some poems over several script steps. Keep those
    # steps, displaying the complete translated poem once and a continuation.
    text=poems[base] if '-' not in name else '（계속）'
    return m[1]+quote(text)
s=pat.sub(replace_poem,s);p.write_text(s,encoding='utf8')
Path('work/unmatched.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
Path('work/conversion-counts.json').write_text(json.dumps(counts,indent=2),encoding='utf8')
print('Converted dialogue calls:',sum(counts.values()),'unmatched:',len(report),'words:',len(words),'poems:',len(poems))
