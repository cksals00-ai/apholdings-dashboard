"""Automatic server QA. Never described as human inspection."""
import functools,http.server,json,threading,re,os,subprocess
from pathlib import Path
from PIL import Image
import newsletter as b
import newsletter_server as publisher

def compact(value):return re.sub(r'\s+','',value)
def check_pdf(issue,folder):
 import pdfplumber
 path=b.ROOT/b.pdf_path(issue).lstrip('/');alltext='';links=set()
 with pdfplumber.open(path) as doc:
  pages=len(doc.pages)
  if not 1<=pages<=12:raise ValueError('Unexpected PDF page count')
  for page in doc.pages:
   text=page.extract_text() or '';alltext+=text
   if '\ufffd' in text or not text.strip():raise ValueError('PDF missing text/glyphs')
   for char in page.chars:
    if char['x0'] < -1 or char['top'] < -1 or char['x1']>page.width+1 or char['bottom']>page.height+1:raise ValueError('PDF text clipping')
   links.update(link['uri'] for link in page.hyperlinks if link.get('uri'))
 for story in issue['stories']:
  for key in ('title','fact','insight'):
   if compact(story[key]) not in compact(alltext):raise ValueError('PDF dropped story text: '+key)
  if story['url'] not in links:raise ValueError('PDF original source link missing')
 subprocess.run(['pdftoppm','-scale-to','1200','-png',str(path),str(folder/'pdf-page')],check=True,timeout=180,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 rendered=list(folder.glob('pdf-page-*.png'))
 if len(rendered)!=pages:raise ValueError('Not every PDF page rendered')
 for image in rendered:
  with Image.open(image) as frame:frame.verify()
 return {'pages':pages,'source_links':len(links),'all_pages_rendered':True}

class QuietHandler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*_):pass

def check_browser(issue,folder):
 from playwright.sync_api import sync_playwright
 handler=functools.partial(QuietHandler,directory=str(b.ROOT));server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
 threading.Thread(target=server.serve_forever,daemon=True).start()
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(executable_path=os.environ.get('AP_NEWS_BROWSER_EXECUTABLE'))
   for width in (390,1440):
    page=browser.new_page(viewport={'width':width,'height':1000})
    page.route('**/supabase.co/**',lambda route:route.abort())
    page.goto(f'http://127.0.0.1:{server.server_port}{b.page_path(issue)}',wait_until='networkidle')
    page.locator('img').evaluate_all("images => images.forEach(i => i.loading='eager')")
    page.evaluate('Promise.all(Array.from(document.images,i=>i.decode()))')
    if page.evaluate('document.documentElement.scrollWidth>innerWidth'):raise ValueError('Web horizontal clipping')
    if page.locator('input[name=consent]').is_checked():raise ValueError('Consent must not be preselected')
    if page.locator('article[id^=story-]').count()!=len(issue['stories']):raise ValueError('Missing web stories')
    page.locator('[data-motion-toggle]').click()
    if not page.locator('.motion-image').get_attribute('src').endswith('.png'):raise ValueError('Pause poster missing')
    page.locator('[data-motion-toggle]').click()
    if not page.locator('.motion-image').get_attribute('src').endswith('.gif'):raise ValueError('Resume animation missing')
    page.emulate_media(reduced_motion='reduce')
    page.wait_for_function("document.querySelector('.motion-image').src.endsWith('.png')")
    if not page.locator('.motion-image').get_attribute('src').endswith('.png'):raise ValueError('Reduced motion missing')
    page.screenshot(path=str(folder/f'web-{width}.png'),full_page=True);page.close()
   # Render exact standalone email bytes without external subscribers or sending.
   page=browser.new_page(viewport={'width':640,'height':1000})
   def local_assets(route):
    rel=route.request.url.split(b.ORIGIN+'/',1)[-1]
    target=b.ROOT/rel.split('?',1)[0]
    if target.is_file():route.fulfill(path=str(target))
    else:route.abort()
   page.route(b.ORIGIN+'/**',local_assets)
   page.set_content(b.render_email(issue),wait_until='networkidle')
   page.evaluate('Promise.all(Array.from(document.images,i=>i.decode()))')
   page.screenshot(path=str(folder/'email.png'),full_page=True)
   browser.close()
 finally:server.shutdown();server.server_close()
 return {'mobile':390,'desktop':1440,'all_images_decoded':True,'motion_pause_and_reduced_motion':True}

def check_all(issue,folder,source_checks):
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
 from newsletter_grounding import validate_grounding
 import hashlib
 if {story['url'] for story,source in source_checks}!={s['url'] for s in issue['stories']}:raise ValueError('Original source receipts do not match issue')
 for story,source in source_checks:
  validate_grounding(story,source,story['review'])
  if hashlib.sha256(source['text'].encode()).hexdigest()!=story['source_hash']:raise ValueError('Source evidence changed after review')
 publisher.verify_documents(issue)
 report={'method':'서버 자동 검증 · 원문 근거 대조 · PDF 전페이지 렌더·문자/경계 검사 · 브라우저 검사','pdf':check_pdf(issue,folder),'browser':check_browser(issue,folder)}
 for im in [s['image']['path'] for s in issue['stories']]+[issue['hero']['path'],issue['hero']['poster']]:
  with Image.open(b.ROOT/im.lstrip('/')) as image:
   for n in range(getattr(image,'n_frames',1)):image.seek(n);image.load()
 with Image.open(b.ROOT/issue['hero']['path'].lstrip('/')) as gif,Image.open(b.ROOT/issue['hero']['poster'].lstrip('/')) as png:
  if gif.convert('RGB').tobytes()!=png.convert('RGB').tobytes():raise ValueError('Hero first frame differs from PDF poster')
 report['checks']={key:True for key in ('original_sources','all_pdf_pages','mobile_layout','image_loading')}
 (folder/'quality.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 return report
