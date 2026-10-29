# La Zagara — nuova esperienza web

## Home video e sezioni indipendenti

Eseguire `python home-scenes.py` per ultimo: porta il loop muto nella hero Home e sostituisce il carosello sticky con quattro sezioni prodotto indipendenti, animate all'ingresso nel viewport. Nessuna intercettazione della rotella. Il logo originale viene composto in SVG con fondo trasparente e fiore opaco; la favicon è un SVG leggero contenente soltanto il simbolo. Le versioni ImageGen sperimentali non sono utilizzate nel sito.

## Loop video hero Azienda

Montaggio locale H.264 1280×720 di 18 secondi, senza traccia audio, con tre clip Mixkit Stock Video Free License. Le fonti sono elencate in `design/video-sources.json` e nella pagina `/crediti-video/`. Le riprese sono illustrative e non documentano l'azienda.

Per ricrearlo: `python make-loop.py` (richiede FFmpeg e accesso alle fonti), quindi `python autoplay-hero.py` dopo gli altri script di generazione. Il file pronto `dist/assets/zagara-hero-loop.mp4` è incluso. La hero usa video HTML nativo con autoplay, muted, loop, playsinline e object-fit: cover. Include pausa/ripresa, copertina di riserva e rispetto del movimento ridotto. Non viene richiesto YouTube per lo sfondo della hero; i filmati on-demand nelle altre sezioni rimangono disponibili.

## Hero guidate dallo scroll

Dopo gli altri script eseguire `python scroll-hero.py`: la homepage usa una sequenza sticky a quattro scene che segue lo scorrimento verticale senza intercettare o bloccare la rotella. Frecce manuali e tastiera rimangono disponibili. Con movimento ridotto si usa una hero statica con selezione manuale. La pagina Azienda include il video aziendale direttamente nella hero, su clic, con chiusura e rimozione del lettore.

## Interazioni e filmati

Eseguire `python interactive.py` dopo `python cinematic.py` per includere schede prodotto a tab accessibili da tastiera, ricerca delle varietà, hero aggiuntivi e video su richiesta. Il lettore YouTube viene creato soltanto al clic e rimosso alla chiusura. Sono presenti collegamenti alternativi a YouTube.

Fonti: video aziendale incorporato da https://www.zagara.com/chi-siamo (`mFyPQzjpzbE`) e “Scent of Zagara”, racconto del territorio pubblicato da https://www.distrettoagrumidisicilia.it/video/ (`KPuC0XRiXWo`). Il secondo filmato non è presentato come produzione aziendale La Zagara. I filmati rimangono sui player dei titolari, senza download o ripubblicazione dei file.

## Edizione cinematografica

Il logo fornito dal cliente è conservato integro in `design/client-logo.png` e distribuito in `dist/assets/zagara-client-logo.png`. Dopo la pipeline di generazione eseguire anche `python cinematic.py` e `python validate.py`. Il sito pronto è già incluso in `dist/`.

La homepage aggiunge capitoli narrativi su territorio, atlante delle varietà, cura e stagionalità. Le scene fotografiche seguono lo scorrimento con movimento ridotto rispettato. Le pagine interne aggiungono approfondimenti coerenti con la loro funzione.

## Edizione pubblica per il cliente

Identità aggiornata con logo vettoriale in `dist/assets/zagara-modern.svg`: fiore geometrico, cuore agrume e wordmark essenziale. Approfondimenti dedicati alle pagine principali e alle schede prodotto; FAQ nella pagina Contatti.

Per rigenerare l'edizione completa eseguire in ordine `python generate.py`, `python enrich.py`, `python deepen.py`, `python validate.py`. Gli script di arricchimento conservano le informazioni della fonte senza introdurre dati commerciali non verificati.

Sito multipagina in HTML, CSS e JavaScript, con generatore Python. Foto, logo, contenuti, articoli e calendari provengono da https://www.zagara.com/.

Direzione: editoriale mediterranea, verde bosco e avorio, accenti arancio, Cormorant Garamond e Manrope. Elemento distintivo: slideshow fotografico a tutta altezza con tipografia monumentale e sigillo animato.

## Sviluppo

`python collect.py` acquisisce la fonte e conserva i documenti in `research/` (non pubblicata). Richiede BeautifulSoup e Pillow.

`python generate.py` rigenera le pagine statiche in `dist/`. Non sono necessarie dipendenze JavaScript o build frontend.

`python -m http.server 4173 --bind 127.0.0.1 --directory dist` avvia l'anteprima.

I moduli di contatto e newsletter preparano una email nel programma di posta; non eseguono invii automatici né salvano iscrizioni. Le schede mantengono i contenuti originali anche in un approfondimento espandibile. Le notizie mantengono le date storiche. L'informativa distingue questa versione dai servizi del sito originario.

Lo slideshow supporta pausa, frecce, touch e tastiera; la gallery supporta dialog modale e tastiera. Il movimento ridotto viene rispettato. Le immagini sono locali, convertite in WebP, con caricamento differito sotto la prima schermata. I font sono locali.
