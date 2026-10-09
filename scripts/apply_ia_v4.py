#!/usr/bin/env python3
"""Idempotent IA v4 postprocessor. Preserve edited HTML and News; never rebuild_site.
Reference: owner-approved IA proposal 7, 2026-10-09.
Hallyu DNS migration is DNS verified by public resolver on 2026-10-09; domain cutover tracked separately.
"""
import re,json,copy
from pathlib import Path
import apply_ia_v3 as v3
ROOT=Path(__file__).resolve().parents[1]; E=v3.E; LOCS=v3.LOCS
DIVS=['intelligence','games','edu','hallyu','entertainment','shop']
LABEL={d:d.title() for d in DIVS}
# Same content in all six languages; menu and product brands remain English.
COPY={
'ko':['국내 교육을, 함께하는 퀴즈로.','학교·학원·기업을 위한 한국어 퀴즈와 교육 콘텐츠.','국내 학교 · 학원 · 교육 담당자','학교 · 학원 퀴즈 팩','수업과 연수에 쓰는 문제 묶음을 준비하고 있습니다.','준비 중','한국을 만나는 여러 가지 방법.','퀴즈와 한글, 공예로 한국 문화를 만납니다.','한국 문화가 궁금한 해외 이용자','한국을 주제로 겨루는 외국인 대상 퀴즈 앱.','App Store 심사 중','한글 학습 사이트','캐릭터·레슨·30일 챌린지를 만나 보세요.','K-Food · K-Pop 콘텐츠를 준비하고 있습니다.','캐릭터에서 시작되는 이야기.','리아와 호랑이 네 남매를 만나 보세요.','한국의 브랜드와 문화를 발견하는 사람들','AI 홍보 배우 · 한국의 브랜드와 문화','페르소나, 뮤직비디오와 촬영 이야기. Instagram·TikTok에서 만나고 Lia Select Shop으로 이어집니다.','호랑이 4남매','다호 · 꼬비 · 아리 · 라미와 함께하는 한글 영상. 앱과 수업은 Hallyu에서.','프랜차이즈 · 상담과 체험은 매장, 주문은 온라인','사업 소개','자세히 보기','회사 소개','전체 사이트맵','브랜드 · 사업 · 회사 정보를 한눈에.','한글 영상 보기','진행 · 정리','단어 · 소리','발음 · 노래','쓰기 · 응원'],
'en':['Quizzes for learning together.','Korean-language quizzes and educational content for schools, academies and companies.','Schools, academies and educators in Korea','School & academy quiz packs','Question packs for classes and training are in preparation.','In preparation','More ways to discover Korea.','Explore Korean culture through quizzes, Hangul and craft.','International audiences curious about Korea','A Korea-themed quiz app for international players.','In App Store review','Hangul learning site','Meet the characters, lessons and 30-day challenge.','K-Food and K-Pop content is in preparation.','Stories begin with characters.','Meet LIA and the four tiger siblings.','People discovering Korean brands and culture','AI promotional actor · Korean brands and culture','Persona, music videos and behind the scenes. Meet LIA on Instagram and TikTok, then explore Lia Select Shop.','Four tiger siblings','Daho, Kkobi, Aari and Rami in Hangul videos. Find the app and lessons in Hallyu.','Franchise · advice and experience in store, orders online','Our businesses','Explore','About','Sitemap','Brands, businesses and company information at a glance.','Watch Hangul videos','Host · wrap-up','Words · sounds','Pronunciation · songs','Writing · cheering'],
'vi':['Cùng học qua câu đố.','Câu đố tiếng Hàn và nội dung giáo dục cho trường học, học viện và doanh nghiệp.','Trường học, học viện và nhà giáo dục tại Hàn Quốc','Gói câu đố cho trường học','Đang chuẩn bị bộ câu hỏi cho lớp học và đào tạo.','Đang chuẩn bị','Nhiều cách khám phá Hàn Quốc.','Khám phá văn hóa Hàn qua câu đố, Hangul và thủ công.','Người nước ngoài quan tâm đến Hàn Quốc','Ứng dụng đố vui về Hàn Quốc dành cho người nước ngoài.','Đang xét duyệt App Store','Trang học Hangul','Nhân vật, bài học và thử thách 30 ngày.','Đang chuẩn bị nội dung K-Food và K-Pop.','Câu chuyện bắt đầu từ nhân vật.','Gặp LIA và bốn anh em hổ.','Người khám phá thương hiệu và văn hóa Hàn','Diễn viên quảng bá AI · thương hiệu và văn hóa Hàn','Chân dung, video âm nhạc và hậu trường. Gặp LIA trên Instagram, TikTok và khám phá Lia Select Shop.','Bốn anh em hổ','Daho, Kkobi, Aari và Rami trong video Hangul. Ứng dụng và bài học nằm ở Hallyu.','Nhượng quyền · tư vấn và trải nghiệm tại cửa hàng, đặt hàng trực tuyến','Các lĩnh vực','Khám phá','Giới thiệu','Sơ đồ trang','Thương hiệu, lĩnh vực và thông tin công ty.','Xem video Hangul','Dẫn chương trình · tổng kết','Từ ngữ · âm thanh','Phát âm · bài hát','Viết · cổ vũ'],
'ja':['一緒に学ぶ、クイズの時間。','学校・塾・企業向けの韓国語クイズと教育コンテンツ。','韓国内の学校・塾・教育担当者','学校・塾向けクイズパック','授業や研修で使う問題集を準備しています。','準備中','韓国と出会う、さまざまな方法。','クイズ、ハングル、工芸で韓国文化に触れます。','韓国文化に関心のある海外の方','海外の方に向けた、韓国がテーマのクイズアプリ。','App Store審査中','ハングル学習サイト','キャラクター、レッスン、30日チャレンジ。','K-Food・K-Popコンテンツは準備中です。','キャラクターから始まる物語。','LIAとトラの4きょうだいに会いましょう。','韓国のブランドや文化を知りたい方','AIプロモーション俳優 · 韓国のブランドと文化','人物紹介、ミュージックビデオ、撮影の舞台裏。Instagram・TikTokからLia Select Shopへ。','トラの4きょうだい','Daho・Kkobi・Aari・Ramiのハングル動画。アプリと授業はHallyuへ。','フランチャイズ · 相談と体験は店舗、注文はオンライン','事業紹介','詳しく見る','会社紹介','サイトマップ','ブランド・事業・会社情報を一覧に。','ハングル動画を見る','進行 · まとめ','単語 · 音','発音 · 歌','書く · 応援'],
'zh-cn':['一起用问答来学习。','面向学校、培训机构和企业的韩语问答与教育内容。','韩国学校、培训机构及教育负责人','学校与培训机构题包','课堂和培训题包正在准备中。','准备中','以多种方式发现韩国。','通过问答、韩文和工艺体验韩国文化。','对韩国文化感兴趣的海外用户','面向海外用户、以韩国为主题的问答应用。','App Store 审核中','韩文学习网站','认识角色、课程和30天挑战。','K-Food与K-Pop内容正在准备中。','故事，从角色开始。','认识LIA和四只小老虎。','发现韩国品牌与文化的人们','AI推广演员 · 韩国品牌与文化','人物介绍、音乐视频与拍摄幕后。在Instagram、TikTok认识LIA，再探索Lia Select Shop。','四只小老虎','与Daho、Kkobi、Aari、Rami一起看韩文视频。应用和课程请前往Hallyu。','加盟业务 · 门店咨询体验，线上下单','业务介绍','了解更多','关于我们','网站地图','一览品牌、业务和公司信息。','观看韩文视频','主持 · 总结','单词 · 声音','发音 · 歌曲','书写 · 鼓励'],
'fr':['Apprendre ensemble par le quiz.','Quiz en coréen et contenus éducatifs pour écoles, académies et entreprises.','Écoles, académies et enseignants en Corée','Packs de quiz éducatifs','Des séries de questions pour les cours et formations sont en préparation.','En préparation','Plusieurs façons de découvrir la Corée.','Explorez la culture coréenne par les quiz, le hangeul et l’artisanat.','Public international curieux de la Corée','Une application de quiz sur la Corée pour le public international.','En cours de validation App Store','Site d’apprentissage du hangeul','Personnages, leçons et défi de 30 jours.','Les contenus K-Food et K-Pop sont en préparation.','Les histoires commencent par les personnages.','Rencontrez LIA et les quatre petits tigres.','Les personnes qui découvrent les marques et la culture coréennes','Actrice promotionnelle IA · marques et culture coréennes','Portrait, clips et coulisses. Retrouvez LIA sur Instagram et TikTok, puis découvrez Lia Select Shop.','Quatre petits tigres','Daho, Kkobi, Aari et Rami en vidéo. L’application et les cours se trouvent dans Hallyu.','Franchise · conseil et expérience en magasin, commande en ligne','Nos activités','Découvrir','À propos','Plan du site','Marques, activités et informations sur l’entreprise.','Voir les vidéos de hangeul','Présentation · synthèse','Mots · sons','Prononciation · chansons','Écriture · encouragement']}
H=copy.deepcopy(v3.HUB)
for l in LOCS:
 c=COPY[l]; select=next(x for x in H['shop'][l]['items'] if x['name']=='AP SELECT');select['tag']=c[21]
 H['intelligence'][l]['items'].insert(2,select)
 H['games'][l]['items']=[x for x in H['games'][l]['items'] if x['name']!='QuizRanker']
 oldedu=H['edu'][l]
 craft=next(x for x in H['shop'][l]['items'] if x['name']=='K-Craft')
 H.setdefault('hallyu',{})[l]={'eyebrow':'HALLYU','title':c[6],'lead':c[7],'for':c[8],'items':[{'name':'K-Ranker','tag':c[9],'desc':c[10],'status':c[10]},oldedu['items'][0],{'name':c[11],'tag':'Hangeul Cubs','desc':c[12],'url':'https://hallyu.apholdings.kr/{edu}/'},craft,{'name':'K-Food · K-Pop','tag':c[5],'desc':c[13],'status':c[5]}]}
 H['edu'][l]={'eyebrow':'EDU','title':c[0],'lead':c[1],'for':c[2],'items':[{'name':'QuizRanker','tag':c[1],'desc':c[2],'url':'/{l}/products/rgrg/'},{'name':c[3],'tag':c[5],'desc':c[4],'status':c[5]}]}
 H.setdefault('entertainment',{})[l]={'eyebrow':'ENTERTAINMENT','title':c[14],'lead':c[15],'for':c[16],'items':[{'name':'LIA','tag':c[17],'desc':c[18],'url':'/{l}/products/lia/'},{'name':'Hangeul Cubs','tag':c[19],'desc':c[20],'url':'/{l}/hallyu/'}]}
 H['shop'][l]['items']=[x for x in H['shop'][l]['items'] if x['name']!='AP SELECT']
 for x in H['shop'][l]['items']:
  if x['name']=='K-Craft':x['url']='/{l}/hallyu/#k-craft'
