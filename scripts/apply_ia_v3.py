#!/usr/bin/env python3
"""IA v3 (2026-10-09, 대표 결정): 상단 메뉴를 사업 5부문 + Company 로 개편.

- 헤더: Intelligence · Media · Edu · Games · Shop · Company▾(About · CI·BI · Investors · Founder's Lab) · 언어. 관리자 링크는 공개 메뉴에서 뺀다.
- 푸터: 같은 5부문 구조로 다시 묶는다. 관리자 링크 제거.
- 부문 허브 페이지 5개 × 6개 언어 생성(/<l>/intelligence|media|edu|games|shop/).
- AP Revenue · AP Travel 은 공개 화면에서 숨긴다: 홈 카드 · 메뉴 · 사이트맵 · IR 링크 제거, 제품 페이지는 Intelligence 허브로 이동(noindex).
생성된 HTML 을 직접 고치는 방식(다른 세션들이 HTML 을 직접 갱신해 왔으므로 build_site 재실행 대신). 여러 번 실행해도 결과가 같다.
"""
import re, json, html
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
LOCS = ['ko', 'en', 'vi', 'ja', 'zh-cn', 'fr']
DIVS = ['intelligence', 'media', 'edu', 'games', 'shop']
DIV_LABEL = {'intelligence': 'Intelligence', 'media': 'Media', 'edu': 'Edu', 'games': 'Games', 'shop': 'Shop'}
E = lambda s: html.escape(s, quote=True)

COMPANY = {
 'ko': {'company': '회사', 'about': '회사 소개', 'brand': 'CI · BI', 'ir': '투자자 (IR)', 'lab': 'Founder’s Lab', 'sitemap': '사이트맵', 'menu_company': 'COMPANY'},
 'en': {'company': 'Company', 'about': 'About', 'brand': 'CI · BI', 'ir': 'Investors (IR)', 'lab': 'Founder’s Lab', 'sitemap': 'Sitemap', 'menu_company': 'COMPANY'},
 'vi': {'company': 'Công ty', 'about': 'Giới thiệu', 'brand': 'CI · BI', 'ir': 'Nhà đầu tư (IR)', 'lab': 'Founder’s Lab', 'sitemap': 'Sơ đồ trang', 'menu_company': 'CÔNG TY'},
 'ja': {'company': '会社', 'about': '会社紹介', 'brand': 'CI · BI', 'ir': '投資家 (IR)', 'lab': 'Founder’s Lab', 'sitemap': 'サイトマップ', 'menu_company': 'COMPANY'},
 'zh-cn': {'company': '公司', 'about': '关于我们', 'brand': 'CI · BI', 'ir': '投资者 (IR)', 'lab': 'Founder’s Lab', 'sitemap': '网站地图', 'menu_company': 'COMPANY'},
 'fr': {'company': 'Entreprise', 'about': 'À propos', 'brand': 'CI · BI', 'ir': 'Investisseurs (IR)', 'lab': 'Founder’s Lab', 'sitemap': 'Plan du site', 'menu_company': 'ENTREPRISE'},
}

def rankers_url(l):
    return f'/{l}/rankers/' if (ROOT / l / 'rankers' / 'index.html').exists() else '/en/rankers/'

def brand_url(l):
    return f'/{l}/brand/' if (ROOT / l / 'brand' / 'index.html').exists() else '/ko/brand/'

def sitemap_url(l):
    return f'/{l}/sitemap/' if (ROOT / l / 'sitemap' / 'index.html').exists() else None

# ---------- which section is "current" ----------
SECTION_OF = [
 ('intelligence', ['/intelligence/', '/products/safe/', '/products/light/']),
 ('media', ['/media/', '/products/lia/', '/news/']),
 ('edu', ['/edu/', '/products/cubs/']),
 ('games', ['/games/', '/products/rgrg/', '/products/rankers/', '/products/lastwave/', '/rankers/']),
 ('shop', ['/shop/', '/products/select/', '/products/commerce/', '/products/craft/', '/products/liaselect/']),
 ('company', ['/about/', '/brand/', '/ir/', '/lab/', '/sitemap/']),
]
def section_for(rel):
    path = '/' + rel.split('/', 1)[1] if '/' in rel else '/'
    for sec, keys in SECTION_OF:
        if any(path.startswith(k) for k in keys):
            return sec
    return None

