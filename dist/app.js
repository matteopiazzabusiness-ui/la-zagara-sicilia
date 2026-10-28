(() => {
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const $ = (s, root=document) => root.querySelector(s);
  const $$ = (s, root=document) => [...root.querySelectorAll(s)];
  if (!reduced.matches && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('js-motion');
    const observer = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); }
    }), {threshold:0.08});
    $$('.reveal').forEach(e => observer.observe(e));
  }
  const menu = $('.menu-toggle');
  menu?.addEventListener('click', () => {
    const open = document.body.classList.toggle('menu-open');
    menu.setAttribute('aria-expanded',String(open));
    menu.setAttribute('aria-label', open?'Chiudi menu':'Apri menu');
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {document.body.classList.remove('menu-open');menu?.setAttribute('aria-expanded','false');menu?.setAttribute('aria-label','Apri menu');}
    if (e.key === 'Tab' && document.body.classList.contains('menu-open')) {
      const focusables = [...$$('.site-header nav a'),menu];
      const first = focusables[0],last = focusables.at(-1);
      if (e.shiftKey && document.activeElement===first) {e.preventDefault();last.focus();}
      else if (!e.shiftKey && document.activeElement===last) {e.preventDefault();first.focus();}
    }
  });
  let scrollPending = false;
  function updateScroll() {
    const y = window.scrollY;
    $('.site-header')?.classList.toggle('scrolled',y>40);
    const max = document.documentElement.scrollHeight-innerHeight;
    $('.read-progress').style.width=(max>0?y/max*100:0)+'%';
    if (!reduced.matches) $$('.parallax-image').forEach(img=>{
      const rect=img.parentElement.getBoundingClientRect();
      if(rect.bottom>0 && rect.top<innerHeight) img.style.transform=`translateY(${(rect.top+rect.height/2-innerHeight/2)*-.10}px)`;
    });
    scrollPending=false;
  }
  addEventListener('scroll',()=>{if(!scrollPending){scrollPending=true;requestAnimationFrame(updateScroll);}},{passive:true});
  updateScroll();
  // Progressive page transitions retain normal link behavior for downloads, external URLs and modified clicks.
  document.addEventListener('click',e=>{
    const a=e.target.closest('a[href]');
    if(!a || e.defaultPrevented || e.button!==0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.target || a.hasAttribute('download') || reduced.matches)return;
    const url=new URL(a.href,location.href);
    if(url.origin!==location.origin || /\.(pdf|png|jpg|jpeg|webp)$/i.test(url.pathname) || (url.pathname===location.pathname && url.hash))return;
    if(url.protocol!=='http:' && url.protocol!=='https:')return;
    e.preventDefault();$('.page-transition')?.classList.add('leaving');
    setTimeout(()=>{location.href=url.href;},420);
  });
  addEventListener('pageshow',()=>$('.page-transition')?.classList.remove('leaving'));
  const slides=$$('.hero-slide');
  if(slides.length){
    let current=0,paused=reduced.matches,timer=null,started=performance.now(),elapsed=0;
    const duration=7500,progress=$('.slide-progress span'),pauseButton=$('.slide-pause');
    function setSlide(i){
      current=(i+slides.length)%slides.length;
      slides.forEach((s,j)=>{s.classList.toggle('active',j===current);s.setAttribute('aria-hidden',String(j!==current));s.inert=j!==current;});
      $('.slide-count').innerHTML=String(current+1).padStart(2,'0')+' <small>/ '+String(slides.length).padStart(2,'0')+'</small>';
      elapsed=0;started=performance.now();progress.style.width='0%';
    }
    function animate(now){
      if(!paused && !document.hidden){elapsed+=now-started;progress.style.width=Math.min(100,elapsed/duration*100)+'%';if(elapsed>=duration)setSlide(current+1);}
      started=now;timer=requestAnimationFrame(animate);
    }
    $('.slide-prev').addEventListener('click',()=>setSlide(current-1));
    $('.slide-next').addEventListener('click',()=>setSlide(current+1));
    function pause(){paused=!paused;pauseButton.textContent=paused?'▶':'Ⅱ';pauseButton.setAttribute('aria-label',paused?'Avvia slideshow':'Metti in pausa slideshow');}
    pauseButton.addEventListener('click',pause);
    $('.hero').addEventListener('focusin',()=>{if(!paused){paused=true;pauseButton.textContent='▶';pauseButton.setAttribute('aria-label','Avvia slideshow');}});
    $('.hero').addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();setSlide(current+1);}if(e.key==='ArrowLeft'){e.preventDefault();setSlide(current-1);}});
    let startX=0;
    $('.hero').addEventListener('touchstart',e=>{startX=e.changedTouches[0].clientX;},{passive:true});
    $('.hero').addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-startX;if(Math.abs(dx)>65)setSlide(current+(dx<0?1:-1));},{passive:true});
    document.addEventListener('visibilitychange',()=>{started=performance.now();});
    setSlide(0);pauseButton.textContent=paused?'▶':'Ⅱ';pauseButton.setAttribute('aria-label',paused?'Avvia slideshow':'Metti in pausa slideshow');timer=requestAnimationFrame(animate);
  }
  const gallery=$$('.gallery-item'),dialog=$('#lightbox');let galleryIndex=0,lastFocus;
  function showImage(i){galleryIndex=(i+gallery.length)%gallery.length;const b=gallery[galleryIndex],im=$('figure img',dialog);im.src=b.dataset.gallery;im.alt=$('img',b).alt;$('figcaption',dialog).textContent=b.dataset.caption;}
  gallery.forEach((b,i)=>b.addEventListener('click',()=>{lastFocus=b;showImage(i);dialog.showModal();document.body.style.overflow='hidden';$('.lightbox-close').focus();}));
  $('.lightbox-close')?.addEventListener('click',()=>dialog.close());
  $('.lightbox-prev')?.addEventListener('click',()=>showImage(galleryIndex-1));
  $('.lightbox-next')?.addEventListener('click',()=>showImage(galleryIndex+1));
  dialog?.addEventListener('close',()=>{document.body.style.overflow='';lastFocus?.focus();});
  dialog?.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
  dialog?.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();showImage(galleryIndex+1);}if(e.key==='ArrowLeft'){e.preventDefault();showImage(galleryIndex-1);}});
  $('.contact-form')?.addEventListener('submit',e=>{
    e.preventDefault();const f=e.currentTarget;if(!f.reportValidity())return;const d=new FormData(f);
    const subject='La Zagara — '+d.get('subject');
    const body=`Nome: ${d.get('name')}\nEmail: ${d.get('email')}\nAzienda: ${d.get('company')||'—'}\n\n${d.get('message')}\n\nHo letto l’informativa privacy e richiedo una risposta alla mia richiesta.`;
    const href='mailto:info@zagara.com?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
    location.href=href;
    const status=$('.form-status',f);status.textContent='Email preparata. Completa l’invio nel tuo programma di posta. Se non si apre, scrivi a info@zagara.com.';
    const retry=document.createElement('a');retry.href=href;retry.textContent='Riapri l’email preparata ↗';retry.className='text-link';status.append(document.createElement('br'),retry);
  });
  $('.newsletter-form')?.addEventListener('submit',e=>{
    e.preventDefault();const f=e.currentTarget;if(!f.reportValidity())return;
    location.href='mailto:info@zagara.com?subject='+encodeURIComponent('Richiesta iscrizione newsletter La Zagara')+'&body='+encodeURIComponent(`Vorrei richiedere l’iscrizione alla newsletter con l’indirizzo: ${new FormData(f).get('email')}.\nHo letto l’informativa privacy.`);
    $('.form-status',f).textContent='Richiesta preparata: completa l’invio nel tuo programma di posta.';
  });
})();
