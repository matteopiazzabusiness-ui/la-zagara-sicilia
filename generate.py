from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request
from PIL import Image
import json, html, re

ROOT=Path(__file__).parent; DIST=ROOT/'dist'; BASE='https://www.zagara.com'
pages=json.loads((ROOT/'research/pages.json').read_text(encoding='utf8'))
assets=json.loads((ROOT/'research/assets.json').read_text(encoding='utf8'))
def esc(s):return html.escape(str(s),quote=True)
def asset(n):
 if n.startswith('https:'):return assets.get(n) or n
 return next((v for u,v in assets.items() if v and u.endswith('/'+n)), '')
# Ship optimized, local photographs. Keep original PNGs for logos and transparent assets.
for u,v in list(assets.items()):
 if v and Path(v).suffix.lower() in ['.jpg','.jpeg']:
  original=DIST/v.lstrip('/')
  if not original.exists():original=ROOT/'research/original-assets'/Path(v).name
  im=Image.open(original);im.thumbnail((1920,1600)); out=Path(v).with_suffix('.webp').as_posix()
  im.convert('RGB').save(DIST/out.lstrip('/'),'WEBP',quality=85);assets[u]=out
def image(n,alt='',cls='',eager=False):return f'<img src="{asset(n)}" alt="{esc(alt)}" class="{cls}" loading="{"eager" if eager else "lazy"}" decoding="async">'
ARROW='<span aria-hidden="true">↗</span>'
def link(url,label,cls='text-link'):return f'<a class="{cls}" href="{url}">{label} {ARROW}</a>'
nav=[('/','Home'),('/chi-siamo','Chi siamo'),('/prodotti','Prodotti'),('/news','News'),('/gallery','Gallery')]
def header(path):
 return f'''<a class="skip-link" href="#main">Vai al contenuto</a><div class="read-progress"></div>
 <header class="site-header"><a href="/" class="brand" aria-label="La Zagara, homepage">{image('logo-la-zagara.png','La Zagara — fresh fruits',eager=True)}</a>
 <nav aria-label="Navigazione principale">{''.join(f'<a href="{u}" {"aria-current=page" if path==u or u!="/" and path.startswith(u+"/") else ""}>{n}</a>' for u,n in nav)}<a href="/contatti" class="nav-contact">Parliamone {ARROW}</a></nav>
 <button class="menu-toggle" aria-label="Apri menu" aria-expanded="false"><span></span><span></span></button></header>'''
def footer():
 return f'''<section class="contact-band"><div><span class="eyebrow">COLTIVIAMO NUOVE RELAZIONI</span><h2>Il prossimo raccolto?<br><em>Inizia da un incontro.</em></h2></div>{link('/contatti','Scrivici','circle-link')}</section>
 <footer><div class="footer-top"><div class="footer-about">{image('logo-la-zagara.png','La Zagara')}<p>La passione per la terra.<br>La qualità in ogni frutto.</p><a href="mailto:info@zagara.com">info@zagara.com ↗</a></div><div><span class="eyebrow">ESPLORA</span>{''.join(f'<a href="{u}">{n}</a>' for u,n in nav[1:])}<a href="/contatti">Contatti</a></div><div><span class="eyebrow">I NOSTRI FRUTTI</span><a href="/prodotti/uva-da-tavola">Uva da tavola</a><a href="/prodotti/arance">Arance</a><a href="/prodotti/limoni">Limoni</a><a href="/prodotti/pomodori">Pomodori</a></div><div><span class="eyebrow">VIENI A TROVARCI</span><p>Giovanni Grasso S.r.l.<br>C.da Vignagrande s.n.<br>95013 Fiumefreddo di Sicilia (CT)</p><a href="tel:+390957762652">+39 095 776 26 52</a><p>Lun — Sab · 8:00 — 20:00<br>Fax +39 095 64 24 96</p></div></div><div class="footer-bottom"><span>© La Zagara · Giovanni Grasso S.r.l. · P.IVA 03257040877</span><a href="/privacy">Privacy & Cookie</a><a href="#top">Torna su ↑</a></div><div class="footer-word" aria-hidden="true">la zagara.</div></footer>'''
