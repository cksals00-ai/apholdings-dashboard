"""Original-image variation checks and restrained date-specific cover motion."""
from pathlib import Path
from PIL import Image,ImageOps,ImageStat

def fingerprint(image):
 values=list(ImageOps.grayscale(image).resize((16,16)).getdata());mean=sum(values)/len(values)
 return [v>mean for v in values]
def image_ok(image,comparisons):
 if min(image.size)<320 or max(ImageStat.Stat(image.convert('RGB')).stddev)<12:return False
 a=fingerprint(image)
 for path in comparisons:
  with Image.open(path) as prior:b=fingerprint(prior)
  if sum(x!=y for x,y in zip(a,b))/len(a)<0.12:return False
 return True

def cover_motion(image,folder,day):
 folder=Path(folder);gif=folder/f'{day}-hero.gif';poster=folder/f'{day}-hero.png'
 frames=[]
 for i in range(24):
  # Smooth, closed zoom cycle; no abrupt jump when email GIF repeats.
  import math
  zoom=1+0.025*(1-math.cos(2*math.pi*i/24))/2
  size=(round(900*zoom),round(600*zoom));frame=ImageOps.fit(image.convert('RGB'),size,method=Image.Resampling.LANCZOS)
  x=(size[0]-900)//2;y=(size[1]-600)//2
  frames.append(frame.crop((x,y,x+900,y+600)).quantize(colors=128))
 temporary=gif.with_suffix('.tmp.gif')
 frames[0].save(temporary,save_all=True,append_images=frames[1:],duration=180,loop=0,optimize=False)
 temporary.replace(gif)
 temporary_poster=poster.with_suffix('.tmp.png')
 with Image.open(gif) as first:first.convert('RGB').save(temporary_poster)
 temporary_poster.replace(poster)
 return gif,poster
