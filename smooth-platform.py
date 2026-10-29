from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).parent;D=R/'dist'
p=D/'chi-siamo/index.html';s=BeautifulSoup(p.read_text(encoding='utf8'),'html.parser');hero=s.select_one('.company-video-hero')
for e in hero.select('video,.background-video-toggle,.stock-credit'):e.decompose()
hero['class']=['company-video-hero','about-photo-hero'];hero.select_one('.company-poster')['src']='/assets/'+next(p.name for p in (D/'assets').glob('*slide-uva-b.webp'))
hero.select_one('.eyebrow').string='CHI SIAMO · LA ZAGARA';hero.select_one('h1').clear();hero.select_one('h1').append(BeautifulSoup('Una storia di terra.<br><em>Una visione che cresce.</em>','html.parser'));hero.select_one('.company-hero-copy p').string='Produzione, selezione e commercializzazione. Con radici in Sicilia e uno sguardo aperto al futuro.'
for e in s.select('.video-stories,.video-section,.video-dialog,.fruit-atlas'):e.decompose()
p.write_text(str(s),encoding='utf8')
js=D/'app.js';text=js.read_text(encoding='utf8');start=text.index('  // Progressive page transitions');end=text.index("  const slides=",start)
text=text[:start]+'''  // Native navigation avoids an artificial delay and preserves browser history.
  addEventListener('pageshow',()=>{document.body.classList.remove('menu-open');menu?.setAttribute('aria-expanded','false');menu?.setAttribute('aria-label','Apri menu');$('.page-transition')?.classList.remove('leaving')});
  const mobileMenu=matchMedia('(max-width:800px)');mobileMenu.addEventListener('change',e=>{if(!e.matches){document.body.classList.remove('menu-open');menu?.setAttribute('aria-expanded','false');menu?.setAttribute('aria-label','Apri menu')}});
'''+text[end:]
# Cache the fixed list of parallax layers instead of querying the DOM on every scroll frame.
text=text.replace('  let scrollPending = false;','  const parallaxImages=$$(\'.parallax-image\');\n  let scrollPending = false;').replace("$$('.parallax-image').forEach",'parallaxImages.forEach')
js.write_text(text,encoding='utf8')
js=D/'interactive.js';text=js.read_text(encoding='utf8');text=text.replace("entries=>entries.forEach(e=>e.target.classList.toggle('chapter-entered',e.isIntersecting))","entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('chapter-entered');observer.unobserve(e.target)}})")
text=text.replace("if(video.getBoundingClientRect().bottom>0)start()","if(video.getBoundingClientRect().bottom>0&&video.getBoundingClientRect().top<innerHeight)start()")
js.write_text(text,encoding='utf8')
css=D/'interactive.css';text=css.read_text(encoding='utf8');text+='''\n/* Stable header geometry and native navigation */
.site-header,.site-header.scrolled{height:88px;transition:box-shadow .25s}.site-header .brand,.site-header.scrolled .brand{height:78px}.site-header .brand img,.site-header.scrolled .brand img{height:72px;transition:none}.page-transition{display:none!important}.about-photo-hero{height:calc(100svh - 88px);min-height:650px}.about-photo-hero .company-poster{animation:none;z-index:0}.about-photo-hero .company-hero-copy h1{font-size:clamp(60px,6.8vw,105px)}.about-photo-hero .company-hero-copy p{max-width:500px;line-height:1.9}.scroll-chapter .chapter-visual img{will-change:auto}.home-video-hero{height:calc(100svh - 88px)}@media(max-width:800px){.site-header,.site-header.scrolled{height:74px}.site-header .brand,.site-header.scrolled .brand{height:66px}.site-header .brand img,.site-header.scrolled .brand img{height:62px}.site-header nav{top:74px}.about-photo-hero,.home-video-hero{height:calc(100svh - 74px)}.about-photo-hero .company-hero-copy h1{font-size:56px}}\n''';css.write_text(text,encoding='utf8')
print('About video removed; stable header, native navigation, one-time chapter entry animations')
