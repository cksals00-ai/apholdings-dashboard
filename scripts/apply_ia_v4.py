#!/usr/bin/env python3
"""IA v4 (2026-10-09, 대표 결정): 상단 메뉴 11칸 + 휴대폰 5칸(Business 그룹), 부문 6개.

- 넓은 화면: Home · Intelligence · Games · Edu · Hallyu · Entertainment · Shop · News · About · Admin · Sitemap (+언어). 메뉴명은 6개 언어 모두 영어.
- 휴대폰(≤1180px): Home · Business(펼치면 부문 6개) · News · About · Admin · Sitemap.
- 허브: intelligence · games · edu · hallyu(새) · entertainment(새, 캐릭터) · shop. /media/ → /entertainment/ 넘김. /products/rankers/ → /rankers/ 넘김.
- About: 창업자 이야기 섹션. about/brand/ir/lab 상단에 회사 탭.
- 사이트맵 페이지 6개 언어. 푸터 7칸.
생성된 HTML을 직접 고친다(build_site 재실행 금지). 여러 번 실행해도 결과가 같다. 원고는 site-source/divisions.json.
"""
import re, json, html
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
LOCS = ['ko', 'en', 'vi', 'ja', 'zh-cn', 'fr']
DIVS = ['intelligence', 'games', 'edu', 'hallyu', 'entertainment', 'shop']
LABEL = {'intelligence': 'Intelligence', 'games': 'Games', 'edu': 'Edu', 'hallyu': 'Hallyu', 'entertainment': 'Entertainment', 'shop': 'Shop'}
E = lambda s: html.escape(str(s), quote=True)
D = json.loads((ROOT / 'site-source' / 'divisions.json').read_text())
CO = D['_company']; CM = D['_common']
CSS_V = 'site.css?v=2.30'
JS_V = 'site.js?v=20261009-ia4'

def exists(l, p): return (ROOT / l / p / 'index.html').exists()
def rankers_url(l): return f'/{l}/rankers/' if exists(l, 'rankers') else '/en/rankers/'
def brand_url(l): return f'/{l}/brand/' if exists(l, 'brand') else '/ko/brand/'
def sub(l): return l if l in ('ko', 'en') else 'en'
def fill(u, l): return u.replace('{l}', l).replace('{rankers}', rankers_url(l)).replace('{edu}', sub(l)).replace('{games}', sub(l))

SECTION_OF = [
 ('intelligence', ['/intelligence/', '/products/safe/', '/products/light/', '/products/select/']),
 ('games', ['/games/', '/products/lastwave/', '/rankers/']),
 ('edu', ['/edu/', '/products/rgrg/']),
 ('hallyu', ['/hallyu/', '/products/cubs/', '/products/craft/']),
 ('entertainment', ['/entertainment/', '/products/lia/']),
 ('shop', ['/shop/', '/products/commerce/', '/products/liaselect/']),
 ('news', ['/news/']),
 ('about', ['/about/', '/brand/', '/ir/', '/lab/']),
 ('sitemap', ['/sitemap/']),
 ('home', ['/']),
]
def section_for(rel):
    path = '/' + rel.split('/', 1)[1] if '/' in rel else '/'
    for sec, keys in SECTION_OF:
        if sec == 'home':
            if path == '/index.html': return 'home'
            continue
        if any(path.startswith(k) for k in keys): return sec
    return None

# ---------- header nav ----------
def nav_items(l):
    return ([('home', f'/{l}/', 'Home')] + [(d, f'/{l}/{d}/', LABEL[d]) for d in DIVS] +
            [('news', f'/{l}/news/', 'News'), ('about', f'/{l}/about/', 'About'), ('admin', '/admin/', 'Admin'), ('sitemap', f'/{l}/sitemap/', 'Sitemap')])

