"""Idempotent Dad & Me registration on the approved public site; no analytics SDK."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1]
def apply():
    for f in (ROOT/'ko').rglob('*.html'):
        t=f.read_text();t=t.replace('<span class="f-soon">Dad &amp; Me · 심사 준비 중</span>','<a href="/ko/products/dadandme/">아빠랑 나랑 · 심사 중</a>')
        if t!=f.read_text():f.write_text(t)
    f=ROOT/'ko/sports/index.html'
    if f.is_file():
        t=f.read_text();t=re.sub(r'<article[^>]*>(?:(?!</article>).)*<h3>Dad &amp; Me</h3>.*?</article>','<article class="product-card hub-card"><span class="status">App Store 심사 중</span><h3>아빠랑 나랑</h3><p class="tag">부모와 아이의 약속 앱</p><p class="desc">달리기·독서·우리만의 약속을 함께 기록해요. 폰 하나로도 시작할 수 있어요.</p><a class="text-link" href="/ko/products/dadandme/">앱 살펴보기 →</a></article>',t,count=1,flags=re.S);f.write_text(t)
    template=(ROOT/'ko/edu/index.html').read_text()
    main=(ROOT/'site-source/pages/dadandme-ko.html').read_text()
    page=re.sub(r'<main\b[^>]*>.*?</main>',main,template,count=1,flags=re.S)
    page=re.sub(r'<title>.*?</title>','<title>아빠랑 나랑 — 약속 하나, 함께 쌓는 하루 | AP Edu</title>',page,count=1)
    page=re.sub(r'<link rel="alternate"[^>]+>','',page)
    page=re.sub(r'<link rel="canonical"[^>]+>','<link rel="canonical" href="https://www.apholdings.kr/ko/products/dadandme/">',page,count=1)
    page=re.sub(r'<meta name="description"[^>]+>','<meta name="description" content="부모와 아이가 약속 하나를 정하고 도장판을 함께 채우는 앱. 무료 약속 하나, 달리기·책읽기·응원·룰렛. 현재 App Store 심사 중.">',page,count=1)
    for key,value in [('title','아빠랑 나랑 — 함께 쌓는 하루'),('description','약속 하나, 도장판 하나, 선물 하나. AP Edu의 가족 약속 앱.'),('url','https://www.apholdings.kr/ko/products/dadandme/'),('image','https://www.apholdings.kr/media/dadandme/home.png')]:
        tag=f'<meta property="og:{key}" content="{value}">'
        if f'property="og:{key}"' in page: page=re.sub(rf'<meta property="og:{key}"[^>]+>',tag,page,count=1)
        else: page=page.replace('</head>',tag+'</head>')
    page=page.replace('</head>','<link rel="stylesheet" href="/assets/v2/dadandme.css?v=20261013"></head>')
    p=ROOT/'ko/products/dadandme/index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(page)
    card='<article class="product-card hub-card" data-product="dadandme"><span class="status">App Store 심사 중</span><h3>아빠랑 나랑</h3><p class="tag">약속 하나, 함께 쌓는 하루</p><p class="desc">달리기·책읽기·우리만의 약속을 정하고 도장판을 채워요. 룰렛과 응원, 절반에서 열리는 편지까지. 약속 하나는 무료로 끝까지.</p><a class="text-link" href="/ko/products/dadandme/?utm_source=ap_edu&amp;utm_medium=website&amp;utm_campaign=dadandme_launch">앱 살펴보기 →</a></article>'
    p=ROOT/'ko/edu/index.html';s=p.read_text();s=re.sub(r'<article[^>]*>(?:(?!</article>).)*<h3>아빠와 아이 프로젝트</h3>.*?</article>',card,s,count=1,flags=re.S)
    s=s.replace('아빠와 아이 프로젝트','아빠랑 나랑').replace('Dad &amp; Me','아빠랑 나랑');p.write_text(s)
    p=ROOT/'ko/index.html';s=p.read_text()
    if 'data-product="dadandme-feature"' not in s:
        feature='<section class="section" data-product="dadandme-feature"><div class="wrap"><span class="eyebrow">AP EDU · NEW APP</span><div class="section-intro"><h2>아빠랑 나랑.<br>약속 하나, 함께 쌓는 하루.</h2><p>부모와 아이의 작은 약속을 도장으로 기록해요.<br>무료로 약속 하나를 끝까지. 현재 App Store 심사 중.</p><a class="button primary" href="/ko/products/dadandme/?utm_source=ap_home&amp;utm_medium=website&amp;utm_campaign=dadandme_launch">앱 살펴보기 →</a></div></div></section>'
        s=s.replace('<section class="story-band">',feature+'<section class="story-band">',1);p.write_text(s)
    p=ROOT/'ko/sitemap/index.html';s=p.read_text()
    if '/ko/products/dadandme/' not in s:s=s.replace('</main>','<section class="section"><div class="wrap"><h2>AP Edu</h2><a class="text-link" href="/ko/products/dadandme/">아빠랑 나랑 · 가족 약속 앱</a></div></section></main>');p.write_text(s)
    p=ROOT/'sitemap.xml';s=p.read_text()
    if '/ko/products/dadandme/' not in s:s=s.replace('</urlset>','<url><loc>https://www.apholdings.kr/ko/products/dadandme/</loc><lastmod>2026-10-13</lastmod></url></urlset>');p.write_text(s)
    p=ROOT/'site-source/status.json';d=json.loads(p.read_text());d['products']['dadandme']={'stage':'in_review','appId':'6821352092','checked':'2026-10-13T15:24:00+09:00','facts':{'appVersion':'1.0','build':'1','appLive':False,'submissionId':'57d3ec9f-1f50-4849-b1ec-c73c29d32abf'},'manual':[{'ko':'앱과 Family Pass 함께 심사 대기','en':'App and Family Pass waiting for review'}]};p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':apply()
