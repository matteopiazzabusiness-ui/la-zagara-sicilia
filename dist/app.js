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

// Cinema scroll: movement follows the viewport and respects reduced motion.
(()=>{const media=matchMedia('(prefers-reduced-motion: reduce)');const scenes=[...document.querySelectorAll('.cinema-scene')];let pending=false;function draw(){if(!media.matches)scenes.forEach(s=>{const r=s.getBoundingClientRect();if(r.bottom>0&&r.top<innerHeight)s.querySelector('.cinema-photo').style.transform=`translateY(${(r.top+r.height/2-innerHeight/2)*-.12}px)`});pending=false}addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(draw)}},{passive:true});draw()})();
