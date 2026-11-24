#!/usr/bin/env python3
"""HOME v5 (2026-10-09): /{l}/index.html 의 <main>을 기획서 1번 구성으로 교체. 재실행해도 결과가 같음. build_site 재실행 금지.
구성: 히어로 → 6부문 흐름 그래픽 → 지금 바로 쓰기(4) → 캐릭터 한 줄 → AP News 최신 3(각 언어 /news/ 목록에서 읽음) → 창업자 이야기 발췌.
다국어 문구 중 ko·en 외는 초안(검수 필요). 끝나면 python3 scripts/check_site.py."""
import re, json, html
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = lambda s: html.escape(str(s), quote=True)
D = json.loads((ROOT/'site-source/divisions.json').read_text())
LOCS = ['ko','en','vi','ja','zh-cn','fr']
SAFE='https://apps.apple.com/kr/app/id6805684034'; LIGHT='https://apps.apple.com/kr/app/id6815295026'
T = {
 'ko':dict(h='AI와 사람을 잇는 회사.',s='판단은 사람에게, 번거로움은 AI에게. 다섯 개 사업이 하나의 흐름으로 움직입니다.',about='회사 소개',bring='데려온다',stay='머물게 한다',earn='매출을 만든다',base='데이터와 가맹으로 받친다',flowh='다섯 사업, 하나의 흐름.',useh='지금 바로 쓸 수 있는 것.',safe='우리 아이가 피하는 성분을 공개 자료로 확인',light='100g 기준 말고, 한 봉지 기준 열량',games='로그인 하나로 웹 게임과 순위표',shop='리아가 고른 한국 상품, 쇼피에서',app='App Store',web='웹에서 열기',buy='쇼핑하기',charh='리아와 호랑이 네 남매.',chars='AP를 세상에 소개하는 얼굴들.',meet='캐릭터 만나기',newsh='AP News',all='전체 보기',story='창업자 이야기',more='이어서 읽기'),
 'en':dict(h='Connecting AI and people.',s='People decide; AI takes the hassle. Five businesses move as one flow.',about='About',bring='Bring people in',stay='Make them stay',earn='Drive revenue',base='Underpinned by data and franchise',flowh='Five businesses. One flow.',useh='Ready to use today.',safe='Check the ingredients your child avoids against public data',light='Calories per bag, not just per 100 g',games='One login for web games and leaderboards',shop='Korean picks by Lia, on Shopee',app='App Store',web='Open on web',buy='Shop now',charh='Lia and the four tiger cubs.',chars='The faces that introduce AP to the world.',meet='Meet the characters',newsh='AP News',all='See all',story='Founder’s story',more='Keep reading'),
 'vi':dict(h='Kết nối AI và con người.',s='Con người quyết định; AI lo phần phiền phức. Năm mảng kinh doanh vận hành như một dòng chảy.',about='Giới thiệu',bring='Đưa người đến',stay='Giữ chân',earn='Tạo doanh thu',base='Nền tảng dữ liệu và nhượng quyền',flowh='Năm mảng. Một dòng chảy.',useh='Dùng được ngay hôm nay.',safe='Kiểm tra thành phần con cần tránh bằng dữ liệu công khai',light='Calo theo cả gói, không chỉ theo 100 g',games='Một lần đăng nhập cho game web và bảng xếp hạng',shop='Hàng Hàn do Lia chọn, trên Shopee',app='App Store',web='Mở trên web',buy='Mua sắm',charh='Lia và bốn chú hổ con.',chars='Những gương mặt giới thiệu AP với thế giới.',meet='Gặp các nhân vật',newsh='AP News',all='Xem tất cả',story='Câu chuyện người sáng lập',more='Đọc tiếp'),
 'ja':dict(h='AIと人をつなぐ会社。',s='判断は人に、手間はAIに。5つの事業がひとつの流れで動きます。',about='会社紹介',bring='人を呼ぶ',stay='とどまらせる',earn='売上をつくる',base='データと加盟で支える',flowh='5つの事業、ひとつの流れ。',useh='今すぐ使えるもの。',safe='子どもが避ける成分を公開データで確認',light='100gではなく、1袋あたりのカロリー',games='ひとつのログインでWebゲームとランキング',shop='リアが選んだ韓国の品を、Shopeeで',app='App Store',web='Webで開く',buy='ショップへ',charh='リアと4匹のトラの子。',chars='APを世界に紹介する顔ぶれ。',meet='キャラクターを見る',newsh='AP News',all='すべて見る',story='創業者の話',more='続きを読む'),
 'zh-cn':dict(h='连接 AI 与人。',s='判断交给人，麻烦交给 AI。五项业务汇成一条流程。',about='关于我们',bring='带来人',stay='留住人',earn='创造收入',base='以数据与加盟支撑',flowh='五项业务，一条流程。',useh='现在就能用。',safe='用公开数据核对孩子要避开的成分',light='按整袋计算热量，而不只是每100克',games='一次登录，网页游戏与排行榜',shop='Lia 精选韩国商品，在 Shopee',app='App Store',web='在网页打开',buy='去购物',charh='Lia 与四只小老虎。',chars='把 AP 介绍给世界的面孔。',meet='认识角色',newsh='AP News',all='查看全部',story='创始人的故事',more='继续阅读'),
 'fr':dict(h='Relier l’IA et les humains.',s='L’humain décide, l’IA s’occupe du reste. Cinq activités, un seul mouvement.',about='À propos',bring='Attirer',stay='Retenir',earn='Générer du revenu',base='Porté par la donnée et la franchise',flowh='Cinq activités. Un seul mouvement.',useh='Disponible dès aujourd’hui.',safe='Vérifiez les ingrédients que votre enfant évite, sur données publiques',light='Les calories par sachet, pas seulement pour 100 g',games='Un seul compte pour les jeux web et les classements',shop='Les choix coréens de Lia, sur Shopee',app='App Store',web='Ouvrir sur le web',buy='Acheter',charh='Lia et les quatre tigreaux.',chars='Les visages qui présentent AP au monde.',meet='Voir les personnages',newsh='AP News',all='Tout voir',story='L’histoire du fondateur',more='Lire la suite'),
}
SM = lambda l: D['_sitemap'][l]['d']
def a(u,x,cls='text-link',ext=False): return f'<a class="{cls}" href="{E(u)}"'+(' target="_blank" rel="noopener noreferrer"' if ext else '')+f'>{x}</a>'
def node(l,d,name=None): return f'<a class="fl-node" href="/{l}/{d}/"><b>{name or d.capitalize()}</b><span>{E(SM(l)[d])}</span></a>'
def news3(l):
    f=ROOT/l/'news'/'index.html'
    if not f.exists(): return ''
    s=f.read_text(); out=[]
    for m in re.finditer(r'<li class="news-item[^"]*"[^>]*><a href="([^"]+)">.*?<div class="news-meta">(.*?)</div><h2>(.*?)</h2>',s,re.S):
        meta=re.sub('<[^>]+>','',m.group(2)); date=(re.findall(r'\d{4}\.\d{2}\.\d{2}',meta) or [''])[-1]
        out.append(f'<li><a href="{m.group(1)}"><span class="hn-date">{date}</span><span class="hn-t">{m.group(3)}</span></a></li>')
        if len(out)==3: break
    return ''.join(out)
