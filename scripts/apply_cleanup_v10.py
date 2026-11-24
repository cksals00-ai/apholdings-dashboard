#!/usr/bin/env python3
"""cleanup v10 (2026-10-15 대표 지시). 여러 번 실행해도 같은 결과.
1) 홈 Decision Intelligence: AP Revenue·Travel 숨김(10-09) 뒤 남은 빈 칸 제거 — AP Light 카드를 한 줄 전체로.
2) IR: 「08 · 창업자」 섹션 삭제, 「09 · 투자자 자료」 → 08.
3) Founder's Lab 폐지: 회사 탭·푸터·사이트맵·버튼 링크 제거, /xx/lab/ 은 회사 소개로 넘기는 noindex 안내 페이지로, sitemap.xml 에서 제외.
"""
import re, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LOCS = ['ko', 'en', 'vi', 'ja', 'zh-cn', 'fr']
CSS_OLD = re.compile(r'site\.css\?v=[0-9A-Za-z.\-]+')
CSS_NEW = 'site.css?v=2.39-c10'
LAB = r'/[a-z-]+/lab/'

def rw(p, f):
    s = open(p, encoding='utf-8').read(); t = f(s)
    if t != s: open(p, 'w', encoding='utf-8').write(t); return 1
    return 0

def links(s):
    s = re.sub(r'<li[^>]*><a href="' + LAB + r'">Founder’s Lab</a></li>', '', s)
    s = re.sub(r'\s*<a (?:class="[^"]*" )?href="' + LAB + r'"(?: aria-current="page")?>Founder’s Lab[^<]*</a>', '', s)
    s = re.sub(r'<div class="actions">\s*</div>', '', s)
    t = re.search(r'<title>([^<]+)</title>', s)
    if t: s = s.replace('<meta property="og:title" content="Founder’s Lab — AP Holdings">', '<meta property="og:title" content="' + t.group(1) + '">')
    return CSS_OLD.sub(CSS_NEW, s)

def ir(s):
    s = re.sub(r'<section class="section soft anchor" id="founder">.*?</section>', '', s, flags=re.S)
    if 'id="founder"' not in s:
        s = re.sub(r'(class="number">)09( ·)', r'\g<1>08\2', s)
    return s

n = 0
lab_pages = {f'{l}/lab/index.html' for l in LOCS}
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith(('_backup', 'site-source', 'node_modules')) or p in lab_pages: continue
    n += rw(p, links)
for l in LOCS:
    p = f'{l}/ir/index.html'
    if os.path.exists(p): n += rw(p, ir)
    lp = f'{l}/lab/index.html'
    stub = (f'<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>AP Holdings</title><meta name="robots" content="noindex,follow"><link rel="canonical" href="https://www.apholdings.kr/{l}/about/">'
            f'<meta http-equiv="refresh" content="0;url=/{l}/about/"></head><body><p><a href="/{l}/about/">AP Holdings</a></p></body></html>\n')
    if os.path.exists(lp) and open(lp, encoding='utf-8').read() != stub:
        open(lp, 'w', encoding='utf-8').write(stub); n += 1
n += rw('apps.html', lambda s: s.replace('/ko/lab/', '/ko/about/'))
n += rw('sitemap.xml', lambda s: re.sub(r'<url><loc>https://www\.apholdings\.kr/[a-z-]+/lab/</loc>.*?</url>\s*', '', s, flags=re.S))
MARK = '/* cleanup v10 (2026-10-15): Decision — AP Light full row */'
css = 'assets/v2/site.css'
c = open(css, encoding='utf-8').read()
if MARK not in c:
    c = c.rstrip('\n') + '\n' + MARK + '\n#decision .commerce-extras{grid-template-columns:1fr}\n@media(min-width:801px){#decision .showcase-lia{grid-template-columns:1fr 1fr;min-height:340px}#decision .showcase-lia .showcase-copy{padding:40px 48px}}\n'
    open(css, 'w', encoding='utf-8').write(c); n += 1

# 4) RANKERS 상태 최신화 — 세 게임 모두 App Store 출시(퀴즈랭커 6810908071 · 투자랭커 6819951527 · 호텔랭커 6819950919, iTunes 조회 10-15)
AS = 'https://apps.apple.com/kr/app/id'
def store(i, t='App Store ↗'):
    return f'<a href="{AS}{i}" target="_blank" rel="noopener noreferrer">{t}</a>'
KO_R = [
    ('<div class="st"><a href="/ko/products/rgrg/">게임 소개 →</a><i>App Store 심사 중</i></div>',
     '<div class="st"><span><a href="/ko/products/rgrg/">게임 소개 →</a> · ' + store(6810908071) + '</span><i>운영 중</i></div>'),
    ('<h3 id="investmentranker">투자랭커</h3><p>같은 시장, 같은 시작 자금. 판단력만으로 수익률을 겨루는 시즌제 투자 시뮬레이션.</p><div class="st"><span></span><i>테스트 중</i></div>',
     '<h3 id="investmentranker">투자랭커</h3><p>같은 시장, 같은 시작 자금. 판단력만으로 수익률을 겨루는 시즌제 투자 시뮬레이션.</p><div class="st">' + store(6819951527) + '<i>운영 중</i></div>'),
    ('<h3 id="hotelranker">호텔랭커</h3><p>가격, 서비스, 운영. 호텔을 경영하며 시즌 성과로 순위를 겨루는 경영 전략 게임.</p><div class="st"><span></span><i>테스트 중</i></div>',
     '<h3 id="hotelranker">호텔랭커</h3><p>가격, 서비스, 운영. 호텔을 경영하며 시즌 성과로 순위를 겨루는 경영 전략 게임.</p><div class="st">' + store(6819950919) + '<i>운영 중</i></div>'),
    ('티어 혜택과 투자·호텔랭커 정산 방식은 정식 출시 전 변경될 수 있습니다.', '티어 혜택과 시즌 정산 방식은 바뀔 수 있습니다.'),
]
def ko_rank(s):
    for a, b in KO_R: s = s.replace(a, b)
    return s
for p in ('ko/rankers/index.html', 'site-source/pages/rankers-ko.html'):
    if os.path.exists(p): n += rw(p, ko_rank)
EN_OLD = '<p class="note">QuizRanker and international edition K-Ranker are in App Store review. Public rankings show QuizRanker category battle records.</p>'
EN_NEW = ('<p class="note">QuizRanker, HotelRanker and InvestRanker are on the App Store — ' + store(6810908071, 'QuizRanker ↗') + ' · '
          + store(6819950919, 'HotelRanker ↗') + ' · ' + store(6819951527, 'InvestRanker ↗')
          + '. The international edition K-Ranker is in review. Public rankings show QuizRanker category battle records.</p>')
n += rw('en/rankers/index.html', lambda s: s.replace(EN_OLD, EN_NEW))

import json
gp = 'site-source/generated-files.json'
g = json.load(open(gp, encoding='utf-8'))
g2 = [x for x in g if not re.match(r'[a-z-]+/lab/index\.html$', x)]
if g2 != g: open(gp, 'w', encoding='utf-8').write(json.dumps(g2, ensure_ascii=False, indent=2) + '\n'); n += 1
n += rw('scripts/check_site.py', lambda s: s.replace("'Founder’s Lab',", ''))
print('changed', n)
