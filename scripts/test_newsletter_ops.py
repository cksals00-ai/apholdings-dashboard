import unittest,json,os,tempfile
from pathlib import Path
from unittest.mock import patch
import newsletter_ops as ops
class OpsTests(unittest.TestCase):
 def test_fixed_test_mail_key_and_retry(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);p=root/'.ap-news-state/rehearsal';p.mkdir(parents=True)
   (p/'email.html').write_text('test html');(p/'manifest.json').write_text(json.dumps({'web_path':'/ko/news/daily/preview/test/','pdf_path':'/newsletters/previews/test.pdf'}))
   for name in ('ko/news/daily/preview/test/index.html','newsletters/previews/test.pdf'):
    target=root/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b'public')
   class Reply:
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def read(self):return b'public'
   calls=[]
   def emit(key,event,*args,**kwargs):
    calls.append((key,event))
    if len(calls)==1:raise ValueError('injected_mail_failure')
    return {'accepted':True}
   with patch.object(ops,'ROOT',root),patch.dict(os.environ,{'GITHUB_RUN_ID':'123'}),patch.object(ops,'urlopen',return_value=Reply()),patch.object(ops,'emit',side_effect=emit),patch.object(ops.time,'sleep') as sleep:
    ops.finish();sleep.assert_called_once_with(20)
   self.assertEqual(calls,[('test-123:newsletter','test_newsletter'),('test-123:newsletter','test_newsletter'),('test-123:recovery','test_recovery')])
 def test_run_id_rejects_path_injection(self):
  with patch.dict(os.environ,{'GITHUB_RUN_ID':'../unsafe'}):
   with self.assertRaises(ValueError):ops.ident()
if __name__=='__main__':unittest.main()
