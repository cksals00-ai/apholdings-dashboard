#!/usr/bin/env python3
"""AP News 정적 생성기 (6개 어권). 홈페이지에 들어가는 것은 모든 어권을 넣는다(대표 지시 2026-10-03, 예외 없음).
원본: site-source/news/NNN-*.md (한국어) · 번역: site-source/news/<lang>/NNN-*.md (en vi ja zh-cn fr)
출력: /<lang>/news/ , /<lang>/news/<slug>/ .  build_site.py 실행 뒤에 돌린다:
  python3.12 scripts/build_site.py && python3 scripts/build_news.py && python3.12 scripts/check_site.py
번역본이 없는 글은 한국어 원문 안내 카드로 대체(누락 방지). 번역은 AI 번역 → 원어민 검수 전 표기."""
import re, json, sys
from pathlib import Path
from html import escape as e
sys.path.insert(0, str(Path(__file__).resolve().parent))
from news_art import cover
from urllib.parse import urlparse
ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT/'site-source/content.json').read_text())
ORIGIN = CFG['origin']
LANGS = ['ko', 'en', 'vi', 'ja', 'zh-cn', 'fr']
LNAME = {'ko': '한국어', 'en': 'English', 'vi': 'Tiếng Việt', 'ja': '日本語', 'zh-cn': '简体中文', 'fr': 'Français'}
INDEXED = {'ko', 'en'}  # 나머지는 원어민 검수 전까지 noindex (site-source/README 정책)
UI = {
 'ko': dict(all='전체', eyebrow='AP NEWS', h1='AI 소식, 우리 일에 쓰는 법까지.', lead='한 주의 AI 소식을 읽고, 작은 팀이 실제로 바꿀 수 있는 것만 골라 적습니다. 모든 글은 AI와 함께 쓰고 편집자가 출처를 확인합니다.', back='← AP News 목록', byline='AP Holdings 편집', title='AP News — AP Holdings', desc='AI 소식을 우리 일에 쓰는 법까지. A.P Holdings가 매주 쓰는 AI 소식지.', suffix='AP News', lang_label='언어', notice=''),
 'en': dict(all='All', eyebrow='AP NEWS', h1='AI news, down to how we use it.', lead='We read the week in AI and write down only what a small team can actually change. Every piece is written with AI and checked by an editor against its sources.', back='← AP News', byline='AP Holdings Editorial', title='AP News — AP Holdings', desc='AI news, down to how we use it. A weekly AI newsletter from A.P Holdings.', suffix='AP News', lang_label='Language', notice='Translated from the Korean original by AI; native-speaker review pending.'),
 'vi': dict(all='Tất cả', eyebrow='AP NEWS', h1='Tin AI, đến tận cách chúng tôi áp dụng.', lead='Chúng tôi đọc tin AI trong tuần và chỉ ghi lại những gì một đội nhỏ thực sự có thể thay đổi. Mọi bài viết được soạn cùng AI và biên tập viên kiểm tra nguồn.', back='← Danh sách AP News', byline='Ban biên tập AP Holdings', title='AP News — AP Holdings', desc='Tin AI, đến tận cách chúng tôi áp dụng. Bản tin AI hằng tuần của A.P Holdings.', suffix='AP News', lang_label='Ngôn ngữ', notice='Bản dịch AI từ bản gốc tiếng Hàn; đang chờ người bản ngữ kiểm tra.'),
 'ja': dict(all='すべて', eyebrow='AP NEWS', h1='AIニュースを、私たちの仕事での使い方まで。', lead='1週間のAIニュースを読み、小さなチームが実際に変えられることだけを書きます。すべての記事はAIと一緒に書き、編集者が出典を確認しています。', back='← AP News 一覧', byline='AP Holdings 編集部', title='AP News — AP Holdings', desc='AIニュースを、私たちの仕事での使い方まで。A.P Holdingsの週刊AIニュースレター。', suffix='AP News', lang_label='言語', notice='韓国語の原文からAIが翻訳したものです。ネイティブによる確認は未実施です。'),
 'zh-cn': dict(all='全部', eyebrow='AP NEWS', h1='AI 资讯，细到我们怎么用。', lead='我们阅读一周的 AI 资讯，只记录小团队真正能改变的部分。所有文章均与 AI 共同撰写，并由编辑核对来源。', back='← AP News 列表', byline='AP Holdings 编辑部', title='AP News — AP Holdings', desc='AI 资讯，细到我们怎么用。A.P Holdings 的每周 AI 资讯。', suffix='AP News', lang_label='语言', notice='本文由 AI 从韩文原文翻译，尚待母语者审校。'),
 'fr': dict(all='Tout', eyebrow='AP NEWS', h1="L'actu IA, jusqu'à la façon de l'utiliser.", lead="Nous lisons l'actualité de l'IA de la semaine et ne retenons que ce qu'une petite équipe peut réellement changer. Chaque article est rédigé avec l'IA, et un éditeur vérifie les sources.", back='← Liste AP News', byline='Rédaction AP Holdings', title='AP News — AP Holdings', desc="L'actu IA, jusqu'à la façon de l'utiliser. La newsletter IA hebdomadaire d'A.P Holdings.", suffix='AP News', lang_label='Langue', notice="Traduit du coréen par IA ; relecture par un locuteur natif en attente."),
}
CATS = {  # 한국어 분류 → 어권별 분류
 '창간': dict(ko='창간', en='Launch', vi='Ra mắt', ja='創刊', **{'zh-cn': '创刊'}, fr='Lancement'),
 '주간 소식': dict(ko='주간 소식', en='Weekly News', vi='Tin hàng tuần', ja='週間ニュース', **{'zh-cn': '每周资讯'}, fr="L'actu de la semaine"),
 '인사이트': dict(ko='인사이트', en='Insight', vi='Góc nhìn', ja='インサイト', **{'zh-cn': '洞察'}, fr='Analyse'),
 '실전': dict(ko='실전', en='Practice', vi='Thực hành', ja='実践', **{'zh-cn': '实践'}, fr='Pratique'),
}

