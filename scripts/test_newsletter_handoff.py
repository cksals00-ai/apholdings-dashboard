import copy, importlib.util, json, tempfile, unittest, zipfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]

class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('newsletter_handoff'), 'Completed-edition handoff is missing')
        import newsletter_handoff as handoff
        self.h=handoff
        self.issue=json.loads((ROOT/'site-source/newsletter/issues/2026-10-27.json').read_text())

    def bundle(self, folder):
        path=Path(folder)/'ready.zip'
        self.h.create_bundle(self.issue['date'], path, reviewed=True)
        return path

    def test_valid_finished_bundle_contains_same_web_pdf_and_email(self):
        with tempfile.TemporaryDirectory() as folder:
            path=self.bundle(folder)
            issue, files=self.h.validate_bundle(path,'2026-10-27')
            self.assertEqual(issue,self.issue)
            self.assertEqual(files['newsletters/AP-News-2026-10-27.pdf'], (ROOT/'newsletters/AP-News-2026-10-27.pdf').read_bytes())
            self.assertIn('newsletters/email/2026-10-27.html',files)
            self.assertEqual(len(files),9)

    def test_unreviewed_bundle_cannot_be_handed_off(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                self.h.create_bundle('2026-10-27',Path(folder)/'ready.zip',reviewed=False)

    def test_tamper_extra_paths_and_duplicate_members_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path=self.bundle(folder)
            with zipfile.ZipFile(path) as z:
                original={name:z.read(name) for name in z.namelist()}
            for mutation in ('tamper','escape','duplicate'):
                bad=Path(folder)/f'{mutation}.zip'
                with zipfile.ZipFile(bad,'w') as z:
                    for name, data in original.items():
                        z.writestr(name, data+b'changed' if mutation=='tamper' and name.endswith('.pdf') else data)
                    if mutation=='escape': z.writestr('../admin/index.html',b'unsafe')
                    if mutation=='duplicate':
                        import warnings
                        with warnings.catch_warnings():
                            warnings.simplefilter('ignore')
                            z.writestr('manifest.json',original['manifest.json'])
                with self.assertRaises(ValueError): self.h.validate_bundle(bad,'2026-10-27')

    def test_wrong_date_cannot_publish_as_today(self):
        with tempfile.TemporaryDirectory() as folder:
            path=self.bundle(folder)
            with self.assertRaises(ValueError): self.h.validate_bundle(path,'2026-10-28')

    def test_hash_consistent_but_corrupt_image_is_rejected(self):
        import hashlib
        with tempfile.TemporaryDirectory() as folder:
            path=self.bundle(folder)
            with zipfile.ZipFile(path) as z:
                files={name:z.read(name) for name in z.namelist()}
            name=self.issue['stories'][0]['image']['path'].lstrip('/')
            files[name]=b'corrupt image'
            manifest=json.loads(files['manifest.json'])
            manifest['files'][name]=hashlib.sha256(files[name]).hexdigest()
            files['manifest.json']=json.dumps(manifest).encode()
            bad=Path(folder)/'corrupt.zip'
            with zipfile.ZipFile(bad,'w') as z:
                for key,data in files.items(): z.writestr(key,data)
            with self.assertRaises(ValueError): self.h.validate_bundle(bad,'2026-10-27')

    def test_noncanonical_upload_name_is_rejected_before_network_access(self):
        with tempfile.TemporaryDirectory() as folder:
            path=self.bundle(folder)
            with patch.object(self.h.subprocess,'check_output',side_effect=AssertionError('No upload allowed')):
                with self.assertRaises(ValueError): self.h.upload_bundle(path,'2026-10-27')

    def test_upload_records_handoff_only_after_the_asset_is_saved(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'AP-News-2026-10-27-ready.zip'
            self.h.create_bundle('2026-10-27',path,reviewed=True)
            commands=[]
            def run(args,**kwargs): commands.append(args)
            with patch.object(self.h.subprocess,'check_output',return_value=b'[{"tag_name":"ap-news-ready-2026-10-27","draft":true}]'), \
                 patch.object(self.h.subprocess,'run',run):
                self.h.upload_bundle(path,'2026-10-27')
            self.assertEqual(commands[0][:3],['gh','release','upload'])
            self.assertEqual(commands[1][:4],['gh','workflow','run','ap-news-daily.yml'])
            self.assertIn('record_handoff=true',commands[1])
            self.assertIn('edition_date=2026-10-27',commands[1])
            self.assertEqual(len(commands),3)
            self.assertIn('reserve_publication=true',commands[2])
            self.assertIn('edition_date=2026-10-27',commands[2])

    def test_changed_editorial_intro_cannot_reuse_an_old_pdf(self):
        import hashlib
        import newsletter as b
        with tempfile.TemporaryDirectory() as folder:
            path=self.bundle(folder)
            with zipfile.ZipFile(path) as z:
                files={name:z.read(name) for name in z.namelist()}
            changed=copy.deepcopy(self.issue)
            changed['intro']='원본 PDF에 없는 교체된 도입문입니다.'
            day=changed['date']
            files[f'site-source/newsletter/issues/{day}.json']=json.dumps(changed,ensure_ascii=False).encode()
            files[f'ko/news/daily/{day}/index.html']=b.render_issue(changed).encode()
            files[f'newsletters/email/{day}.html']=b.render_email(changed).encode()
            manifest=json.loads(files['manifest.json'])
            for name in manifest['files']:
                manifest['files'][name]=hashlib.sha256(files[name]).hexdigest()
            files['manifest.json']=json.dumps(manifest).encode()
            bad=Path(folder)/'mismatch.zip'
            with zipfile.ZipFile(bad,'w') as z:
                for name,data in files.items(): z.writestr(name,data)
            with self.assertRaises(ValueError): self.h.validate_bundle(bad,day)

    def test_server_copies_finished_pdf_without_calling_pdf_generator(self):
        import newsletter as b
        import newsletter_server as s
        with tempfile.TemporaryDirectory() as folder:
            path=self.bundle(folder)
            target=Path(folder)/'site'; target.mkdir()
            with patch.object(s,'ROOT',target), patch.object(b,'ROOT',target), \
                 patch.object(b,'ISSUES',target/'site-source/newsletter/issues'), \
                 patch.object(b,'render_pdf',side_effect=AssertionError('Server must not create PDF')):
                self.h.install_bundle(path,'2026-10-27',target)
            self.assertEqual((target/'newsletters/AP-News-2026-10-27.pdf').read_bytes(), (ROOT/'newsletters/AP-News-2026-10-27.pdf').read_bytes())
            self.assertEqual(json.loads((target/'newsletters/latest.json').read_text())['date'],'2026-10-27')

    def test_unready_day_does_not_fall_back_to_yesterday_or_call_api(self):
        import newsletter_server as s
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(s,'ROOT',Path(folder)), patch.object(s.builder,'ISSUES',Path(folder)/'issues'), \
                 patch.object(self.h,'download_bundle',return_value=None):
                result=s.prepare('2026-10-28',now=datetime.fromisoformat('2026-10-28T08:00:00+09:00'))
            self.assertEqual(result['state'],'awaiting_ready')
            self.assertFalse(result['due'])

    def test_before_08_finished_bundle_is_not_installed(self):
        import newsletter_server as s
        with patch.object(self.h,'download_bundle',side_effect=AssertionError('Too early')):
            result=s.prepare('2026-10-28',now=datetime.fromisoformat('2026-10-28T07:59:59+09:00'))
        self.assertEqual(result['state'],'not_due')
        self.assertFalse(result['due'])

    def test_future_bundle_cannot_publish_early_through_manual_date_input(self):
        import newsletter_server as s
        with patch.object(self.h,'download_bundle',side_effect=AssertionError('Future edition accessed')):
            result=s.prepare('2026-10-28',now=datetime.fromisoformat('2026-10-27T14:00:00+09:00'))
        self.assertFalse(result['due'])
        self.assertEqual(result['state'],'not_due')

if __name__=='__main__': unittest.main()