v3.HUB=H;v3.DIV_LABEL=LABEL

def section(rel):
 p='/'+rel.split('/',1)[-1]
 if rel.endswith('index.html') and rel.count('/')==1:return 'home'
 for d,paths in [('intelligence',['/intelligence/','/products/safe/','/products/light/','/products/select/']),('games',['/games/','/rankers/','/products/lastwave/']),('edu',['/edu/','/products/rgrg/']),('hallyu',['/hallyu/','/products/cubs/','/products/craft/']),('entertainment',['/entertainment/','/products/lia/']),('shop',['/shop/','/products/liaselect/','/products/commerce/']),('news',['/news/']),('about',['/about/','/brand/','/ir/','/lab/']),('sitemap',['/sitemap/'])]:
  if any(p.startswith(x) for x in paths):return d

def a(url,label,cur=False):return f'<a href="{E(url)}"'+(' aria-current="page"' if cur else '')+f'>{E(label)}</a>'
def links(l,sec):
 return [(f'/{l}/','Home','home')]+[(f'/{l}/{d}/',LABEL[d],d) for d in DIVS]+[(f'/{l}/news/','News','news'),(f'/{l}/about/','About','about'),('/admin/','Admin','admin'),(f'/{l}/sitemap/','Sitemap','sitemap')]
