#!/usr/bin/env python3
"""release v11 (2026-10-15 대표 지시). 여러 번 실행해도 같은 결과.
1) 아빠랑 나랑 App Store 출시(1.0, id6821352092, 10-14) 반영 — 제품 페이지·홈·Edu·Sports·푸터·사이트맵 6개 언어.
2) 퀴즈랭커 App Store 출시(id6810908071) 반영 — 제품 페이지 6개 언어, ko 히어로 줄바꿈 정리.
3) 한국어 제목·리드 줄바꿈: 낱말 중간에서 끊기지 않게(word-break:keep-all).
"""
import re, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LOCS = ['ko', 'en', 'vi', 'ja', 'zh-cn', 'fr']
AS = 'https://apps.apple.com/kr/app/id'
DAD, QUIZ = AS + '6821352092', AS + '6810908071'
EXT = ' target="_blank" rel="noopener noreferrer"'
n = 0
def rw(p, f):
    global n
    if not os.path.exists(p): return
    s = open(p, encoding='utf-8').read(); t = f(s)
    if t != s: open(p, 'w', encoding='utf-8').write(t); n += 1

# ---------- 1) 아빠랑 나랑 ----------
def dad_common(s):
    s = s.replace('<a href="/ko/products/dadandme/">아빠랑 나랑 · 심사 중</a>', '<a href="/ko/products/dadandme/">아빠랑 나랑</a>')
    s = re.sub(r'<span class="f-soon">(?:아빠랑 나랑|Dad &amp; Me) · 심사 준비 중</span>', '<a href="/ko/products/dadandme/">아빠랑 나랑</a>', s)
    s = re.sub(r'<span class="f-soon">Dad &amp; Me · [^<]*</span>', f'<a href="{DAD}">Dad &amp; Me</a>', s)
    s = s.replace('<li style="margin-bottom:16px">Dad &amp; Me · 심사 준비 중</li>', '<li style="margin-bottom:16px"><a href="/ko/products/dadandme/">아빠랑 나랑</a></li>')
    s = s.replace('무료로 약속 하나를 끝까지. 현재 App Store 심사 중.', '무료로 약속 하나를 끝까지. 지금 App Store에서.')
    s = re.sub(r'(<article class="product-card hub-card"[^>]*>)<span class="status">App Store 심사 중</span>(<h3>아빠랑 나랑</h3>)', r'\1<span class="status">운영 중</span>\2', s)
    s = s.replace('font-weight="600" fill="#141716">Dad &amp; Me</text><text x="770" y="130" text-anchor="middle" font-size="14" fill="#5b6260">심사 준비 중</text>',
                  'font-weight="600" fill="#141716">Dad &amp; Me</text><text x="770" y="130" text-anchor="middle" font-size="14" fill="#5b6260">운영 중</text>')
    return s

def dad_page(s):
    s = s.replace('현재 App Store 심사 중."', 'App Store에서 무료로 시작할 수 있어요."')
    s = s.replace('<span class="dad-status">App Store 심사 중 · 출시 준비</span>', '<span class="dad-status">App Store 운영 중 · 무료</span>')
    s = s.replace('<a class="button primary" href="#how">어떻게 함께하나요? ↓</a><p class="dad-note">현재 다운로드 전 심사 단계입니다.<br>승인 후 이 페이지에서 App Store로 연결합니다.</p>',
                  f'<div class="actions"><a class="button primary" href="{DAD}"{EXT}>App Store에서 받기 ↗</a><a class="button" href="#how">어떻게 함께하나요? ↓</a></div>')
    s = s.replace('한 번 구매, 구독 없음. 현재 앱과 함께 심사 중입니다.', '한 번 구매, 구독 없음.')
    s = s.replace('<p class="dad-note">2026년 10월 13일 기준 iOS 1.0(1) 및 가족 패스 심사 대기.<br>승인과 실제 스토어 공개를 확인한 뒤 다운로드 안내를 엽니다.</p>',
                  f'<p class="dad-note">iOS 1.0 · 2026년 10월 14일 App Store 출시.<br><a href="{DAD}"{EXT}>App Store에서 받기 ↗</a></p>')
    return s

for p in glob.glob('**/*.html', recursive=True):
    if p.startswith(('_backup', 'node_modules')): continue
    rw(p, dad_common)
for p in ('ko/products/dadandme/index.html', 'site-source/pages/dadandme-ko.html'):
    rw(p, dad_page)


