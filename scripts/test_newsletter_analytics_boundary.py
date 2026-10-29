"""Shared site instrumentation must not mutate completed newsletter artifacts."""
import unittest,tempfile,subprocess,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class AnalyticsBoundaryTests(unittest.TestCase):
 def test_installer_preserves_edition_and_preview_bytes_but_tags_archive(self):
  with tempfile.TemporaryDirectory() as f:
   root=Path(f);(root/'analytics').mkdir();shutil.copyfile(ROOT/'analytics/install.py',root/'analytics/install.py');(root/'CNAME').write_text('www.apholdings.kr')
   paths=['ko/news/daily/2026-10-30/index.html','ko/news/daily/preview/automation-123/index.html','ko/news/daily/index.html','ko/news/index.html']
   raw=b'<html><head></head><body>verified content</body></html>'
   for name in paths:
    p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
   subprocess.run([sys.executable,str(root/'analytics/install.py')],check=True,capture_output=True)
   for name in paths[:2]:self.assertEqual((root/name).read_bytes(),raw)
   for name in paths[2:]:self.assertIn(b'data-ap-analytics',(root/name).read_bytes())
   first={name:(root/name).read_bytes() for name in paths}
   subprocess.run([sys.executable,str(root/'analytics/install.py')],check=True,capture_output=True)
   self.assertEqual(first,{name:(root/name).read_bytes() for name in paths})
if __name__=='__main__':unittest.main()
