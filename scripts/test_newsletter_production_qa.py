import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
import newsletter_production_qa as q
class PDFImageTests(unittest.TestCase):
 def test_text_complete_pdf_with_missing_article_art_is_rejected(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);(root/'newsletters').mkdir();(root/'img').mkdir()
   for n,color in [('story','navy'),('poster','green')]:Image.new('RGB',(20,10),color).save(root/f'img/{n}.png')
   issue={'date':'2026-10-30','stories':[{'title':'Source title','fact':'Fact text','insight':'Conditional insight','url':'https://blog.google/example','image':{'path':'/img/story.png'}}],'hero':{'poster':'/img/poster.png'}}
   c=Canvas(str(root/'newsletters/AP-News-2026-10-30.pdf'))
   for i,line in enumerate(['Source title','Fact text','Conditional insight']):c.drawString(30,750-i*20,line)
   c.linkURL(issue['stories'][0]['url'],(30,700,200,760));c.save()
   with patch.object(q.b,'ROOT',root),self.assertRaisesRegex(ValueError,'PDF.*image'):
    q.check_pdf(issue,root)
if __name__=='__main__':unittest.main()
