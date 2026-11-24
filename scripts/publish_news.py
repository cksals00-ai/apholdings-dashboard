#!/usr/bin/env python3
"""AP News 반영 (2026-10-15, 클레어). site-source/news 에 넣은 새 글을 실제 페이지로 만든다. 여러 번 실행해도 같은 결과.

왜 이렇게 하나: build_news.py 는 뉴스 페이지의 머리·메뉴·푸터를 옛 틀로 다시 써서
다른 정리 스크립트(apply_*: 메뉴·푸터·언어 링크·CSS 버전)의 결과를 되돌린다.
그래서 임시 복사본에서 빌드한 뒤, 아래 세 가지만 실제 사이트로 옮긴다.
  1) 글 페이지의 <main> 본문 (기존 글은 본문만 교체 — 관련 글·이전/다음 갱신)
  2) 새 글은 같은 언어의 기존 글 페이지를 틀로 써서 머리·메뉴·푸터를 현재 것 그대로 유지
  3) 목록 페이지의 <ul class="news-grid">, sitemap.xml 의 새 뉴스 주소
사용: python3 scripts/publish_news.py   (그다음 python3 scripts/check_site.py)
"""
import os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ['ko', 'en', 'vi', 'ja', 'zh-cn', 'fr']
MAIN = re.compile(r'<main id="main">.*?</main>', re.S)
GRID = re.compile(r'<ul class="news-grid">.*?</ul>', re.S)


def rd(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)


def slugs():
    out = []
    d = os.path.join(ROOT, 'site-source/news')
    for fn in sorted(os.listdir(d)):
        if fn.endswith('.md'):
            m = re.search(r'^slug:\s*(\S+)', rd(os.path.join(d, fn)), re.M)
            if m:
                out.append(m.group(1))
    return out


def build(tmp):
    def ign(path, names):
        return [n for n in names if n in ('.git', '_to_delete', 'node_modules') or n.startswith('_backup')]
    shutil.copytree(ROOT, tmp, ignore=ign, dirs_exist_ok=True)
    cmd = ['uv', 'run', '-q', '--python', '3.12', '--no-project', '--with', 'reportlab', '--with', 'pillow',
           'python', 'scripts/build_news.py']
    r = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=170)
    if r.returncode != 0:
        sys.exit('build_news 실패:\n' + r.stdout[-1500:] + r.stderr[-1500:])


def head_swap(page, built):
    for pat in (r'<title>[^<]*</title>', r'<meta name="description" content="[^"]*">',
                r'<meta property="og:title" content="[^"]*">', r'<meta property="og:description" content="[^"]*">'):
        b = re.search(pat, built)
        if b:
            page = re.sub(pat, lambda m: b.group(0), page, count=1)
    return page


def main():
    tmp = tempfile.mkdtemp(prefix='apnews_')
    try:
        build(tmp)
        all_slugs = slugs()
        changed, created = 0, []
        for l in LANGS:
            existing = [s for s in all_slugs if os.path.exists(os.path.join(ROOT, l, 'news', s, 'index.html'))]
            ref = existing[-1] if existing else None
            for s in all_slugs:
                bp = os.path.join(tmp, l, 'news', s, 'index.html')
                cp = os.path.join(ROOT, l, 'news', s, 'index.html')
                if not os.path.exists(bp):
                    continue
                built = rd(bp)
                bm = MAIN.search(built)
                if not bm:
                    continue
                if os.path.exists(cp):
                    cur = rd(cp)
                    new = MAIN.sub(lambda m: bm.group(0), cur, count=1)
                else:
                    if not ref:
                        continue
                    tpl = rd(os.path.join(ROOT, l, 'news', ref, 'index.html'))
                    a, b = tpl.split('<main id="main">', 1)
                    b = b.split('</main>', 1)[1]
                    new = head_swap(a.replace(ref, s), built) + bm.group(0) + b.replace(ref, s)
                    cur = None
                    created.append(f'{l}/news/{s}/')
                if new != cur:
                    wr(cp, new)
                    changed += 1
            ip, bip = os.path.join(ROOT, l, 'news', 'index.html'), os.path.join(tmp, l, 'news', 'index.html')
            if os.path.exists(ip) and os.path.exists(bip):
                cur, bg = rd(ip), GRID.search(rd(bip))
                if bg:
                    new = GRID.sub(lambda m: bg.group(0), cur, count=1)
                    if new != cur:
                        wr(ip, new)
                        changed += 1
        sp, bsp = os.path.join(ROOT, 'sitemap.xml'), os.path.join(tmp, 'sitemap.xml')
        cur = rd(sp)
        have = set(re.findall(r'<loc>([^<]+)</loc>', cur))
        add = [u for u in re.findall(r'<url><loc>[^<]*/news/[^<]*</loc>.*?</url>', rd(bsp), re.S)
               if re.search(r'<loc>([^<]+)</loc>', u).group(1) not in have]
        if add:
            wr(sp, cur.replace('</urlset>', ''.join(add) + '</urlset>'))
            changed += 1
        print('changed', changed, '· new pages', len(created), created, '· sitemap +', len(add))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
