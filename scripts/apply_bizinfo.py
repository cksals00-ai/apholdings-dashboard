#!/usr/bin/env python3
"""사업자 정보 푸터 줄 (2026-10-21, 클레어 · 대표 지시 「통신판매업 신고번호 홈페이지에도 노출」).

생성된 HTML의 <div class="footer-bottom"> 바로 앞에 <p class="footer-biz"> 한 줄을 넣는다.
원고는 site-source/business-info.json. 여러 번 실행해도 결과가 같다(기존 줄은 지우고 다시 넣음).
한국어 페이지(/ko/ 와 루트 한국어 페이지)는 한국어, 나머지는 영어.
"""
import json, os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = json.load(open(os.path.join(ROOT, 'site-source/business-info.json'), encoding='utf-8'))
E = lambda s: html.escape(str(s), quote=True)
STYLE = 'font-size:12px;line-height:1.6;color:var(--muted,#5b6260);margin:0 0 12px;word-break:keep-all'
OLD = re.compile(r'<p class="footer-biz"[^>]*>.*?</p>', re.S)
SKIP = ('_backup', '.git', 'node_modules', 'admin')

def line(ko):
    v = f'<a href="{E(B["verify_url"])}" target="_blank" rel="noopener noreferrer">' + ('사업자정보 확인' if ko else 'Verify') + '</a>'
    if ko:
        parts = [B['name_ko'], '대표 ' + B['ceo_ko'], '사업자등록번호 ' + B['biz_no'], '통신판매업신고 ' + B['mailorder_ko']]
    else:
        parts = [B['name_en'], 'CEO ' + B['ceo_en'], 'Business Reg. No. ' + B['biz_no'], 'Mail-order Sales Reg. No. ' + B['mailorder_en']]
    return f'<p class="footer-biz" style="{STYLE}">' + ' · '.join(E(p) for p in parts) + ' · ' + v + '</p>'

def main():
    n = 0
    for d, dirs, files in os.walk(ROOT):
        rel = os.path.relpath(d, ROOT)
        if any(rel == s or rel.startswith(s + os.sep) or ('/' + s + '/') in ('/' + rel + '/') for s in SKIP):
            dirs[:] = []
            continue
        for fn in files:
            if not fn.endswith('.html'):
                continue
            p = os.path.join(d, fn)
            s = open(p, encoding='utf-8').read()
            if '<div class="footer-bottom">' not in s:
                continue
            m = re.search(r'<html[^>]*\blang="([^"]+)"', s)
            ko = (m.group(1).lower().startswith('ko')) if m else rel.split(os.sep)[0] == 'ko'
            t = OLD.sub('', s)
            t = t.replace('<div class="footer-bottom">', line(ko) + '<div class="footer-bottom">', 1)
            if t != s:
                open(p, 'w', encoding='utf-8').write(t); n += 1
    print('pages', n)

if __name__ == '__main__':
    main()
