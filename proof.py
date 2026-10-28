from PIL import Image,ImageDraw
from pathlib import Path
import json
a=json.loads(Path('research/assets.json').read_text())
names=['slide-uva-b.jpg','slide-arance6.jpg','slide-limoni.jpg','slide-pom-n2.jpg','sicilia.jpg','chisiamo-n.jpg','logo-la-zagara.png','uvac.jpg','agrumic.jpg','limoni-n.jpg','pomodori-n2.jpg','chisiamo1d.jpg']
sheet=Image.new('RGB',(1000,900),'white');draw=ImageDraw.Draw(sheet)
for i,n in enumerate(names):
 v=next((v for u,v in a.items() if v and u.endswith('/'+n)),None)
 if not v:continue
 im=Image.open('dist'+v).convert('RGB');print(n,im.size);im.thumbnail((320,190))
 x=i%3*333;y=i//3*225;sheet.paste(im,(x,y));draw.text((x,y+195),n,fill='black')
sheet.save('research/contact.jpg')
