from pathlib import Path
import shutil,re,os
R=Path(__file__).parent
target=R/'_site'
target.mkdir(exist_ok=True)
shutil.copytree(R/'dist',target,dirs_exist_ok=True)
repo=os.environ.get('GITHUB_REPOSITORY','matteopiazzabusiness-ui/la-zagara-sicilia')
owner,name=repo.split('/')
prefix='/'+name+'/'
origin='https://'+owner+'.github.io'+prefix.rstrip('/')
for file in target.rglob('*'):
 if file.suffix not in ['.html','.css','.js','.xml','.txt']:continue
 text=file.read_text(encoding='utf8')
 text=text.replace('https://la-zagara-sicilia.info861460.chatgpt.site',origin)
 if file.suffix=='.html':
  text=re.sub(r'''((?:href|src|poster)=["'])/(?!/)''',lambda m:m[1]+prefix,text)
 if file.suffix=='.css':
  text=re.sub(r'''(url\(["']?)/(?!/)''',lambda m:m[1]+prefix,text)
 file.write_text(text,encoding='utf8')
(target/'.nojekyll').touch()
print('Client website:',origin+'/')
