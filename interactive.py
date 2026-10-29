from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).parent;D=R/'dist'
def pic(term):return '/assets/'+next(p.name for p in (D/'assets').glob('*.webp') if term in p.name)
items=[('Uva da tavola','Varietà standard ed esclusive, con e senza semi. Un mondo di colori e consistenze.','uva-da-tavola',pic('slide-uva-b')),('Arance','Moro, Tarocco, Sanguinello, Lane Late e Clementine Tacle: il carattere degli agrumi.','arance',pic('sicilia')),('Limoni','Femminello Siracusano e Zagara Bianca. Profumo intenso e fioriture che seguono le stagioni.','limoni',pic('slide-limoni')),('Pomodori','Ciliegino, Datterino e Piccadilly: piccoli frutti, diverse personalità.','pomodori',pic('slide-pom'))]
explorer='<section class="interactive-explorer wrap"><span class="eyebrow">SCEGLI, OSSERVA, SCOPRI</span><h2>Lasciati guidare<br><em>dal tuo gusto.</em></h2><div class="fruit-tabs" role="tablist" aria-label="Esplora le famiglie di prodotti">'+''.join(f'<button role="tab" id="fruit-tab-{i}" aria-controls="fruit-panel-{i}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">{n}</button>' for i,(n,_,_,_) in enumerate(items))+'</div>'+''.join(f'<div class="fruit-panel" id="fruit-panel-{i}" role="tabpanel" aria-labelledby="fruit-tab-{i}" {"hidden" if i else ""}><img src="{im}" alt="{n}" loading="lazy"><div><span class="eyebrow">0{i+1} / LA ZAGARA</span><h3>{n}</h3><p>{desc}</p><a class="button green" href="/prodotti/{url}">Esplora varietà e dettagli ↗</a></div></div>' for i,(n,desc,url,im) in enumerate(items))+'</section>'
video='<section class="video-stories wrap"><div class="section-heading"><div><span class="eyebrow">STORIE DA GUARDARE</span><h2>Il territorio si muove.<br><em>Entra nel racconto.</em></h2></div></div><div class="video-grid">'
for id,title,desc,im,credit,url in [('mFyPQzjpzbE','Dentro La Zagara','Il filmato aziendale già presentato sul sito originale.',pic('slide-uva-b'),'Fonte: La Zagara','https://www.zagara.com/chi-siamo'),('KPuC0XRiXWo','Scent of Zagara','Un viaggio nei paesaggi e nella cultura degli agrumi siciliani. Un racconto del territorio, pubblicato dal Distretto Agrumi di Sicilia.',pic('sicilia'),'Fonte: Distretto Produttivo Agrumi di Sicilia','https://www.distrettoagrumidisicilia.it/video/')]:
 video+=f'<article><button class="video-launch" data-video="{id}" data-title="{title}" aria-label="Riproduci {title}"><img src="{im}" alt="" loading="lazy"><span class="play-disc">▶</span><span class="video-label">GUARDA IL FILMATO</span></button><h3>{title}</h3><p>{desc}</p><a class="video-credit" href="{url}" target="_blank" rel="noopener">{credit} ↗</a></article>'
video+='</div><p class="video-note">Premi play per caricare il lettore YouTube. Il video parte solo su tua richiesta.</p></section>'
dialog='''<dialog class="video-dialog" aria-label="Riproduzione video"><button class="video-close" aria-label="Chiudi video">×</button><h2></h2><div class="video-frame"></div><p>Se il filmato non è disponibile qui, <a class="video-fallback" target="_blank" rel="noopener">guardalo su YouTube ↗</a>.</p></dialog>'''
for f in D.rglob('index.html'):
 s=BeautifulSoup(f.read_text(encoding='utf8'),'html.parser');main=s.select_one('main');key=f.parent.name if f.parent!=D else 'home'
 if not s.select_one('script[src="/interactive.js"]'):
  tag=s.new_tag('script',src='/interactive.js',defer='');s.head.append(tag)
  tag=s.new_tag('link',rel='stylesheet',href='/interactive.css');s.head.append(tag)
 if key in ['home','prodotti'] and not s.select_one('.interactive-explorer'):
  anchor=s.select_one('.fruit-atlas')
  if anchor:anchor.insert_after(BeautifulSoup(explorer,'html.parser'))
  else:main.append(BeautifulSoup(explorer,'html.parser'))
 if key in ['home','chi-siamo','gallery'] and not s.select_one('.video-stories'):
  main.append(BeautifulSoup(video,'html.parser'));s.body.append(BeautifulSoup(dialog,'html.parser'))
 if key in ['news','contatti','gallery'] and not s.select_one('.distributed-hero'):
  title={'news':'Le storie continuano.<br><em>Il futuro cresce.</em>','contatti':'Ogni incontro,<br><em>una nuova possibilità.</em>','gallery':'Guarda più vicino.<br><em>Lasciati sorprendere.</em>'}[key]
  hero=f'<section class="distributed-hero"><img src="{pic("sicilia")}" alt="Agrumi La Zagara" loading="lazy"><div><span class="eyebrow">LA ZAGARA · FRUTTI DI SICILIA</span><h2>{title}</h2><a class="button light" href="/prodotti">Scopri la nostra selezione ↗</a></div></section>'
  main.append(BeautifulSoup(hero,'html.parser'))
 grid=s.select_one('.variety-grid')
 if grid and not s.select_one('.variety-search'):
  grid.insert_before(BeautifulSoup('<div class="variety-search"><label for="variety-query">Trova una varietà in questa pagina</label><input id="variety-query" type="search" placeholder="Scrivi il nome o una caratteristica…"><p class="variety-results" aria-live="polite"></p></div>','html.parser'))
  grid.insert_after(BeautifulSoup('<p class="variety-empty" hidden>Nessuna varietà corrisponde alla ricerca. Prova un altro termine.</p>','html.parser'))
 if key=='home' and not s.select_one('.chapter-links'):
  nav='<nav class="chapter-links" aria-label="Capitoli della homepage"><a href="#scopri">I prodotti</a><a href="#la-terra">La terra</a><a href="#la-passione">La passione</a><a href="/gallery">Le immagini ↗</a></nav>'
  s.select_one('.ticker').insert_after(BeautifulSoup(nav,'html.parser'))
 if key=='privacy':
  for p in s.select('p'):
   if 'Video, mappe e fonti esterne si aprono soltanto' in p.get_text():
    p.string='Le fotografie e i caratteri sono ospitati localmente. Non sono integrati strumenti di analisi, pubblicità o profilazione. I lettori YouTube vengono caricati soltanto dopo il clic sul pulsante play e possono trattare dati secondo le informative del fornitore. Mappe e fonti esterne si aprono tramite collegamenti scelti dal visitatore. La piattaforma di hosting può trattare dati tecnici necessari al servizio.'
 f.write_text(str(s),encoding='utf8')
(D/'404.html').write_text((D/'404/index.html').read_text(encoding='utf8'),encoding='utf8')
print('Video stories, tabs, search and distributed heroes integrated')
