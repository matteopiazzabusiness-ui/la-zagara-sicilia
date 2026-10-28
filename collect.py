from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import json, hashlib, re

ROOT=Path(__file__).parent
BASE='https://www.zagara.com'
paths=['/','/chi-siamo','/prodotti','/prodotti/uva-da-tavola','/prodotti/arance','/prodotti/limoni','/prodotti/pomodori','/news','/gallery','/contatti','/privacy','/varieta-innovative','/varieta-standard','/arance-tarocco','/varieta-innovative-snfl','/varieta-innovative-ifg','/blog-news/2-puntiamo-anche-all-uva-senza-semi','/blog-news/1-partenza-tiepida-ma-la-qualita-e-salva','/blog-news/3-uva-italia-e-cominciata-la-raccolta-nel-barese']
def get(url):
 return urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read()
def page(p):
 try:
  raw=get(BASE+p); soup=BeautifulSoup(raw.decode('utf-8'),'html.parser')
  (ROOT/'research'/((p.strip('/').replace('/','__') or 'home')+'.html')).write_bytes(raw)
  main=soup.select_one('#sp-main-body') or soup.select_one('main') or soup
  return p,{'title':soup.title.get_text(),'text':main.get_text('\n',strip=True),'images':[urljoin(BASE,x.get('src','')) for x in main.select('img')],'all_images':[urljoin(BASE,x.get('src','')) for x in soup.select('img')], 'links':list(dict.fromkeys(urljoin(BASE,x.get('href','')) for x in main.select('a[href]')))}
 except Exception as e:return p,{'error':str(e)}
pages=dict(ThreadPoolExecutor(6).map(page,paths))
(ROOT/'research/pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf8')
images=set(x for v in pages.values() for x in v.get('all_images',[]) if '/images/' in x)
for f in (ROOT/'research').glob('*.html'):
 for x in re.findall(r'''(?:https://www.zagara.com)?/?images/[^\s'"<>;)]+''',f.read_text(encoding='utf8')):
  images.add(urljoin(BASE+'/',x))
def download(url):
 try:
  name=hashlib.sha1(url.encode()).hexdigest()[:8]+'-'+Path(urlparse(url).path).name
  original=Path(name).suffix.lower() in ['.jpg','.jpeg']
  target=(ROOT/'research/original-assets' if original else ROOT/'dist/assets')/name
  target.parent.mkdir(parents=True,exist_ok=True)
  if not target.exists():target.write_bytes(get(url))
  return url,'/assets/'+name
 except Exception as e:return url,None
assets=dict(ThreadPoolExecutor(8).map(download,images))
(ROOT/'research/assets.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2),encoding='utf8')
for pdf in ['Calendario_prodotti.pdf','Calendario_uva.pdf']:
 (ROOT/'dist/assets'/pdf).write_bytes(get(BASE+'/calendari/'+pdf))
print('Pages:',len(pages),'Images:',len(assets),'Failed:',[u for u,v in assets.items() if not v])
