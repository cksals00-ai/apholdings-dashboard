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
    def test_unverified_issue_cannot_publish(self):
        broken=deepcopy(self.issue);broken['verified']=False
        with self.assertRaises(ValueError): validate_issue(broken)

if __name__=='__main__': unittest.main()