# ---------- 1b) 허브·사이트맵·IR 상태 문구 ----------
LIVE = {'ko': '운영 중', 'en': 'Live', 'vi': 'Đang hoạt động', 'ja': '運営中', 'zh-cn': '运营中', 'fr': 'En service'}
IR_Q = {'ko': ('QuizRanker 6인 실시간 대결 빌드 · 출시 준비', 'QuizRanker 6인 실시간 대결 · App Store 출시'),
        'en': ('QuizRanker six-player live match build · preparing for release', 'QuizRanker six-player live match · on the App Store'),
        'vi': ('QuizRanker bản dựng trận đấu trực tiếp sáu người chơi · đang chuẩn bị phát hành', 'QuizRanker trận đấu trực tiếp sáu người chơi · đã có trên App Store'),
        'ja': ('QuizRanker 6人同時ライブ対戦ビルド · リリース準備中', 'QuizRanker 6人同時ライブ対戦 · App Storeで配信中'),
        'zh-cn': ('QuizRanker 六人实时对战版本 · 发布准备中', 'QuizRanker 六人实时对战 · 已在 App Store 上架'),
        'fr': ('QuizRanker, version de match en direct à six joueurs · préparation de la publication', 'QuizRanker, match en direct à six joueurs · disponible sur l’App Store')}
def hubs(l):
    live = LIVE[l]
    def f(s):
        s = re.sub(r'(<article class="product-card hub-card"[^>]*>)<span class="status">[^<]*</span>(<h3>(?:Dad &amp; Me|아빠랑 나랑)</h3>)', lambda m: m.group(1) + f'<span class="status">{live}</span>' + m.group(2), s)
        s = re.sub(r'(>Dad &amp; Me</text><text[^>]*>)[^<]*(</text>)', lambda m: m.group(1) + live + m.group(2), s)
        if l != 'ko':
            s = re.sub(r'<li style="margin-bottom:16px">Dad &amp; Me · [^<]*</li>', f'<li style="margin-bottom:16px"><a href="{DAD}">Dad &amp; Me ↗</a></li>', s)
        a, b = IR_Q[l]; s = s.replace(a, b)
        if l == 'ko':
            s = re.sub(r'(<article class="product-card hub-card"[^>]*>)<span class="status">출시 준비 중</span>(<h3>퀴즈랭커 \(한국어판\)</h3>)', r'\1<span class="status">운영 중</span>\2', s)
            s = re.sub(r'(>퀴즈랭커 \(한국어판\)</text><text[^>]*>)출시 준비 중(</text>)', r'\1운영 중\2', s)
        if l == 'en':
            s = s.replace('Dad &amp; Kid Project', 'Dad &amp; Me')
            s = re.sub(r'(<article class="product-card hub-card"[^>]*>)<span class="status">Coming soon</span>(<h3>Dad &amp; Me</h3>)', r'\1<span class="status">Live</span>\2', s)
            s = re.sub(r'(>Dad &amp; Me</text><text[^>]*>)Coming soon(</text>)', r'\1Live\2', s)
        return s
    return f
for l in LOCS:
    for pg in ('sports', 'edu', 'ir', 'sitemap'):
        rw(f'{l}/{pg}/index.html', hubs(l))


# ---------- 1c) About 창업자 이야기 마지막 문장 ----------
STORY = {'ko': ('그래서 「아빠와 아이 프로젝트」로 준비하고 있습니다.', '그래서 「아빠랑 나랑」으로 만들어 App Store에 내놓았습니다.'),
         'en': ('So we are preparing it as the Dad &amp; Kid Project.', 'So we built it into Dad &amp; Me, now on the App Store.'),
         'vi': ('Vì thế chúng tôi đang chuẩn bị nó thành Dự án Bố &amp; Con.', 'Vì thế chúng tôi đã làm thành Dad &amp; Me, nay đã có trên App Store.'),
         'ja': ('そこで「パパと子どもプロジェクト」として準備しています。', 'そこで「Dad &amp; Me」としてApp Storeで公開しました。'),
         'zh-cn': ('于是我们把它做成“爸爸与孩子计划”来准备。', '于是我们把它做成了 “Dad &amp; Me”，现已在 App Store 上架。'),
         'fr': ('Nous la préparons donc comme le Projet Papa &amp; Enfant.', 'Nous en avons donc fait Dad &amp; Me, désormais sur l’App Store.')}
