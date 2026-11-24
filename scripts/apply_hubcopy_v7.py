#!/usr/bin/env python3
"""HUBCOPY v7 (2026-10-09): 허브 6개 첫 화면 제목·설명을 추상 문구에서 구체 문구로 교체. 재실행해도 같음.
주의: 원본 원고 site-source/divisions.json은 그대로다(클레어 검수 필요)."""
import re, html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; E=lambda s:html.escape(str(s),quote=True)
LOCS=['ko','en','vi','ja','zh-cn','fr']
import json as _json
D=_json.loads((ROOT/'site-source/divisions.json').read_text())
FOR={l:D['_common'][l]['for'] for l in LOCS}
HUB={
'ko':{'intelligence':('성분표를 읽는 앱과 매장.','AP Safe · AP Light 앱, AI 커넥터, 그리고 상담·체험 매장.'),'games':('게임은 달라도 티어는 하나.','AP Games · RANKERS · LAST WAVE.'),'edu':('놀면서 배우는 한국, 교실의 실시간 퀴즈.','K-Ranker · Hangeul Cubs · 한글 학습 사이트 · 퀴즈랭커 · 학교·학원 퀴즈팩 · 아빠와 아이 프로젝트.'),'entertainment':('리아와 호랑이 네 남매.','AI 배우 리아와 Hangeul Cubs 캐릭터.'),'shop':('한국 상품을 해외로.','Lia Select Shop · LIA Select · Global K-Commerce · K-Craft.')},
'en':{'intelligence':('An app and stores that read labels.','AP Safe · AP Light apps, the AI connector, and stores for consultation.'),'games':('Different games, one tier.','AP Games · RANKERS · LAST WAVE.'),'edu':('Learn Korea by playing, live quizzes for class.','K-Ranker · Hangeul Cubs · learning site · QuizRanker · school packs · the Dad & Child project.'),'entertainment':('Lia and four tiger cubs.','Lia, the AI actor, and the Hangeul Cubs characters.'),'shop':('Korean products, shipped abroad.','Lia Select Shop · LIA Select · Global K-Commerce · K-Craft.')},
'vi':{'intelligence':('Ứng dụng và cửa hàng đọc nhãn.','Ứng dụng AP Safe · AP Light, đầu nối AI, cửa hàng tư vấn.'),'games':('Game khác nhau, một hệ thống hạng.','AP Games · RANKERS · LAST WAVE.'),'edu':('Học Hàn Quốc qua trò chơi, quiz trực tiếp cho lớp.','K-Ranker · Hangeul Cubs · trang học · QuizRanker · gói quiz cho trường · dự án Bố và Bé.'),'entertainment':('Lia và bốn chú hổ con.','Diễn viên AI Lia và các nhân vật Hangeul Cubs.'),'shop':('Hàng Hàn Quốc ra nước ngoài.','Lia Select Shop · LIA Select · Global K-Commerce · K-Craft.')},
'ja':{'intelligence':('ラベルを読むアプリと店舗。','AP Safe・AP Light アプリ、AIコネクタ、相談できる店舗。'),'games':('ゲームは違っても、ティアは一つ。','AP Games・RANKERS・LAST WAVE。'),'edu':('遊びながら学ぶ韓国、教室のリアルタイムクイズ。','K-Ranker・Hangeul Cubs・学習サイト・QuizRanker・学校用クイズパック・父と子のプロジェクト。'),'entertainment':('リアと4匹のトラの子。','AI俳優リアと Hangeul Cubs のキャラクター。'),'shop':('韓国の商品を海外へ。','Lia Select Shop・LIA Select・Global K-Commerce・K-Craft。')},
'zh-cn':{'intelligence':('会读标签的应用与门店。','AP Safe、AP Light 应用、AI 连接器，以及可咨询的门店。'),'games':('游戏不同，段位统一。','AP Games、RANKERS、LAST WAVE。'),'edu':('边玩边学韩国，课堂实时答题。','K-Ranker、Hangeul Cubs、学习网站、QuizRanker、校园题包、父子项目。'),'entertainment':('Lia 与四只小老虎。','AI 演员 Lia 与 Hangeul Cubs 角色。'),'shop':('把韩国商品送到海外。','Lia Select Shop、LIA Select、Global K-Commerce、K-Craft。')},
'fr':{'intelligence':('Une app et des boutiques qui lisent les étiquettes.','Apps AP Safe · AP Light, connecteur IA, boutiques de conseil.'),'games':('Des jeux différents, un seul rang.','AP Games · RANKERS · LAST WAVE.'),'edu':('Apprendre la Corée en jouant, des quiz en direct en classe.','K-Ranker · Hangeul Cubs · site d’apprentissage · QuizRanker · packs scolaires · projet Père et enfant.'),'entertainment':('Lia et quatre tigreaux.','Lia, l’acteur IA, et les personnages Hangeul Cubs.'),'shop':('Des produits coréens à l’étranger.','Lia Select Shop · LIA Select · Global K-Commerce · K-Craft.')},
}

