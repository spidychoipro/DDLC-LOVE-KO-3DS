#!/usr/bin/env python3
"""Build locally from separately obtained upstream game and translation files."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,urllib.request

ROOT=Path(__file__).resolve().parent

def run(name):
    subprocess.run([sys.executable,str(ROOT/'tools'/name)],cwd=ROOT,check=True)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--assets',type=Path,required=True,help='Upstream v1.1.9 DDLC-3DS.zip')
    p.add_argument('--korean',type=Path,required=True,help='Korean patch 1.2 normal ZIP')
    p.add_argument('--mkromfs',type=Path,required=True,help='devkitPro mkromfs3ds executable')
    p.add_argument('--cia-template',type=Path,help='Upstream v1.1.9 DDLC-3DS.cia')
    p.add_argument('--makerom',type=Path,help='Project_CTR makerom 0.19.0 executable')
    p.add_argument('--reference-dir',type=Path,help='Offline English .rpy reference files')
    p.add_argument('--fetch-reference',action='store_true',help='Download the pinned English comparison text')
    p.add_argument('--lua',type=Path,help='Optional Lua 5.1 interpreter for runtime tests')
    args=p.parse_args()
    # Resolve user arguments before changing cwd. Paths containing spaces are safe.
    for key,value in vars(args).items():
        if isinstance(value,Path):setattr(args,key,value.resolve())
    if args.cia_template and not args.makerom:p.error('--cia-template requires --makerom')
    if not args.reference_dir and not args.fetch_reference:p.error('Use --reference-dir or --fetch-reference')
    os.chdir(ROOT)
    sys.path.insert(0,str(ROOT/'tools'))
    from prepare_inputs import prepare
    prepare(args.assets,args.korean)
    manifest=json.loads((ROOT/'tools/english-reference.json').read_text())
    dest=ROOT/'work/english';dest.mkdir(parents=True,exist_ok=True)
    for filename,expected in manifest['files'].items():
        if args.reference_dir:data=(args.reference_dir/filename).read_bytes()
        else:
            url=f"https://raw.githubusercontent.com/{manifest['repo']}/{manifest['commit']}/game/{filename}"
            data=urllib.request.urlopen(url,timeout=60).read()
        if hashlib.sha256(data).hexdigest()!=expected:raise ValueError('Reference hash mismatch: '+filename)
        (dest/filename).write_bytes(data)
    shutil.copyfile('runtime/ko.lua','work/ko.lua')
    shutil.copyfile('tools/extra-translations.json','work/extra-translations.json')
    run('extract_ast.py')
    # Extract only literal poetry and menu data; never execute the Ren'Py code.
    import re
    menu={}
    for name in ['poems','poems_special']:
        nodes=json.loads(Path('work/kr-ast',name+'.json').read_text(encoding='utf8'))
        sources=[n['source'] for n in nodes if n['type']=='PyCode' and 'source' in n]
        if sources:Path('work',name+'-source.txt').write_text(sources[0],encoding='utf8')
    for file in dest.glob('script*.rpy'):
        english=[m[1] for line in file.read_text(encoding='utf8').splitlines() if (m:=re.match(r'\s*"([^"\n]+)"\s*(?:if .*?)?:\s*$',line))]
        nodes=json.loads(Path('work/kr-ast',file.stem+'.json').read_text(encoding='utf8'))
        korean=[text for n in nodes if n['type']=='Menu' for text in n.get('menu_texts','').split('\n') if text]
        if len(english)==len(korean):menu.update(zip(english,korean))
    Path('work/menu-translations.json').write_text(json.dumps(menu,ensure_ascii=False),encoding='utf8')
    for name in ['align.py','resolve_alignment.py','build_patch.py','finalize_patch.py','apply_name_runtime.py','polish_content.py','rebuild_name_font.py']:run(name)
    if args.lua:
        for test in ['test_hangul.lua','test_korean.lua','test_nameinput.lua']:
            subprocess.run([str(args.lua),str(ROOT/'tests'/test)],check=True)
    dist=ROOT/'dist';dist.mkdir(exist_ok=True)
    romfs=ROOT/'work/korean.romfs'
    subprocess.run([str(args.mkromfs),'work/patched/game',str(romfs)],check=True)
    import struct
    from package_cia import smdh_labels
    data=bytearray(Path('work/3ds/DDLC-3DS.3dsx').read_bytes())
    smdh_offset,smdh_size=struct.unpack_from('<II',data,32)
    data[smdh_offset:smdh_offset+smdh_size]=smdh_labels(data[smdh_offset:smdh_offset+smdh_size])
    data+=b'\0'*((-len(data))%4096)
    struct.pack_into('<I',data,40,len(data));data+=romfs.read_bytes()
    (dist/'DDLC-LOVE-KO-0.2.0.3dsx').write_bytes(data)
    if args.cia_template:
        subprocess.run([sys.executable,'tools/package_cia.py','--template',str(args.cia_template),'--romfs',str(romfs),'--makerom',str(args.makerom),'--output',str(dist/'DDLC-LOVE-KO-0.2.0.cia')],check=True)
    files=list(dist.glob('*.cia'))+list(dist.glob('*.3dsx'))
    (dist/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name+'\n' for f in sorted(files)),encoding='ascii')
    print('Local build complete:',dist)

if __name__=='__main__':main()
