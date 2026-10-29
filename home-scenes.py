from pathlib import Path
from bs4 import BeautifulSoup
import base64
R=Path(__file__).parent;D=R/'dist'
image=base64.b64encode((R/'design/client-logo.png').read_bytes()).decode()
# SVG compositing preserves the supplied pixels while keying the near-white background.
# Opaque petal shapes sit behind the original colored artwork so the flower stays white.
petals='''<g fill="#fffdf6"><path d="M815 494Q737 443 798 315Q842 370 837 421Q835 470 815 494Z"/><path d="M815 494Q858 386 966 399Q925 471 852 496Z"/><path d="M815 494Q920 497 929 596Q849 569 815 494Z"/><path d="M815 494Q769 568 655 569Q719 510 815 494Z"/><path d="M815 494Q710 512 651 473Q723 397 815 494Z"/></g>'''
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="190 150 1150 760"><defs><filter id="cut" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 -1 -1 -1 0 3"/><feComponentTransfer><feFuncA type="discrete" tableValues="0 0 1 1 1 1 1 1"/></feComponentTransfer></filter></defs>{petals}<image width="1536" height="1024" href="data:image/png;base64,{image}" filter="url(#cut)"/></svg>'''
(D/'assets/zagara-cutout.svg').write_text(svg,encoding='utf8')
favicon='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M10 10C37 12 56-9 69 22L78 30L34 76C54 71 67 96 85 86C60 112 36 76 10 88L67 24C47 12 33 30 10 10Z" fill="#173c2b"/><path d="M68 32Q77 9 96 14Q88 28 68 32" fill="#173c2b"/><path d="M73 33C104 38 107 69 84 82L70 66L88 50Q75 46 64 56Z" fill="#f58220"/><g fill="#fffdf6"><path d="M62 64Q48 43 59 31Q70 48 62 64"/><path d="M62 64Q71 42 88 49Q78 65 62 64"/><path d="M62 64Q84 65 83 83Q66 80 62 64"/><path d="M62 64Q56 84 39 79Q42 66 62 64"/><path d="M62 64Q43 68 35 57Q51 46 62 64"/></g><g fill="#dda42a"><circle cx="61" cy="61" r="3"/><circle cx="56" cy="51" r="2"/><circle cx="65" cy="49" r="2"/><circle cx="70" cy="56" r="2"/></g></svg>'''
(D/'assets/zagara-symbol.svg').write_text(favicon,encoding='utf8')
home=D/'index.html';s=BeautifulSoup(home.read_text(encoding='utf8'),'html.parser');company=BeautifulSoup((D/'chi-siamo/index.html').read_text(encoding='utf8'),'html.parser');video=company.select_one('.company-video-hero')
video['class']=['company-video-hero','home-video-hero'];video.select_one('h1').clear();video.select_one('h1').append(BeautifulSoup('La Sicilia,<br>in ogni <em>frutto.</em>','html.parser'));video.select_one('.eyebrow').string='DALLA NOSTRA TERRA, CON PASSIONE';video.select_one('.company-hero-copy p').string='Una terra straordinaria. Una passione che si rinnova a ogni raccolto.';cta=video.select_one('.company-hero-copy .button');cta['href']='#scene-uva';cta.string='Scorri e scopri il nostro mondo ↓'
stage=s.select_one('.scroll-stage')
if stage:stage.replace_with(video)
def pic(term):return '/assets/'+next(p.name for p in (D/'assets').glob('*.webp') if term in p.name)
scenes='<div class="scroll-chapters">'
for i,(name,title,desc,url,im) in enumerate([
 ('UVA DA TAVOLA','La dolcezza,<br><em>in tutte le sue forme.</em>','Con e senza semi. Varietà tradizionali ed esclusive, tra Sicilia e Puglia.','uva-da-tavola',pic('slide-uva-b')),
 ('ARANCE','Il sole ha<br><em>un carattere.</em>','Moro, Tarocco e Sanguinello. Il colore e il profumo degli agrumi siciliani.','arance',pic('sicilia')),
 ('LIMONI','Il Mediterraneo,<br><em>da vicino.</em>','Femminello Siracusano e Zagara Bianca: un mondo di fioriture e profumi.','limoni',pic('slide-limoni')),
 ('POMODORI','Il rosso della<br><em>nostra passione.</em>','Ciliegino, Datterino e Piccadilly: il gusto autentico della nostra selezione.','pomodori',pic('slide-pom'))]):
 scenes+=f'<section class="scroll-chapter" id="scene-{("uva" if i==0 else url)}"><div class="chapter-visual"><img src="{im}" alt="{name}" loading="lazy"></div><div class="chapter-tint"></div><div class="chapter-copy"><span class="eyebrow">0{i+1} / {name}</span><h2>{title}</h2><p>{desc}</p><a class="button light" href="/prodotti/{url}">Esplora {name.lower()} ↗</a></div><span class="chapter-counter" aria-hidden="true">0{i+1}</span></section>'
scenes+='</div>'
if not s.select_one('.scroll-chapters'):s.select_one('.home-video-hero').insert_after(BeautifulSoup(scenes,'html.parser'))
home.write_text(str(s),encoding='utf8')
for f in D.rglob('*.html'):
 page=BeautifulSoup(f.read_text(encoding='utf8'),'html.parser')
 for im in page.select('.brand img,.footer-about img'):im['src']='/assets/zagara-cutout.svg'
 for icon in page.select('link[rel=icon]'):icon['href']='/assets/zagara-symbol.svg?v=2';icon['type']='image/svg+xml'
 f.write_text(str(page),encoding='utf8')
css=D/'interactive.css';text=css.read_text(encoding='utf8')
text+='''\n/* Independent animated scroll chapters */
.brand{height:90px;overflow:visible;transition:height .3s,width .3s}.brand img{height:84px;object-fit:contain;mix-blend-mode:normal;transition:height .3s}.site-header.scrolled .brand{height:66px}.site-header.scrolled .brand img{height:64px}.footer-about img{mix-blend-mode:normal}.scroll-chapter{position:relative;min-height:760px;height:100svh;isolation:isolate;overflow:hidden;background:var(--deep);color:var(--cream)}.chapter-visual{position:absolute;inset:0;z-index:-2;overflow:hidden}.chapter-visual img{width:100%;height:100%;object-fit:cover;transform:scale(1.16);transition:transform 1.8s cubic-bezier(.15,.65,.2,1),filter 1.5s;filter:brightness(.75)}.chapter-tint{position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,#102a20b0,transparent),linear-gradient(0deg,#102a2070,transparent)}.chapter-copy{position:absolute;left:8%;right:8%;bottom:17%;max-width:1000px;opacity:1;transform:none}.chapter-copy h2{font-size:clamp(60px,7vw,110px);margin:28px 0}.chapter-copy em{color:#f3b47b}.chapter-copy p{font-size:14px;color:#e6ecdd;max-width:430px;margin-bottom:30px}.chapter-counter{position:absolute;right:5%;top:7%;font:150px var(--serif);color:#fff3}.chapters-motion .chapter-copy{opacity:0;transform:translateY(70px);transition:opacity 1s .15s,transform 1.2s .15s cubic-bezier(.2,.7,.2,1)}.chapter-entered .chapter-copy{opacity:1;transform:translateY(0)}.chapter-entered .chapter-visual img{transform:scale(1);filter:brightness(1)}.home-video-hero{height:calc(100svh - 98px);min-height:650px}@media(max-width:700px){.brand{height:66px;width:145px}.brand img{height:62px}.site-header.scrolled .brand{height:62px}.site-header.scrolled .brand img{height:58px}.scroll-chapter{height:90svh;min-height:620px}.chapter-copy{left:6%;right:6%;bottom:16%}.chapter-copy h2{font-size:52px}.chapter-copy p{font-size:12px}.chapter-counter{font-size:100px}.home-video-hero{height:calc(100svh - 74px);min-height:610px}}@media(prefers-reduced-motion:reduce){.chapters-motion .chapter-copy{opacity:1;transform:none;transition:none}.chapter-visual img{transform:none;filter:none;transition:none}}
''';css.write_text(text,encoding='utf8')
js=D/'interactive.js';text=js.read_text(encoding='utf8')
text+='''\n// Independent chapters enter as the visitor scrolls naturally between sections.
(()=>{const reduced=matchMedia('(prefers-reduced-motion: reduce)');if(reduced.matches||!('IntersectionObserver'in window))return;const chapters=[...document.querySelectorAll('.scroll-chapter')];document.documentElement.classList.add('chapters-motion');const observer=new IntersectionObserver(entries=>entries.forEach(e=>e.target.classList.toggle('chapter-entered',e.isIntersecting)),{threshold:.2});chapters.forEach(s=>observer.observe(s));})();
''';js.write_text(text,encoding='utf8')
print('Home video, separate scroll chapters, transparent SVG logo and symbol favicon installed')