def nav_html(l, sec):
    t = COMPANY[l]
    cur = lambda s: ' aria-current="page"' if sec == s else ''
    divs = ''.join(f'<a href="/{l}/{d}/"{cur(d)}>{DIV_LABEL[d]}</a>' for d in DIVS)
    items = [(f'/{l}/about/', t['about']), (brand_url(l), t['brand']), (f'/{l}/ir/', t['ir']), (f'/{l}/lab/', t['lab'])]
    lis = ''.join(f'<li><a href="{u}">{E(x)}</a></li>' for u, x in items)
    comp_cls = ' class="nav-group is-current"' if sec == 'company' else ' class="nav-group"'
    desktop = f'<nav class="desktop-nav" aria-label="Main">{divs}<details{comp_cls}><summary>{E(t["company"])}</summary><ul>{lis}</ul></details></nav>'
    mob_items = ''.join(f'<a href="{u}">{E(x)}</a>' for u, x in items)
    mobile = f'<nav aria-label="Mobile">{divs}<span class="m-label">{E(t["menu_company"])}</span>{mob_items}</nav>'
    return desktop, mobile

# ---------- footer ----------
FOOT = {
 'ko': {'connect_s': '세이프리스트 · 클로드', 'connect_l': '라이트리스트 · 클로드', 'news': 'AP News', 'shop': 'Lia Select Shop ↗'},
 'en': {'connect_s': 'Safelist · Claude', 'connect_l': 'LightList · Claude', 'news': 'AP News', 'shop': 'Lia Select Shop ↗'},
}
def footer_map(l):
    t = COMPANY[l]; f = FOOT.get(l, FOOT['en'])
    a = lambda u, x: f'<a href="{u}">{E(x)}</a>'
    head = lambda d: f'<b><a href="/{l}/{d}/">{DIV_LABEL[d]}</a></b>'
    comp = [a(f'/{l}/about/', t['about']), a(brand_url(l), t['brand']), a(f'/{l}/ir/', 'IR / INVESTORS'), a(f'/{l}/lab/', 'Founder’s Lab')]
    if sitemap_url(l): comp.append(a(sitemap_url(l), t['sitemap']))
    cols = [
     '<div><b>AP Holdings</b>' + ''.join(comp) + '</div>',
     '<div>' + head('intelligence') + a(f'/{l}/products/safe/', 'AP Safe') + a(f'/{l}/products/light/', 'AP Light') + a('/business/safelist-connect.html', f['connect_s']) + a('/business/lightlist-connect.html', f['connect_l']) + '</div>',
     '<div>' + head('media') + a(f'/{l}/products/lia/', 'LIA') + a(f'/{l}/news/', f['news']) + '</div>',
     '<div>' + head('edu') + a(f'https://edu.apholdings.kr/{l if l in ("ko","en") else "en"}/', 'AP Edu ↗') + a(f'/{l}/products/cubs/', 'Hangeul Cubs') + '</div>',
     '<div>' + head('games') + a(f'https://games.apholdings.kr/{l if l in ("ko","en") else "en"}/', 'AP Games ↗') + a(rankers_url(l), 'RANKERS') + a(f'/{l}/products/rgrg/', 'QuizRanker') + a(f'/{l}/products/lastwave/', 'LAST WAVE') + '</div>',
     '<div>' + head('shop') + a('https://shop.apholdings.kr/', f['shop']) + a(f'/{l}/products/liaselect/', 'LIA Select') + a(f'/{l}/products/select/', 'AP SELECT') + a(f'/{l}/products/commerce/', 'Global K-Commerce') + a(f'/{l}/products/craft/', 'K-Craft') + '</div>',
    ]
    return '<div class="footer-map footer-map-v3">' + ''.join(cols) + '</div>'

# ---------- hub copy ----------
HUB = json.loads((ROOT / 'site-source' / 'divisions.json').read_text())