LANG_NAME = {'ko': '한국어', 'en': 'English', 'vi': 'Tiếng Việt', 'ja': '日本語', 'zh-cn': '简体中文', 'fr': 'Français'}
def nav_html(l, sec, lang_items=''):
    cur = lambda s: ' aria-current="page"' if sec == s else ''
    desk = ''.join('<a href="%s"%s%s>%s</a>' % (u, cur(k), ' class="nav-admin"' if k == 'admin' else '', t) for k, u, t in nav_items(l))
    desktop = f'<nav class="desktop-nav nav-v4" aria-label="Main">{desk}</nav>'
    divs = ''.join(f'<a href="/{l}/{d}/"{cur(d)}>{LABEL[d]}</a>' for d in DIVS)
    g_open = ' open' if sec in DIVS else ''
    mobile = (f'<nav aria-label="Mobile" class="m-nav-v4"><a href="/{l}/"{cur("home")}>Home</a>'
              f'<details class="m-group"{g_open}><summary>{CM[l]["business"]}</summary><div>{divs}</div></details>'
              f'<a href="/{l}/news/"{cur("news")}>News</a><a href="/{l}/about/"{cur("about")}>About</a>'
              f'<a href="/admin/" class="nav-admin">Admin</a><div class="m-foot"><a href="/{l}/sitemap/" class="m-sitemap"{cur("sitemap")}>Sitemap</a>'
              f'<details class="m-lang"><summary>{LANG_NAME[l]} ⌄</summary><div>{lang_items}</div></details></div></nav>')
    return desktop, mobile

# ---------- footer ----------
def footer_map(l):
    t = CO[l]; a = lambda u, x: f'<a href="{u}">{E(x)}</a>'
    head = lambda d: f'<b><a href="/{l}/{d}/">{LABEL[d]}</a></b>'
    def items(d, limit=5):
        out = []
        for it in D[d][l]['items'][:limit]:
            if it.get('url'): out.append(a(fill(it['url'], l), it['name']))
            else: out.append(f'<span class="f-soon">{E(it["name"])} · {E(it.get("status", CM[l]["soon"]))}</span>')
        return ''.join(out)
    ent = D['entertainment'][l]
    cols = [
     '<div><b>AP Holdings</b>' + a(f'/{l}/about/', t['about']) + a(brand_url(l), t['brand']) + a(f'/{l}/ir/', 'IR / INVESTORS') + a(f'/{l}/lab/', 'Founder’s Lab') + a(f'/{l}/news/', 'AP News') + a(f'/{l}/sitemap/', t['sitemap']) + '</div>',
     '<div>' + head('intelligence') + items('intelligence') + '</div>',
     '<div>' + head('games') + items('games') + '</div>',
     '<div>' + head('edu') + items('edu') + '</div>',
     '<div>' + head('hallyu') + items('hallyu', 4) + '</div>',
     '<div>' + head('entertainment') + a(f'/{l}/products/lia/', 'LIA') + a(f'/{l}/entertainment/#cubs', 'Hangeul Cubs') + '</div>',
     '<div>' + head('shop') + items('shop', 3) + '</div>',
    ]
    return '<div class="footer-map footer-map-v3 footer-map-v4">' + ''.join(cols) + '</div>'

# ---------- hub pages ----------
def hub_main(l, d):
    c = D[d][l]; common = CM[l]
    cards = []
    for it in c['items']:
        url = fill(it.get('url', ''), l); ext = url.startswith('http')
        st = f'<span class="status">{E(it["status"])}</span>' if it.get('status') else ''
        lk = (f'<a class="text-link" href="{E(url)}"' + (' target="_blank" rel="noopener noreferrer"' if ext else '') + f'>{E(it.get("cta", common["more"]))}{" ↗" if ext and not it.get("cta", "").endswith("↗") else ""}</a>') if url else ''
        cards.append(f'<article class="product-card hub-card">{st}<h3>{E(it["name"])}</h3><p class="tag">{E(it["tag"])}</p><p class="desc">{E(it["desc"])}</p>{lk}</article>')
    primary = ''
    if c.get('primary'):
        p = c['primary']; u = fill(p['url'], l); ext = u.startswith('http')
        primary = f'<div class="actions"><a class="button primary" href="{E(u)}"' + (' target="_blank" rel="noopener noreferrer"' if ext else '') + f'>{E(p["label"])}</a></div>'
    who = f'<p class="hub-who"><b>{E(common["for"])}</b> {E(c["for"])}</p>'
    links = f'<div class="hub-links"><a class="text-link" href="/{l}/ir/">{E(common["ir"])}</a><a class="text-link" href="{brand_url(l)}">{E(common["brand"])}</a></div>'
    return (f'<main id="main"><section class="page-hero hub-hero"><div class="wrap"><span class="eyebrow">{E(c["eyebrow"])}</span>'
            f'<h1>{E(c["title"])}</h1><p class="lead">{E(c["lead"])}</p>{who}{primary}</div></section>'
            f'<section class="section hub-section"><div class="wrap"><div class="grid-3 hub-grid">{"".join(cards)}</div>{links}</div></section></main>')