for l in LOCS:
    a, b = STORY[l]
    rw(f'{l}/about/index.html', lambda s, a=a, b=b: s.replace(a, b))

# ---------- 2) 퀴즈랭커 ----------
OLD_DESC = '가족·친구·동료와 다양한 주제의 퀴즈를 즐길 수 있도록 개발하고 있습니다. 웹 게임은 AP Games에서 안내하며 iPhone 앱은 출시 준비 중입니다.'
NEW_DESC = '가족·친구·동료와 다양한 주제의 퀴즈를 함께 즐기는 실시간 퀴즈 게임. iPhone은 App Store, 웹은 AP Games에서.'
TODAY = {'ko': ('iPhone · 출시 준비 중.', 'iPhone · App Store 출시.'),
         'en': ('iPhone · preparing for release.', 'iPhone · now on the App Store.'),
         'vi': ('iPhone · đang chuẩn bị phát hành.', 'iPhone · đã có trên App Store.'),
         'ja': ('iPhone · リリース準備中。', 'iPhone · App Storeで配信中。'),
         'zh-cn': ('iPhone · 发布筹备中。', 'iPhone · 已在 App Store 上架。'),
         'fr': ('iPhone · sortie en préparation.', 'iPhone · disponible sur l’App Store.')}
def quiz(l):
    def f(s):
        a, b = TODAY[l]
        s = s.replace(f'<h2>{a}</h2>', f'<h2>{b}</h2>')
        s = re.sub(r'(<div class="cta-block"><span class="number">06 · [^<]*</span><h2>[^<]*</h2><p>[^<]*</p><div class="actions">)<a class="button primary" href="(https://games\.apholdings\.kr/[a-z-]+/)">AP Games</a>',
                   lambda m: m.group(1) + f'<a class="button primary" href="{QUIZ}"{EXT}>App Store ↗</a><a class="button" href="{m.group(2)}">AP Games</a>', s)
        if l == 'ko':
            s = s.replace(OLD_DESC, NEW_DESC)
            s = s.replace('<span class="status">iOS 출시 준비 중</span><h1 class="product-name">QuizRanker (퀴즈랭커)</h1><h2>여러 이용자가 함께 참여하는 실시간 퀴즈 게임입니다.</h2><p class="lead">' + NEW_DESC + '</p>',
                          '<span class="status">App Store 운영 중</span><h1 class="product-name">퀴즈랭커</h1><h2>여럿이 함께 겨루는<br>실시간 퀴즈 게임.</h2><p class="lead">가족·친구·동료와 다양한 주제의 퀴즈를 함께 즐겨요.<br>iPhone은 App Store에서, 웹은 AP Games에서.</p>'
                          + f'<div class="actions"><a class="button primary" href="{QUIZ}"{EXT}>App Store에서 받기 ↗</a><a class="button" href="https://games.apholdings.kr/ko/">AP Games</a></div>')
        return s
    return f
for l in LOCS:
    rw(f'{l}/products/rgrg/index.html', quiz(l))

# ---------- 3) 한국어 줄바꿈 ----------
MARK = '/* release v11 (2026-10-15): 한국어 제목·리드 낱말 단위 줄바꿈 */'
def css(c):
    if MARK in c: return c
    return c.rstrip('\n') + '\n' + MARK + '\nhtml[lang="ko"] h1,html[lang="ko"] h2,html[lang="ko"] h3,html[lang="ko"] .lead,html[lang="ko"] .intro-side p{word-break:keep-all;overflow-wrap:break-word}\n'
rw('assets/v2/site.css', css)
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith(('_backup', 'node_modules')): continue
    rw(p, lambda s: s.replace('site.css?v=2.39-c10', 'site.css?v=2.40-r11'))
# 버튼은 CSS가 화살표를 붙이므로 글자 ↗ 제거
def noarrow(t):
    return re.sub(r'(<a class="button[^"]*" href="https://apps\.apple\.com[^"]*"[^>]*>)([^<]*?) ↗</a>', r'\1\2</a>', t)
for p in [f'{l}/products/rgrg/index.html' for l in LOCS] + ['ko/products/dadandme/index.html', 'site-source/pages/dadandme-ko.html']:
    rw(p, noarrow)
def divs(t):
    for a, b in STORY.values():
        t = t.replace(a, b).replace(a.replace('&amp;', '&'), b.replace('&amp;', '&'))
    return t
rw('site-source/divisions.json', divs)
print('changed', n)
