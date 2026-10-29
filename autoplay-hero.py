from pathlib import Path
from bs4 import BeautifulSoup
import json,subprocess
R=Path(__file__).parent;D=R/'dist'
subprocess.run(['ffmpeg','-y','-i',str(D/'assets/zagara-hero-loop.mp4'),'-frames:v','1',str(D/'assets/zagara-loop-poster.webp')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
f=D/'chi-siamo/index.html';s=BeautifulSoup(f.read_text(encoding='utf8'),'html.parser');hero=s.select_one('.company-video-hero')
for el in hero.select('.company-player,.company-play,.company-stop,.company-youtube'):el.decompose()
poster=hero.select_one('.company-poster');poster['src']='/assets/zagara-loop-poster.webp'
v=BeautifulSoup('<video class="company-background-video" autoplay muted loop playsinline preload="auto" poster="/assets/zagara-loop-poster.webp" aria-label="Montaggio illustrativo di agrumi e ortofrutta"><source src="/assets/zagara-hero-loop.mp4" type="video/mp4"></video>','html.parser');hero.insert(1,v)
hero.select_one('.eyebrow').string='LA NATURA IN MOVIMENTO · LA ZAGARA'
copy=hero.select_one('.company-hero-copy');copy.select_one('p').string='La passione per i frutti. La cura per ogni dettaglio.'
copy.append(BeautifulSoup('<a class="button light" href="#azienda-dettagli">Scopri la nostra azienda ↓</a>','html.parser'))
hero.append(BeautifulSoup('<button class="background-video-toggle" aria-label="Metti in pausa il video di sfondo">Ⅱ Pausa</button><a class="stock-credit" href="/crediti-video/">Riprese illustrative · Crediti video</a>','html.parser'))
story=s.select_one('.story')
if story:story['id']='azienda-dettagli'
f.write_text(str(s),encoding='utf8')
js=D/'interactive.js';text=js.read_text(encoding='utf8');text=text.split('// Company hero player:')[0]
text+='''// Self-hosted silent video background.
(()=>{const video=document.querySelector('.company-background-video');if(!video)return;const btn=document.querySelector('.background-video-toggle');const reduced=matchMedia('(prefers-reduced-motion: reduce)');let userPaused=reduced.matches;video.muted=true;video.defaultMuted=true;function sync(){btn.textContent=video.paused?'▶ Riproduci':'Ⅱ Pausa';btn.setAttribute('aria-label',video.paused?'Riproduci il video di sfondo':'Metti in pausa il video di sfondo')}function start(){if(userPaused||document.hidden)return;video.play().then(sync).catch(sync)}btn.addEventListener('click',()=>{userPaused=!video.paused;if(userPaused)video.pause();else start();sync()});video.addEventListener('play',sync);video.addEventListener('pause',sync);if(reduced.matches){video.removeAttribute('autoplay');video.pause()}else start();new IntersectionObserver(entries=>{if(entries[0].isIntersecting)start();else video.pause()},{threshold:.05}).observe(video);document.addEventListener('visibilitychange',()=>{if(document.hidden)video.pause();else if(video.getBoundingClientRect().bottom>0)start()});reduced.addEventListener('change',()=>{userPaused=reduced.matches;if(userPaused)video.pause();else start();sync()});sync()})();
''';js.write_text(text,encoding='utf8')
p=D/'interactive.css';text=p.read_text(encoding='utf8')
text+='''\n/* Full-bleed self-hosted motion hero */
.company-video-hero{height:100svh;min-height:620px}.company-background-video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0}.company-video-hero .company-video-shade{z-index:1;pointer-events:none;background:linear-gradient(90deg,#102a20bf,#102a2020),linear-gradient(0deg,#102a2070,transparent)}.company-video-hero .company-hero-copy{z-index:2;bottom:19%;visibility:visible}.background-video-toggle{position:absolute;right:35px;bottom:28px;z-index:3;padding:10px 17px;border:1px solid #ffffff70;color:white;background:#102a2060;backdrop-filter:blur(5px);font-size:11px;border-radius:30px}.stock-credit{position:absolute;left:8%;bottom:35px;z-index:3;font-size:9px;letter-spacing:.6px;color:#f7f5edbb}.company-video-hero .company-poster{animation:none}@media(max-width:700px){.company-video-hero{height:calc(100svh - 74px);min-height:610px}.background-video-toggle{right:20px;bottom:22px}.stock-credit{left:6%;bottom:30px;font-size:8px}.company-video-hero .company-hero-copy{bottom:21%}}\n''';p.write_text(text,encoding='utf8')
# Use the existing document shell for a transparent credits page.
source=json.loads((R/'design/video-sources.json').read_text(encoding='utf8'))
credits=BeautifulSoup((D/'privacy/index.html').read_text(encoding='utf8'),'html.parser');credits.title.string='Crediti video | La Zagara';main=credits.select_one('main');main.clear()
main.append(BeautifulSoup('<section class="page-intro"><span class="eyebrow">FONTI E LICENZE</span><h1>Un racconto<br><em>per immagini.</em></h1><p>Il video di sfondo della pagina Azienda è un montaggio illustrativo di 18 secondi realizzato con riprese stock: non documenta gli stabilimenti o i campi di La Zagara.</p></section><section class="article-body"><h2>Riprese e licenza</h2><p>Le clip sono distribuite con Mixkit Stock Video Free License, che consente uso commerciale e personale. Il montaggio è senza audio e usa tre riprese con dissolvenze.</p>'+''.join('<p><a href="'+x['page']+'" target="_blank" rel="noopener">'+x['title'].replace('-',' ').title()+' ↗</a></p>' for x in source)+'<p><a href="https://mixkit.co/license/#videoFree" target="_blank" rel="noopener">Licenza Mixkit Stock Video Free ↗</a></p></section>','html.parser'))
for tag in credits.select('link[rel=canonical],meta[property="og:url"]'):
 if tag.name=='link':tag['href']='https://la-zagara-sicilia.info861460.chatgpt.site/crediti-video/'
 else:tag['content']='https://la-zagara-sicilia.info861460.chatgpt.site/crediti-video/'
(D/'crediti-video').mkdir(exist_ok=True);(D/'crediti-video/index.html').write_text(str(credits),encoding='utf8')
print('18-second native muted autoplay loop installed with credits')
