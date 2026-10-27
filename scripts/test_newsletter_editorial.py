import json, unittest
from pathlib import Path
import newsletter as b
import newsletter_handoff as h

class EditorialTests(unittest.TestCase):
    def issue(self):
        i=json.loads((b.ISSUES/'2026-10-27.json').read_text())
        i.update(layout='editorial-v2', hero={'path':'/img/newsletter/ap-signal-v1.gif','poster':'/img/newsletter/ap-signal-v1.png','alt':'AP의 AI 신호와 연결을 표현한 추상 그래픽','caption':'AP 브랜드 모션 그래픽 · 실제 제품 화면 아님'})
        return i
    def test_shared_motion_and_no_repetitive_action(self):
        i=self.issue()
        for output in (b.render_issue(i),b.render_email(i)):
            self.assertIn(i['hero']['path'],output)
            self.assertIn('AP의 시선',output)
            self.assertNotIn('오늘 해볼 일',output)
            for s in i['stories']:
                for k in ('summary','fact','insight'): self.assertIn(b.esc(s[k]),output)
        self.assertIn('data-motion-toggle',b.render_issue(i))
        self.assertIn('{{unsubscribe_url}}',b.render_email(i))
        self.assertIn(i['hero']['poster'].lstrip('/'), h.paths_for(i))
        self.assertIn(i['hero']['path'].lstrip('/'), h.paths_for(i))
    def test_v2_bundle_round_trip_and_static_pdf(self):
        import tempfile
        from unittest.mock import patch
        from pypdf import PdfReader
        i=self.issue()
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); (root/'img').symlink_to(b.ROOT/'img',target_is_directory=True)
            (root/'site-source/newsletter/issues').mkdir(parents=True)
            (root/'site-source/newsletter/fonts').symlink_to(b.ROOT/'site-source/newsletter/fonts',target_is_directory=True)
            (root/'site-source/newsletter/issues'/f"{i['date']}.json").write_text(json.dumps(i,ensure_ascii=False))
            with h.document_root(root), patch.object(h,'ROOT',root):
                b.write(b.page_path(i)+'index.html',b.render_issue(i))
                b.write('/newsletters/email/'+i['date']+'.html',b.render_email(i))
                pdf=b.render_pdf(i)
                text=''.join(page.extract_text() for page in PdfReader(pdf).pages)
                self.assertIn('AP의 시선',text); self.assertNotIn('오늘 해볼 일',text)
                bundle=h.create_bundle(i['date'],root/'ready.zip',reviewed=True)
                recovered,files=h.validate_bundle(bundle,i['date'])
                self.assertEqual(recovered,i)
                self.assertIn(i['hero']['path'].lstrip('/'),files)
                self.assertIn(i['hero']['poster'].lstrip('/'),files)

    def test_invalid_motion_paths_rejected(self):
        for key in ('path','poster'):
            i=self.issue(); i['hero'][key]='/img/newsletter/../../secret.gif'
            with self.assertRaises(ValueError): b.validate_issue(i)
    def test_legacy_unchanged(self):
        i=self.issue();del i['layout'];del i['hero']
        self.assertIn('오늘 해볼 일',b.render_issue(i))
        self.assertNotIn('data-motion-toggle',b.render_issue(i))

if __name__=='__main__':unittest.main()