def main_html(l):
    t=T[l]; st=D['_story'][l]
    flow=(f'<div class="hflow" role="list">'
      f'<div class="fl-col" role="listitem"><span class="fl-k">01 · {t["bring"]}</span>{node(l,"entertainment","Entertainment")}<a class="fl-node" href="/{l}/news/"><b>News</b><span>{E(SM(l)["news"])}</span></a></div>'
      f'<div class="fl-col" role="listitem"><span class="fl-k">02 · {t["stay"]}</span>{node(l,"edu","Edu")}{node(l,"games","Games")}</div>'
      f'<div class="fl-col" role="listitem"><span class="fl-k">03 · {t["earn"]}</span>{node(l,"shop","Shop")}</div>'
      f'<div class="fl-base" role="listitem"><span class="fl-k">04 · {t["base"]}</span>{node(l,"intelligence","Intelligence")}</div></div>')
    g='ko' if l=='ko' else 'en'
    use=[('AP Safe',t['safe'],SAFE,t['app']),('AP Light',t['light'],LIGHT,t['app']),('AP Games',t['games'],f'https://games.apholdings.kr/{g}/',t['web']),('Lia Select Shop',t['shop'],'https://shop.apholdings.kr/',t['buy'])]
    uses=''.join(f'<li><span class="status">{E(D["_common"][l]["live"])}</span><h3>{n}</h3><p>{E(p)}</p>{a(u,E(c)+" ↗",ext=True)}</li>' for n,p,u,c in use)
    return (f'<main id="main">'
     f'<section class="hero home-hero hv5"><div class="wrap"><span class="eyebrow">AP HOLDINGS</span><h1>{E(t["h"])}</h1><p class="lead">{E(t["s"])}</p>'
     f'<div class="actions">{a(f"/{l}/about/",E(t["about"]),"button")}{a(f"/{l}/ir/","IR / INVESTORS","button primary")}</div></div></section>'
     f'<section class="section hv5-flow" id="businesses"><div class="wrap"><h2>{E(t["flowh"])}</h2>{flow}</div></section>'
     f'<section class="section hv5-use" id="use"><div class="wrap"><h2>{E(t["useh"])}</h2><ul class="use-list">{uses}</ul></div></section>'
     f'<section class="section soft hv5-char" id="characters"><div class="wrap hc-in"><div class="hc-img"><img src="/media/lia/lia_hero_sq.jpg" alt="LIA" width="600" height="600" loading="lazy">'
     + ''.join(f'<img src="/media/cubs/chars/{k}.webp" alt="" width="140" height="187" loading="lazy">' for k in ['daho','kkobi','aari','rami'])
     + f'</div><div><h2>{E(t["charh"])}</h2><p class="lead">{E(t["chars"])}</p>{a(f"/{l}/entertainment/",E(t["meet"])+" →")}</div></div></section>'
     f'<section class="section hv5-news" id="news"><div class="wrap"><div class="hn-head"><h2>{t["newsh"]}</h2>{a(f"/{l}/news/",E(t["all"])+" →")}</div><ol class="hn-list">{news3(l)}</ol></div></section>'
     f'<section class="section hv5-story" id="story"><div class="wrap"><span class="eyebrow">{E(t["story"])}</span><blockquote><p>{E(st["paras"][0])}</p><p>{E(st["paras"][1])}</p></blockquote>{a(f"/{l}/about/#story",E(t["more"])+" →")}</div></section>'
     f'</main>')
def main():
    n=0
    for l in LOCS:
        f=ROOT/l/'index.html'
        if not f.exists(): continue
        s=f.read_text(); new=re.sub(r'<main id="main">.*?</main>',lambda _:main_html(l),s,count=1,flags=re.S)
        new=re.sub(r'<title>.*?</title>',f'<title>AP HOLDINGS — {E(T[l]["h"])}</title>',new,count=1,flags=re.S)
        if new!=s: f.write_text(new); n+=1
    print({'home_pages':n})
if __name__=='__main__': main()
