#!/usr/bin/env python3
"""Release gate: static links, locale/SEO contracts, legacy naming and sensitive public copy."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.links=[];self.ids=[];self.meta={};self.canonical=[];self.alternates=[];self.h1=0;self.lang=None;self.visible=[];self.skip=0;self.feed(s)
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='html':self.lang=d.get('lang')
  if 'id' in d:self.ids.append(d['id'])
  if t in ('style','script'):self.skip+=1
  if t=='h1':self.h1+=1
  if t=='meta':self.meta[d.get('name',d.get('property',''))]=d.get('content','')
  if t in ('a','img','video','source','script','link'):
   val=d.get('href',d.get('src'))
   if val:self.links.append(val)
  if t=='link' and d.get('rel')=='canonical':self.canonical.append(d.get('href'))
  if t=='link' and d.get('rel')=='alternate':self.alternates.append(d.get('hreflang'))
 def handle_endtag(self,t):
  if t in ('style','script'):self.skip-=1
 def handle_data(self,s):
  if not self.skip:self.visible.append(s)
files=json.loads((ROOT/'site-source/generated-files.json').read_text())
retired=set(json.loads((ROOT/'site-source/retired-public-files.json').read_text()))
# Original assets remain in the remote repository; manifest supplied by the audited snapshot.
manifest_path=ROOT/'site-source/preserved-assets.json'
assets=set(json.loads(manifest_path.read_text())) if manifest_path.exists() else set()
errors=[];checks=0;pages={}
for name in files:
 if not name.endswith('.html'):continue
 s=(ROOT/name).read_text();p=Page(s);pages[name]=p;checks+=1
 if len(p.ids)!=len(set(p.ids)):errors.append(f'{name}: duplicate IDs')
 visible=' '.join(p.visible)
 if re.search(r'Quiz\s*Arena|퀴즈\s*아레나|승규|SEUNGGYU|열한 살',visible,re.I):errors.append(f'{name}: retired name or creator PII')
 if re.search(r'(sk-[A-Za-z0-9]{24,}|sb_secret_|service_role|BEGIN PRIVATE KEY|ghp_[A-Za-z0-9]+)',s):errors.append(f'{name}: secret marker')
 if name.startswith(('ko/','en/')) or name=='index.html':
  if p.h1!=1:errors.append(f'{name}: expected one H1, got {p.h1}')
  if not p.meta.get('description') or len(p.canonical)!=1:errors.append(f'{name}: SEO fields missing')
  if not all(x in p.alternates for x in ['ko','en','x-default']):errors.append(f'{name}: missing alternates')
  if re.search(r'\b(37 downloads|937 followers)\b',visible):errors.append(f'{name}: headline vanity metrics')
 for url in p.links:
  u=urlsplit(url)
  if u.scheme or url.startswith('//'):continue
  dest=unquote(u.path)
  if not dest:target=ROOT/name
  elif dest.startswith('/'):target=ROOT/dest.lstrip('/')
  else:target=(ROOT/name).parent/dest
  try:rel=str(target.resolve().relative_to(ROOT))
  except ValueError:errors.append(f'{name}: link escapes site');continue
  if rel in retired:errors.append(f'{name}: retired public material linked')
  if target.is_dir():target=target/'index.html';rel=str(target.relative_to(ROOT))
  if not target.exists() and rel not in assets:errors.append(f'{name}: missing {url}')
  elif u.fragment and target.suffix=='.html' and target.exists():
   destp=Page(target.read_text())
   if unquote(u.fragment) not in destp.ids:errors.append(f'{name}: missing fragment {url}')
for l in ['ko','en']:
 s=(ROOT/f'{l}/index.html').read_text()
 for name in ['Global-by-Design','AP Revenue','AP SELECT','LIA','RGRG','Founder’s Lab','IR / INVESTORS','A store designed','Expert Collaboration']:
  if name not in s:errors.append(f'{l}: missing {name}')
 ir=(ROOT/f'{l}/ir/index.html').read_text()
 for name in ['PUBLIC','INVESTOR SHARE','NDA / DATA ROOM','Working Proof','Request','mailto:','FOUNDER-PROVIDED']:
  if name not in ir:errors.append(f'{l}/ir: missing {name}')
for l in ['vi','ja','zh-cn','fr']:
 p=pages[l+'/index.html']
 if p.meta.get('robots')!='noindex,follow':errors.append(f'{l}: unreviewed content indexable')
 if 'hreflang="'+l+'"' in (ROOT/'en/index.html').read_text():errors.append(f'{l}: premature hreflang')
for name in files:
 if name.endswith('.html'):
  s=(ROOT/name).read_text()
  if 'admin.apholdings.kr' in s:errors.append(f'{name}: private admin link in corporate navigation')
print(json.dumps({'html_pages_checked':checks,'errors':errors,'passed':not errors},ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
