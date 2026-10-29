from pathlib import Path
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
import json,re,subprocess
R=Path(__file__).parent;work=R/'research/stock-video';work.mkdir(parents=True,exist_ok=True)
slugs=['many-half-oranges-in-a-close-shot-42942','presentation-of-many-fruits-and-vegetables-10421','serving-juice-in-a-glass-with-some-oranges-on-a-10428']
sources=[]
for slug in slugs:
 url='https://mixkit.co/free-stock-video/'+slug+'/'
 raw=urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'})).read().decode()
 text=BeautifulSoup(raw,'html.parser').get_text(' ',strip=True)
 assert 'commercial or personal use' in text and 'Stock Video Free License' in text,'License verification failed: '+url
 (work/(slug+'.html')).write_text(raw,encoding='utf8')
 id=slug.split('-')[-1];media=re.search(r'https://assets\.mixkit\.co/videos/'+id+r'/'+id+r'-720\.mp4',raw).group()
 target=work/(id+'.mp4')
 if not target.exists():target.write_bytes(urlopen(Request(media,headers={'User-Agent':'Mozilla/5.0'})).read())
 sources.append({'title':slug,'page':url,'media':media,'license':'Mixkit Stock Video Free License','license_url':'https://mixkit.co/license/#videoFree'})
 subprocess.run(['ffmpeg','-y','-i',str(target),'-t','6.5','-an','-vf','scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=25,setsar=1','-c:v','libx264','-preset','fast','-crf','21',str(work/(id+'-cut.mp4'))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
cmd=['ffmpeg','-y']
for slug in slugs:cmd+=['-i',str(work/(slug.split('-')[-1]+'-cut.mp4'))]
cmd+=['-i',str(work/'42942-cut.mp4')]
cmd+=['-filter_complex','[0:v][1:v]xfade=transition=fade:duration=0.5:offset=6[v1];[v1][2:v]xfade=transition=fade:duration=0.5:offset=12[v2];[v2][3:v]xfade=transition=fade:duration=0.5:offset=18[v3];[v3]trim=start=0.5:end=18.5,setpts=PTS-STARTPTS,eq=saturation=0.90:brightness=-0.035[v]','-map','[v]','-an','-c:v','libx264','-pix_fmt','yuv420p','-preset','fast','-crf','23','-movflags','+faststart',str(R/'dist/assets/zagara-hero-loop.mp4')]
subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
(R/'design/video-sources.json').write_text(json.dumps(sources,indent=2),encoding='utf8')
subprocess.run(['ffmpeg','-y','-i',str(R/'dist/assets/zagara-hero-loop.mp4'),'-frames:v','1',str(R/'dist/assets/zagara-loop-poster.jpg')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print('Rendered 18-second seamless montage with licensed footage')
