import tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
import newsletter_art_checks as a
class ArtTests(unittest.TestCase):
 def test_blank_and_repeated_art_rejected(self):
  image=Image.new('RGB',(768,512),'ivory');self.assertFalse(a.image_ok(image,[]))
  ImageDraw.Draw(image).polygon([(10,10),(700,20),(40,490)],fill='navy')
  self.assertTrue(a.image_ok(image,[]))
  with tempfile.TemporaryDirectory() as temp:
   path=Path(temp)/'prior.png';image.save(path);self.assertFalse(a.image_ok(image,[path]))
 def test_cover_all_frames_decode_and_poster_matches_first(self):
  image=Image.new('RGB',(768,512),'ivory');d=ImageDraw.Draw(image);d.rectangle((80,80,500,360),fill='navy')
  with tempfile.TemporaryDirectory() as temp:
   gif,png=a.cover_motion(image,temp,'2026-10-31')
   with Image.open(gif) as g,Image.open(png) as p:
    self.assertGreater(g.n_frames,1);self.assertEqual(g.convert('RGB').tobytes(),p.convert('RGB').tobytes())
    for n in range(g.n_frames):g.seek(n);g.load()
if __name__=='__main__':unittest.main()
