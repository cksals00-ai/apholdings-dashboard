from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def apply():
    source=ROOT/'site-source/pages/b2b-apps.html'
    (ROOT/'business/apps.html').write_text(source.read_text())
    card='<section id="b2b-app-service" class="section"><div class="wrap"><span class="eyebrow">FOR SMALL BUSINESS</span><h2>중소기업 업무 앱, 운영까지.</h2><p>앱·가이드·관리자 구축과 AP 서버 운영. 제작 300만 원부터, 가이드·관리자는 별도 견적, 월 운영 10만 원부터(부가세 별도).</p><a class="button primary" href="/business/apps.html">기업 앱 제작·운영 보기</a></div></section>'
    for rel in ['ko/index.html','ko/about/index.html']:
        p=ROOT/rel
        s=p.read_text()
        if 'id="b2b-app-service"' not in s: p.write_text(s.replace('</main>',card+'</main>'))
    p=ROOT/'sitemap.xml'
    s=p.read_text()
    if '/business/apps.html' not in s: p.write_text(s.replace('</urlset>','<url><loc>https://www.apholdings.kr/business/apps.html</loc><lastmod>2026-10-30</lastmod></url></urlset>'))
if __name__=='__main__': apply()
