from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).parent;D=R/'dist'
for f in D.rglob('index.html'):
 s=BeautifulSoup(f.read_text(encoding='utf8'),'html.parser');hero=s.select_one('.hero')
 if hero and not s.select_one('.scroll-stage'):
  stage=s.new_tag('div',attrs={'class':'scroll-stage'});hero.wrap(stage)
  pause=hero.select_one('.slide-pause')
  if pause:pause.decompose()
  label=hero.select_one('.scroll-link')
  if label:label.clear();label.append(BeautifulSoup('<span>↓</span> SCORRI PER ESPLORARE','html.parser'))
  hero['aria-label']='I frutti La Zagara, sequenza guidata dallo scorrimento'
 if f.parent.name=='chi-siamo' and not s.select_one('.company-video-hero'):
  image='/assets/'+next(p.name for p in (D/'assets').glob('*sicilia.webp'))
  markup=f'''<section class="company-video-hero"><img class="company-poster" src="{image}" alt="Agrumi La Zagara"><div class="company-video-shade"></div><div class="company-hero-copy"><span class="eyebrow">IL FILMATO AZIENDALE · LA ZAGARA</span><h1>La nostra storia.<br><em>In movimento.</em></h1><p>Entra nei luoghi e nel lavoro di La Zagara.</p><button class="company-play button light">▶ Guarda il video aziendale</button><a class="company-youtube" href="https://www.youtube.com/watch?v=mFyPQzjpzbE" target="_blank" rel="noopener">Apri su YouTube ↗</a></div><div class="company-player"></div><button class="company-stop" hidden aria-label="Chiudi il video e torna alla copertina">×</button></section>'''
  s.select_one('.page-intro').replace_with(BeautifulSoup(markup,'html.parser'))
 f.write_text(str(s),encoding='utf8')