CUB_IMG = {'다호': 'daho', 'Daho': 'daho', 'ダホ': 'daho', '꼬비': 'kkobi', 'Kkobi': 'kkobi', 'コビ': 'kkobi', '아리': 'aari', 'Aari': 'aari', 'アリ': 'aari', '라미': 'rami', 'Rami': 'rami', 'ラミ': 'rami'}
CUB_ORDER = ['daho', 'kkobi', 'aari', 'rami']
def ent_main(l):
    c = D['entertainment'][l]; common = CM[l]; lia = c['lia']; cubs = c['cubs']
    who = f'<p class="hub-who"><b>{E(common["for"])}</b> {E(c["for"])}</p>'
    lia_links = ''.join(f'<a class="text-link" href="{E(fill(u, l))}"' + (' target="_blank" rel="noopener noreferrer"' if u.startswith('http') else '') + f'>{E(x)}</a>' for u, x in lia['links'])
    lia_html = (f'<section class="section ent-section" id="lia"><div class="wrap"><div class="lia-feature ent-lia"><div class="photo"><img src="/media/lia/lia_hero_sq.jpg" alt="LIA" width="1200" height="1200" loading="eager"></div>'
                f'<div class="content"><span class="eyebrow">{E(lia["role"])}</span><h3>{E(lia["name"])}</h3><h4>{E(lia["h"])}</h4><p>{E(lia["p1"])}</p><p>{E(lia["p2"])}</p><div class="hub-links ent-links">{lia_links}</div></div></div></div></section>')
    cards = []
    for i, (name, role, desc) in enumerate(cubs['chars']):
        key = CUB_ORDER[i]
        cards.append(f'<article class="cub-card"><img src="/media/cubs/chars/{key}.webp" alt="{E(name)}" width="420" height="562" loading="lazy"><h3>{E(name)}</h3><p class="tag">{E(role)}</p><p class="desc">{E(desc)}</p></article>')
    cubs_html = (f'<section class="section soft ent-section" id="cubs"><div class="wrap"><div class="section-intro"><div><span class="eyebrow">{E(cubs["role"])}</span><h2>{E(cubs["name"])}</h2></div><div class="intro-side"><p>{E(cubs["h"])}</p><p>{E(cubs["p"])}</p></div></div>'
                 f'<div class="cubs-grid">{"".join(cards)}</div><div class="hub-links"><a class="text-link" href="/{l}/hallyu/">{E(cubs["app"])} →</a><a class="text-link" href="/{l}/products/cubs/">Hangeul Cubs</a></div></div></section>')
    return (f'<main id="main"><section class="page-hero hub-hero"><div class="wrap"><span class="eyebrow">{E(c["eyebrow"])}</span><h1>{E(c["title"])}</h1><p class="lead">{E(c["lead"])}</p>{who}</div></section>'
            f'{lia_html}{cubs_html}</main>')

def retitle(s, title, desc):
    s = re.sub(r'<title>.*?</title>', f'<title>{E(title)}</title>', s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + E(desc) + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + E(title) + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + E(desc) + m.group(2), s, count=1)
    return s

def make_hub(l, d):
    tpl = (ROOT / l / 'lab' / 'index.html').read_text()
    c = D[d][l]
    s = tpl.replace('/lab/', f'/{d}/')
    s = retitle(s, f'{LABEL[d]} — AP Holdings', c['lead'])
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', '', s, count=1, flags=re.S)
    body = ent_main(l) if d == 'entertainment' else hub_main(l, d)
    s = re.sub(r'<main id="main">.*?</main>', lambda m: body, s, count=1, flags=re.S)
    out = ROOT / l / d / 'index.html'; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(s)
    return f'{l}/{d}/index.html'

