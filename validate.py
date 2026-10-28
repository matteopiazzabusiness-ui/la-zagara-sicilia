from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
import json,shutil
ROOT=Path(__file__).parent.resolve();DIST=ROOT/'dist';errors=[];count=0
# Preserve source photographs in the excluded research directory; publish optimized copies only.
raw=ROOT/'research/original-assets';raw.mkdir(exist_ok=True)
for p in (DIST/'assets').iterdir():
 if p.suffix.lower() in ['.jpg','.jpeg']:
  destination=(raw/p.name).resolve()
  assert p.resolve().is_relative_to(DIST.resolve()) and destination.is_relative_to(raw.resolve())
  shutil.copy2(p,destination);p.unlink()
for file in DIST.rglob('*.html'):
 soup=BeautifulSoup(file.read_text(encoding='utf8'),'html.parser');count+=1
 for e in soup.select('[href],[src]'):
  url=e.get('href') or e.get('src')
  if not url or not url.startswith('/') or url.startswith('//'):continue
  path=DIST/unquote(urlsplit(url).path).lstrip('/')
  if path.is_dir():path=path/'index.html'
  if not path.exists():errors.append(f'{file.relative_to(DIST)}: missing {url}')
 if not soup.title or not soup.select_one('main h1'):errors.append(f'{file}: missing title/h1')
 if '\ufffd' in file.read_text(encoding='utf8'):errors.append(f'{file}: replacement characters')
for name in ['Calendario_prodotti.pdf','Calendario_uva.pdf']:
 if not (DIST/'assets'/name).read_bytes().startswith(b'%PDF'):errors.append('Invalid PDF '+name)
standard=BeautifulSoup((DIST/'varieta-standard/index.html').read_text(encoding='utf8'),'html.parser')
if len(standard.select('.variety-mini-grid article'))!=13:errors.append('Expected 13 standard grape varieties')
result={'pages':count,'grapeVarieties':len(standard.select('.variety-mini-grid article')),'publishedMB':round(sum(p.stat().st_size for p in DIST.rglob('*') if p.is_file())/1024**2,2),'errors':errors}
(ROOT/'research/validation.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result));raise SystemExit(bool(errors))
