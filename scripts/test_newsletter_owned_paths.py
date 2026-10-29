"""Publishing must leave shared homepage pages byte-identical."""
import json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import newsletter as b
import newsletter_handoff as h

class OwnedPathsTests(unittest.TestCase):
 def test_completed_publication_updates_only_news_owned_paths(self):
  original=b.ROOT
  issue=json.loads((b.ISSUES/'2026-10-30.json').read_text())
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder)
   for name in ('site-source','img'):(root/name).symlink_to(original/name,target_is_directory=True)
   shared=['sitemap.xml']+[f'{lang}/news/index.html' for lang in ('ko','en','vi','ja','zh-cn','fr')]
   for name in shared:
    p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'\xffBROKEN HOMEPAGE UTF8')
   pdf=root/b.pdf_path(issue).lstrip('/');pdf.parent.mkdir(parents=True,exist_ok=True);pdf.write_bytes((original/b.pdf_path(issue).lstrip('/')).read_bytes())
   with h.document_root(root):b.build_all(render_documents=False,update_shared_pages=False)
   for name in shared:self.assertEqual((root/name).read_bytes(),b'\xffBROKEN HOMEPAGE UTF8')
   latest=(root/'ko/news/daily/latest/index.html').read_text()
   self.assertIn(b.page_path(issue),latest)
   self.assertIn('noindex',latest)
   self.assertEqual((root/'newsletters/AP-News-latest.pdf').read_bytes(),pdf.read_bytes())
if __name__=='__main__':unittest.main()