def langlinks():return ''.join(a(f'/{l}/',name) for l,name in [('ko','한국어'),('en','English'),('vi','Tiếng Việt'),('ja','日本語'),('zh-cn','简体中文'),('fr','Français')])
def nav(l,sec):
 items=links(l,sec);desk='<nav class="desktop-nav" aria-label="Main">'+''.join(a(u,n,k==sec) for u,n,k in items)+'</nav>'
 mob='<nav aria-label="Mobile">'+a(f'/{l}/','Home',sec=='home')+'<details class="mobile-business"><summary>Business</summary><div>'+''.join(a(f'/{l}/{d}/',LABEL[d],sec==d) for d in DIVS)+'</div></details>'+''.join(a(u,n,k==sec) for u,n,k in items if k in ['news','about','admin'])+'<div class="mobile-bottom">'+a(f'/{l}/sitemap/','Sitemap')+'<details class="mobile-language"><summary>'+l.upper()+' ⌄</summary><div>'+langlinks()+'</div></details></div></nav>'
 return desk,mob

def footer(l):
 cols=[]
 for d in DIVS:
  it=H[d][l]['items'];ls=[]
  for x in it:
   u=x.get('url','').replace('{l}',l).replace('{rankers}',v3.rankers_url(l)).replace('{edu}',l if l in ['ko','en'] else 'en').replace('{games}',l if l in ['ko','en'] else 'en')
   if u:ls.append(a(u,x['name']))
  cols.append('<div><b>'+a(f'/{l}/{d}/',LABEL[d])+'</b>'+''.join(ls)+'</div>')
 cols.append('<div><b>AP Holdings</b>'+''.join(a(u,n) for u,n,k in links(l,None) if k in ['home','news','about','admin','sitemap'])+a(v3.brand_url(l),'CI · BI')+a(f'/{l}/ir/','IR')+a(f'/{l}/lab/',"Founder’s Lab")+'</div>')
 return '<div class="footer-map footer-map-v3 footer-map-v4">'+''.join(cols)+'</div>'