def intro(kicker,title,desc='',cls=''):
 return f'<section class="page-intro {cls}"><span class="eyebrow reveal">{kicker}</span><h1 class="reveal">{title}</h1>{f"<p class=\"reveal\">{desc}</p>" if desc else ""}</section>'
def write(path,title,body,description='La Zagara: produzione e commercializzazione di agrumi, uva da tavola e ortofrutta. Dalla Sicilia, con passione.'):
 dest=DIST/path.strip('/')/'index.html' if path!='/' else DIST/'index.html';dest.parent.mkdir(parents=True,exist_ok=True)
 canonical='https://la-zagara-sicilia.info861460.chatgpt.site'+path
 doc=f'''<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#173c2b"><title>{esc(title)} | La Zagara</title><meta name="description" content="{esc(description)}"><meta property="og:title" content="{esc(title)} | La Zagara"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://la-zagara-sicilia.info861460.chatgpt.site{asset('slide-uva-b.jpg')}"><link rel="canonical" href="{canonical}"><link rel="icon" href="{asset('logo-bollino.png')}"><link rel="stylesheet" href="/style.css"><script src="/app.js" defer></script></head><body id="top">{header(path)}<main id="main">{body}</main>{footer()}<div class="page-transition" aria-hidden="true"><span>la zagara.</span></div><dialog id="lightbox" aria-label="Galleria fotografica"><button class="lightbox-close" aria-label="Chiudi immagine">×</button><button class="lightbox-prev" aria-label="Foto precedente">←</button><figure><img alt=""><figcaption></figcaption></figure><button class="lightbox-next" aria-label="Foto successiva">→</button></dialog></body></html>'''
 dest.write_text(doc,encoding='utf8')

products=[('Uva da tavola','uva-da-tavola','uvac.jpg','01','La dolcezza, in tutte le sue sfumature.'),('Arance','arance','agrumic.jpg','02','Il carattere inconfondibile della Sicilia.'),('Limoni','limoni','limoni-n.jpg','03','Un profumo che sa di Mediterraneo.'),('Pomodori','pomodori','pomodori-n2.jpg','04','Il sapore autentico della nostra terra.')]
def product_grid():return '<div class="product-grid">'+''.join(f'<a class="product-card reveal" href="/prodotti/{slug}"><div class="product-image">{image(img,name)}<span class="product-num">{num} /</span><span class="round-arrow">↗</span></div><h3>{name}</h3><p>{desc}</p></a>' for name,slug,img,num,desc in products)+'</div>'
certs=[('geogr-protetta2.png','Indicazione Geografica Protetta'),('arancia-rossa2.png','Arancia Rossa di Sicilia'),('ifs3.png','IFS'),('agr-bio2.png','Agricoltura biologica'),('limone-siracusa2.png','Limone di Siracusa'),('global-gap.png','GLOBALG.A.P.'),('global-grasp2.png','GRASP')]
def certification():return '<section class="certifications wrap"><div><span class="eyebrow">LA QUALITÀ, PRIMA DI TUTTO</span><p>La qualità prende forma.<br>In ogni fase del nostro lavoro.</p></div><div class="cert-logos">'+''.join(image(a,b) for a,b in certs)+'</div></section>'
news=[('/blog-news/2-puntiamo-anche-all-uva-senza-semi','Puntiamo anche all’uva senza semi','15 OTTOBRE 2019','news2.jpg','Innovazione varietale e nuove prospettive per l’uva da tavola siciliana.'),('/blog-news/1-partenza-tiepida-ma-la-qualita-e-salva','Partenza tiepida, ma la qualità è salva','05 AGOSTO 2019','news1.jpg','Giovanni Grasso racconta la stagione e l’evoluzione del mercato.'),('/blog-news/3-uva-italia-e-cominciata-la-raccolta-nel-barese','Uva Italia: è cominciata la raccolta nel barese','09 SETTEMBRE 2016','news3.jpg','La raccolta, i mercati e la storia della famiglia Grasso.')]
def news_grid():return '<div class="news-grid">'+''.join(f'<a class="news-card reveal" href="{p}"><div>{image(im,t)}</div><span class="eyebrow">{date} · NEWS</span><h3>{t} {ARROW}</h3><p>{desc}</p></a>' for p,t,date,im,desc in news)+'</div>'
def values():
 vals=[('01','Qualità che si riconosce','Prodotti freschi e standard elevati per la grande distribuzione italiana ed estera.'),('02','Rispetto per la terra','Metodi tradizionali, attenzione all’ambiente e packaging EcoFriendly.'),('03','Voglia di andare oltre','Varietà esclusive e macchinari all’avanguardia, per continuare a migliorare.'),('04','Cura, fino alla tua tavola','Controlli attenti e tutela del consumatore in ogni fase del nostro lavoro.')]
 return '<section class="values wrap"><div class="section-heading reveal"><span class="eyebrow">LE NOSTRE RADICI</span><h2>Buoni frutti.<br><em>Solidi valori.</em></h2></div><div class="value-rows">'+''.join(f'<details class="reveal" {"open" if i=="01" else ""}><summary><span>{i}</span><h3>{t}</h3><b>+</b></summary><p>{d}</p></details>' for i,t,d in vals)+'</div></section>'
