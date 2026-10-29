from pathlib import Path
from bs4 import BeautifulSoup
import base64,shutil
R=Path(__file__).parent;D=R/'dist'
shutil.copyfile(R/'design/client-logo.png',D/'assets/zagara-client-logo.png')
image=base64.b64encode((R/'design/client-logo.png').read_bytes()).decode()
petals='''<g fill="#fffdf6"><path d="M777 475Q685 421 759 307Q811 364 793 427Z"/><path d="M777 475Q819 373 911 392Q871 466 777 475Z"/><path d="M777 475Q858 487 871 583Q810 568 777 475Z"/><path d="M777 475Q737 552 613 568Q670 504 777 475Z"/><path d="M777 475Q682 516 613 466Q683 394 777 475Z"/></g>'''
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="170 130 1200 785"><defs><filter id="cut" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 -1 -1 -1 0 3"/><feComponentTransfer><feFuncA type="discrete" tableValues="0 0 1 1 1 1 1 1"/></feComponentTransfer></filter></defs>{petals}<image width="1536" height="1024" href="data:image/png;base64,{image}" filter="url(#cut)"/></svg>'''
(D/'assets/zagara-cutout.svg').write_text(svg,encoding='utf8')
favicon='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 110 105"><path d="M7 13C32 15 49-7 64 20L70 28L30 76C49 72 59 95 80 88C57 108 30 77 8 88L62 24C43 15 29 31 7 13Z" fill="#173c2b"/><path d="M63 34Q72 12 89 15Q81 31 63 34" fill="#173c2b"/><path d="M68 35C94 37 96 64 76 77L61 62L78 49Q66 46 58 55Z" fill="#f58220"/><g fill="#fffdf6"><path d="M58 62Q45 42 55 31Q66 47 58 62"/><path d="M58 62Q69 42 84 48Q75 64 58 62"/><path d="M58 62Q77 64 76 80Q62 77 58 62"/><path d="M58 62Q52 81 37 77Q41 65 58 62"/><path d="M58 62Q41 66 32 56Q48 47 58 62"/></g><g fill="#dda42a"><circle cx="58" cy="60" r="3"/><circle cx="54" cy="49" r="2"/><circle cx="65" cy="53" r="2"/></g><g fill="#831c50"><circle cx="90" cy="38" r="6"/><circle cx="103" cy="35" r="6"/><circle cx="89" cy="51" r="5"/><circle cx="100" cy="48" r="5"/><circle cx="96" cy="61" r="5"/></g><path d="M85 28Q92 13 108 21Q99 30 85 28" fill="#173c2b"/><circle cx="89" cy="82" r="14" fill="#bd3022"/><path d="M89 65l3 6 6-1-4 5 3 5-7-2-5 5 1-7-7-3 7-2Z" fill="#173c2b" stroke="#fffdf6" stroke-width="1.5"/></svg>'''
(D/'assets/zagara-symbol.svg').write_text(favicon,encoding='utf8')
for f in D.rglob('*.html'):
 s=BeautifulSoup(f.read_text(encoding='utf8'),'html.parser')
 for im in s.select('.brand img,.footer-about img'):im['src']='/assets/zagara-cutout.svg?v=3';im['alt']='La Zagara — Fiumefreddo di Sicilia'
 for link in s.select('link[rel=icon]'):link['href']='/assets/zagara-symbol.svg?v=3'
 f.write_text(str(s),encoding='utf8')
print('Updated supplied logo and fruit symbol favicon')