def company_tabs(l,rel):
 return '<nav class="company-tabs" aria-label="About AP Holdings">'+''.join(a(u,n,rel==u.strip('/')+'/index.html') for u,n in [(f'/{l}/about/','About'),(v3.brand_url(l),'CI · BI'),(f'/{l}/ir/','IR'),(f'/{l}/lab/',"Founder’s Lab")])+'</nav>'

def transform(rel,s):
 l=rel.split('/')[0] if rel.split('/')[0] in LOCS else 'ko';sec=section(rel)
 desk,mob=nav(l,sec)
 s=re.sub(r'<nav class="desktop-nav" aria-label="Main">.*?</nav>(?=<details class="language">)',lambda m:desk,s,count=1,flags=re.S)
 s=re.sub(r'(<details class="mobile-menu"><summary>[^<]*</summary>)<nav aria-label="Mobile">.*?</nav>',lambda m:m[1]+mob,s,count=1,flags=re.S)
 s=re.sub(r'<div class="footer-map[^"]*">.*?</div>(?=</div><ul class="footer-policies")',lambda m:footer(l),s,count=1,flags=re.S)
 s=re.sub(r'site.css\?v=[^"\s]+','site.css?v=2.21-ia4',s)
 s=re.sub(r'site.js\?v=[^"\s]+','site.js?v=20261009-ia4',s)
 s=s.replace(f'/{l}/media/',f'/{l}/entertainment/').replace(f'/{l}/products/rankers/',f'/{l}/rankers/')
 s=re.sub(r'<nav class="company-tabs".*?</nav>','',s,flags=re.S)
 if sec=='about':s=s.replace('<main id="main">','<main id="main">'+company_tabs(l,rel),1)
 return s

