"""Original AP editorial paper motion, version2. No external image or API."""
import math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[1]

def build():
 w,h=960,540;frames=[]
 for f in range(48):
  t=f/48*2*math.pi; lift=math.sin(t)*7
  im=Image.new('RGB',(w,h));d=ImageDraw.Draw(im)
  for y in range(h):
   v=y/h;d.line((0,y,w,y),fill=(247-int(8*v),244-int(8*v),237-int(8*v)))
  cards=[(168,111-lift,485,429-lift,'#172338'),(369,74+lift,721,392+lift,'#83a79b'),(290,151,715,451,'#fffdf7')]
  for x0,y0,x1,y1,color in cards:
   layer=Image.new('RGBA',(w,h));s=ImageDraw.Draw(layer);s.rounded_rectangle((x0+5,y0+12,x1+5,y1+12),radius=4,fill=(23,35,56,35));layer=layer.filter(ImageFilter.GaussianBlur(14));im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB');d=ImageDraw.Draw(im);d.rounded_rectangle((x0,y0,x1,y1),radius=3,fill=color)
  # Architectural lines make the back sheets feel like an editorial composition.
  for x in (199,230,261):d.line((x,155-lift,x,390-lift),fill='#50626c',width=1)
  d.line((404,110+lift,680,110+lift),fill='#c4d4c7',width=1)
  # A bold editorial crop: ink, sage and brass against an ivory page.
  d.rectangle((320,181,565,340),fill='#20354a')
  d.polygon([(320,340),(456,181),(565,181),(565,340)],fill='#688e83')
  d.polygon([(435,340),(565,210),(565,340)],fill='#a4bbae')
  d.line((320,345,565,345),fill='#b59465',width=3)
  # Type-like rules are intentionally abstract: no fabricated headlines.
  for y,length in ((378,225),(392,194),(406,212)):
   d.rounded_rectangle((320,y,320+length,y+3),radius=1,fill='#b7b9af')
  for y,length in ((185,85),(199,65),(230,75),(244,85),(275,85),(289,54)):
   d.rounded_rectangle((594,y,594+length,y+3),radius=1,fill='#bcc4ba')
  # Subtle moving light on the brass guide; a calm eight-second seamless loop.
  x=342+(math.sin(t)+1)*100
  d.line((x,344,x+24,344),fill='#f4dfb7',width=3)
  d.line((180,477,742,477),fill='#cfc8b9',width=1)
  d.rectangle((180,475,232,479),fill='#b59465')
  frames.append(im)
 out=ROOT/'img/newsletter';out.mkdir(exist_ok=True)
 frames[0].save(out/'ap-editorial-v2.png')
 frames[0].save(out/'ap-editorial-v2.gif',save_all=True,append_images=frames[1:],duration=165,loop=0,optimize=True,disposal=2)
if __name__=='__main__':build()
