#!/usr/bin/env python3
"""HOME v9 (2026-10-09): 시각 우선 · 글 최소. 실제 이미지와 도표로 서비스를 보여준다.
히어로 → 숫자 띠 → 이미지 서비스 6 → 캐릭터 띠 → 뉴스 이미지 카드 → 창업자 한 줄. 재실행해도 같음."""
import re, json, html, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; E=lambda s:html.escape(str(s),quote=True)
D=json.loads((ROOT/'site-source/divisions.json').read_text())
LOCS=['ko','en','vi','ja','zh-cn','fr']
DIVS=['intelligence','games','edu','entertainment','shop']
LABEL={d:d.capitalize() for d in DIVS}
IMG={'intelligence':'/media/gfx/safe_scene.jpg','games':'/media/gfx/lw_waves.jpg','edu':'/media/cubs/family.jpg','entertainment':'/media/lia/lia_hero_sq.jpg','shop':'/media/shop/01_dalba.jpg'}
TINT={'intelligence':'#e8f1ec','games':'#e9ecf7','edu':'#f7efe3','entertainment':'#f7e8f0','shop':'#e5f2f0'}
SAFE='https://apps.apple.com/kr/app/id6805684034'; LIGHT='https://apps.apple.com/kr/app/id6815295026'
T={
'ko':dict(h=['Built','with','AI.','Made','for','people.'],sub='성분 확인 · 게임 · 교육 · 캐릭터 · 쇼핑. 전부 한 팀이 직접 만듭니다.',svc='우리가 만드는 것',about='회사 소개',live='지금 운영 중',all='전체 보기',story='창업자 이야기',more='이어서 읽기',lab='Founder’s Lab',meet='캐릭터 만나기',charh='리아와 호랑이 네 남매.',
 lines={'intelligence':'성분표를 읽는 앱 — AP Safe · AP Light · AP SELECT','games':'하나의 티어, 여러 게임 — AP Games · RANKERS · LAST WAVE','edu':'놀면서 배우는 한국, 교실의 실시간 퀴즈 — K-Ranker · Hangeul Cubs · QuizRanker','entertainment':'AI 배우 리아와 호랑이 네 남매','shop':'한국 상품을 해외로 — Lia Select Shop · K-Craft'},stat=['사업','언어','운영 중 서비스']),
'en':dict(h=['Built','with','AI.','Made','for','people.'],sub='Ingredient checks · games · education · characters · shopping — all built in-house by one small team.',svc='What we make',about='About',live='Live now',all='See all',story='Founder’s story',more='Keep reading',lab='Founder’s Lab',meet='Meet the characters',charh='Lia and the four tiger cubs.',
 lines={'intelligence':'Apps that read labels — AP Safe · AP Light · AP SELECT','games':'One tier, many games — AP Games · RANKERS · LAST WAVE','edu':'Learn Korea by playing, live quizzes for class — K-Ranker · Hangeul Cubs · QuizRanker','entertainment':'Lia, the AI actor, and four tiger cubs','shop':'Korean products, shipped abroad — Lia Select Shop · K-Craft'},stat=['Businesses','Languages','Services live']),
'vi':dict(h=['Built','with','AI.','Made','for','people.'],sub='Kiểm tra thành phần · game · giáo dục · nhân vật · mua sắm — tất cả do một đội ngũ nhỏ tự làm.',svc='Những gì chúng tôi làm',about='Giới thiệu',live='Đang hoạt động',all='Xem tất cả',story='Câu chuyện người sáng lập',more='Đọc tiếp',lab='Founder’s Lab',meet='Gặp các nhân vật',charh='Lia và bốn chú hổ con.',
 lines={'intelligence':'Ứng dụng đọc nhãn — AP Safe · AP Light · AP SELECT','games':'Một hệ thống hạng, nhiều game — AP Games · RANKERS · LAST WAVE','edu':'Học Hàn Quốc qua trò chơi, quiz trực tiếp cho lớp — K-Ranker · Hangeul Cubs · QuizRanker','entertainment':'Diễn viên AI Lia và bốn chú hổ con','shop':'Hàng Hàn Quốc ra nước ngoài — Lia Select Shop · K-Craft'},stat=['Mảng','Ngôn ngữ','Dịch vụ đang chạy']),
'ja':dict(h=['Built','with','AI.','Made','for','people.'],sub='成分確認・ゲーム・教育・キャラクター・ショッピング。すべて小さなチームが自社で作ります。',svc='私たちが作るもの',about='会社紹介',live='運営中',all='すべて見る',story='創業者の話',more='続きを読む',lab='Founder’s Lab',meet='キャラクターを見る',charh='リアと4匹のトラの子。',
 lines={'intelligence':'ラベルを読むアプリ — AP Safe・AP Light・AP SELECT','games':'ひとつのティア、複数のゲーム — AP Games・RANKERS・LAST WAVE','edu':'遊びながら学ぶ韓国、教室のリアルタイムクイズ — K-Ranker・Hangeul Cubs・QuizRanker','entertainment':'AI俳優リアと4匹のトラの子','shop':'韓国の商品を海外へ — Lia Select Shop・K-Craft'},stat=['事業','言語','運営中サービス']),
'zh-cn':dict(h=['Built','with','AI.','Made','for','people.'],sub='成分查询 · 游戏 · 教育 · 角色 · 购物 — 全部由一支小团队自研。',svc='我们做的产品',about='关于我们',live='正在运营',all='查看全部',story='创始人的故事',more='继续阅读',lab='Founder’s Lab',meet='认识角色',charh='Lia 与四只小老虎。',
 lines={'intelligence':'会读标签的应用 — AP Safe、AP Light、AP SELECT','games':'统一段位，多款游戏 — AP Games、RANKERS、LAST WAVE','edu':'边玩边学韩国，课堂实时答题 — K-Ranker、Hangeul Cubs、QuizRanker','entertainment':'AI 演员 Lia 与四只小老虎','shop':'韩国商品，送往海外 — Lia Select Shop、K-Craft'},stat=['业务','语言','运营中服务']),
'fr':dict(h=['Built','with','AI.','Made','for','people.'],sub='Vérification des ingrédients · jeux · éducation · personnages · achats — tout est conçu en interne par une petite équipe.',svc='Ce que nous faisons',about='À propos',live='En service',all='Tout voir',story='L’histoire du fondateur',more='Lire la suite',lab='Founder’s Lab',meet='Voir les personnages',charh='Lia et les quatre tigreaux.',
 lines={'intelligence':'Des apps qui lisent les étiquettes — AP Safe · AP Light · AP SELECT','games':'Un seul rang, plusieurs jeux — AP Games · RANKERS · LAST WAVE','edu':'Apprendre la Corée en jouant, quiz en direct en classe — K-Ranker · Hangeul Cubs · QuizRanker','entertainment':'Lia, l’actrice IA, et quatre tigreaux','shop':'Produits coréens à l’étranger — Lia Select Shop · K-Craft'},stat=['Activités','Langues','Services en service']),
}
def orbit(l):
    """AP를 중심으로 다섯 사업이 도는 궤도 — 각 노드는 실제 제품 사진 + 이름, 허브로 링크"""
    L=[];Dd=[];N=[];C=[]
    for i,d in enumerate(DIVS):
        a=-math.pi/2+i*2*math.pi/len(DIVS); x=300+205*math.cos(a); y=300+205*math.sin(a)
        L.append(f'<line class="ob-l" style="--i:{i}" x1="300" y1="300" x2="{x:.0f}" y2="{y:.0f}"/>')
        Dd.append(f'<circle class="ob-dot" r="4"><animateMotion dur="3.2s" begin="{1.6+i*0.35:.2f}s" repeatCount="indefinite" path="M{x:.0f},{y:.0f} L300,300"/></circle>')
        C.append(f'<clipPath id="obc{i}"><circle cx="{x:.0f}" cy="{y:.0f}" r="46"/></clipPath>')
        ty=y+74 if y>=300 else y-58
        N.append(f'<a href="/{l}/{d}/" class="ob-n" style="--i:{i}"><circle class="ob-halo" cx="{x:.0f}" cy="{y:.0f}" r="50"/>'
                 f'<image href="{IMG[d]}" x="{x-46:.0f}" y="{y-46:.0f}" width="92" height="92" preserveAspectRatio="xMidYMid slice" clip-path="url(#obc{i})"/>'
                 f'<circle class="ob-rim" cx="{x:.0f}" cy="{y:.0f}" r="46"/><text x="{x:.0f}" y="{ty:.0f}" text-anchor="middle">{LABEL[d]}</text></a>')
    return ('<svg class="hv6-orbit hv9-orbit" viewBox="-20 -10 640 640" role="img" aria-label="AP: '+' · '.join(LABEL[d] for d in DIVS)+'"><defs>'+''.join(C)+'</defs>'
      '<circle class="ob-ring" cx="300" cy="300" r="205"/><circle class="ob-ring r2" cx="300" cy="300" r="120"/>'+''.join(L)+''.join(Dd)+
      '<circle class="ob-pulse" cx="300" cy="300" r="56"/><circle class="ob-core" cx="300" cy="300" r="56"/><text class="ob-ap" x="300" y="312" text-anchor="middle">AP</text>'+''.join(N)+'</svg>')
