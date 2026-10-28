# La Zagara — nuova esperienza web

Sito multipagina in HTML, CSS e JavaScript, con generatore Python. Foto, logo, contenuti, articoli e calendari provengono da https://www.zagara.com/.

Direzione: editoriale mediterranea, verde bosco e avorio, accenti arancio, Cormorant Garamond e Manrope. Elemento distintivo: slideshow fotografico a tutta altezza con tipografia monumentale e sigillo animato.

## Sviluppo

`python collect.py` acquisisce la fonte e conserva i documenti in `research/` (non pubblicata). Richiede BeautifulSoup e Pillow.

`python generate.py` rigenera le pagine statiche in `dist/`. Non sono necessarie dipendenze JavaScript o build frontend.

`python -m http.server 4173 --bind 127.0.0.1 --directory dist` avvia l'anteprima.

I moduli di contatto e newsletter preparano una email nel programma di posta; non eseguono invii automatici né salvano iscrizioni. Le schede mantengono i contenuti originali anche in un approfondimento espandibile. Le notizie mantengono le date storiche. L'informativa distingue questa versione dai servizi del sito originario.

Lo slideshow supporta pausa, frecce, touch e tastiera; la gallery supporta dialog modale e tastiera. Il movimento ridotto viene rispettato. Le immagini sono locali, convertite in WebP, con caricamento differito sotto la prima schermata. I font sono locali.
