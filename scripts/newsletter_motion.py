"""Generate original AP abstract brand motion locally; no API or borrowed media."""
import math
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]

def build():
    w,h=960,540; frames=[]
    for frame in range(48):
        image=Image.new('RGB',(w,h),'#172338');d=ImageDraw.Draw(image)
        for y in range(h):
            t=y/h;d.line((0,y,w,y),fill=(23+int(9*t),35+int(24*t),56+int(15*t)))
        cx,cy=w//2,h//2
        for j,r in enumerate((62,112,170,229)):
            box=(cx-r,cy-r,cx+r,cy+r)
            d.ellipse(box,outline='#3e5b62',width=1)
            phase=frame*360/48*(1 if j%2==0 else -1)+j*70
            d.arc(box,phase,phase+92,fill=('#83b5a3' if j%2==0 else '#b89a70'),width=3)
            a=math.radians(phase);x=cx+r*math.cos(a);y=cy+r*math.sin(a)
            d.ellipse((x-4,y-4,x+4,y+4),fill='#d9e5d9')
        d.ellipse((cx-15,cy-15,cx+15,cy+15),fill='#83b5a3')
        frames.append(image)
    out=ROOT/'img/newsletter';out.mkdir(exist_ok=True)
    frames[0].save(out/'ap-signal-v1.png')
    frames[0].save(out/'ap-signal-v1.gif',save_all=True,append_images=frames[1:],duration=125,loop=0,optimize=True,disposal=2)
if __name__=='__main__':build()