# ---------- sitemap pages ----------
def sitemap_main(l):
    t = CO[l]; sm = D['_sitemap'][l]
    li = lambda inner: f'<li style="margin-bottom:16px">{inner}</li>'
    a = lambda u, x: f'<a href="{u}">{E(x)}</a>'
    cards = ['<article class="brand-card" style="--brand-color:#111"><h2 style="font-size:24px">AP HOLDINGS</h2><p>' + E(sm['company']) + '</p><ul>' +
             li(a(f'/{l}/about/', t['about'])) + li(a(f'/{l}/about/#story', t['story'])) + li(a(brand_url(l), t['brand'])) + li(a(f'/{l}/ir/', t['ir'])) + li(a(f'/{l}/lab/', t['lab'])) + li(a('/admin/', t['admin'])) + '</ul></article>']
    for d in DIVS:
        inner = ''
        if d == 'entertainment':
            inner = li(a(f'/{l}/products/lia/', 'LIA')) + li(a(f'/{l}/entertainment/#cubs', 'Hangeul Cubs · ' + t['characters']))
        else:
            for it in D[d][l]['items']:
                if it.get('url'): inner += li(a(fill(it['url'], l), it['name'] + (' ↗' if it['url'].startswith('http') else '')))
                else: inner += li(E(it['name']) + ' · ' + E(it.get('status', CM[l]['soon'])))
            if d == 'games': inner += li(a(f'/{l}/rankers/rankings/' if (ROOT / l / 'rankers' / 'rankings' / 'index.html').exists() else '/en/rankers/rankings/', 'RANKERS · rankings'))
        cards.append(f'<article class="brand-card" style="--brand-color:#111"><h2 style="font-size:24px"><a href="/{l}/{d}/">{LABEL[d]}</a></h2><p>{E(sm["d"][d])}</p><ul>{inner}</ul></article>')
    cards.append(f'<article class="brand-card" style="--brand-color:#111"><h2 style="font-size:24px"><a href="/{l}/news/">News</a></h2><p>{E(sm["d"]["news"])}</p><ul>{li(a(f"/{l}/news/", "AP News"))}</ul></article>')
    return (f'<main id="main"><section class="page-hero"><div class="wrap"><span class="eyebrow">{E(sm["eyebrow"])}</span><h1>{sm["title"]}</h1><p class="lead">{E(sm["lead"])}</p></div></section>'
            f'<section class="section"><div class="wrap"><div class="brand-grid sitemap-grid">{"".join(cards)}</div></div></section></main>')

def make_sitemap(l):
    tpl = (ROOT / 'ko' / 'sitemap' / 'index.html').read_text()
    s = tpl
    if l != 'ko':
        s = s.replace('<html lang="ko">', f'<html lang="{l}">', 1)
        s = s.replace('https://www.apholdings.kr/ko/sitemap/', f'https://www.apholdings.kr/{l}/sitemap/')
        s = re.sub(r'(<details class="language">.*?</details>)', lambda m: m.group(1).replace(' aria-current="page"', '').replace(f'<a href="/{l}/sitemap/" lang="{l}"', f'<a href="/{l}/sitemap/" lang="{l}" aria-current="page"'), s, count=1, flags=re.S)
        s = s.replace('<a class="skip" href="#main">본문으로 이동</a>', '<a class="skip" href="#main">Skip to content</a>')
        s = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="%s">' % ('index,follow' if l == 'en' else 'noindex,follow'), s, count=1)
    # alternates: ko · en · x-default
    s = re.sub(r'(<link rel="alternate"[^>]*>\s*)+', '', s)
    alts = '<link rel="alternate" hreflang="ko" href="https://www.apholdings.kr/ko/sitemap/"><link rel="alternate" hreflang="en" href="https://www.apholdings.kr/en/sitemap/"><link rel="alternate" hreflang="x-default" href="https://www.apholdings.kr/en/sitemap/">'
    s = s.replace('<link rel="canonical"', alts + '<link rel="canonical"', 1)
    s = retitle(s, f'{CO[l]["sitemap"]} — AP Holdings', D['_sitemap'][l]['lead'])
    s = re.sub(r'<main id="main">.*?</main>', lambda m: sitemap_main(l), s, count=1, flags=re.S)
    out = ROOT / l / 'sitemap' / 'index.html'; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(s)
    return f'{l}/sitemap/index.html'