def news(l):
    f=ROOT/l/'news'/'index.html'
    if not f.exists(): return ''
    s=f.read_text(); out=[]
    for ch in s.split('<li class="news-item')[1:]:
        h=re.search(r'<a href="([^"]+)"',ch); t=re.search(r'<h2>(.*?)</h2>',ch,re.S); im=re.search(r'<img[^>]*src="([^"]+)"',ch); sv=re.search(r'(<svg class="cover".*?</svg>)',ch,re.S)
        if not(h and t): continue
        cover=(f'<img src="{im.group(1)}" alt="" loading="lazy">' if im else (sv.group(1) if sv else '<span class="nc-ph"></span>'))
        out.append(f'<li><a href="{h.group(1)}"><span class="nc-img">{cover}</span><h3>{t.group(1)}</h3></a></li>')
        if len(out)==3: break
    return ''.join(out)
def build(l):
    t=T[l]; st=D['_story'][l]; g='ko' if l=='ko' else 'en'
    words=''.join(f'<span class="w" style="--i:{i}">{E(w)}</span> ' for i,w in enumerate(t['h']))
    live=''.join(f'<a href="{u}" target="_blank" rel="noopener noreferrer"><i></i>{n}</a>' for n,u in [('AP Safe',SAFE),('AP Light',LIGHT),('AP Games',f'https://games.apholdings.kr/{g}/'),('Lia Select Shop','https://shop.apholdings.kr/')])
    tiles=''.join(f'<a class="svc-card" style="--i:{i};--tint:{TINT[d]}" href="/{l}/{d}/"><span class="sc-img"><img src="{IMG[d]}" alt="" loading="lazy"></span><span class="sc-body"><b>{LABEL[d]}</b><span>{E(t["lines"][d])}</span></span></a>' for i,d in enumerate(DIVS))
    cubs=''.join(f'<img src="/media/cubs/chars/{k}.webp" alt="" width="140" height="187" loading="lazy">' for k in ['daho','kkobi','aari','rami'])
    stats=''.join(f'<div><b>{v}</b><span>{lab}</span></div>' for v,lab in [(5,t['stat'][0]),(6,t['stat'][1]),(4,t['stat'][2])])
    return (f'<main id="main">'
      f'<section class="hv6" aria-label="AP Holdings"><div class="wrap hv6-in"><div class="hv6-copy">'
      f'<span class="eyebrow">AP HOLDINGS · AI PEOPLE</span><h1>{words}</h1><p class="hv7-sub">{E(t["sub"])}</p>'
      f'<div class="actions"><a class="button primary" href="/{l}/about/">{E(t["about"])}</a><a class="button ghost" href="/{l}/ir/">IR / INVESTORS</a></div></div>'
      f'<div class="hv6-art">{orbit(l)}</div></div>'
      f'<div class="hv6-live"><div class="wrap"><span>{E(t["live"])}</span>{live}</div></div></section>'
      f'<section class="section svc" id="businesses"><div class="wrap"><h2 class="svc-h">{E(t["svc"])}</h2><div class="svc-cards">{tiles}</div></div></section>'
      f'<section class="char-band" id="characters"><div class="wrap cb-in"><div class="cb-img"><img src="/media/lia/lia_hero_sq.jpg" alt="LIA" width="600" height="600" loading="lazy">{cubs}</div>'
      f'<div class="cb-copy"><h2>{E(t["charh"])}</h2><a class="button ghost-dark" href="/{l}/entertainment/">{E(t["meet"])} →</a></div></div></section>'
      f'<section class="section news-sec" id="news"><div class="wrap"><div class="hn-head"><h2>AP News</h2><a class="text-link" href="/{l}/news/">{E(t["all"])} →</a></div><ol class="news-cards">{news(l)}</ol></div></section>'
      f'<section class="story-band"><div class="wrap"><p>“{E(st["paras"][0])}”</p><a class="text-link" href="/{l}/about/#story">{E(t["more"])} →</a> <a class="text-link" href="/{l}/lab/">{E(t["lab"])} →</a></div></section>'
      f'</main>')
def main():
    n=0
    for l in LOCS:
        f=ROOT/l/'index.html'
        if not f.exists(): continue
        s=f.read_text(); o=s
        s=re.sub(r'<script data-v6>.*?</script>','',s,flags=re.S)
        s=re.sub(r'<main id="main">.*?</main>',lambda _:build(l),s,count=1,flags=re.S)
        s=re.sub(r'<title>.*?</title>',f'<title>AP HOLDINGS — {E(" ".join(T[l]["h"]))}</title>',s,count=1,flags=re.S)
        s=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{E(T[l]["sub"])}">',s,count=1)
        s=re.sub(r'<meta property="og:description" content="[^"]*">',f'<meta property="og:description" content="{E(T[l]["sub"])}">',s,count=1)
        s=re.sub(r'data-home="[^"]*"','data-home="v9"',s,count=1) if 'data-home=' in s else s.replace('<body','<body data-home="v9"',1)
        if s!=o: f.write_text(s); n+=1
    print({'home_v9':n})
if __name__=='__main__': main()
