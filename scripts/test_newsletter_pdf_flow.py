import json,re,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import newsletter as b
from pypdf import PdfReader
import pdfplumber
class PdfFlowTests(unittest.TestCase):
 def issue(self):return json.loads((b.ISSUES/'2026-10-30.json').read_text())
 def render(self,issue):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);(root/'img').mkdir()
   assets=['img/ap_mark.png',issue['hero']['path'].lstrip('/')]+[s['image']['path'].lstrip('/') for s in issue['stories']]
   for name in assets:
    target=root/name;target.parent.mkdir(parents=True,exist_ok=True);target.symlink_to(b.ROOT/name)
   from PIL import Image
   issue['hero']['poster']='/img/newsletter/pdf-fixture-poster.png';Image.new('RGB',(900,600),'#172338').save(root/issue['hero']['poster'].lstrip('/'))
   (root/'site-source/newsletter').mkdir(parents=True);(root/'site-source/newsletter/fonts').symlink_to(b.ROOT/'site-source/newsletter/fonts',target_is_directory=True)
   with patch.object(b,'ROOT',root):path=b.render_pdf(issue)
   reader=PdfReader(path);text=''.join(page.extract_text() for page in reader.pages)
   with pdfplumber.open(path) as pdf:
    for page in pdf.pages:
     self.assertTrue(all(ch['x0']>=-1 and ch['x1']<=page.width+1 and ch['top']>=-1 and ch['bottom']<=page.height+1 for ch in page.chars))
   links={a.get_object().get('/A',{}).get('/URI') for page in reader.pages for a in page.get('/Annots',[])}
   self.assertTrue({s['url'] for s in issue['stories']}.issubset(links))
   return re.sub(r'\s+','',text),len(reader.pages)
 def test_actual_test_cover_prefix_and_timestamp_note_fit_without_clipping(self):
  issue=self.issue();issue['title']='[서버 자동 제작 테스트] NVIDIA, AI 에이전트로 시뮬레이션 개발 혁신';issue['intro']='정규 발행과 구분한 서버 제작 검증용 테스트호입니다. NVIDIA가 AI 에이전트와 Omniverse 라이브러리로 시뮬레이션 개발을 지원합니다.'
  issue['edition_note']='전날 이후 발표로 선정 · 실제 발표2026-10-29~2026-10-29 · 원문 조회2026-10-30T16:21:00+09:00 · 지면 검증2026-10-30T17:50:00+09:00 · 서버 AI 작성 및 원문 근거 자동 대조 · 사람 검수 아님'
  text,pages=self.render(issue)
  for field in ('title','intro','edition_note'):self.assertIn(re.sub(r'\s+','',issue[field]),text)
 def test_maximum_producer_cover_copy_can_flow_to_an_extra_cover_page(self):
  issue=self.issue();issue['title']='긴제목검증'*18;issue['intro']=('원문내용보존'*60)[:350];issue['edition_note']='검증기록'*60
  text,pages=self.render(issue)
  for field in ('title','intro','edition_note'):self.assertIn(re.sub(r'\s+','',issue[field]),text)
  self.assertGreaterEqual(pages,7)
 def test_long_but_allowed_story_fields_flow_without_losing_facts_or_links(self):
  issue=self.issue();story=issue['stories'][0];story['title']='원문 기반 제목 '*8;story['summary']='요약 문장 '*26;story['fact']='확인한 사실과 조건을 보존합니다. '*32;story['insight']='AP에서 적용 가능성을 검토할 수 있습니다. '*14
  text,pages=self.render(issue)
  for field in ('title','summary','fact','insight'):self.assertIn(re.sub(r'\s+','',story[field]),text)
  self.assertGreaterEqual(pages,7)
if __name__=='__main__':unittest.main()