hero_slides=[('slide-uva-b.jpg','UVA DA TAVOLA','La Sicilia,<br>in ogni <em>frutto.</em>','Una terra straordinaria. Una passione che si rinnova a ogni raccolto. Benvenuti nel mondo La Zagara.','/prodotti/uva-da-tavola','Scopri la nostra uva'),('sicilia.jpg','AGRUMI DI SICILIA','Il sole,<br>ha un <em>sapore.</em>','Dagli agrumeti alle pendici dell’Etna, il carattere autentico delle nostre arance.','/prodotti/arance','Esplora le arance'),('slide-limoni.jpg','LIMONI','L’essenza<br>del <em>Mediterraneo.</em>','Femminello Siracusano e Zagara Bianca: il profumo intenso dei nostri limoni.','/prodotti/limoni','Scopri i limoni'),('slide-pom-n2.jpg','POMODORI','Rosso,<br>di <em>passione.</em>','Ciliegino, Datterino e Piccadilly. Il gusto che racconta la cucina italiana.','/prodotti/pomodori','Scopri i pomodori')]
hero='<section class="hero" aria-roledescription="carosello" aria-label="I frutti La Zagara"><div class="hero-slides">'+''.join(f'<article class="hero-slide {"active" if i==0 else ""}" aria-hidden="{"false" if i==0 else "true"}">{image(im,label,"hero-bg",i==0)}<div class="hero-shade"></div><div class="hero-content"><span class="eyebrow">DALLA NOSTRA TERRA, CON PASSIONE</span><h1>{title}</h1><p>{desc}</p>{link(u,cta,"button light")}</div><div class="hero-caption"><span class="tiny-line"></span>{label} <span>·</span> LA ZAGARA</div></article>' for i,(im,label,title,desc,u,cta) in enumerate(hero_slides))+'</div><div class="hero-seal" aria-hidden="true"><svg viewBox="0 0 120 120"><defs><path id="sealCircle" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"/></defs><text><textPath href="#sealCircle">COLTIVIAMO PASSIONE · RACCOGLIAMO QUALITÀ · </textPath></text></svg><span>✳</span></div><div class="hero-bottom"><a href="#scopri" class="scroll-link"><span>↓</span> UN MONDO DA SCOPRIRE</a><div class="slide-controls"><span class="slide-count">01 <small>/ 04</small></span><button class="slide-prev" aria-label="Slide precedente">←</button><button class="slide-next" aria-label="Slide successiva">→</button><button class="slide-pause" aria-label="Metti in pausa slideshow">Ⅱ</button></div></div><div class="slide-progress"><span></span></div></section>'
home=hero+'''<div class="ticker" aria-hidden="true"><div>COLTIVIAMO PASSIONE <span>✳</span> RACCOGLIAMO QUALITÀ <span>✳</span> PORTIAMO LA SICILIA NEL MONDO <span>✳</span> COLTIVIAMO PASSIONE <span>✳</span> RACCOGLIAMO QUALITÀ <span>✳</span> PORTIAMO LA SICILIA NEL MONDO <span>✳</span></div></div>'''
home+=f'''<section class="products-section wrap" id="scopri"><div class="section-heading reveal"><div><span class="eyebrow">NATURALMENTE, LA ZAGARA</span><h2>Una terra generosa.<br><em>Frutti straordinari.</em></h2></div><div><p>Selezioniamo il meglio della natura.<br>Ne custodiamo il gusto, fino a voi.</p>{link('/prodotti','Tutti i nostri prodotti')}</div></div>{product_grid()}</section>
<section class="story wrap"><div class="story-photo reveal">{image('chisiamo1d.jpg','Arancia rossa di Sicilia appena raccolta')}<span class="photo-label">SICILIA · LA NOSTRA NATURA</span><div class="small-photo">{image('chisiamo-n.jpg','La lavorazione dei prodotti La Zagara')}</div></div><div class="story-text reveal"><span class="eyebrow">PIÙ CHE UN LAVORO, UNA PASSIONE</span><h2>Le mani nella terra.<br><em>Lo sguardo lontano.</em></h2><p>Ci sono cose che nascono solo in certi luoghi. E persone che sanno prendersene cura.</p><p>Produciamo e commercializziamo agrumi e ortofrutta con metodi tradizionali e naturali. La nostra missione è portare ai clienti prodotti di alto valore qualitativo, tutelando la terra e chi la coltiva.</p>{link('/chi-siamo','La nostra storia','button green')}</div></section>
<section class="landscape">{image('slide-uva-b.jpg','Filari di uva La Zagara','parallax-image')}<div class="landscape-shade"></div><div class="reveal"><span class="eyebrow">LA NOSTRA FILOSOFIA</span><h2>La natura detta il ritmo.<br><em>Noi ci mettiamo il cuore.</em></h2><p>In serra e in campo aperto. Dalla produzione alla commercializzazione.<br>Ogni scelta nasce dal rispetto per il prodotto.</p>{link('/gallery','Entra nel nostro mondo','button light')}</div></section>'''
home+=values()+certification()+f'<section class="news-section wrap"><div class="section-heading reveal"><div><span class="eyebrow">DAL NOSTRO MONDO</span><h2>Storie di terra.<br><em>Notizie di gusto.</em></h2></div>{link("/news","Tutte le news")}</div>{news_grid()}</section>'
home+=f'<section class="newsletter wrap reveal"><div><span class="eyebrow">RESTIAMO IN CONTATTO</span><h2>Novità fresche,<br><em>direttamente da noi.</em></h2><p>Richiedi l’iscrizione alla newsletter di La Zagara.</p></div><form class="newsletter-form"><label for="newsletter-email">La tua email</label><div><input id="newsletter-email" name="email" type="email" placeholder="nome@esempio.it" required autocomplete="email"><button type="submit" aria-label="Richiedi iscrizione via email">↗</button></div><label class="check"><input type="checkbox" required> Ho letto l’<a href="/privacy">informativa privacy</a>.</label><small>La richiesta si apre nel tuo programma di posta.</small><p class="form-status" role="status"></p></form></section>'
write('/','L’essenza della Sicilia',home)
write('/prodotti','I nostri prodotti',intro('LA NATURA FA IL SUO CORSO','Il meglio della terra.<br><em>Il gusto della qualità.</em>','Agrumi, uva da tavola e ortofrutta: una selezione che nasce dalla passione.')+'<section class="wrap catalog">'+product_grid()+'</section>'+f'<section class="other-products wrap reveal"><span class="eyebrow">E NON FINISCE QUI</span><h2>Una gamma che segue<br><em>la generosità della natura.</em></h2><p>Oltre a pomodori e pomodoro cherry, di cui siamo anche produttori, commercializziamo agrumi, uva da tavola, patate, carote e orticoli in genere. Coltiviamo in serra e in campo aperto.</p>{link("/assets/Calendario_prodotti.pdf","Consulta il calendario prodotti","button green")}</section>'+certification())
about=intro('LA ZAGARA · CHI SIAMO','La nostra storia<br>ha radici <em>profonde.</em>','Produzione e commercializzazione di agrumi e ortofrutta. Una passione che unisce qualità, innovazione e rispetto per la terra.')
about+=f'<section class="story wrap"><div class="story-photo reveal">{image("chisiamo-n.jpg","Lavorazione e confezionamento La Zagara")}</div><div class="story-text reveal"><span class="eyebrow">L’AZIENDA</span><h2>Coltivare bene.<br><em>Guardare avanti.</em></h2><p>Siamo specializzati nella produzione e commercializzazione di prodotti agrumicoli ed ortofrutticoli, coltivati con metodi tradizionali e naturali, nel pieno rispetto della genuinità del prodotto e con un occhio attento all’ambiente.</p><p>Il nostro obiettivo è garantire ai clienti produzioni agricole di alto valore qualitativo, tutelando allo stesso tempo la terra e chi la coltiva.</p><p>Il processo continuo di innovazione ci ha portato ad avere l’esclusiva di particolari uve senza semi e arance Tarocco. Anche i nostri packaging sono EcoFriendly.</p></div></section>'
about+=values()+f'<section class="landscape">{image("sicilia.jpg","Agrumi siciliani","parallax-image")}<div class="landscape-shade"></div><div class="reveal"><span class="eyebrow">LA NOSTRA GAMMA</span><h2>Qualità, dal campo<br><em>al mercato.</em></h2><p>Pomodori, pomodoro cherry, agrumi, uva da tavola, patate, carote e orticoli.<br>Esperienza nella produzione in serra e in campo aperto.</p>{link("/prodotti","Scopri i prodotti","button light")}</div></section>'+certification()
# Original company video stays opt-in: no third-party iframe is loaded before the click.
original=BeautifulSoup((ROOT/'research/chi-siamo.html').read_text(encoding='utf8'),'html.parser');iframe=original.select_one('iframe')
if iframe:
 about+=f'<section class="wrap video-section reveal"><span class="eyebrow">GUARDA DA VICINO</span><h2>Dentro il mondo <em>La Zagara.</em></h2><a class="button green" href="{esc(iframe.get("src",""))}" target="_blank" rel="noopener">Guarda il video aziendale ↗</a></section>'