def redirect(l,target):
 u=f'/{l}/{target}/';return f'<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0;url={u}"><link rel="canonical" href="https://www.apholdings.kr{u}"><title>AP Holdings</title></head><body>{a(u,"Continue →")}</body></html>\n'

def write_page(l,path,title,desc,body):
 s=(ROOT/l/'lab/index.html').read_text();s=re.sub(r'<main id="main">.*?</main>',lambda m:'<main id="main">'+body+'</main>',s,flags=re.S)
 s=re.sub(r'<title>.*?</title>',lambda m:f'<title>{E(title)} — AP Holdings</title>',s,count=1)
 s=re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*',lambda m:m[1]+E(desc),s)
 s=s.replace('/lab/',f'/{path}/');s=re.sub(r'<script type="application/ld\+json">.*?</script>','',s,flags=re.S)
 p=ROOT/l/path/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(transform(f'{l}/{path}/index.html',s))

CSS='''
/* IA v4: six divisions, eleven desktop links, five mobile entries */
@media(min-width:1181px){.header-inner{max-width:1560px;width:96%;gap:18px}.header-inner .brand{margin-right:auto;flex-shrink:0}.header-inner .ap-ci-logo{width:175px;height:auto}.desktop-nav{display:flex;gap:clamp(10px,1.2vw,20px);font-size:12px;white-space:nowrap}.mobile-menu{display:none}}
@media(max-width:1180px){.desktop-nav{display:none!important}.header-inner>.language{display:none}.mobile-menu{display:block!important;margin-left:auto}.mobile-menu>nav{position:absolute;top:100%;left:0;right:0;background:var(--paper,#fff);padding:24px max(24px,5vw);max-height:calc(100dvh - 80px);overflow-y:auto;box-shadow:0 12px 24px #0001}.mobile-menu:not([open])>nav{display:none}.mobile-menu[open]>nav{display:flex;flex-direction:column;gap:8px}.mobile-menu nav>a,.mobile-business>summary,.mobile-language>summary{padding:12px 0;font-size:18px;cursor:pointer}.mobile-business>div,.mobile-language>div{display:grid;gap:10px;padding:12px 20px}.mobile-bottom{border-top:1px solid var(--line);margin-top:12px;padding-top:12px}.mobile-business a{padding:7px}.header-inner{position:relative}}
.footer-map-v4{grid-template-columns:repeat(4,minmax(0,1fr))}.division-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.division-card{padding:28px;border:1px solid var(--line);background:var(--paper);border-radius:16px;display:flex;flex-direction:column;text-decoration:none;color:inherit}.division-card:hover{border-color:var(--accent)}.division-card h3{font-size:26px;margin:18px 0 12px}.division-card p{color:var(--muted);line-height:1.7}.division-card .text-link{margin-top:auto}.company-tabs{max-width:1200px;margin:24px auto 0;padding:0 24px;display:flex;gap:24px;flex-wrap:wrap}.company-tabs a{padding:12px 0;text-decoration:none}.company-tabs [aria-current]{border-bottom:2px solid var(--accent)}.character-feature{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center;padding:48px 0}.character-feature img{width:100%;border-radius:22px}.character-feature h2{font-size:clamp(42px,7vw,84px)}.cubs-cast{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin:30px 0}.cubs-cast img{width:100%;height:220px;object-fit:contain}.cubs-cast article{border-radius:18px;background:var(--soft);padding:20px;text-align:center}.ia-sitemap{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}.ia-sitemap a{display:block;margin:10px 0}.hub-card .status{position:static;align-self:flex-start;margin-bottom:12px}.flow-v4{font-size:20px;line-height:1.9;max-width:900px}.ia-ent .hub-hero{padding-bottom:10px}
@media(max-width:800px){.division-cards,.ia-sitemap{grid-template-columns:repeat(2,minmax(0,1fr))}.character-feature{grid-template-columns:1fr;gap:24px}.cubs-cast{grid-template-columns:repeat(2,1fr)}.footer-map-v4{grid-template-columns:repeat(2,1fr)}}
@media(max-width:480px){.division-cards,.ia-sitemap{grid-template-columns:1fr}.division-card{padding:24px}.cubs-cast{gap:10px}.cubs-cast article{padding:12px}.cubs-cast img{height:160px}}
'''

