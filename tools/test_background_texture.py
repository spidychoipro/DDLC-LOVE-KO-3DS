from pathlib import Path
from PIL import Image
import math
p=Path('work/patched/game/images/bg/menu_bg.png')
with Image.open(p) as image:
    assert image.mode=='RGBA' and image.size==(512,512)
    assert image.getchannel('A').getextrema()==(255,255)
    width,height=image.size
    # Model exactly the old loader's written rows versus allocated texture.
    allocated_width=1<<(width-1).bit_length()
    allocated_height=1<<(height-1).bit_length()
    unwritten=allocated_width*allocated_height-width*height
    assert unwritten==0,unwritten
    assert 81+400<=width and 81+240<=height
    with Image.open('work/3ds/game/images/bg/menu_bg.png') as original:
        expected=original.convert('RGBA').crop((0,0,512,512))
        assert image.tobytes()==expected.tobytes(),'Original visible dots must be unchanged'
print('PASS: exact 512x512 RGBA background; no unwritten native GPU padding; full scrolling viewport retains original pixels')
