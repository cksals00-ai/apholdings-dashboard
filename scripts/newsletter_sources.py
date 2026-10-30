"""Bounded collection from already-allowed official feeds and article metadata."""
import hashlib,json,re,time,xml.etree.ElementTree as ET
from datetime import datetime,timezone,date,timedelta
from email.utils import parsedate_to_datetime
from urllib.request import Request,HTTPRedirectHandler,build_opener
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup
import newsletter_server as publisher

FEEDS=(('Google','https://blog.google/rss/'),('AWS','https://aws.amazon.com/blogs/machine-learning/feed/'),('Microsoft','https://blogs.microsoft.com/feed/'),('NVIDIA','https://blogs.nvidia.com/feed/'),('Hugging Face','https://huggingface.co/blog/feed.xml'),('GitHub','https://github.blog/feed/'),('OpenAI','https://openai.com/news/rss.xml'))
AI=re.compile(r'\b(ai|artificial intelligence|gemini|claude|copilot|llm|agents?|generative|machine learning|gpt|model|inference|diffusion)\b',re.I)
class OfficialRedirect(HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  publisher.official_url(newurl)
  return super().redirect_request(req,fp,code,msg,headers,newurl)

def fetch(url):
 publisher.official_url(url)
 for attempt in range(3):
  try:
   request=Request(url,headers={'User-Agent':'AP-News-Source-Check/1.0 (+https://www.apholdings.kr/ko/news/)','Accept':'text/html,application/xml,text/xml;q=0.9'})
   with build_opener(OfficialRedirect()).open(request,timeout=40) as response:
    data=response.read(8_000_001)
    if len(data)>8_000_000:raise ValueError('Official source too large')
    return data
  except HTTPError as exc:
   if exc.code not in (408,429,500,502,503,504) or attempt==2:raise
  except (URLError,TimeoutError):
   if attempt==2:raise
  time.sleep(2**attempt)

def iso_day(value):
 value=value.strip()
 try:return datetime.fromisoformat(value.replace('Z','+00:00')).date().isoformat()
 except ValueError:return parsedate_to_datetime(value).date().isoformat()

def parse_feed(data,source):
 root=ET.fromstring(data);rows=[];seen=set()
 for item in root.iter():
  if item.tag.split('}')[-1] not in ('item','entry'):continue
  fields={x.tag.split('}')[-1]:x for x in item}
  try:
   title=''.join(fields['title'].itertext()).strip();link=fields['link'];url=link.get('href') or (link.text or '').strip()
   publisher.official_url(url)
   stamp=fields.get('pubDate')
   if stamp is None:stamp=fields.get('published')
   if stamp is None:stamp=fields.get('updated')
   day=iso_day(stamp.text)
   if url in seen or not AI.search(title):continue
   seen.add(url);rows.append({'url':url,'title':title,'published':day,'source':source})
  except (KeyError,ValueError,AttributeError,TypeError):continue
 return rows

def parse_article(html,url,source,feed_day):
 publisher.official_url(url)
 soup=BeautifulSoup(html,'html.parser');stamps=[]
 for meta in soup.find_all('meta'):
  if (meta.get('property') or meta.get('name','')).lower() in ('article:published_time','datepublished','date','pubdate','publishdate','dc.date.issued') and meta.get('content'):stamps.append(meta['content'])
 def collect(value):
  if isinstance(value,dict):
   if value.get('datePublished'):stamps.append(value['datePublished'])
   for v in value.values():collect(v)
  elif isinstance(value,list):
   for v in value:collect(v)
 primary_stamps=list(stamps)
 for block in soup.find_all('script',type='application/ld+json'):
  try:collect(json.loads(block.string or block.get_text()))
  except (ValueError,TypeError):pass
 for t in soup.find_all('time'):
  if t.get('datetime'):stamps.append(t['datetime'])
 dates=[]
 for stamp in (primary_stamps or stamps):
  try:dates.append(iso_day(str(stamp)))
  except (ValueError,TypeError,AttributeError):pass
 if feed_day not in dates:raise ValueError('Feed publication date not corroborated by article metadata')
 title=soup.find('h1') or soup.title
 title=title.get_text(' ',strip=True) if title else ''
 article=soup.find('article') or soup.find('main')
 if not article:raise ValueError('No official article body')
 for node in article.select('script,style,nav,footer,header,form,button,aside'):node.decompose()
 paragraphs=[p.get_text(' ',strip=True) for p in article.find_all(['p','li','h2','h3'])]
 paragraphs=[p for p in paragraphs if len(p)>35]
 text='\n'.join(dict.fromkeys(paragraphs))[:16000]
 if len(text)<200 or not AI.search(title+' '+text):raise ValueError('Insufficient original AI article text')
 return {'url':url,'source':source,'title':title,'published':feed_day,'text':text,'checked_at':datetime.now(timezone.utc).isoformat(),'body_sha256':hashlib.sha256(text.encode()).hexdigest()}

def collect_candidates(day,previous):
 today=date.fromisoformat(day);rows=[];errors=[]
 for source,url in FEEDS:
  try:rows.extend(parse_feed(fetch(url),source))
  except Exception as exc:errors.append({'source':source,'stage':'feed','error':str(exc)[:180]})
 rows=sorted(rows,key=lambda x:x['published'],reverse=True);seen=set(previous);verified=[]
 for row in rows:
  if row['url'] in seen or not today-timedelta(days=7)<=date.fromisoformat(row['published'])<=today:continue
  seen.add(row['url'])
  try:
   verified.append(parse_article(fetch(row['url']),row['url'],row['source'],row['published']))
   if len(verified)>=12:break
  except Exception as exc:errors.append({'source':row['source'],'url':row['url'],'stage':'article','error':str(exc)[:180]})
 return verified,errors