def hub_main(l, d):
    c = HUB[d][l]; t = COMPANY[l]; common = HUB['_common'][l]
    cards = []
    for it in c['items']:
        url = it.get('url', '')
        url = url.replace('{l}', l).replace('{rankers}', rankers_url(l)).replace('{edu}', l if l in ('ko', 'en') else 'en').replace('{games}', l if l in ('ko', 'en') else 'en')
        ext = url.startswith('http')
        st = f'<span class="status">{E(it["status"])}</span>' if it.get('status') else ''
        lk = (f'<a class="text-link" href="{E(url)}"' + (' target="_blank" rel="noopener noreferrer"' if ext else '') + f'>{E(it.get("cta", common["more"]))}{" ↗" if ext else ""}</a>') if url else ''
        cards.append(f'<article class="product-card hub-card">{st}<h3>{E(it["name"])}</h3><p class="tag">{E(it["tag"])}</p><p class="desc">{E(it["desc"])}</p>{lk}</article>')
    primary = ''
    if c.get('primary'):
        p = c['primary']; ext = p['url'].startswith('http')
        primary = f'<div class="actions"><a class="button primary" href="{E(p["url"].replace("{l}", l))}"' + (' target="_blank" rel="noopener noreferrer"' if ext else '') + f'>{E(p["label"])}</a></div>'
    who = f'<p class="hub-who"><b>{E(common["for"])}</b> {E(c["for"])}</p>'
    links = (f'<div class="hub-links"><a class="text-link" href="/{l}/ir/">{E(common["ir"])}</a>'
             f'<a class="text-link" href="{brand_url(l)}">{E(common["brand"])}</a></div>')
    return (f'<main id="main"><section class="page-hero hub-hero"><div class="wrap"><span class="eyebrow">{E(c["eyebrow"])}</span>'
            f'<h1>{E(c["title"])}</h1><p class="lead">{E(c["lead"])}</p>{who}{primary}</div></section>'
            f'<section class="section hub-section"><div class="wrap"><div class="grid-3 hub-grid">{"".join(cards)}</div>{links}</div></section></main>')

def make_hub(l, d):
    tpl = (ROOT / l / 'lab' / 'index.html').read_text()
    c = HUB[d][l]
    title = f'{DIV_LABEL[d]} — AP Holdings'
    desc = c['lead']
    s = tpl.replace('/lab/', f'/{d}/')
    s = re.sub(r'<title>.*?</title>', f'<title>{E(title)}</title>', s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + E(desc) + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + E(title) + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + E(desc) + m.group(2), s, count=1)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', '', s, count=1, flags=re.S)
    s = re.sub(r'<main id="main">.*?</main>', lambda m: hub_main(l, d), s, count=1, flags=re.S)
    out = ROOT / l / d / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s)
    return f'{l}/{d}/index.html'

# ---------- per-page transforms ----------
def transform(rel, s):
    m = re.match(r'(ko|en|vi|ja|zh-cn|fr)/', rel)
    l = m.group(1) if m else 'ko'
    if '<header class="site-header">' in s:
        sec = section_for(rel) if m else None
        desk, mob = nav_html(l, sec)
        s = re.sub(r'<nav class="desktop-nav" aria-label="Main">.*?</nav>(?=<details class="language">)',
                   lambda _: desk, s, count=1, flags=re.S)
        # if a previous run left nav-group, the regex above still matches up to language
        s = re.sub(r'(<details class="mobile-menu"><summary>[^<]*</summary>)<nav aria-label="Mobile">.*?</nav>', lambda mm: mm.group(1) + mob, s, count=1, flags=re.S)
    if '<div class="footer-map' in s:
        s = re.sub(r'<div class="footer-map[^"]*">.*?</div>(?=</div><ul class="footer-policies")', lambda _: footer_map(l), s, count=1, flags=re.S)
    # hide AP Revenue / AP Travel cards and links in page bodies
    s = re.sub(r'<a class="compact-project" href="/[a-z-]+/products/(?:revenue|travel)/">.*?</a>', '', s, flags=re.S)
    s = s.replace('<div class="compact-grid"></div>', '')
    s = re.sub(r'<li[^>]*><a href="/[a-z-]+/products/(?:revenue|travel)/">[^<]*</a></li>', '', s)
    s = re.sub(r'<a (?:class="[^"]*" )?href="/[a-z-]+/products/(?:revenue|travel)/"[^>]*>(.*?)</a>', r'\1', s, flags=re.S)
    s = re.sub(r'site\.css\?v=[0-9.]+', 'site.css?v=2.20', s)
    s = re.sub(r'site\.js\?v=[^"]+', 'site.js?v=20261009-ia3', s)
    if re.match(r'(ko|en|vi|ja|zh-cn|fr)/ir/index\.html$', rel):
        s = re.sub(r'<a class="button" href="https://revenue\.apholdings\.kr/">[^<]*</a>', '', s)
        s = re.sub(r'<div class="proof"><h3>AP Revenue</h3>.*?</div>', '', s, flags=re.S)
    return s

