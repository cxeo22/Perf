from pathlib import Path
from PIL import Image
import sys
assets=Path(__file__).resolve().parent/'assets'
im=Image.open(sys.argv[1]).convert('RGBA')
im.save(assets/'feather-source.png')
im=im.crop(im.getbbox())
base=Image.new('RGBA',(1024,1024));im.thumbnail((850,900),Image.Resampling.LANCZOS)
base.alpha_composite(im,((1024-im.width)//2,(1024-im.height)//2))
for size in (16,32,40,48,96,256):base.resize((size,size),Image.Resampling.LANCZOS).save(assets/f'feather-{size}.png')
base.save(assets/'feather.ico',sizes=[(s,s) for s in (16,24,32,48,64,128,256)])
for i in range(21):
    frame=base.resize((96,96),Image.Resampling.LANCZOS)
    frame.putalpha(frame.getchannel('A').point(lambda a:round(a*i/20)))
    frame.save(assets/f'feather-fade-{i}.png')
print('Updated all feather sizes, startup fade frames and Windows icon.')