def main():
 generated=[];redirects=[]
 for l in LOCS:
  c=COPY[l]
  for d in DIVS:
   rel=v3.make_hub(l,d);generated.append(rel)
   p=ROOT/rel;s=p.read_text()
   if d=='hallyu':s=s.replace('<h3>K-Craft</h3>','<h3 id="k-craft">K-Craft</h3>')
   p.write_text(s)
  # Editorial weighting: dominant LIA feature, compact four-cub section, no LEO.
  cast=''.join(f'<article><img src="https://hallyu.apholdings.kr/assets/art/{id}_3d.png" alt="{name}" width="628" height="840" loading="lazy"><h3>{name}</h3><p>{E(c[28+i])}</p></article>' for i,(id,name) in enumerate(zip(['daho','kkobi','aari','rami'],['다호','꼬비','아리','라미'] if l=='ko' else ['Daho','Kkobi','Aari','Rami'])))
  body=f'<section class="page-hero hub-hero"><div class="wrap"><span class="eyebrow">ENTERTAINMENT</span><h1>{E(c[14])}</h1><p class="lead">{E(c[15])}</p><div class="character-feature"><img src="/media/lia/lia_hero_sq.jpg" alt="LIA" width="800" height="800"><div><span class="eyebrow">AI CHARACTER</span><h2>LIA</h2><p class="lead">{E(c[17])}</p><p>{E(c[18])}</p><div class="actions">{a(f"/{l}/products/lia/",c[23])}{a("https://ent.apholdings.kr/","Entertainment ↗")}{a("https://shop.apholdings.kr/","Lia Select Shop ↗")}</div></div></div></div></section><section class="section soft"><div class="wrap"><span class="eyebrow">HANGEUL CUBS</span><h2>{E(c[19])}</h2><p>{E(c[20])}</p><div class="cubs-cast">{cast}</div><div class="actions">{a(f"/{l}/hallyu/","Hallyu →")}{a("https://www.youtube.com/@APHoldings",c[27])}</div></div></section>'
  write_page(l,'entertainment','Entertainment',c[15],body)
  # Replace only old home business blocks; preserve why/global/about and existing hero.
  p=ROOT/l/'index.html';s=p.read_text()
  cards=''.join(f'<a class="division-card" href="/{l}/{d}/" id="{d}"><span class="number">0{i+1}</span><h3>{LABEL[d]}</h3><p>{E(H[d][l]["lead"])}</p><span class="text-link">{E(c[23])} →</span></a>' for i,d in enumerate(DIVS))
  block=f'<section class="home-portfolio section soft" id="businesses"><div class="wrap" id="portfolio"><div class="section-head"><span class="eyebrow">OUR BUSINESSES</span><h2>{E(c[22])}</h2></div><div class="division-cards">{cards}</div></div></section>'
  start=s.find('<section class="section" id="businesses"');end=s.find('<section class="home-why')
  if start<0:start=s.find('<section class="home-portfolio')
  if start>=0 and end>start:s=s[:start]+block+s[end:]
  p.write_text(s)
  # Company tabs and sitemap; preserve News body and subscription implementation.
  sections=''
  for d in DIVS:
   sections+=f'<section><h2>{LABEL[d]}</h2>{a(f"/{l}/{d}/",LABEL[d]+" →")}'
   for x in H[d][l]['items']:
    u=x.get('url','').replace('{l}',l).replace('{rankers}',v3.rankers_url(l)).replace('{edu}',l if l in ['ko','en'] else 'en').replace('{games}',l if l in ['ko','en'] else 'en')
    sections+=a(u,x['name']) if u else f'<p>{E(x["name"])} · {E(x.get("status",c[5]))}</p>'
   sections+='</section>'
  sections+='<section><h2>AP Holdings</h2>'+''.join(a(u,n) for u,n,k in links(l,None) if k in ['home','news','about','admin'])+a(v3.brand_url(l),'CI · BI')+a(f'/{l}/ir/','IR')+a(f'/{l}/lab/',"Founder’s Lab")+'</section>'
  write_page(l,'sitemap',c[25],c[26],f'<section class="page-hero"><div class="wrap"><h1>{E(c[25])}</h1><p class="lead">{E(c[26])}</p></div></section><section class="section"><div class="wrap ia-sitemap">{sections}</div></section>');generated.append(f'{l}/sitemap/index.html')
  for src,target in [('media','entertainment'),('products/rankers','rankers'),('products/revenue','intelligence'),('products/travel','intelligence')]:
   # Use existing English Rankers content for the four previously missing locale routes, marked AI-localized by site convention.
   if target=='rankers' and not (ROOT/l/'rankers/index.html').exists():
    items=H['games'][l]['items'];write_page(l,'rankers','RANKERS',H['games'][l]['lead'],v3.hub_main(l,'games').replace('<main id="main">','').replace('</main>',''));generated.append(f'{l}/rankers/index.html')
   p=ROOT/l/src/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(redirect(l,target));redirects.append(str(p.relative_to(ROOT)))
 for l in LOCS:
  for page in ['ir','about']:
   p=ROOT/l/page/'index.html';s=p.read_text()
   for old,new in [('Media','Entertainment · News'),('Edu and Games','Hallyu, Edu and Games'),('Edu와 Games','Hallyu · Edu · Games'),('Edu et Games','Hallyu, Edu et Games'),('Edu và Games','Hallyu, Edu và Games'),('EduとGames','Hallyu・Edu・Games'),('Edu 和 Games','Hallyu、Edu 和 Games'),('five businesses','six businesses'),('5부문','6부문'),('다섯 사업','여섯 사업'),('5部門','6部門'),('五个业务','六个业务'),('cinq activités','six activités'),('năm lĩnh vực','sáu lĩnh vực'),('Shop은 직접 판매 · 수수료 · 가맹.','Shop은 직접 판매 · 수수료. Intelligence는 가맹 시스템도 맡습니다.'),('Shop: direct sales, commissions and franchising.','Shop: direct sales and commissions. Intelligence also supports franchising.'),('Shop: bán hàng trực tiếp, hoa hồng và nhượng quyền.','Shop: bán hàng trực tiếp và hoa hồng. Intelligence hỗ trợ hệ thống nhượng quyền.'),('직접 판매 · 수수료 · 가맹','직접 판매 · 수수료')]:
    if new not in s:s=s.replace(old,new)
   p.write_text(s)
 for p in ROOT.rglob('*.html'):
  rel=str(p.relative_to(ROOT))
  if rel.startswith(('admin/','.git/','_backup','docs/')):continue
  s=p.read_text().replace('edu.apholdings.kr','hallyu.apholdings.kr')
  if '<header class="site-header">' in s:p.write_text(transform(rel,s))
 css=ROOT/'assets/v2/site.css';s=css.read_text().split('\n/* IA v4:')[0];css.write_text(s+CSS)
 gf=ROOT/'site-source/generated-files.json';g=json.loads(gf.read_text());g=[x for x in g if x not in redirects];g=list(dict.fromkeys(g+generated));gf.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n')
 sm=ROOT/'sitemap.xml';s=sm.read_text();s=re.sub(r'<url><loc>[^<]+/(?:media|products/rankers|products/revenue|products/travel)/</loc>.*?</url>','',s)
 for l in ['ko','en']:
  for d in DIVS+['sitemap']:
   u=f'https://www.apholdings.kr/{l}/{d}/'
   if u not in s:s=s.replace('</urlset>',f'<url><loc>{u}</loc><lastmod>2026-10-09</lastmod></url></urlset>')
 sm.write_text(s)
 print('IA v4: six locales, six divisions; News preserved.')
if __name__=='__main__':main()
