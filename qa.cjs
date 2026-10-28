const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright-core');
const fs=require('fs');
(async()=>{
 const browser=await chromium.launch({headless:true});
 const ctx=await browser.newContext({viewport:{width:1440,height:1000}});
 const page=await ctx.newPage();const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400)errors.push(r.status()+' '+r.url());});
 await page.goto('http://127.0.0.1:8765/',{waitUntil:'networkidle'});
 await page.screenshot({path:'research/home-desktop.png'});
 await page.getByRole('button',{name:'Slide successiva',exact:true}).click();
 if(!await page.locator('.hero-slide.active').textContent().then(x=>x.includes('Il sole')))throw Error('Slide next failed');
 await page.getByRole('button',{name:'Slide precedente',exact:true}).click();
 if(!await page.locator('.hero-slide.active').textContent().then(x=>x.includes('La Sicilia')))throw Error('Slide previous failed');
 await page.emulateMedia({reducedMotion:'reduce'});await page.reload({waitUntil:'networkidle'});
 await page.screenshot({path:'research/home-full.png',fullPage:true});
 await page.goto('http://127.0.0.1:8765/gallery/',{waitUntil:'networkidle'});
 if(await page.locator('.gallery-item').count()!==37)throw Error('Missing gallery images');
 await page.locator('.gallery-item').first().click();
 if(!await page.locator('#lightbox').isVisible())throw Error('Lightbox failed');
 await page.keyboard.press('ArrowRight');
 if(!await page.locator('#lightbox figcaption').innerText().then(x=>x.includes('Foto 2')))throw Error('Lightbox keyboard navigation failed');
 await page.keyboard.press('Escape');
 if(await page.locator('#lightbox').isVisible())throw Error('Lightbox escape failed');
 await page.goto('http://127.0.0.1:8765/prodotti/arance/',{waitUntil:'networkidle'});
 await page.screenshot({path:'research/arance-desktop.png',fullPage:true});
 const mobile=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,reducedMotion:'reduce'});
 const m=await mobile.newPage();m.on('pageerror',e=>errors.push(e.message));
 const routes=['/','/chi-siamo/','/prodotti/','/prodotti/uva-da-tavola/','/prodotti/arance/','/prodotti/limoni/','/prodotti/pomodori/','/varieta-standard/','/varieta-innovative/','/varieta-innovative-snfl/','/varieta-innovative-ifg/','/arance-tarocco/','/news/','/gallery/','/contatti/','/privacy/', '/blog-news/2-puntiamo-anche-all-uva-senza-semi/'];
 for(const route of routes){
  const res=await m.goto('http://127.0.0.1:8765'+route,{waitUntil:'networkidle'});
  if(res.status()!==200)errors.push('Route '+route+' '+res.status());
  const layout=await m.evaluate(()=>({w:innerWidth,sw:document.documentElement.scrollWidth,broken:[...document.images].filter(i=>i.hasAttribute('src')&&i.complete&&!i.naturalWidth).map(i=>i.src)}));
  if(layout.sw>layout.w+1)errors.push('Overflow '+route+' '+layout.sw);
  if(layout.broken.length)errors.push('Broken images '+route+JSON.stringify(layout.broken));
 }
 await m.goto('http://127.0.0.1:8765/',{waitUntil:'networkidle'});
 for(let y=0;y<await m.evaluate(()=>document.body.scrollHeight);y+=650){await m.evaluate(y=>scrollTo(0,y),y);await m.waitForTimeout(90);}
 await m.evaluate(()=>scrollTo(0,0));await m.waitForTimeout(200);
 await m.screenshot({path:'research/home-mobile.png',fullPage:true});
 for(let i=0;i<4;i++){const overflow=await m.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);if(overflow)errors.push('Slide overflow '+i);await m.getByRole('button',{name:'Slide successiva',exact:true}).click();}
 await m.getByRole('button',{name:'Apri menu',exact:true}).click();
 if(await m.getByRole('button',{name:'Chiudi menu',exact:true}).getAttribute('aria-expanded')!=='true')throw Error('Menu failed');
 await m.screenshot({path:'research/menu-mobile.png'});
 await m.getByRole('navigation').getByRole('link',{name:'Chi siamo',exact:true}).click();
 await m.waitForURL('**/chi-siamo/');
 await m.goto('http://127.0.0.1:8765/contatti/',{waitUntil:'networkidle'});
 await m.screenshot({path:'research/contact-mobile.png',fullPage:true});
 if(await m.locator('.contact-form input[required]').count()<2)throw Error('Missing required fields');
 fs.writeFileSync('research/qa-result.json',JSON.stringify({routes:routes.length,checks:['Slideshow next/previous','Gallery 37 images','Lightbox keyboard navigation and Escape','Mobile menu and navigation','Reduced motion','Mobile overflow','Missing images','Browser console'],errors},null,2));
 console.log(JSON.stringify({checkedRoutes:routes.length,errors}));
 await browser.close();if(errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