UX = {
 'ko': dict(glance='한눈에 보기', mins='분 읽기', related='이어서 읽기', latest='최신', sources='출처'),
 'en': dict(glance='At a glance', mins='min read', related='Keep reading', latest='Latest', sources='Sources'),
 'vi': dict(glance='Tóm lược', mins='phút đọc', related='Đọc tiếp', latest='Mới nhất', sources='Nguồn'),
 'ja': dict(glance='要点を一覧', mins='分で読めます', related='あわせて読む', latest='最新', sources='出典'),
 'zh-cn': dict(glance='一览', mins='分钟阅读', related='继续阅读', latest='最新', sources='来源'),
 'fr': dict(glance='En un coup d’œil', mins='min de lecture', related='À lire aussi', latest='À la une', sources='Sources'),
}
CATCLS = {'창간': 'launch', '주간 소식': 'weekly', '인사이트': 'insight', '실전': 'practice'}
REF = re.compile(r'^- \[(.+?)\]\((https?://[^)\s]+)\)(.*)$')
TPL = {l: (ROOT/('ko/index.html' if l == 'ko' else 'en/index.html')).read_text() for l in ('ko', 'en')}

def inline(t):
    t = e(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lambda m: f'<a href="{m.group(2)}"' + (' target="_blank" rel="noopener noreferrer"' if m.group(2).startswith('http') else '') + f'>{m.group(1)}</a>', t)
    return t

def refcard(items):
    li = ''
    for t, u, rest in items:
        dom = urlparse(u).netloc.replace('www.', '')
        tag = re.sub(r'^\s*[—-]\s*', '', rest).strip()
        li += f'<li><a href="{e(u, quote=True)}" target="_blank" rel="noopener noreferrer"><span class="ref-dom">{e(dom)}</span><span class="ref-ttl">{e(t)}</span>' + (f'<span class="ref-tag">{e(tag)}</span>' if tag else '') + '</a></li>'
    return f'<ul class="refs">{li}</ul>'