REDIRECT = '<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0;url=/{l}/intelligence/"><link rel="canonical" href="https://www.apholdings.kr/{l}/intelligence/"><title>AP Holdings</title></head><body><a href="/{l}/intelligence/">AP Holdings — Intelligence</a></body></html>\n'

CSS = '''
/* IA v3 (2026-10-09): 사업 5부문 메뉴 · Company 드롭다운 · 부문 허브 */
.desktop-nav{gap:26px}.desktop-nav>a[aria-current=page]{border-bottom:1px solid var(--ink)}
.nav-group{position:relative}.nav-group summary{cursor:pointer;list-style:none;padding:12px 0}.nav-group summary::after{content:'⌄';margin-left:6px}
.nav-group.is-current summary{border-bottom:1px solid var(--ink)}
.nav-group ul{position:absolute;top:100%;right:-12px;padding:8px;list-style:none;margin:0;width:200px;background:var(--paper);border:1px solid var(--line);box-shadow:0 15px 35px #0000000d;z-index:40}
.nav-group ul a{display:block;padding:9px 12px}.nav-group ul a:hover{background:var(--soft)}
.mobile-menu .m-label{font-size:11px;letter-spacing:.14em;color:var(--muted);padding:16px 0 4px;font-weight:700}
.footer-map-v3{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:22px}
.footer-map-v3 b a{color:inherit}
.hub-hero .hub-who{margin-top:18px;color:var(--muted);font-size:15px;max-width:760px}.hub-hero .hub-who b{color:var(--accent);margin-right:6px}
.hub-section{padding-top:20px}.hub-grid{gap:22px}.hub-card .text-link{margin-top:auto}
.hub-card{position:relative}.hub-card .status{position:absolute;top:24px;right:24px}
.hub-links{display:flex;flex-wrap:wrap;gap:12px 28px;margin-top:38px;padding-top:22px;border-top:1px solid var(--line)}
@media(max-width:1100px){.footer-map-v3{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:800px){.footer-map-v3{grid-template-columns:repeat(2,minmax(0,1fr))}.hub-grid{grid-template-columns:1fr}}
'''

def main():
    changed = []
    css = ROOT / 'assets/v2/site.css'
    cs = css.read_text()
    cs = cs.split('\n/* IA v3 (2026-10-09)')[0]
    css.write_text(cs + CSS)
    hubs = [make_hub(l, d) for l in LOCS for d in DIVS]
    for l in LOCS:
        for p in ('revenue', 'travel'):
            f = ROOT / l / 'products' / p / 'index.html'
            if f.exists():
                f.write_text(REDIRECT.replace('{l}', l))
    b = ROOT / 'business/inbound.html'
    if b.exists():
        b.write_text(re.sub(r'url=/ko/products/travel/', 'url=/ko/intelligence/', b.read_text()))
    for f in sorted(ROOT.glob('**/*.html')):
        rel = str(f.relative_to(ROOT))
        if rel.startswith(('admin/', '.git', '_backup', 'docs/', 'firstinvest/', 'node_modules')):
            continue
        s = f.read_text()
        if '<header class="site-header">' not in s and 'compact-project' not in s and 'products/revenue' not in s and 'products/travel' not in s:
            continue
        n = transform(rel, s)
        if n != s:
            f.write_text(n); changed.append(rel)
    # sitemap.xml: hide revenue/travel, add hubs (ko·en indexed only)
    sm = ROOT / 'sitemap.xml'; x = sm.read_text()
    x = re.sub(r'<url><loc>https://www\.apholdings\.kr/[a-z-]+/products/(?:revenue|travel)/</loc>.*?</url>', '', x)
    for l in ('ko', 'en'):
        for d in DIVS:
            u = f'https://www.apholdings.kr/{l}/{d}/'
            if u not in x:
                x = x.replace('</urlset>', f'<url><loc>{u}</loc><lastmod>2026-10-09</lastmod></url></urlset>')
    sm.write_text(x)
    gf = ROOT / 'site-source/generated-files.json'; g = json.loads(gf.read_text())
    g = [x for x in g if not re.match(r'[a-z-]+/products/(revenue|travel)/index\.html$', x)]
    for h in hubs:
        if h not in g: g.append(h)
    gf.write_text(json.dumps(g, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'hubs': len(hubs), 'pages_changed': len(changed)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
