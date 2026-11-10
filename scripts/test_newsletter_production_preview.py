import io,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
import newsletter_production_preview as p
class PreviewDeliveryTests(unittest.TestCase):
 def fixture(self,root):
  out=root/'.ap-news-state/server-rehearsal';out.mkdir(parents=True)
  path='ko/news/daily/preview/server-123/index.html';target=root/path;target.parent.mkdir(parents=True);target.write_bytes(b'public')
  (out/'email.html').write_text('test email');(out/'manifest.json').write_text(json.dumps({'paths':[path],'page':'/ko/news/daily/preview/server-123/','pdf':'/newsletters/previews/test.pdf','run_id':'123'}));return out
 def test_real_test_newsletter_is_the_only_mail_after_injected_failure(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);out=self.fixture(root);calls=[]
   def emit(key,event,*args,**kwargs):
    calls.append((key,event))
    if len(calls)==1:raise HTTPError('https://test.invalid',503,'injected',{},io.BytesIO(b'{"error":"Error: injected_mail_failure"}'))
    return {'accepted':True,'id':'provider-one'}
   with patch.object(p.b,'ROOT',root),patch.dict('os.environ',{'GITHUB_RUN_ID':'123','RUN_URL':'https://run.invalid'}),patch.object(p,'urlopen',return_value=io.BytesIO(b'public')),patch.object(p,'emit',side_effect=emit),patch.object(p.time,'sleep') as sleep,patch.object(p.server,'database',side_effect=AssertionError('No regular queue writes')):
    p.finish()
   self.assertEqual(calls,[('test-123:newsletter','test_newsletter')]*2);sleep.assert_called_once_with(20)
   proof=json.loads((out/'mail-proof.json').read_text());self.assertTrue(proof['injected_failure_observed']);self.assertTrue(proof['accepted']);self.assertEqual(proof['operational_mail_sent'],0)
 def test_no_injected_failure_cannot_claim_recovery(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);self.fixture(root)
   with patch.object(p.b,'ROOT',root),patch.dict('os.environ',{'GITHUB_RUN_ID':'123','RUN_URL':'https://run.invalid'}),patch.object(p,'urlopen',return_value=io.BytesIO(b'public')),patch.object(p,'emit',return_value={'accepted':True,'id':'provider-one'}),self.assertRaises(ValueError):p.finish()
 def test_stage_exposes_ten_isolated_files_including_the_actual_test_email(self):
  day='2026-11-10';paths=[f'img/newsletter/{day}-test-123-story-{i}.png' for i in range(1,6)];hero=[f'img/newsletter/{day}-test-123-hero.gif',f'img/newsletter/{day}-test-123-hero.png'];issue={'date':day,'stories':[{'image':{'path':'/'+x}} for x in paths],'hero':{'path':'/'+hero[0],'poster':'/'+hero[1]}}
  files={x:b'image' for x in paths+hero};files.update({f'ko/news/daily/{day}/index.html':b'<html>test</html>',f'newsletters/AP-News-{day}.pdf':b'PDF',f'newsletters/email/{day}.html':b'<html>{{unsubscribe_url}}</html>'})
  with tempfile.TemporaryDirectory() as folder,patch.object(p.b,'ROOT',Path(folder)),patch.dict('os.environ',{'GITHUB_RUN_ID':'123'}),patch.object(p.h,'validate_bundle',return_value=(issue,files)):
   p.stage(Path('bundle'),day);out=Path(folder)/'.ap-news-state/server-rehearsal';manifest=json.loads((out/'manifest.json').read_text())
   self.assertEqual(len(manifest['paths']),10);self.assertEqual((Path(folder)/manifest['email']).read_bytes(),(out/'email.html').read_bytes());self.assertNotIn('{{unsubscribe_url}}',(out/'email.html').read_text())
if __name__=='__main__':unittest.main()