write('/chi-siamo','Chi siamo',about)

def soup_for(path):return BeautifulSoup((ROOT/'research'/((path.strip('/').replace('/','__') or 'home')+'.html')).read_text(encoding='utf8'),'html.parser')
def clean(text):return re.sub(r'\s+',' ',text).strip()
def source_intro(path):
 s=soup_for(path);first=s.select_one('#sp-main-body .sppb-section .sppb-addon-text-block .sppb-addon-content')
 if not first:return ''
 for n in first.select('h2,h4,ul'):n.decompose()
 return clean(first.get_text(' ',strip=True))
def variety_cards(path):
 s=soup_for(path);cards=[];seen=set()
 for sec in s.select('#sp-main-body .page-content > section'):
  pics=sec.select('.sppb-addon-single-image img');h=sec.select_one('h3.sppb-addon-title')
  if not pics or not h:continue
  title=clean(h.get_text(' ',strip=True));img=urljoin(BASE,pics[0].get('src',''))
  if 'Scopri le nostre' in title or title in seen:continue
  seen.add(title)
  texts=[]
  for x in sec.select('.sppb-addon-text-block'):
   t=clean(x.get_text(' ',strip=True))
   if t and not t.startswith('#'):texts.append(t.split('#')[0].strip())
  links=[(x.get('href'),clean(x.get_text())) for x in sec.select('a.sppb-btn') if x.get('href','').startswith('/') and not x.get('href').startswith('/images/')]
  cards.append((title,img,' '.join(texts),links))
 return '<div class="variety-grid">'+''.join(f'<article class="variety-card reveal"><div>{image(im,t)}</div><span class="eyebrow">LA ZAGARA · SELEZIONE</span><h3>{t}</h3><p>{desc}</p>{"".join(link(u,l) for u,l in links)}</article>' for t,im,desc,links in cards)+'</div>' if cards else ''
