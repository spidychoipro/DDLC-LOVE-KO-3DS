"""Read local input archives; never execute Ren'Py code from the patch."""
from pathlib import Path
import zipfile,pickle,io,zlib

def extract_zip(source,target,keep=lambda name:True):
    target=Path(target);target.mkdir(parents=True,exist_ok=True)
    for member in zipfile.ZipFile(source).infolist():
        name=member.filename.replace('\\','/')
        if member.is_dir() or not keep(name):continue
        dest=target/name
        if not dest.resolve().is_relative_to(target.resolve()):raise ValueError('Unsafe ZIP entry')
        dest.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(source).open(member) as f:dest.write_bytes(f.read())

class IndexReader(pickle.Unpickler):
    def find_class(self,module,name):raise ValueError('RPA index globals are not allowed')

def extract_rpa(path,target):
    target=Path(target)
    with Path(path).open('rb') as f:
        header=f.readline().split()
        if header[0]!=b'RPA-3.0':raise ValueError('Expected RPA-3.0')
        offset,key=int(header[1],16),int(header[2],16)
        f.seek(offset);index=IndexReader(io.BytesIO(zlib.decompress(f.read())),encoding='bytes').load()
        for name,entries in index.items():
            if isinstance(name,bytes):name=name.decode('utf8')
            dest=target/name
            if not dest.resolve().is_relative_to(target.resolve()):raise ValueError('Unsafe RPA entry')
            output=bytearray()
            for entry in entries:
                start,length=entry[:2];prefix=entry[2] if len(entry)>2 else b''
                f.seek(start^key);output.extend(prefix);output.extend(f.read(length^key))
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(output)

def prepare(assets,korean):
    extract_zip(assets,'work/3ds')
    assert Path('work/3ds/game/main.lua').is_file(),'Wrong 3DS asset archive'
    extract_zip(korean,'work/korean',lambda name:name in ('game/fonts.rpa','game/images.rpa','game/scripts.rpa'))
    for name in ('fonts','images','scripts'):extract_rpa(Path('work/korean/game')/(name+'.rpa'),'work/kr-unpacked')
