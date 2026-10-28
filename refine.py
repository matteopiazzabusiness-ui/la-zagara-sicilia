from pathlib import Path
p=Path('generate.py');s=p.read_text(encoding='utf8')
s=s.replace('I riferimenti di qualità<br>presentati da La Zagara.','La qualità prende forma.<br>In ogni fase del nostro lavoro.')
s=s.replace('Ho letto l’<a href="/privacy">informativa privacy</a> e accetto il trattamento dei dati per la risposta alla richiesta.','<span>Ho letto l’<a href="/privacy">informativa privacy</a> e accetto il trattamento dei dati per la risposta alla richiesta.</span>')
p.write_text(s,encoding='utf8')