def original_details(path):
 s=soup_for(path);main=s.select_one('#sp-main-body')
 if not main:return ''
 for x in main.select('.sppb-section.sppb-hidden-md.sppb-hidden-lg,script,style'):x.decompose()
 lines=[clean(x) for x in main.get_text('\n',strip=True).splitlines() if clean(x)]
 return '<details class="original-details"><summary>Leggi tutti gli approfondimenti <span>+</span></summary><div>'+''.join('<p>'+esc(x)+'</p>' for x in lines)+'</div></details>'
product_pages={
 '/prodotti/uva-da-tavola':('Uva da tavola','La dolcezza<br>prende <em>forma.</em>','slide-uva-b.jpg'),
 '/prodotti/arance':('Arance','Tutto il sole.<br><em>Tutto il carattere.</em>','sicilia.jpg'),
 '/prodotti/limoni':('Limoni','L’essenza più<br><em>luminosa.</em>','slide-limoni.jpg'),
 '/prodotti/pomodori':('Pomodori','Un piccolo frutto.<br><em>Un grande sapore.</em>','slide-pom-n2.jpg'),
 '/arance-tarocco':('Arance Tarocco','Il cuore rosso<br><em>della Sicilia.</em>','sicilia.jpg'),
 '/varieta-innovative':('Varietà esclusive','La natura incontra<br><em>l’innovazione.</em>','slide-uva-b.jpg'),
 '/varieta-standard':('Varietà standard','Il piacere dei<br><em>grandi classici.</em>','slide-uva-b.jpg'),
 '/varieta-innovative-snfl':('S.N.F.L.','Nuove varietà.<br><em>Nuove emozioni.</em>','slide-uva-b.jpg'),
 '/varieta-innovative-ifg':('International Fruit Genetics™','Senza semi.<br><em>Con carattere.</em>','slide-uva-b.jpg')}
