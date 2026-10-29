from pathlib import Path
from bs4 import BeautifulSoup
root=Path(__file__).parent
for f in (root/'dist').rglob('index.html'):
 s=BeautifulSoup(f.read_text(encoding='utf8'),'html.parser')
 if s.select_one('.journey'):continue
 target=s.select_one('.catalog') or s.select_one('.varieties')
 if not target:continue
 section=BeautifulSoup('''<section class="journey wrap"><span class="eyebrow">DAL CAMPO ALLE RELAZIONI</span><h2>Ogni frutto racconta<br><em>un percorso di cura.</em></h2><div class="journey-grid"><article><span>01 / ORIGINE</span><h3>La terra, al centro.</h3><p>Produzioni in serra e in campo aperto, metodi tradizionali e attenzione alla genuinità del prodotto.</p></article><article><span>02 / SELEZIONE</span><h3>Il valore della qualità.</h3><p>Controlli attenti, innovazione varietale e cura nella lavorazione: la qualità accompagna ogni fase.</p></article><article><span>03 / DESTINAZIONE</span><h3>Uno sguardo europeo.</h3><p>Produzione e commercializzazione per la grande distribuzione, con attenzione al consumatore e all’ambiente.</p></article></div><a class="text-link" href="/chi-siamo">Conosci la nostra filosofia ↗</a></section>''','html.parser')
 target.insert_after(section)
 if s.select_one('.catalog'):
  controls=BeautifulSoup('''<div class="catalog-guide"><span class="eyebrow">SCEGLI IL TUO PERCORSO</span><div><a href="/prodotti/uva-da-tavola">Uva e varietà esclusive ↗</a><a href="/prodotti/arance">Il mondo degli agrumi ↗</a><a href="/assets/Calendario_prodotti.pdf">Calendario stagionale ↗</a><a href="/contatti">Informazioni commerciali ↗</a></div></div>''','html.parser')
  s.select_one('.catalog').insert(0,controls)
 f.write_text(str(s),encoding='utf8')
p=root/'dist/style.css'
p.write_text(p.read_text(encoding='utf8')+'''\n/* Editorial depth and product discovery */
.catalog-guide{margin-bottom:45px;padding:25px 0;border-bottom:1px solid var(--line)}.catalog-guide>div{display:flex;gap:25px;flex-wrap:wrap;margin-top:17px}.catalog-guide a{font-size:11px;border-bottom:1px solid #173c2b40;padding-bottom:8px}.journey{padding:80px 0 100px;border-top:1px solid var(--line)}.journey h2{margin:25px 0 45px}.journey-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:45px}.journey-grid article{border-top:1px solid var(--line);padding-top:20px}.journey-grid article>span{font-size:9px;letter-spacing:1.5px;color:var(--muted)}.journey-grid h3{font-family:var(--serif);font-size:35px;margin:20px 0 15px}.journey-grid p{font-size:12px;line-height:1.9}.journey>.text-link{margin-top:35px}.product-image{box-shadow:0 18px 35px -25px #102a2060}.product-card{transition:transform .5s}.product-card:hover{transform:translateY(-7px)}.story-photo>img{box-shadow:0 25px 50px -30px #102a2070}.variety-card{padding-bottom:20px;border-bottom:1px solid var(--line)}.hero-seal{box-shadow:0 20px 60px #0003}.product-intro{position:relative}.product-intro:before{content:'LA ZAGARA';position:absolute;right:0;bottom:0;font:80px var(--serif);letter-spacing:6px;color:#173c2b06;pointer-events:none}@media(max-width:700px){.journey{padding:55px 0}.journey-grid{grid-template-columns:1fr;gap:30px}.journey h2{font-size:44px}.catalog-guide>div{gap:15px}.product-intro:before{font-size:43px}}@media(prefers-reduced-motion:reduce){.product-card:hover{transform:none}}
''',encoding='utf8')
