#!/usr/bin/env python3
"""PAGES v5 (2026-10-09): 허브 6개 + 제품 페이지 후처리. 재실행해도 같음. build_site 재실행 금지. 끝나면 check_site.py.
허브: 히어로 아래에 부문 그래픽(인라인 SVG — 제품을 한 줄 흐름의 점으로) 1장 삽입.
제품: ①상태를 운영 중·심사 중·준비 중 3가지로 통일 ②breadcrumb을 「부문 허브 / 제품」으로 ③숨겨진 product-body 제거 ④맨 끝에 「← 부문 허브」 줄 추가."""
import re, json, html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; E=lambda s:html.escape(str(s),quote=True)
D=json.loads((ROOT/'site-source/divisions.json').read_text()); CM=D['_common']
LOCS=['ko','en','vi','ja','zh-cn','fr']; DIVS=['intelligence','games','edu','shop']
LABEL={'intelligence':'Intelligence','games':'Games','edu':'Edu','hallyu':'Hallyu','entertainment':'Entertainment','shop':'Shop'}
PROD={'safe':('intelligence','live'),'light':('intelligence','live'),'select':('intelligence','soon'),'lastwave':('games','soon'),'rgrg':('edu','live'),'cubs':('edu','live'),'craft':('shop','soon'),'lia':('entertainment','live'),'liaselect':('shop','live'),'commerce':('shop','soon')}
def st_key(s):
    s=(s or '')
    for k in ('live','review','soon'):
        if any(s==CM[l][k] for l in LOCS): return k
    return 'soon' if s else 'live'
def hub_svg(l,d):
    its=D[d][l]['items']; n=len(its); W=1200; H=150; pad=90; step=(W-2*pad)/max(n-1,1)
    g=[f'<line x1="{pad}" y1="60" x2="{W-pad}" y2="60" stroke="#141716" stroke-width="1.5"/>']
    for i,it in enumerate(its):
        x=pad+i*step if n>1 else W/2; pid=re.search(r'/products/([a-z]+)/',it.get('url',''))
        k=PROD[pid.group(1)][1] if pid and pid.group(1) in PROD else (st_key(it['status']) if it.get('status') else None); live=k in ('live',None)
        g.append(f'<circle cx="{x:.0f}" cy="60" r="{12 if live else 9}" fill="{"#245548" if live else "#fff"}" stroke="#245548" stroke-width="2"/>')
        g.append(f'<text x="{x:.0f}" y="104" text-anchor="middle" font-size="19" font-weight="600" fill="#141716">{E(it["name"])}</text>')
        lbl = E(CM[l][k]) if k else ''
        g.append(f'<text x="{x:.0f}" y="130" text-anchor="middle" font-size="14" fill="#5b6260">{lbl}</text>')
    lab=' · '.join(E(i['name']) for i in its)
    return f'<section class="hub-graphic"><div class="wrap"><svg viewBox="0 0 {W} {H}" role="img" aria-label="{LABEL[d]}: {lab}" class="hub-svg">{"".join(g)}</svg></div></section>'
def do_hub(l,d,s):
    s=re.sub(r'<section class="hub-graphic">.*?</section>','',s,flags=re.S)
    return s.replace('</section><section class="section hub-section">','</section>'+hub_svg(l,d)+'<section class="section hub-section">',1)
def do_prod(l,pid,s):
    d,k=PROD[pid]
    s=re.sub(r'(<section class="page-hero">.*?)<span class="status">[^<]*</span>',lambda m:m.group(1)+f'<span class="status">{E(CM[l][k])}</span>',s,count=1,flags=re.S)
    s=re.sub(r'<div class="breadcrumb">.*?</div>',lambda m:f'<div class="breadcrumb"><a href="/{l}/{d}/">{LABEL[d]}</a> / '+re.sub(r'.*/\s*','',re.sub('<[^>]+>','',m.group(0))).strip()+'</div>' if '<a' in m.group(0) else m.group(0),s,count=1,flags=re.S)
    s=re.sub(r'<div class="product-body" hidden>.*?</div>(?=</div></section>)','',s,flags=re.S)
    s=re.sub(r'<section class="section back-hub">.*?</section>','',s,flags=re.S)
    return s.replace('</main>',f'<section class="section back-hub"><div class="wrap"><a class="text-link" href="/{l}/{d}/">← {LABEL[d]}</a></div></section></main>',1)
def main():
    n=0
    for l in LOCS:
        for d in DIVS:
            f=ROOT/l/d/'index.html'
            if f.exists():
                s=f.read_text(); t=do_hub(l,d,s)
                if t!=s: f.write_text(t); n+=1
        for pid in PROD:
            f=ROOT/l/'products'/pid/'index.html'
            if f.exists():
                s=f.read_text(); t=do_prod(l,pid,s)
                if t!=s: f.write_text(t); n+=1
    print({'pages_changed':n})
if __name__=='__main__': main()