for path,(name,title,im) in product_pages.items():
 body=f'<section class="product-hero">{image(im,name,"hero-bg",True)}<div class="hero-shade"></div><div><a class="eyebrow" href="/prodotti">← I NOSTRI PRODOTTI</a><h1>{title}</h1><span class="product-hero-name">{name}</span></div></section>'
 body+=f'<section class="product-intro wrap"><div class="reveal"><span class="eyebrow">NATURALMENTE LA ZAGARA</span><h2>{name}</h2></div><div class="reveal"><p>{source_intro(path)}</p>{link("/contatti","Richiedi informazioni","button green")}</div></section>'
 body+='<section class="wrap varieties"><div class="section-heading reveal"><span class="eyebrow">IL GUSTO DI SCEGLIERE</span><h2>Scopri le nostre <em>varietà.</em></h2></div>'+variety_cards(path)
 if path=='/varieta-standard':
  body+='<div class="variety-mini-grid">'
  s=soup_for(path)
  for feature in s.select('.white-popup-block .col-sm'):
   h=feature.select_one('strong');imn=feature.select_one('img')
   if h and imn:
    title=clean(h.get_text());desc=clean(feature.get_text(' ',strip=True));desc=desc.removeprefix(title).strip()
    body+=f'<article class="reveal">{image(urljoin(BASE,imn["src"]),title)}<h3>{title}</h3><p>{desc}</p></article>'
  body+='</div>'
 body+=original_details(path)+'</section>'+certification()
 pdf='Calendario_uva.pdf' if 'uva' in path or 'varieta' in path else 'Calendario_prodotti.pdf'
 body+=f'<section class="calendar wrap reveal"><span class="eyebrow">OGNI FRUTTO, IL SUO MOMENTO</span><h2>Il ritmo delle <em>stagioni.</em></h2><p>Consulta il calendario di La Zagara per scoprire la stagionalità dei prodotti.</p>{link("/assets/"+pdf,"Apri il calendario PDF","button green")}</section>'
 write(path,name,body)