def md(body):
    out, lst, buf = [], None, []
    def close():
        nonlocal lst, buf
        if lst == 'ul':
            ms = [REF.match('- ' + b) for b in buf]
            if buf and all(ms): out.append(refcard([m.groups() for m in ms]))
            else: out.append('<ul>' + ''.join(f'<li>{inline(b)}</li>' for b in buf) + '</ul>')
        elif lst == 'ol': out.append('</ol>')
        lst = None; buf = []
    for ln in body.strip().split('\n'):
        s = ln.rstrip()
        if not s.strip(): close(); continue
        if s.startswith('## '): close(); out.append(f'<h2>{inline(s[3:])}</h2>'); continue
        if s.startswith('> '): close(); out.append(f'<blockquote>{inline(s[2:])}</blockquote>'); continue
        m = re.match(r'^(\d+)\.\s+(.*)', s)
        if m:
            if lst != 'ol': close(); out.append('<ol>'); lst = 'ol'
            out.append(f'<li>{inline(m.group(2))}</li>'); continue
        if s.startswith('- '):
            if lst != 'ul': close(); lst = 'ul'
            buf.append(s[2:]); continue
        close(); out.append(f'<p>{inline(s)}</p>')
    close(); return '\n'.join(out)

def glance(body):
    parts = re.split(r'^## ', body, flags=re.M)[1:]
    hs = []
    for sec in parts:
        title = sec.split('\n', 1)[0].strip()
        if re.search(r'\]\(https?://', sec): continue  # 출처 섹션 제외
        hs.append(re.sub(r'\*\*', '', title))
    return hs

def readmins(body, lang):
    txt = re.sub(r'[#>*\[\]()`-]', '', body)
    n = len(txt) / (450 if lang in ('ko', 'ja', 'zh-cn') else 1) if lang in ('ko', 'ja', 'zh-cn') else len(txt.split()) / 190
    return max(2, round(n))

def load(dirpath):
    res = {}
    for f in sorted(dirpath.glob('*.md')):
        raw = f.read_text(encoding='utf-8')
        m = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.S)
        if not m: continue
        meta = dict(l.split(': ', 1) for l in m.group(1).split('\n') if ': ' in l)
        meta['no'] = int(meta['no']); meta['body'] = m.group(2); res[meta['no']] = meta
    return res
KO = load(ROOT/'site-source/news')
TR = {l: load(ROOT/'site-source/news'/l) for l in LANGS if l != 'ko'}

def shell(lang, title, desc, path, main_html, og_type='website'):
    t = TPL['ko' if lang == 'ko' else 'en']
    i_main = t.index('<main id="main">'); i_end = t.index('</main>') + len('</main>')
    h, foot = t[:i_main], t[i_end:]
    h = h.replace('<html lang="en">', f'<html lang="{lang}">', 1).replace('<html lang="ko">', f'<html lang="{lang}">', 1)
    h = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', h, 1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc, quote=True)}">', h, 1)
    h = re.sub(r'<meta name="robots" content="[^"]*">', f'<meta name="robots" content="{"index,follow" if lang in INDEXED else "noindex,follow"}">', h, 1)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{ORIGIN}{path}">', h, 1)
    for k, v in (('og:title', title), ('og:description', desc), ('og:url', ORIGIN+path), ('og:type', og_type)):
        h = re.sub(rf'<meta property="{k}" content="[^"]*">', f'<meta property="{k}" content="{e(v, quote=True)}">', h, 1)
    h = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', h)
    sub = path.split(f'/{lang}/news/', 1)[1]  # '' 또는 'slug/'
    if lang in INDEXED:
        alts = ''.join(f'<link rel="alternate" hreflang="{k}" href="{ORIGIN}/{k}/news/{sub}">' for k in ('ko', 'en'))
        h = h.replace('</head>', alts + '</head>', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="/assets/v2/news.css?v=2.0"></head>', 1)
    # 언어 선택: 같은 글의 각 어권 버전으로
    lis = ''.join(f'<li><a href="/{k}/news/{sub}" lang="{k}"' + (' aria-current="page"' if k == lang else '') + f'>{LNAME[k]}</a></li>' for k in LANGS)
    h = re.sub(r'<details class="language">.*?</details>', f'<details class="language"><summary aria-label="{UI[lang]["lang_label"]}">{lang.upper()}</summary><ul>{lis}</ul></details>', h, 1, re.S)
    if lang not in ('ko', 'en'):  # 메뉴의 AP News 링크를 해당 어권으로
        h = h.replace('/en/news/', f'/{lang}/news/')
    f2 = foot.replace('/en/news/', f'/{lang}/news/') if lang not in ('ko', 'en') else foot
    return h + main_html + f2

def out(path, text):
    p = ROOT/path.lstrip('/'); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding='utf-8')

