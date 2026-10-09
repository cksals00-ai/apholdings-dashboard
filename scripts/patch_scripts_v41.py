#!/usr/bin/env python3
"""IA v4.1 (2026-10-09): Hallyu 칸을 없애고 Edu로 합친다. 저장소 루트에서 1회 실행(재실행 안전)."""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def patch(path, pairs):
    p = ROOT / path; s = p.read_text(); o = s
    for a, b in pairs:
        if a not in s and b in s: continue
        assert a in s, (path, a[:70]); s = s.replace(a, b)
    if s != o: p.write_text(s)
    print('patched', path)

# ---- apply_ia_v4.py: 5 divisions, grouped hub items, hallyu redirect
patch('scripts/apply_ia_v4.py', [
 ("DIVS = ['intelligence', 'games', 'edu', 'hallyu', 'entertainment', 'shop']", "DIVS = ['intelligence', 'games', 'edu', 'entertainment', 'shop']"),
 (" ('edu', ['/edu/', '/products/rgrg/']),\n ('hallyu', ['/hallyu/', '/products/cubs/', '/products/craft/']),", " ('edu', ['/edu/', '/products/rgrg/', '/products/cubs/']),"),
 (" ('shop', ['/shop/', '/products/commerce/', '/products/liaselect/']),", " ('shop', ['/shop/', '/products/commerce/', '/products/liaselect/', '/products/craft/']),"),
 # grouped items in hub_main
 ("    cards = []\n    for it in c['items']:\n        url = fill(it.get('url', ''), l); ext = url.startswith('http')",
  "    cards = []; last_group = None\n    for it in c['items']:\n        if it.get('group') and it['group'] != last_group:\n            cards.append(f'<h2 class=\"hub-group\">{E(it[\"group\"])}</h2>'); last_group = it['group']\n        url = fill(it.get('url', ''), l); ext = url.startswith('http')"),
 # footer: drop hallyu column, edu shows 4, shop 4
 ("     '<div>' + head('edu') + items('edu') + '</div>',\n     '<div>' + head('hallyu') + items('hallyu', 4) + '</div>',",
  "     '<div>' + head('edu') + items('edu', 4) + '</div>',"),
 ("     '<div>' + head('shop') + items('shop', 3) + '</div>',", "     '<div>' + head('shop') + items('shop', 4) + '</div>',"),
 # redirects: hallyu → edu
 ("        f = ROOT / l / 'products' / 'rankers' / 'index.html'\n        if f.exists(): f.write_text(REDIRECT.replace('{l}', l).replace('{to}', rankers_url(l)))",
  "        f = ROOT / l / 'products' / 'rankers' / 'index.html'\n        if f.exists(): f.write_text(REDIRECT.replace('{l}', l).replace('{to}', rankers_url(l)))\n        f = ROOT / l / 'hallyu' / 'index.html'\n        if f.exists(): f.write_text(REDIRECT.replace('{l}', l).replace('{to}', f'/{l}/edu/'))"),
 ("    s = re.sub(r'href=\"/([a-z-]+)/media/\"', r'href=\"/\\1/entertainment/\"', s)",
  "    s = re.sub(r'href=\"/([a-z-]+)/media/\"', r'href=\"/\\1/entertainment/\"', s)\n    s = re.sub(r'href=\"/([a-z-]+)/hallyu/(#[a-z-]+)?\"', r'href=\"/\\1/edu/\"', s)"),
 ("    x = re.sub(r'<url><loc>https://www\\.apholdings\\.kr/[a-z-]+/(?:media|products/rankers|products/revenue|products/travel)/</loc>.*?</url>', '', x)",
  "    x = re.sub(r'<url><loc>https://www\\.apholdings\\.kr/[a-z-]+/(?:media|hallyu|products/rankers|products/revenue|products/travel)/</loc>.*?</url>', '', x)"),
 ("    g = [p for p in g if not re.match(r'[a-z-]+/(media|products/rankers|products/revenue|products/travel)/index\\.html$', p)]",
  "    g = [p for p in g if not re.match(r'[a-z-]+/(media|hallyu|products/rankers|products/revenue|products/travel)/index\\.html$', p)]"),
 # css: group heading
 (".hub-links{display:flex;flex-wrap:wrap;gap:12px 28px;margin-top:38px;padding-top:22px;border-top:1px solid var(--line)}",
  ".hub-links{display:flex;flex-wrap:wrap;gap:12px 28px;margin-top:38px;padding-top:22px;border-top:1px solid var(--line)}\n.hub-group{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:700;margin:34px 0 6px;padding-top:0}.hub-group:first-child{margin-top:0}"),
])

# ---- v5 pages: products cubs→edu, craft→shop; DIVS without hallyu
patch('scripts/apply_pages_v5.py', [
 ("DIVS=['intelligence','games','edu','hallyu','shop']", "DIVS=['intelligence','games','edu','shop']"),
 ("'cubs':('hallyu','live'),'craft':('hallyu','soon')", "'cubs':('edu','live'),'craft':('shop','soon')"),
])
# ---- v5 cleanup: five divisions
patch('scripts/apply_cleanup_v5.py', [
 ("DIVS=['intelligence','games','edu','hallyu','entertainment','shop']", "DIVS=['intelligence','games','edu','entertainment','shop']"),
 ("H={'ko':'여섯 사업.','en':'Six businesses.','vi':'Sáu mảng.','ja':'6つの事業。','zh-cn':'六项业务。','fr':'Six activités.'}",
  "H={'ko':'다섯 사업.','en':'Five businesses.','vi':'Năm mảng.','ja':'5つの事業。','zh-cn':'五项业务。','fr':'Cinq activités.'}"),
])
# ---- v5 home: no hallyu node, five
patch('scripts/apply_home_v5.py', [
 ("{node(l,\"hallyu\",\"Hallyu\")}{node(l,\"edu\",\"Edu\")}", "{node(l,\"edu\",\"Edu\")}"),
 ("여섯 개 사업이 하나의 흐름으로 움직입니다.", "다섯 개 사업이 하나의 흐름으로 움직입니다."), ("flowh='여섯 사업, 하나의 흐름.'", "flowh='다섯 사업, 하나의 흐름.'"),
 ("Six businesses move as one flow.", "Five businesses move as one flow."), ("flowh='Six businesses. One flow.'", "flowh='Five businesses. One flow.'"),
 ("Sáu mảng kinh doanh vận hành như một dòng chảy.", "Năm mảng kinh doanh vận hành như một dòng chảy."), ("flowh='Sáu mảng. Một dòng chảy.'", "flowh='Năm mảng. Một dòng chảy.'"),
 ("6つの事業がひとつの流れで動きます。", "5つの事業がひとつの流れで動きます。"), ("flowh='6つの事業、ひとつの流れ。'", "flowh='5つの事業、ひとつの流れ。'"),
 ("六项业务汇成一条流程。", "五项业务汇成一条流程。"), ("flowh='六项业务，一条流程。'", "flowh='五项业务，一条流程。'"),
 ("Six activités, un seul mouvement.", "Cinq activités, un seul mouvement."), ("flowh='Six activités. Un seul mouvement.'", "flowh='Cinq activités. Un seul mouvement.'"),
])
# ---- check_site: no Hallyu requirement
patch('scripts/check_site.py', [("'Edu','Hallyu','Entertainment'", "'Edu','Entertainment'")])
print('done')
