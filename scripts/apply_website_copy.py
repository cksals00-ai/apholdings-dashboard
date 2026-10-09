#!/usr/bin/env python3
"""Apply the approved Korean copy after v4/v5/v6 page generation. Idempotent."""
from pathlib import Path
import json, re, html
import apply_ia_v4 as ia
import apply_pages_v5 as pages
ROOT=Path(__file__).resolve().parents[1]
M=json.loads((ROOT/'site-source/website-copy-ko.json').read_text())
E=html.escape
DESCRIPTION='AP Holdings는 식품 성분·영양 정보 조회 서비스, 한국어 학습 콘텐츠, 온라인 게임, AI 캐릭터 콘텐츠와 한국 상품의 해외 판매 사업을 운영·개발합니다.'
def rewrite(s):
    for old,new in sorted(M.items(),key=lambda x:len(x[0]),reverse=True):
        s=s.replace(E(old,quote=True),E(new,quote=True))
    # Narrative quotations and article titles stay intact; only descriptive endings change.
    for old,new in {'영상에서 본다': '콘텐츠 확인', '다시 산다': '재구매', '저장한다': '상품 저장', '산다': '주문', '받는다': '배송'}.items():
        s=s.replace('>'+old+'<','>'+new+'<')
    return s

def source_rewrite(v):
    if isinstance(v,str):
        for old,new in sorted(M.items(),key=lambda x:len(x[0]),reverse=True):v=v.replace(old,new)
        return v
    if isinstance(v,list):return [source_rewrite(x) for x in v]
    if isinstance(v,dict):return {k:source_rewrite(x) for k,x in v.items()}
    return v

def main():
    for name in ['locales/ko.json','home-copy.json','ir-v3.json']:
        p=ROOT/'site-source'/name;d=json.loads(p.read_text())
        if name in ('home-copy.json','ir-v3.json'):d['ko']=source_rewrite(d['ko'])
        else:d=source_rewrite(d)
        p.write_text(json.dumps(d,ensure_ascii=False,indent=1)+'\n')
    for div in ia.DIVS:
        p=ROOT/'ko'/div/'index.html';s=p.read_text()
        body=ia.ent_main('ko') if div=='entertainment' else ia.hub_main('ko',div)
        s=re.sub(r'<main id="main">.*?</main>',lambda _:body,s,count=1,flags=re.S)
        if div in pages.DIVS:s=pages.do_hub('ko',div,s)
        c=ia.D[div]['ko'];s=ia.retitle(s,c['title']+' — AP Holdings',c['lead'])
        p.write_text(s)
    p=ROOT/'ko/sitemap/index.html';s=p.read_text();s=re.sub(r'<main id="main">.*?</main>',lambda _:ia.sitemap_main('ko'),s,count=1,flags=re.S);p.write_text(s)
    targets=[ROOT/'ko/index.html',ROOT/'ko/about/index.html',ROOT/'ko/ir/index.html',ROOT/'ko/rankers/index.html']+list((ROOT/'ko/products').glob('*/index.html'))
    for p in targets:
        s=rewrite(p.read_text())
        if p==ROOT/'ko/index.html':
            s=re.sub(r'(<div class="hv6-copy">.*?<h1>).*?</h1>',lambda m:m[1]+'AI 기반 정보 서비스부터<br>교육·게임·한국 상품 판매까지</h1>',s,count=1,flags=re.S)
            s=re.sub(r'<p class="hv6-rot">.*?</p>','<p class="hv6-description">'+E(DESCRIPTION)+'</p>',s,count=1,flags=re.S)
            s=s.replace('지금 운영 중','앱·게임 이용 및 상품 안내')
            s=re.sub(r'<li><span class="status">운영 중</span><h3>Lia Select Shop</h3>', '<li><span class="status">판매 준비 중</span><h3>Lia Select Shop</h3>',s)
            s=s.replace('>쇼핑하기 ↗</a>','>상품 안내 ↗</a>')
            steps=[('식품 정보 조회','AP Safe·AP Light로 원재료와 열량을 확인합니다.'),('교육·게임·AI 콘텐츠','한글 학습, 온라인 게임과 캐릭터 콘텐츠를 제공합니다.'),('한국 상품 해외 판매','Lia Select Shop을 중심으로 상품을 소개하고 판매를 준비합니다.')]
            for i,(h,d) in enumerate(steps):
                s=re.sub(r'(<li class="rv" style="--i:'+str(i)+r'">.*?<h3>).*?</h3><p>.*?</p>',lambda m:m[1]+h+'</h3><p>'+d+'</p>',s,count=1,flags=re.S)
            s=ia.retitle(s,'AP Holdings — 식품 정보·교육·게임·AI 콘텐츠·해외 판매',DESCRIPTION)
        if p==ROOT/'ko/products/rgrg/index.html':
            s=re.sub(r'(<section class="page-hero">.*?)<span class="status">운영 중</span>',r'\1<span class="status">iOS 출시 준비 중</span>',s,count=1,flags=re.S)
        if p==ROOT/'ko/products/liaselect/index.html':
            s=re.sub(r'(<section class="page-hero">.*?)<span class="status">운영 중</span>',r'\1<span class="status">콘텐츠 운영 · 판매 준비 중</span>',s,count=1,flags=re.S)
        if p==ROOT/'ko/about/index.html':s=ia.retitle(s,'회사 소개 — AP Holdings',DESCRIPTION)
        # Keep structured metadata consistent with the page description.
        desc=re.search(r'<meta name="description" content="([^"]*)"',s)
        if desc:
            def schema(m):
                data=json.loads(m[1]);data['description']=html.unescape(desc[1]);return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+'</script>'
            s=re.sub(r'<script type="application/ld\+json">(.*?)</script>',schema,s,flags=re.S)
        p.write_text(s)
    css=ROOT/'assets/v2/website-copy.css'
    css.write_text('''/* Korean service description: retain the existing homepage visual. */
html[lang="ko"] .hv6 h1{font-size:clamp(2rem,4.1vw,4rem);line-height:1.3;word-break:keep-all;overflow-wrap:anywhere}
.hv6-description{margin-top:24px;font-size:clamp(1rem,1.4vw,1.2rem);line-height:1.8;color:#c9d6d1;word-break:keep-all}
html[lang="ko"] .page-hero h1{word-break:keep-all;overflow-wrap:anywhere}
''')
    # Korean navigation labels remain compact; service descriptors accompany them in hubs/footer.
    labels={'Home':'홈','News':'뉴스','About':'회사 소개','Admin':'관리자','Sitemap':'사이트맵'}
    for p in (ROOT/'ko').rglob('*.html'):
        s=p.read_text()
        if p in targets:s=rewrite(s)
        for old,new in labels.items():s=re.sub(r'(<a\b[^>]*>)'+old+r'(</a>)',lambda m:m[1]+new+m[2],s)
        for div,label in [('intelligence','식품 정보'),('games','온라인 게임'),('edu','한국어 학습'),('entertainment','AI 콘텐츠'),('shop','해외 판매')]:
            s=re.sub(r'(<b><a href="/ko/'+div+r'/">)'+ia.LABEL[div]+r'(</a></b>)',lambda m:m[1]+ia.LABEL[div]+' · '+label+m[2],s)
        s=s.replace('Build with AP.</h3>','서비스·사업 협력 문의</h3>')
        if p in targets or p.parent.name in ia.DIVS:
            if '/assets/v2/website-copy.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="/assets/v2/website-copy.css?v=20261009"></head>')
        p.write_text(s)
    print('Korean website copy applied; other locales and article bodies preserved.')
if __name__=='__main__':main()
