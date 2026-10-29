from pathlib import Path
p=Path(__file__).parent/'dist/interactive.js'
s=p.read_text(encoding='utf8')
s=s.replace("dialog.querySelector('.video-close').addEventListener('click',()=>dialog.close());","dialog.querySelector('.video-close').addEventListener('click',()=>{dialog.querySelector('.video-frame').replaceChildren();dialog.close()});dialog.addEventListener('cancel',()=>dialog.querySelector('.video-frame').replaceChildren());")
p.write_text(s,encoding='utf8')