def view(lang, no):
    """어권별 글 메타(번역 있으면 번역, 없으면 한국어 원문+안내)."""
    k = KO[no]
    if lang == 'ko': return dict(k, missing=False)
    t = TR[lang].get(no)
    if t: return dict(t, missing=False, slug=k['slug'], date=k['date'], kcat=k['category'])
    return dict(k, missing=True, kcat=k['category'])

nos = sorted(KO, reverse=True)
built = {}
for lang in LANGS:
    ui = UI[lang]
    posts = [view(lang, n) for n in nos]
    for p in posts: p.setdefault('kcat', p['category'])
    catkeys = []
    for p in posts:
        if p['kcat'] not in catkeys: catkeys.append(p['kcat'])
    def cname(kc): return CATS.get(kc, {}).get(lang, kc)
    filt = f'<div class="news-filter" role="group"><button type="button" aria-pressed="true" data-c="">{e(ui["all"])}</button>' + ''.join(f'<button type="button" aria-pressed="false" data-c="{e(kc, quote=True)}">{e(cname(kc))}</button>' for kc in catkeys) + '</div>'
    note = f'<p class="news-notice">{e(ui["notice"])}</p>' if ui['notice'] else ''
    def card(p, big=False):
        cl = CATCLS.get(p["kcat"], 'launch')
        return f'<li class="news-item cat-{cl}{" is-feature" if big else ""}" data-c="{e(p["kcat"], quote=True)}"><a href="/{lang}/news/{p["slug"]}/"><div class="news-thumb">{cover(p["no"], big)}<span class="news-badge">NO. {p["no"]:02d}</span></div><div class="news-txt"><div class="news-meta">{e(cname(p["kcat"]))} <span>· {e(p["tags"])} · {p["date"].replace("-", ".")}</span></div><h2>{e(p["title"])}</h2><p>{e(p["summary"])}</p></div></a></li>'
    items = ''.join(card(p, i == 0) for i, p in enumerate(posts))
    js = "<script>document.querySelectorAll('.news-filter button').forEach(function(b){b.addEventListener('click',function(){document.querySelectorAll('.news-filter button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});var c=b.dataset.c;document.querySelectorAll('.news-item').forEach(function(li){li.hidden=c&&li.dataset.c!==c})})})</script>"
    main = f'<main id="main"><section class="news-hero"><div class="wrap news-hero-in"><div class="news-hero-txt"><span class="eyebrow">{ui["eyebrow"]}</span><h1>{e(ui["h1"])}</h1><p>{e(ui["lead"])}</p>{note}{filt}</div><div class="news-hero-art" aria-hidden="true">{cover(8, True)}</div></div></section><section><div class="wrap"><ul class="news-grid">{items}</ul></div></section>{js}</main>'
    out(f'{lang}/news/index.html', shell(lang, ui['title'], ui['desc'], f'/{lang}/news/', main))
    for k, p in enumerate(posts):
        newer = posts[k-1] if k > 0 else None; older = posts[k+1] if k+1 < len(posts) else None
        nav = '<div class="post-nav"><span>' + (f'<a href="/{lang}/news/{older["slug"]}/">← {e(older["title"][:30])}…</a>' if older else '') + '</span><span>' + (f'<a href="/{lang}/news/{newer["slug"]}/">{e(newer["title"][:30])}… →</a>' if newer else '') + '</span></div>'
        warn = ''
        if p['missing']: warn = f'<p class="news-notice">{e(ui["notice"] or "")} (Translation not yet available — showing the Korean original.)</p>'
        elif ui['notice']: warn = f'<p class="news-notice">{e(ui["notice"])}</p>'
        body_lang = 'ko' if p['missing'] else lang
        ux = UX[lang]
        cl = CATCLS.get(p["kcat"], 'launch')
        hs = glance(p["body"])
        gl = ''
        if len(hs) >= 3:
            gl = f'<aside class="glance"><div class="glance-h">{e(ux["glance"])}</div><ol>' + ''.join(f'<li><span>{i+1}</span><b>{e(h[:56] + ("…" if len(h) > 56 else ""))}</b></li>' for i, h in enumerate(hs[:7])) + '</ol></aside>'
        rel_src = [q for q in posts if q["no"] != p["no"]]
        rel_src.sort(key=lambda q: (q["kcat"] != p["kcat"], abs(q["no"] - p["no"])))
        rel = ''.join(f'<li class="news-item cat-{CATCLS.get(q["kcat"], "launch")}"><a href="/{lang}/news/{q["slug"]}/"><div class="news-thumb">{cover(q["no"])}<span class="news-badge">NO. {q["no"]:02d}</span></div><div class="news-txt"><div class="news-meta">{e(cname(q["kcat"]))}</div><h2>{e(q["title"])}</h2></div></a></li>' for q in rel_src[:3])
        main = f'<main id="main"><article class="post cat-{cl}"><div class="post-cover">{cover(p["no"], True)}</div><div class="wrap"><a class="post-back" href="/{lang}/news/">{e(ui["back"])}</a><div class="post-kicker">NO. {p["no"]:02d} · {e(cname(p["kcat"]))}</div><h1>{e(p["title"])}</h1><div class="post-meta">{e(p["tags"])} · {p["date"].replace("-", ".")} · {e(ui["byline"])} · {readmins(p["body"], lang)} {e(ux["mins"])}</div>{warn}<p class="post-lede">{e(p["summary"])}</p>{gl}<div class="post-body" lang="{body_lang}">{md(p["body"])}</div>{nav}<section class="related"><h3>{e(ux["related"])}</h3><ul class="news-grid three">{rel}</ul></section></div></article></main>'
        out(f'{lang}/news/{p["slug"]}/index.html', shell(lang, f'{p["title"]} — {ui["suffix"]}', p['summary'], f'/{lang}/news/{p["slug"]}/', main, 'article'))
    built[lang] = sum(1 for p in posts if not p['missing'])

sm = (ROOT/'sitemap.xml').read_text()
sm = re.sub(r'<url><loc>[^<]*/news/[^<]*</loc><lastmod>[^<]*</lastmod></url>', '', sm)
add = ''
for lang in INDEXED:
    add += f'<url><loc>{ORIGIN}/{lang}/news/</loc><lastmod>{KO[nos[0]]["date"]}</lastmod></url>' + ''.join(f'<url><loc>{ORIGIN}/{lang}/news/{KO[n]["slug"]}/</loc><lastmod>{KO[n]["date"]}</lastmod></url>' for n in nos)
(ROOT/'sitemap.xml').write_text(sm.replace('</urlset>', add + '</urlset>'))
print('AP News 어권별 번역 반영:', built, '/ 원문', len(KO))
