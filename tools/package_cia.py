"""Rebuild a homebrew CIA from the user's original, unencrypted CIA template.

No Nintendo keys or DSP firmware are included. Code/permissions come from the
unmodified upstream executable; the title ID and RomFS are rebuilt locally.
"""
from pathlib import Path
import argparse, struct, hashlib, subprocess

def align(n, boundary): return (n+boundary-1)//boundary*boundary
def sha(data): return hashlib.sha256(data).digest()

def ivfc(raw):
    padded=raw+b'\0'*(align(len(raw),4096)-len(raw))
    hashes2=b''.join(sha(padded[i:i+4096]) for i in range(0,len(padded),4096))
    p2=hashes2+b'\0'*(align(len(hashes2),4096)-len(hashes2))
    hashes1=b''.join(sha(p2[i:i+4096]) for i in range(0,len(p2),4096))
    p1=hashes1+b'\0'*(align(len(hashes1),4096)-len(hashes1))
    master=b''.join(sha(p1[i:i+4096]) for i in range(0,len(p1),4096))
    h=bytearray(0x60)
    struct.pack_into('<4sII',h,0,b'IVFC',0x10000,len(master))
    for i,(offset,size) in enumerate([(0,len(hashes1)),(len(p1),len(hashes2)),(len(p1)+len(p2),len(raw))]):
        struct.pack_into('<QQII',h,0xc+i*24,offset,size,12,0)
    struct.pack_into('<I',h,0x54,0x5c)
    prefix=bytes(h)+master
    assert len(prefix)<=4096
    result=prefix+b'\0'*(4096-len(prefix))+padded+p1+p2
    # Independently read back descriptors and check every stored hash.
    assert result[4096:4096+len(raw)]==raw
    for data,hashes in [(padded,hashes2),(p2,hashes1),(p1,master)]:
        assert all(sha(data[i:i+4096])==hashes[i//4096*32:i//4096*32+32] for i in range(0,len(data),4096))
    return result

def extract_content(cia):
    hs,_,_,cert,ticket,tmd,_,size=struct.unpack_from('<IHHIIIIQ',cia)
    offset=align(align(align(align(hs,64)+cert,64)+ticket,64)+tmd,64)
    content=cia[offset:offset+size]
    assert content[0x100:0x104]==b'NCCH'
    assert len(content)==size
    return content

def smdh_labels(icon):
    out=bytearray(icon)
    assert out[:4]==b'SMDH'
    for lang in range(16):
        short,long,author=('DDLC-LOVE Korean','Unofficial Korean port for Nintendo 3DS','DDLC-LOVE contributors')
        if lang==7: short,long,author=('문예부 한글판','DDLC-LOVE 비공식 한국어판','DDLC-LOVE 한국어화 기여자')
        start=8+lang*0x200
        for offset,length,text in [(0,128,short),(128,256,long),(384,128,author)]:
            encoded=text.encode('utf-16le')
            assert len(encoded)<length
            out[start+offset:start+offset+length]=encoded+b'\0'*(length-len(encoded))
    return bytes(out)

def rebuild(template,raw,title_id):
    original=extract_content(template)
    assert original[0x18f]&4, 'Only decrypted homebrew templates are supported'
    romfs_offset=struct.unpack_from('<I',original,0x1b0)[0]*512
    out=bytearray(original[:romfs_offset])
    old_id=bytes(out[0x118:0x120]);new_id=struct.pack('<Q',title_id)
    for offset in (0x108,0x118,0x400,0x800):
        assert bytes(out[offset:offset+8])==old_id,(hex(offset),'Unexpected title layout')
        out[offset:offset+8]=new_id
    out[0x150:0x160]=b'CTR-P-DLKO'+b'\0'*6
    struct.pack_into('<H',out,0x112,2)
    exoff,exsize,exhash=struct.unpack_from('<III',out,0x1a0);exoff*=512
    # Replace only fixed-size SMDH labels. The upstream icon art is preserved.
    for i in range(10):
        base=exoff+i*16
        name=bytes(out[base:base+8]).split(b'\0')[0]
        offset,size=struct.unpack_from('<II',out,base+8)
        if name==b'icon':
            start=exoff+512+offset;icon=smdh_labels(bytes(out[start:start+size]))
            out[start:start+size]=icon
            out[exoff+0x1e0-i*32:exoff+0x200-i*32]=sha(icon)
    out[0x160:0x180]=sha(out[0x200:0x600])
    out[0x1c0:0x1e0]=sha(out[exoff:exoff+exhash*512])
    romfs=ivfc(raw)
    struct.pack_into('<III',out,0x1b0,romfs_offset//512,align(len(romfs),512)//512,1)
    out[0x1e0:0x200]=sha(romfs[:512])
    out.extend(romfs)
    out.extend(b'\0'*(align(len(out),512)-len(out)))
    struct.pack_into('<I',out,0x104,len(out)//512)
    assert out[0x160:0x180]==sha(out[0x200:0x600])
    return bytes(out)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--template',type=Path,required=True)
    p.add_argument('--romfs',type=Path,required=True)
    p.add_argument('--makerom',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    cxi=args.output.with_suffix('.cxi')
    cxi.write_bytes(rebuild(args.template.read_bytes(),args.romfs.read_bytes(),0x0004000000DDFB00))
    subprocess.run([str(args.makerom.resolve()),'-f','cia','-ignoresign','-content',str(cxi)+':0:0','-ver','4','-o',str(args.output)],check=True)
    assert extract_content(args.output.read_bytes())==cxi.read_bytes()
    print('Verified CIA content, NCCH header hashes and three RomFS hash levels:',args.output)

if __name__=='__main__':main()