write('/news','News',intro('STORIE, RACCOLTI E INNOVAZIONE','Notizie dalla<br><em>nostra terra.</em>','L’archivio delle notizie e delle interviste di La Zagara.')+'<section class="wrap news-section">'+news_grid()+'</section>')
for path,t,date,im,desc in news:
 s=soup_for(path);main=s.select_one('#sp-main-body');article=main.select_one('[itemprop="articleBody"]') or main
 for x in article.select('script,style'):x.decompose()
 paragraphs=article.select('p');text=''.join(f'<p>{esc(clean(x.get_text(" ",strip=True)).replace("/p>",""))}</p>' for x in paragraphs if clean(x.get_text()))
 if not text:text=''.join(f'<p>{esc(x)}</p>' for x in pages[path]['text'].split('\n')[4:])
 sources=[x for x in main.select('a[href]') if x.get('href','').startswith('http') and 'zagara.com' not in x.get('href','')]
 source_links=''.join(f'<a href="{esc(x["href"])}" rel="noopener" target="_blank">{esc(x.get_text())} ↗</a>' for x in sources)
 write(path,t,intro(date+' · ARCHIVIO NEWS',t)+f'<div class="article-cover wrap">{image(im,t)}</div><article class="article-body">{text}<div class="article-source">Fonte originale: {source_links}</div>{link("/news","Torna alle news")}</article>')

