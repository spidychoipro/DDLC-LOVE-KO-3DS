from pathlib import Path
import pickle,zlib,struct,json
classes={}
class Obj:
 def __new__(cls,*a,**k):return object.__new__(cls)
 def __init__(self,*a,**k):pass
 def __setstate__(self,s):
  if isinstance(s,tuple) and len(s)==2 and isinstance(s[1],dict): self.__dict__.update(s[1])
  elif isinstance(s,dict):self.__dict__.update(s)
  else:self.state=s
class Safe(pickle.Unpickler):
 def find_class(self,m,n):
  if not m.startswith('renpy.'):raise ValueError((m,n))
  if (m,n) not in classes:classes[m,n]=type(n,(Obj,),{})
  return classes[m,n]
def read(p):
 b=p.read_bytes()
 if b.startswith(b'RENPY RPC2'):
  _,s,l=struct.unpack('<III',b[10:22]);b=b[s:s+l]
 return Safe(__import__('io').BytesIO(zlib.decompress(b)),encoding='utf8').load()
for p in Path('work/kr-unpacked').glob('*.rpyc'):
 try:
  data=read(p);seen=set();nodes=[]
  def walk(o):
   if id(o) in seen:return
   seen.add(id(o))
   if isinstance(o,Obj):
    nodes.append(o)
    for k,v in o.__dict__.items():
     if k!='next':walk(v)
   elif isinstance(o,(list,tuple)):
    for v in o:walk(v)
   elif isinstance(o,dict):
    for v in o.values():walk(v)
  walk(data)
  for n in nodes:
   if type(n).__name__=='PyCode' and hasattr(n,'state'):
    n.source=n.state[1]
  for n in nodes:
   if type(n).__name__=='Menu':n.menu_texts='\n'.join(t[0] for t in n.items if t[0])
  out=[{'type':type(n).__name__,**{k:v for k,v in n.__dict__.items() if isinstance(v,(str,int,float,bool)) or v is None}} for n in nodes]
  Path('work/kr-ast').mkdir(exist_ok=True);Path('work/kr-ast',p.stem+'.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
  print(p.name,len(out),'say',sum(type(n).__name__=='Say' for n in nodes))
 except Exception as e:print(p.name,repr(e))