EYE={
'ko':{'intelligence':'INTELLIGENCE · 성분 확인과 매장','games':'GAMES · 하나의 티어','edu':'EDU · 세계와 교실','entertainment':'ENTERTAINMENT · 캐릭터','shop':'SHOP · 해외 판매'},
'en':{'intelligence':'INTELLIGENCE · Ingredient checks and stores','games':'GAMES · One tier','edu':'EDU · The world and the classroom','entertainment':'ENTERTAINMENT · Characters','shop':'SHOP · Global selling'},
'vi':{'intelligence':'INTELLIGENCE · Kiểm tra thành phần và cửa hàng','games':'GAMES · Một hệ thống hạng','edu':'EDU · Thế giới và lớp học','entertainment':'ENTERTAINMENT · Nhân vật','shop':'SHOP · Bán ra quốc tế'},
'ja':{'intelligence':'INTELLIGENCE · 成分確認と店舗','games':'GAMES · ひとつのティア','edu':'EDU · 世界と教室','entertainment':'ENTERTAINMENT · キャラクター','shop':'SHOP · 海外販売'},
'zh-cn':{'intelligence':'INTELLIGENCE · 成分查询与门店','games':'GAMES · 统一段位','edu':'EDU · 世界与课堂','entertainment':'ENTERTAINMENT · 角色','shop':'SHOP · 海外销售'},
'fr':{'intelligence':'INTELLIGENCE · Vérification et boutiques','games':'GAMES · Un seul rang','edu':'EDU · Le monde et la classe','entertainment':'ENTERTAINMENT · Personnages','shop':'SHOP · Vente à l’étranger'}}
WHO={
'ko':{'intelligence':'앱 사용자 · 파트너 · 가맹 매장','games':'개인 플레이어','edu':'한국을 배우는 외국인 · 학교·학원 선생님 · 부모','entertainment':'AP를 처음 만난 사람 · 팬','shop':'한국 상품을 찾는 해외 고객'},
'en':{'intelligence':'App users · partners · franchise stores','games':'Individual players','edu':'Foreign learners · teachers · parents','entertainment':'First-time visitors · fans','shop':'Overseas customers'},
'vi':{'intelligence':'Người dùng ứng dụng · đối tác · cửa hàng nhượng quyền','games':'Người chơi cá nhân','edu':'Người nước ngoài học tiếng Hàn · giáo viên · phụ huynh','entertainment':'Người mới biết AP · người hâm mộ','shop':'Khách hàng nước ngoài'},
'ja':{'intelligence':'アプリ利用者・パートナー・加盟店','games':'個人プレイヤー','edu':'韓国語を学ぶ外国人・学校・塾の先生・保護者','entertainment':'APを初めて知る人・ファン','shop':'韓国商品を探す海外のお客様'},
'zh-cn':{'intelligence':'应用用户 · 合作伙伴 · 加盟门店','games':'个人玩家','edu':'学习韩语的外国人 · 学校·机构老师 · 家长','entertainment':'初次认识 AP 的人 · 粉丝','shop':'寻找韩国商品的海外客户'},
'fr':{'intelligence':'Utilisateurs · partenaires · boutiques franchisées','games':'Joueurs individuels','edu':'Apprenants étrangers · enseignants · parents','entertainment':'Premiers visiteurs · fans','shop':'Clients à l’étranger'}}

def fix(l,s):
    s=s.replace('<section class="page-hero hub-hero">','<section class="page-hero hub-hero" data-div="Entertainment">',1)
    def rep(m):
        sec=m.group(0); d=m.group(1).lower(); t=HUB[l][d]
        sec=re.sub(r'<h1>.*?</h1>',f'<h1>{E(t[0])}</h1>',sec,count=1,flags=re.S)
        sec=re.sub(r'<p class="lead">.*?</p>',f'<p class="lead">{E(t[1])}</p>',sec,count=1,flags=re.S)
        sec=re.sub(r'<span class="eyebrow">.*?</span>',f'<span class="eyebrow">{E(EYE[l][d])}</span>',sec,count=1,flags=re.S)
        sec=re.sub(r'<p class="hub-who">.*?</p>',f'<p class="hub-who"><b>{E(FOR[l])}</b> {E(WHO[l][d])}</p>',sec,count=1,flags=re.S)
        return sec
    return re.sub(r'<section class="page-hero hub-hero" data-div="([A-Za-z]+)">.*?</section>',rep,s,flags=re.S)
def main():
    n=0
    for l in LOCS:
        for d in HUB[l]:
            f=ROOT/l/d/'index.html'
            if f.exists():
                s=f.read_text(); t=fix(l,s)
                if t!=s: f.write_text(t); n+=1
    print({'hub_copy':n})
if __name__=='__main__': main()
