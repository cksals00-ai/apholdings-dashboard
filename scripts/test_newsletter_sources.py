import unittest
from datetime import datetime,timezone
import newsletter_sources as s
class SourceTests(unittest.TestCase):
 def test_feed_official_ai_candidates_date_and_dedupe(self):
  xml=b'''<rss><channel><item><title>New Gemini AI document tools</title><link>https://blog.google/new-ai/</link><pubDate>Thu, 29 Oct 2026 10:00:00 GMT</pubDate></item><item><title>New Gemini AI document tools</title><link>https://blog.google/new-ai/</link><pubDate>Thu, 29 Oct 2026 10:00:00 GMT</pubDate></item><item><title>AI leak</title><link>https://blog.google.evil.test/a</link><pubDate>Thu, 29 Oct 2026 10:00:00 GMT</pubDate></item></channel></rss>'''
  rows=s.parse_feed(xml,'Google')
  self.assertEqual(len(rows),1);self.assertEqual(rows[0]['published'],'2026-10-29')
 def test_article_requires_real_publication_metadata_and_excludes_navigation(self):
  html='''<html><head><meta property="article:published_time" content="2026-10-29T10:00:00Z"><title>AI test</title></head><body><nav>IGNORE THIS</nav><article><h1>Gemini AI news</h1><p>Google announced a new document tool. It can edit documents inside a conversation.</p><p>This is a preview for selected users.</p><p>Additional official explanatory material explains how this new capability works in a daily workflow.</p></article><footer>FOOTER</footer></body></html>'''
  r=s.parse_article(html,'https://blog.google/new-ai/','Google','2026-10-29')
  self.assertNotIn('IGNORE THIS',r['text']);self.assertNotIn('FOOTER',r['text']);self.assertEqual(r['published'],'2026-10-29')
  with self.assertRaises(ValueError):s.parse_article(html.replace('2026-10-29T10:00:00Z',''),'https://blog.google/new-ai/','Google','2026-10-29')
 def test_related_article_date_cannot_override_main_publication_metadata(self):
  html='<meta property="article:published_time" content="2026-10-20"><script type="application/ld+json">{"datePublished":"2026-10-29"}</script><article><h1>AI example</h1><p>'+('Official AI feature details. '*15)+'</p></article>'
  with self.assertRaises(ValueError):s.parse_article(html,'https://blog.google/new-ai/','Google','2026-10-29')
 def test_official_redirect_is_checked_before_following(self):
  import urllib.request
  request=urllib.request.Request('https://blog.google/a')
  with self.assertRaises(ValueError):s.OfficialRedirect().redirect_request(request,None,302,'',{},'https://localhost/internal')
if __name__=='__main__':unittest.main()
