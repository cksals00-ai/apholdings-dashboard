import unittest
from copy import deepcopy
from newsletter import validate_issue, render_issue, render_email

class IssueTests(unittest.TestCase):
    def setUp(self):
        self.issue = {'date':'2026-10-09','number':1,'status':'published','verified':True,'title':'AI 소식을 오늘의 판단으로','intro':'확인된 뉴스입니다.','edition_note':'2026-10-09 09:00 KST 확인','takeaway':'원문을 확인하세요.','stories':[{'title':f'기사 {i}','source':'공식','url':f'https://example.com/news/{i}','published':'2026-10-08','fact':'발표 내용','insight':'AP의 해석','action':'오늘 할 일'} for i in range(5)]}
    def test_requires_original_source_and_dates(self):
        validate_issue(self.issue)
        for key in ('url','published','fact'):
            broken=deepcopy(self.issue);del broken['stories'][0][key]
            with self.assertRaises(ValueError): validate_issue(broken)
        broken=deepcopy(self.issue);broken['stories'][0]['url']='javascript:alert(1)'
        with self.assertRaises(ValueError): validate_issue(broken)
        broken=deepcopy(self.issue);broken['stories'][0]['published']='2026-10-10'
        with self.assertRaises(ValueError): validate_issue(broken)
    def test_email_and_web_share_titles_and_link_pdf(self):
        web=render_issue(self.issue);mail=render_email(self.issue)
        for story in self.issue['stories']:
            self.assertIn(story['title'],web);self.assertIn(story['title'],mail)
        self.assertIn('AP-News-2026-10-09.pdf',web)
        self.assertIn('AP-News-2026-10-09.pdf',mail)
        self.assertIn('{{unsubscribe_url}}',mail)
    def test_editorial_content_shared_by_web_and_email(self):
        story=self.issue['stories'][0]
        story.update(summary='미국 성인 대상 실험', image={'path':'/img/newsletter/test.png','alt':'게임 세계 편집 일러스트','caption':'AI 제작 · 편집 일러스트'})
        from unittest.mock import patch
        with patch('pathlib.Path.is_file', return_value=True):
            for output in (render_issue(self.issue), render_email(self.issue)):
                for value in (story['summary'],story['image']['path'],story['image']['alt'],story['image']['caption'],story['action']):
                    self.assertIn(value,output)
    def test_image_paths_cannot_escape_asset_directory(self):
        for path in ('/img/newsletter/../../secret.png','https://example.com/a.png','/img/ap_mark.png'):
            self.issue['stories'][0]['image']={'path':path,'alt':'이미지','caption':'편집 일러스트'}
            with self.assertRaises(ValueError): validate_issue(self.issue)

    def test_pdf_supports_image_after_text_only_first_story(self):
        import json, tempfile
        from pathlib import Path
        from unittest.mock import patch
        import newsletter
        issue=json.loads((newsletter.ISSUES/'2026-10-11.json').read_text())
        del issue['stories'][0]['image']
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for folder in ('img','site-source'):
                (root/folder).symlink_to(newsletter.ROOT/folder,target_is_directory=True)
            with patch.object(newsletter,'ROOT',root):
                output=newsletter.render_pdf(issue)
                self.assertTrue(output.is_file())

    def test_unverified_issue_cannot_publish(self):
        broken=deepcopy(self.issue);broken['verified']=False
        with self.assertRaises(ValueError): validate_issue(broken)

if __name__=='__main__': unittest.main()