# ---------- about: founder story + company tabs ----------
def story_html(l):
    st = D['_story'][l]
    first = E(st['paras'][0])
    rest = ''.join('<p>%s</p>' % E(p) for p in st['paras'][1:])
    return ('<section class="section soft anchor story-section" id="story"><div class="wrap"><div class="section-intro"><div><span class="number">%s</span><h2>%s</h2></div><div class="intro-side story"><p>%s</p></div></div><div class="story-body">%s</div></div></section>'
            % (E(st['label']), E(st['title']), first, rest))

def co_tabs(l, cur):
    t = CO[l]
    items = [('about', f'/{l}/about/', t['about']), ('brand', brand_url(l), t['brand']), ('ir', f'/{l}/ir/', t['ir']), ('lab', f'/{l}/lab/', t['lab'])]
    return '<div class="wrap"><nav class="co-tabs" aria-label="Company">' + ''.join('<a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if k == cur else '', E(x)) for k, u, x in items) + '</nav></div>'

# ---------- per-page transform ----------
def transform(rel, s):
    m = re.match(r'(ko|en|vi|ja|zh-cn|fr)/', rel)
    l = m.group(1) if m else 'ko'
    if '<header class="site-header">' in s:
        sec = section_for(rel) if m else None
        lm = re.search(r'<details class="language">.*?<ul>(.*?)</ul>', s, re.S)
        lang_items = re.sub(r'</?li>', '', lm.group(1)) if lm else ''
        desk, mob = nav_html(l, sec, lang_items)
        s = re.sub(r'<nav class="desktop-nav[^"]*" aria-label="Main">.*?</nav>(?=<details class="language">)', lambda _: desk, s, count=1, flags=re.S)
        s = re.sub(r'(<details class="mobile-menu"><summary>[^<]*</summary>)<nav aria-label="Mobile"[^>]*>.*?</nav>', lambda mm: mm.group(1) + mob, s, count=1, flags=re.S)
    if '<div class="footer-map' in s:
        s = re.sub(r'<div class="footer-map[^"]*">.*?</div>(?=</div><ul class="footer-policies")', lambda _: footer_map(l), s, count=1, flags=re.S)
    s = re.sub(r'href="/([a-z-]+)/media/"', r'href="/\1/entertainment/"', s)
    s = re.sub(r'href="/([a-z-]+)/products/rankers/"', lambda mm: f'href="{rankers_url(mm.group(1))}"', s)
    s = re.sub(r'site\.css\?v=[0-9.]+', CSS_V, s)
    s = re.sub(r'site\.js\?v=[^"]+', JS_V, s)
    # company tabs (remove the earlier company-tabs block; keep one tab row)
    s = re.sub(r'<nav class="company-tabs"[^>]*>.*?</nav>', '', s, count=1, flags=re.S)
    page = re.match(r'(?:ko|en|vi|ja|zh-cn|fr)/(about|brand|ir|lab)/index\.html$', rel)
    if page and m:
        tabs = co_tabs(l, page.group(1))
        if 'class="co-tabs"' in s:
            s = re.sub(r'<div class="wrap"><nav class="co-tabs".*?</nav></div>', lambda _: tabs, s, count=1, flags=re.S)
        else:
            s = s.replace('<main id="main">', '<main id="main">' + tabs, 1)
        if page.group(1) == 'about':
            st = story_html(l)
            if 'id="story"' in s:
                s = re.sub(r'<section class="section soft anchor story-section" id="story">.*?</section>', lambda _: st, s, count=1, flags=re.S)
            else:
                s = re.sub(r'(<section class="section[^"]*anchor" id="name">)', lambda mm: st + mm.group(1), s, count=1)
    return s

REDIRECT = '<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0;url={to}"><link rel="canonical" href="https://www.apholdings.kr{to}"><title>AP Holdings</title></head><body><a href="{to}">AP Holdings</a></body></html>\n'

CSS = '''
/* IA v4 (2026-10-09): 11칸 메뉴 · 휴대폰 Business 그룹 · Hallyu · Entertainment · 창업자 이야기 · 회사 탭 */
.desktop-nav.nav-v4{gap:20px;font-size:13.5px}.desktop-nav.nav-v4 a{white-space:nowrap}.desktop-nav.nav-v4 a[aria-current=page]{color:var(--ink);border-bottom:1px solid var(--ink)}
.desktop-nav .nav-admin{color:var(--muted);font-size:12.5px}.desktop-nav .nav-admin::before{content:'⚙';margin-right:4px;font-size:12px}
@media(max-width:1340px){.desktop-nav.nav-v4{gap:14px;font-size:13px}}
@media(max-width:1180px){.desktop-nav.nav-v4{display:none}.language{margin-left:auto}.mobile-menu{display:block}.mobile-menu summary{cursor:pointer;font-size:14px;padding:12px 0;list-style:none}.mobile-menu nav{position:absolute;top:100%;left:0;right:0;background:var(--paper);border-bottom:1px solid var(--line);padding:16px 20px 20px;box-shadow:0 20px 35px #0000000d;display:grid;max-height:calc(100vh - 80px);overflow:auto}.mobile-menu nav a{padding:12px 0;font-size:16px;border-bottom:1px solid var(--line)}.mobile-menu nav a:last-child{border-bottom:0}}
.m-nav-v4 .m-group summary{cursor:pointer;list-style:none;padding:12px 0;font-size:16px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center}.m-nav-v4 .m-group summary::after{content:'⌄';color:var(--muted)}.m-nav-v4 .m-group[open] summary::after{content:'⌃'}
.m-nav-v4 .m-group div{display:grid;border-left:2px solid var(--accent);margin:4px 0 6px 6px;padding-left:14px}.m-nav-v4 .m-group div a{font-size:15px;padding:10px 0}.m-nav-v4 .m-group div a:last-child{border-bottom:0}
.m-nav-v4 .m-foot{display:flex;justify-content:space-between;align-items:center;gap:16px;padding-top:12px}.m-nav-v4 .m-foot a{border:0;padding:6px 0}.m-nav-v4 .m-lang summary{cursor:pointer;list-style:none;font-size:14px;color:var(--muted);padding:6px 0}.m-nav-v4 .m-lang div{display:grid;gap:2px;padding:6px 0 0}.m-nav-v4 .m-lang div a{font-size:14px;padding:6px 0;border:0}.m-nav-v4 .m-lang div a[aria-current=page]{font-weight:700}
.m-nav-v4 a[aria-current=page]{font-weight:700}.m-nav-v4 .nav-admin{color:var(--muted)}.m-nav-v4 .m-sitemap{font-size:13px;color:var(--muted);padding-top:14px}
.footer-map-v4{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:22px 18px}.footer-map-v4 b a{color:inherit}.footer-map-v4 .f-soon{display:block;font-size:13.5px;padding:5px 0;color:var(--muted)}
.hub-hero .hub-who{margin-top:18px;color:var(--muted);font-size:15px;max-width:760px}.hub-hero .hub-who b{color:var(--accent);margin-right:6px}
.hub-section{padding-top:20px}.hub-grid{gap:22px}.hub-card .text-link{margin-top:auto}.hub-card{position:relative}.hub-card .status{position:absolute;top:24px;right:24px}
.hub-links{display:flex;flex-wrap:wrap;gap:12px 28px;margin-top:38px;padding-top:22px;border-top:1px solid var(--line)}
.ent-section{padding:60px 0}.ent-lia{margin-top:0}.ent-lia .content h3{font-size:clamp(2.4rem,4vw,3.4rem)}.ent-links{margin-top:26px;padding-top:18px}
.cubs-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin-top:40px}.cub-card{background:#fcf3e7;border:1px solid var(--line);padding:18px 18px 22px;display:flex;flex-direction:column}.cub-card img{width:70%;height:auto;margin:0 auto 14px}.cub-card h3{font-size:22px}.cub-card .tag{font-size:13px;color:var(--accent);font-weight:600;margin-top:4px;letter-spacing:.02em}.cub-card .desc{font-size:14.5px;color:var(--muted);margin-top:12px;line-height:1.6}
.co-tabs{display:flex;flex-wrap:wrap;gap:4px 26px;padding:14px 0 0;font-size:14px;border-bottom:1px solid var(--line)}.co-tabs a{padding:8px 0 12px;color:var(--muted);border-bottom:2px solid transparent;margin-bottom:-1px}.co-tabs a[aria-current=page]{color:var(--ink);font-weight:600;border-bottom-color:var(--ink)}.co-tabs a:hover{color:var(--ink)}
.story-section .story p{font-size:18px}.story-body{max-width:860px;margin-top:8px}.story-body p{font-size:17px;line-height:1.85;color:var(--muted);margin-top:18px}.story-body p:last-child{color:var(--ink)}
@media(max-width:1100px){.cubs-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:800px){.hub-grid{grid-template-columns:1fr}.ent-section{padding:44px 0}.co-tabs{gap:2px 18px;font-size:13px}}
'''

def main():
    changed = []
    css = ROOT / 'assets/v2/site.css'; cs = css.read_text()
    cs = cs.split('\n/* IA v4 (2026-10-09)')[0]
    css.write_text(cs + CSS)
    # redirects: media → entertainment, products/rankers → rankers
    for l in LOCS:
        f = ROOT / l / 'media' / 'index.html'
        if f.exists(): f.write_text(REDIRECT.replace('{l}', l).replace('{to}', f'/{l}/entertainment/'))
        f = ROOT / l / 'products' / 'rankers' / 'index.html'
        if f.exists(): f.write_text(REDIRECT.replace('{l}', l).replace('{to}', rankers_url(l)))
    # pages
    for f in sorted(ROOT.glob('**/*.html')):
        rel = str(f.relative_to(ROOT))
        if rel.startswith(('admin/', '.git', '_backup', 'docs/', 'firstinvest/', 'node_modules')): continue
        s = f.read_text()
        if '<header class="site-header">' not in s and '/media/"' not in s and 'products/rankers' not in s: continue
        n = transform(rel, s)
        if n != s: f.write_text(n); changed.append(rel)
    # hubs (after transform so the lab template already carries the new header/footer/tabs)
    hubs = [make_hub(l, d) for l in LOCS for d in DIVS]
    # sitemap pages (ko first: template, then others from it)
    sms = [make_sitemap('ko')] + [make_sitemap(l) for l in LOCS if l != 'ko']
    for rel in hubs + sms:
        f = ROOT / rel; t = f.read_text(); n = transform(rel, t)
        if n != t: f.write_text(n)
    # sitemap.xml
    sm = ROOT / 'sitemap.xml'; x = sm.read_text()
    x = re.sub(r'<url><loc>https://www\.apholdings\.kr/[a-z-]+/(?:media|products/rankers|products/revenue|products/travel)/</loc>.*?</url>', '', x)
    for l in ('ko', 'en'):
        for d in DIVS + ['sitemap']:
            u = f'https://www.apholdings.kr/{l}/{d}/'
            if u not in x: x = x.replace('</urlset>', f'<url><loc>{u}</loc><lastmod>2026-10-09</lastmod></url></urlset>')
    sm.write_text(x)
    gf = ROOT / 'site-source/generated-files.json'; g = json.loads(gf.read_text())
    g = [p for p in g if not re.match(r'[a-z-]+/(media|products/rankers|products/revenue|products/travel)/index\.html$', p)]
    for h in hubs + sms:
        if h not in g: g.append(h)
    gf.write_text(json.dumps(g, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'hubs': len(hubs), 'sitemaps': len(sms), 'pages_changed': len(changed)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
