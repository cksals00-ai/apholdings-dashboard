#!/usr/bin/env python3
"""CLEANUP v5 (2026-10-09): 기획서와 어긋나는 것 제거. 재실행해도 같음. build_site 재실행 금지. 끝나면 check_site.py.
1 products/safe: 「웹 파일럿」 섹션(#pilot, revenue.apholdings.kr 링크) 제거 — AP Revenue 숨김 정책
2 lab: 히어로와 똑같은 문구를 반복하는 .lab-head 제거
3 about #business: 옛 3묶음(근거 있는 선택·커머스·플레이&런, 커머스에 AP SELECT) → 6부문 줄 목록(divisions.json _sitemap)
4 전 페이지: 옛 /{l}/#portfolio 링크 → /{l}/#businesses
5 products/safe: 🔴 이모지 → 텍스트 표시(색만으로 구분 금지)"""
import re, json, html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; E=lambda s:html.escape(str(s),quote=True)
D=json.loads((ROOT/'site-source/divisions.json').read_text()); LOCS=['ko','en','vi','ja','zh-cn','fr']
DIVS=['intelligence','games','edu','hallyu','entertainment','shop']; LABEL={d:d.capitalize() for d in DIVS}
H={'ko':'여섯 사업.','en':'Six businesses.','vi':'Sáu mảng.','ja':'6つの事業。','zh-cn':'六项业务。','fr':'Six activités.'}
MARK={'ko':'[피함]','en':'[avoid]','vi':'[tránh]','ja':'[回避]','zh-cn':'[避开]','fr':'[à éviter]'}
def biz(l):
    rows=''.join(f'<li><a href="/{l}/{d}/"><b>{LABEL[d]}</b><span>{E(D["_sitemap"][l]["d"][d])}</span></a></li>' for d in DIVS)
    return f'<section class="section anchor" id="business"><div class="wrap"><div class="section-intro"><div><span class="number">03</span><h2>{H[l]}</h2></div></div><ul class="biz-list">{rows}</ul></div></section>'
def fix(rel,l,s):
    s=re.sub(rf'href="/{l}/#portfolio"',f'href="/{l}/#businesses"',s)
    if rel.endswith('products/safe/index.html'):
        s=re.sub(r'<section class="section[^"]*" id="pilot">.*?</section>','',s,count=1,flags=re.S)
        s=s.replace('🔴',MARK[l])
    if rel.endswith('/lab/index.html'):
        s=re.sub(r'<div class="lab-head">.*?</div></div>','',s,count=1,flags=re.S)
    if rel.endswith('/about/index.html'):
        s=re.sub(r'<section class="section[^"]*" id="business">.*?</section>',lambda _:biz(l),s,count=1,flags=re.S)
    return s
def main():
    n=0
    for l in LOCS:
        for f in (ROOT/l).glob('**/index.html'):
            rel=str(f.relative_to(ROOT)); s=f.read_text(); t=fix(rel,l,s)
            if t!=s: f.write_text(t); n+=1
    print({'pages_changed':n})
if __name__=='__main__': main()
