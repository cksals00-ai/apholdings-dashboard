"""AP News 표지·도형 생성 (글자 없는 SVG → 모든 어권 공통). 색은 CSS 변수(--cv-*)로 분류별 팔레트를 받는다."""
import math
def _r(x,y,w,h,c,rx=0,op=1):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="var(--cv-{c})" opacity="{op}"/>'
def _c(x,y,r,c,op=1):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="var(--cv-{c})" opacity="{op}"/>'
def _s(x,y,r,c,w=3):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="var(--cv-{c})" stroke-width="{w}"/>'
def _l(x1,y1,x2,y2,c,w=3,op=1):return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="var(--cv-{c})" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'
def _p(d,c,w=3,fill='none'):return f'<path d="{d}" fill="{fill}" stroke="var(--cv-{c})" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
def welcome():return ''.join([_c(340,135,118,'b',.25),_c(340,135,84,'b',.4),_c(340,135,52,'a'),_c(340,135,20,'c'),_r(60,196,72,10,'a',5),_r(60,214,120,10,'b',5),_r(60,232,48,10,'c',5)])
def weekly():return ''.join(_r(56+i*84,190-h,58,h,'a' if i!=2 else 'b',6) for i,h in enumerate([60,100,150,84,120]))+_l(40,192,440,192,'a',3)+_c(316,38,14,'c')+_r(56,40,150,10,'a',5)+_r(56,60,96,10,'b',5)
def label():
    g=''.join(_r(60+i*58,60+j*50,46,38,'b',4,.35 if (i+j)%2 else .6) for i in range(6) for j in range(3))
    return g+_s(300,128,52,'a',6)+_l(338,166,372,200,'a',8)+_l(0,128,480,128,'c',2,.8)
def models():
    return ''.join(_r(40+i*70,170-i*22,56,60+i*22,'a' if i%2==0 else 'b',6,.9-i*.08) for i in range(6))+_p('M52 150 C120 60 220 120 300 50 S420 70 440 40','c',4)+_c(440,40,9,'c')
def debt():
    rows=[(330,'a'),(300,'a'),(270,'b'),(120,'c'),(90,'c')]
    return ''.join(_r(40,36+i*40,w,22,c,11,1 if i>2 else .55) for i,(w,c) in enumerate(rows))+_p('M392 60 L440 60 M440 52 L452 60 L440 68','a',4)+_p('M392 236 L452 236','b',3)
def ask():
    return _r(40,50,170,22,'b',11,.55)+_r(40,86,130,22,'b',11,.55)+_r(40,122,150,22,'b',11,.55)+_s(330,100,56,'a',10)+_p('M300 80 q0 -28 30 -28 q30 0 30 26 q0 18 -30 26 v14','a',9)+_c(330,172,8,'c')+_r(40,196,200,12,'c',6)
def leaks():
    return _p('M120 80 L150 220 L330 220 L360 80 Z','a',5,'var(--cv-b)')+_p('M120 80 L360 80','a',5)+''.join(_c(x,y,r,'c') for x,y,r in [(180,40,9),(240,28,11),(300,46,9)])+''.join(_c(x,y,7,'a',.7) for x,y in [(150,238),(240,248),(330,238)])
def skills():
    hl={(1,2),(3,5),(6,1),(8,4),(10,6),(4,7)}
    return ''.join(_c(48+i*34,40+j*30,8 if (i,j) not in hl else 13,'a' if (i,j) in hl else 'b',1 if (i,j) in hl else .55) for i in range(13) for j in range(8))
def connect():
    n=[(70,70),(190,50),(130,160),(300,120),(240,215),(410,190)]
    e_=[(0,1),(0,2),(1,3),(2,3),(2,4),(3,5),(4,5)]
    return ''.join(_l(*n[a],*n[b],'b',4,.7) for a,b in e_)+''.join(_c(x,y,18 if i in(0,5) else 12,'a' if i in(0,5) else 'c') for i,(x,y) in enumerate(n))
def lenses():
    return _c(180,130,84,'a',.55)+_c(300,130,84,'b',.55)+_c(240,70,84,'c',.6)+_s(180,130,84,'a',3)+_s(300,130,84,'b',3)+_s(240,70,84,'c',3)
def plans():
    return ''.join(_r(240-w/2,36+i*46,w,36,c,6) for i,(w,c) in enumerate([(70,'c'),(170,'b'),(270,'a'),(370,'b')]))+_l(240,222,240,252,'a',4)
def voice():
    pts=[(40+i*10,135+math.sin(i*.9)*(70-i*.9)*(1 if i%2 else -1)) for i in range(41)]
    d='M'+' L'.join(f'{x:.0f} {y:.0f}' for x,y in pts)
    return _p(d,'b',4)+_p('M40 135 C140 80 220 190 320 120 S430 150 440 135','a',6)+_c(440,135,10,'c')
def timeline():
    return _p('M40 190 L100 150 L150 60 L210 190 L260 200 L320 110 L380 40 L440 70','a',6)+''.join(_c(x,y,9,'c' if y<100 else 'b') for x,y in [(150,60),(210,190),(260,200),(380,40)])+_l(40,230,440,230,'b',3)+_r(190,214,90,14,'b',7,.5)
def prompt():
    return _r(80,36,320,200,'a',12,.12)+''.join(_r(112,70+i*26,(200 if i%2==0 else 150)+ (i==5)*40,12,'c' if i in(1,3,5) else 'b',6,1 if i in(1,3,5) else .6) for i in range(6))
MOTIFS={'launch':welcome,'weekly':weekly,'label':label,'models':models,'debt':debt,'ask':ask,'leaks':leaks,'skills':skills,'connect':connect,'lenses':lenses,'plans':plans,'voice':voice,'timeline':timeline,'prompt':prompt}
BY_NO={1:'launch',2:'weekly',3:'label',4:'models',5:'debt',6:'ask',7:'leaks',8:'skills',9:'connect',10:'lenses',11:'plans',12:'voice',13:'timeline',14:'prompt'}
def cover(no,large=False):
    f=MOTIFS[BY_NO.get(no,'launch')]
    par='meet' if large else 'slice'
    return f'<svg class="cover{" cover-lg" if large else ""}" viewBox="0 0 480 270" preserveAspectRatio="xMidYMid {par}" role="img" aria-hidden="true" focusable="false"><rect width="480" height="270" fill="var(--cv-bg)"/>{f()}</svg>'