gallery=pages['/gallery']['images'];gallery_body=intro('UNO SGUARDO DA VICINO','La nostra terra.<br><em>Il nostro mondo.</em>','Tra i filari, nei campi e dove ci prendiamo cura di ogni raccolto. Le fotografie originali di La Zagara.')
gallery_body+='<section class="gallery-grid wrap">'+''.join(f'<button class="gallery-item reveal" data-gallery="{asset(im)}" data-caption="La Zagara · Foto {i+1} di {len(gallery)}" aria-label="Ingrandisci foto {i+1}">{image(im,f"La Zagara, foto aziendale {i+1}")}<span>ESPLORA ↗</span></button>' for i,im in enumerate(gallery))+'</section>'
write('/gallery','Gallery',gallery_body)
contact=intro('SIAMO QUI PER TE','Le buone relazioni<br>si <em>coltivano.</em>','Informazioni sui prodotti, disponibilità e collaborazioni. Iniziamo a parlarne.')
contact+=f'''<section class="contact-layout wrap"><div class="contact-info reveal"><span class="eyebrow">LA ZAGARA · GIOVANNI GRASSO S.R.L.</span><h2>Dalla Sicilia,<br><em>sempre in contatto.</em></h2><a class="big-link" href="mailto:info@zagara.com">info@zagara.com ↗</a><a class="big-link" href="tel:+390957762652">+39 095 776 26 52</a><div class="contact-address"><h3>Vieni a trovarci</h3><p>C.da Vignagrande s.n.<br>95013 Fiumefreddo di Sicilia (CT)<br>Italia</p><p>Lunedì — Sabato: 8:00 — 20:00<br>Fax: +39 095 64 24 96<br>P.IVA 03257040877</p><a class="text-link" href="https://www.google.com/maps/search/?api=1&query=La+Zagara+Giovanni+Grasso+Fiumefreddo+di+Sicilia" target="_blank" rel="noopener">Apri le indicazioni ↗</a></div></div><form class="contact-form reveal"><span class="eyebrow">SCRIVICI DUE RIGHE</span><div class="form-row"><label>Nome e cognome<input name="name" autocomplete="name" required placeholder="Come ti chiami?"></label><label>Email<input type="email" name="email" required autocomplete="email" placeholder="La tua email"></label></div><label>Azienda <small>(facoltativo)</small><input name="company" autocomplete="organization" placeholder="La tua azienda"></label><label>Di cosa vuoi parlare?<select name="subject"><option>Informazioni sui prodotti</option><option>Uva da tavola</option><option>Arance</option><option>Limoni</option><option>Pomodori</option><option>Collaborazioni commerciali</option><option>Altro</option></select></label><label>Il tuo messaggio<textarea name="message" rows="5" required placeholder="Raccontaci la tua richiesta…"></textarea></label><label class="check"><input type="checkbox" required> <span>Ho letto l’<a href="/privacy">informativa privacy</a> e accetto il trattamento dei dati per la risposta alla richiesta.</span></label><button class="button green" type="submit">Prepara la tua email ↗</button><small>Si aprirà il tuo programma di posta. Il messaggio verrà inviato solo dopo la tua conferma nell’app email.</small><p class="form-status" role="status"></p></form></section>'''
write('/contatti','Contatti',contact)
privacy=intro('TRASPARENZA E INFORMAZIONI','Privacy <em>& Cookie.</em>')
privacy+='''<section class="article-body"><h2>Informazioni su questa versione del sito</h2><p>Questa versione presenta i contenuti pubblici di La Zagara. I moduli di contatto e newsletter preparano una email nel programma di posta del visitatore: non salvano né inviano dati attraverso un database di questo sito. L’invio avviene quando il visitatore lo conferma nel proprio programma di posta.</p><p>Le fotografie e i caratteri sono ospitati localmente. Non sono integrati strumenti di analisi, pubblicità o profilazione. Video, mappe e fonti esterne si aprono soltanto tramite un collegamento scelto dal visitatore e applicano le rispettive informative. La piattaforma di hosting può trattare i dati tecnici necessari a erogare il servizio.</p><h2>Contatti del titolare indicato nel sito originale</h2><p>Giovanni Grasso S.r.l., C.da Vignagrande s.n., 95013 Fiumefreddo di Sicilia (CT). Email: <a href="mailto:info@zagara.com">info@zagara.com</a>. Telefono: +39 095 776 26 52.</p><p>L’informativa originale è riportata di seguito per conservare le informazioni della fonte. Descrive anche servizi del sito originale che non sono attivi in questa versione.</p>'''+original_details('/privacy')+'</section>'
write('/privacy','Privacy e Cookie',privacy)
write('/blog-news','Archivio news',intro('DAL NOSTRO MONDO','Storie di <em>La Zagara.</em>')+'<section class="wrap news-section">'+news_grid()+'</section>')
write('/404','Pagina non trovata',intro('404','Questa strada<br>torna <em>alla terra.</em>','La pagina richiesta non è disponibile.')+'<section class="wrap error-page">'+link('/','Torna alla homepage','button green')+'</section>')
(DIST/'404.html').write_text((DIST/'404/index.html').read_text(encoding='utf8'),encoding='utf8')
# Fonts are bundled locally to keep the presentation self-contained.
for name,family in [('display','Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500'),('sans','Manrope:wght@400;500;600;700')]:
 try:
  css=urlopen(Request('https://fonts.googleapis.com/css2?family='+family+'&display=swap',headers={'User-Agent':'Mozilla/5.0'})).read().decode()
  urls=list(dict.fromkeys(re.findall(r'url\((https://[^)]+)\)',css)))
  for i,url in enumerate(urls):
   ext='woff2' if '.woff2' in url else 'ttf';fname=f'/assets/{name}-{i}.{ext}';(DIST/fname.lstrip('/')).write_bytes(urlopen(url).read());css=css.replace(url,fname)
  (DIST/f'{name}-fonts.css').write_text(css,encoding='utf8')
 except Exception as e: print('Font fallback:',e)
(DIST/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://la-zagara-sicilia.info861460.chatgpt.site/sitemap.xml\n')
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>https://la-zagara-sicilia.info861460.chatgpt.site'+p+'</loc></url>' for p in pages)+'</urlset>')
print('Generated',len(list(DIST.rglob('index.html'))),'pages')