js=D/'app.js';text=js.read_text(encoding='utf8');start=text.index("  const slides=$$('.hero-slide');");end=text.index("  const gallery=",start)
text=text[:start]+'''  const slides=$$('.hero-slide');
  if(slides.length){
    const stage=$('.scroll-stage'),hero=$('.hero'),progress=$('.slide-progress span');let current=-1,queued=false;
    function setSlide(i){i=Math.max(0,Math.min(slides.length-1,i));if(i===current)return;current=i;
      slides.forEach((s,j)=>{s.classList.toggle('active',j===i);s.classList.toggle('passed',j<i);s.setAttribute('aria-hidden',String(j!==i));s.inert=j!==i;});
      $('.slide-count').innerHTML=String(i+1).padStart(2,'0')+' <small>/ '+String(slides.length).padStart(2,'0')+'</small>';
      progress.style.width=((i+1)/slides.length*100)+'%';
    }
    function measure(){if(!reduced.matches&&stage){const top=stage.getBoundingClientRect().top+scrollY-parseFloat(getComputedStyle(hero).top||0);const distance=stage.offsetHeight-hero.offsetHeight;const ratio=Math.max(0,Math.min(.999,(scrollY-top)/Math.max(1,distance)));setSlide(Math.floor(ratio*slides.length));}queued=false;}
    function go(i){const next=Math.max(0,Math.min(slides.length-1,i));setSlide(next);if(!reduced.matches&&stage){const top=stage.getBoundingClientRect().top+scrollY-parseFloat(getComputedStyle(hero).top||0);const distance=stage.offsetHeight-hero.offsetHeight;scrollTo({top:Math.max(0,top+distance*(next+.12)/slides.length),behavior:'instant'});}}
    $('.slide-prev').addEventListener('click',()=>go(current-1));$('.slide-next').addEventListener('click',()=>go(current+1));
    hero.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();go(current+1)}if(e.key==='ArrowLeft'){e.preventDefault();go(current-1)}});
    addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(measure)}},{passive:true});addEventListener('resize',measure);reduced.addEventListener('change',()=>{setSlide(0);measure()});setSlide(0);measure();
  }
'''+text[end:];js.write_text(text,encoding='utf8')
p=D/'interactive.js';text=p.read_text(encoding='utf8')
if '// Company hero player' not in text:
 text+='''\n// Company hero player: playback is inline and starts on an explicit click.
(()=>{const hero=document.querySelector('.company-video-hero');if(!hero)return;const play=hero.querySelector('.company-play'),stop=hero.querySelector('.company-stop'),slot=hero.querySelector('.company-player');play.addEventListener('click',()=>{const f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/mFyPQzjpzbE?autoplay=1&rel=0&playsinline=1';f.title='La Zagara — video aziendale';f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';f.allowFullscreen=true;f.referrerPolicy='strict-origin-when-cross-origin';slot.replaceChildren(f);hero.classList.add('playing');stop.hidden=false;stop.focus()});function close(){slot.replaceChildren();hero.classList.remove('playing');stop.hidden=true;play.focus()}stop.addEventListener('click',close);hero.addEventListener('keydown',e=>{if(e.key==='Escape'&&hero.classList.contains('playing'))close()})})();
''';p.write_text(text,encoding='utf8')
p=D/'interactive.css';text=p.read_text(encoding='utf8')
if '/* Scroll-directed heroes */' not in text:
 text+='''\n/* Scroll-directed heroes */
.scroll-stage{position:relative;height:400svh}.scroll-stage>.hero{position:sticky;top:78px;height:calc(100svh - 78px);min-height:560px;max-height:none}.scroll-stage .hero-slide{transition:transform .85s cubic-bezier(.2,.7,.2,1),opacity .85s;transform:translateY(100%);visibility:visible;opacity:0}.scroll-stage .hero-slide.active{transform:translateY(0);opacity:1}.scroll-stage .hero-slide.passed{transform:translateY(-100%);opacity:0}.scroll-stage .hero-slide.active .hero-bg{animation:kenburns 12s ease-out both}.company-video-hero{height:calc(100svh - 98px);min-height:600px;position:relative;isolation:isolate;overflow:hidden;background:var(--deep);color:var(--cream)}.company-poster{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;animation:hero-drift 18s ease-in-out infinite alternate}.company-video-shade{position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,#102a20cc,#102a2033)}.company-hero-copy{position:absolute;left:8%;right:8%;bottom:18%}.company-hero-copy h1{margin:30px 0;font-size:clamp(65px,8vw,120px)}.company-hero-copy em{color:#f3b47b}.company-hero-copy p{font-size:14px;color:#e0e7d7;margin-bottom:30px}.company-youtube{display:block;font-size:10px;margin-top:20px;text-decoration:underline;text-underline-offset:5px}.company-player{position:absolute;inset:0;z-index:3;pointer-events:none}.company-player iframe{width:100%;height:100%;border:0;pointer-events:auto;background:black}.company-video-hero.playing .company-hero-copy{visibility:hidden}.company-stop{position:absolute;right:22px;top:22px;z-index:4;width:48px;height:48px;border:1px solid #fff8;border-radius:50%;background:#102a20bb;color:white;font-size:30px}.company-stop[hidden]{display:none}@media(max-width:700px){.scroll-stage{height:340svh}.scroll-stage>.hero{top:70px;height:calc(100svh - 70px);min-height:560px}.company-video-hero{height:calc(100svh - 74px);min-height:580px}.company-hero-copy{left:6%;right:6%;bottom:12%}.company-hero-copy h1{font-size:63px}.company-hero-copy p{font-size:12px}}@media(prefers-reduced-motion:reduce){.scroll-stage{height:auto}.scroll-stage>.hero{position:relative;top:auto}.scroll-stage .hero-slide{transform:none;transition:none}.scroll-stage .hero-slide:not(.active){display:none}.company-poster{animation:none}}
''';p.write_text(text,encoding='utf8')
print('Scroll-driven slideshow and inline company video hero installed')
