#!/usr/bin/env python3
"""IR v12 (2026-10-15 대표 지시): 「05 · 왜 AP인가」에서 「창업자 15년」 카드 삭제 → 세 가지로. 6개 언어. 여러 번 실행해도 같은 결과."""
import re, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R = {
 'ko': [('네 가지가\n한 회사에 있다.', '세 가지가\n한 회사에 있다.'),
        ('사용자에게서 가져가지 않아 신뢰가 쌓이고,\n창업자가 현장을 안다.', '사용자에게서 가져가지 않아 신뢰가 쌓인다.')],
 'en': [('Four things\nin one company.', 'Three things\nin one company.'),
        ('channels already in hand, trust built by taking nothing from users, and a founder who knows the field.', 'channels already in hand, and trust built by taking nothing from users.')],
 'vi': [('Bốn điều\ntrong một công ty.', 'Ba điều\ntrong một công ty.'),
        ('các kênh đã nắm trong tay, niềm tin được xây dựng bằng cách không lấy gì từ người dùng, và một nhà sáng lập hiểu rõ lĩnh vực.', 'các kênh đã nắm trong tay, và niềm tin được xây dựng bằng cách không lấy gì từ người dùng.')],
 'ja': [('ひとつの会社に、\n四つの強み。', 'ひとつの会社に、\n三つの強み。'),
        ('すでに手元にあるチャネル、ユーザーから何も奪わないことで築く信頼、そして現場を知る創業者。', 'すでに手元にあるチャネル、そしてユーザーから何も奪わないことで築く信頼。')],
 'zh-cn': [('一家公司,\n四个优势。', '一家公司,\n三个优势。'),
           ('渠道已在手,以不向用户索取赢得的信任,以及一位了解行业的创始人。', '渠道已在手,以及以不向用户索取赢得的信任。')],
 'fr': [('Quatre atouts\nau sein d’une même entreprise.', 'Trois atouts\nau sein d’une même entreprise.'),
        ('des canaux déjà acquis, une confiance construite en ne prenant rien aux utilisateurs, et un fondateur qui connaît le terrain.', 'des canaux déjà acquis, et une confiance construite en ne prenant rien aux utilisateurs.')],
}
FOUNDER_H3 = ['창업자 15년', 'Founder, fifteen years', 'Nhà sáng lập, mười lăm năm', '創業者の15年', '创始人,十五年', 'Fondateur, quinze ans']
n = 0
for l, pairs in R.items():
    p = f'{l}/ir/index.html'; s = open(p, encoding='utf-8').read(); t = s
    for a, b in pairs: t = t.replace(a, b)
    for h in FOUNDER_H3:
        t = re.sub(r'<article><span>[^<]*</span><h3>' + re.escape(h) + r'</h3><p>[^<]*</p></article>', '', t)
    # 05 섹션의 카드 묶음을 3칸으로
    m = re.search(r'(<span class="number">05 · .*?)<div class="milestones">', t, re.S)
    if m and '<div class="milestones m3">' not in t[m.start():m.end() + 30]:
        t = t[:m.end() - len('<div class="milestones">')] + '<div class="milestones m3">' + t[m.end():]
    if t != s: open(p, 'w', encoding='utf-8').write(t); n += 1
css = 'assets/v2/site.css'; c = open(css, encoding='utf-8').read()
MARK = '/* ir v12: 세 칸 카드 */'
if MARK not in c:
    c = c.rstrip('\n') + '\n' + MARK + '\n@media(min-width:801px){.milestones.m3{grid-template-columns:repeat(3,1fr)}}\n'
    open(css, 'w', encoding='utf-8').write(c); n += 1
print('changed', n)
