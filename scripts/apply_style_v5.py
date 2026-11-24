#!/usr/bin/env python3
"""STYLE v5: site.css 끝에 v5 블록을 붙이고(재실행해도 같음) Noto Sans 링크를 head에 1회 삽입. build_site 재실행 금지.
사용: assets/v2/style_v5.css 옆에 두고 `python3 scripts/apply_style_v5.py` → `python3 scripts/check_site.py`"""
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CSS=(Path(__file__).parent/'style_v5.css').read_text()+'\n'+(Path(__file__).parent/'v6.css').read_text()+'\n'+(Path(__file__).parent/'v7.css').read_text()+'\n'+(Path(__file__).parent/'v8.css').read_text()+'\n'+(Path(__file__).parent/'v9.css').read_text()
FONT='<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700&family=Noto+Sans+KR:wght@400;600;700&display=swap" data-v5>'
f=ROOT/'assets/v2/site.css';s=f.read_text().split('\n/* STYLE v5')[0];f.write_text(s+'\n'+CSS)
n=0
for p in ROOT.glob('**/*.html'):
    r=str(p.relative_to(ROOT))
    if r.startswith(('admin/','.git','_backup','docs/','node_modules')) or 'privacy' in r: continue
    t=p.read_text()
    if 'data-v5' in t or 'site.css' not in t: continue
    p.write_text(t.replace('</head>',FONT+'</head>',1));n+=1
RV='<script data-rv>(()=>{if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;const io=new IntersectionObserver(e=>e.forEach(x=>{if(x.isIntersecting){x.target.classList.add("in");io.unobserve(x.target)}}),{threshold:.12});document.querySelectorAll("main .section .section-intro, main .section .pic, main .hub-card, main .milestones article, main .biz-list li, main .sitemap-grid .brand-card, main .lab-card, main .cub-card, main .svc-tile, main .svc-card, main .news-cards li").forEach((el,i)=>{el.classList.add("rv");el.style.setProperty("--i",i%4);io.observe(el)})})();</script>'
m=0
for p in ROOT.glob('**/*.html'):
    r=str(p.relative_to(ROOT))
    if r.startswith(('admin/','.git','_backup','docs/','node_modules')) or 'privacy' in r: continue
    t=p.read_text()
    if 'site.css' not in t or 'data-rv' in t: continue
    p.write_text(t.replace('</body>',RV+'</body>',1)); m+=1
print({'pages_font':n,'reveal':m})
