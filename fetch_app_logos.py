from pathlib import Path
import urllib.request,urllib.parse,re,html,io,json,concurrent.futures
from PIL import Image
from app_starter import CATALOG
out=Path('assets/apps');out.mkdir(exist_ok=True)
custom={'chrome':'https://www.google.com/chrome/static/images/favicons/favicon.ico','drive':'https://ssl.gstatic.com/images/branding/product/2x/drive_2020q4_48dp.png','nvidia':'https://www.nvidia.com/favicon.ico','epic':'https://store.epicgames.com/favicon.ico','steam':'https://store.steampowered.com/favicon.ico','afterburner':'https://www.msi.com/favicon-32x32.png','obs':'https://obsproject.com/favicon-96x96.png'}
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=15) as r:return r.read(3000000)
def one(row):
    key,name,_,_,site=row;candidates=[custom[key]] if key in custom else []
    try:
        page=get(site).decode('utf-8',errors='replace')
        for tag in re.findall(r'<link\b[^>]+>',page,re.I):
            if re.search(r'rel=[\"\'][^\"\']*icon',tag,re.I):
                href=re.search(r'href=[\"\']([^\"\']+)',tag,re.I)
                if href and '.svg' not in href[1]:candidates.append(urllib.parse.urljoin(site,html.unescape(href[1])))
    except Exception:pass
    candidates.append(urllib.parse.urljoin(site,'/favicon.ico'))
    for url in dict.fromkeys(candidates):
        try:
            im=Image.open(io.BytesIO(get(url))).convert('RGBA');im.thumbnail((64,64),Image.Resampling.LANCZOS)
            canvas=Image.new('RGBA',(72,72));canvas.alpha_composite(im,((72-im.width)//2,(72-im.height)//2));canvas.save(out/(key+'.png'))
            return key,url
        except Exception:pass
    return key,'MISSING'
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:results=dict(pool.map(one,CATALOG))
(out/'sources.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
for key,url in results.items():print(key+': '+url)
