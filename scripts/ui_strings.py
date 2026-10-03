"""vi/ja/zh-cn/fr: build_site.py 가 영어로 직접 박아 둔 짧은 UI 문구의 번역(전 어권 원칙). 영어 원문 → 어권별 문구."""
import re
S={
'Admin':('Quản trị','管理','管理','Admin'),
'Connectors':('Trình kết nối','コネクタ','连接器','Connecteurs'),
'Safelist · Claude':('Safelist · Claude','Safelist · Claude','Safelist · Claude','Safelist · Claude'),
'App privacy policies':('Chính sách quyền riêng tư của ứng dụng','アプリのプライバシーポリシー','应用隐私政策','Politiques de confidentialité des applications'),
'Play film':('Phát video','動画を再生','播放视频','Lire la vidéo'),
'Pause film':('Tạm dừng video','動画を停止','暂停视频','Mettre la vidéo en pause'),
'AP Games official site — LAST WAVE':('Trang chính thức AP Games — LAST WAVE','AP Games公式サイト — LAST WAVE','AP Games 官方网站 — LAST WAVE','Site officiel AP Games — LAST WAVE'),
'Live Quiz Battle':('Đấu trí trực tiếp','ライブクイズバトル','实时问答对战','Quiz en direct'),
'LIVE QUIZ BATTLE PLATFORM':('NỀN TẢNG ĐẤU TRÍ TRỰC TIẾP','ライブクイズバトル・プラットフォーム','实时问答对战平台','PLATEFORME DE QUIZ EN DIRECT'),
'Anyone':('Mọi người','だれでも','人人','Tout le monde'),
'all ages, one stage':('mọi lứa tuổi, một sân khấu','老若男女、ひとつのステージ','男女老少，同台竞技','tous âges, une seule scène'),
'Play':('Chơi','遊び','玩','Jeu'),
'a game, not study':('là trò chơi, không phải học bài','勉強ではなくゲーム','是游戏，不是学习','un jeu, pas une leçon'),
'Knowledge':('Kiến thức','知識','常识','Culture générale'),
'grows as you play':('lớn dần khi bạn chơi','遊ぶうちに自然と身につく','边玩边增长','grandit en jouant'),
'AP Holdings YouTube channel':('Kênh YouTube AP Holdings','AP Holdings YouTubeチャンネル','AP Holdings YouTube 频道','Chaîne YouTube AP Holdings'),
'Company profile PDF · Korean · Sept 2026':('Hồ sơ công ty (PDF) · tiếng Hàn · 09/2026','会社概要PDF · 韓国語 · 2026年9月','公司简介 PDF · 韩文 · 2026年9月','Présentation de l’entreprise (PDF) · en coréen · sept. 2026'),
'Ideas we build, test and learn from.':('Những ý tưởng chúng tôi xây dựng, thử nghiệm và học hỏi.','私たちが作り、試し、学ぶアイデア。','我们构建、测试并从中学习的想法。','Des idées que nous construisons, testons et dont nous tirons des enseignements.'),
'Build → Release → Learn.':('Xây dựng → Phát hành → Học hỏi.','つくる → 公開する → 学ぶ。','构建 → 发布 → 学习。','Construire → Publier → Apprendre.'),
'Claude connector · running':('Trình kết nối Claude · đang chạy','Claudeコネクタ · 稼働中','Claude 连接器 · 运行中','Connecteur Claude · en service'),
'Claude connector · maintenance':('Trình kết nối Claude · đang bảo trì','Claudeコネクタ · メンテナンス中','Claude 连接器 · 维护中','Connecteur Claude · en maintenance'),
'Siri · from 1.5':('Siri · từ bản 1.5','Siri · 1.5以降','Siri · 自 1.5 版起','Siri · à partir de la 1.5'),
'ChatGPT · listing in preparation':('ChatGPT · đang chuẩn bị đăng ký','ChatGPT · 掲載準備中','ChatGPT · 上架准备中','ChatGPT · référencement en préparation'),
'ChatGPT · Gemini · later':('ChatGPT · Gemini · sau này','ChatGPT · Gemini · 今後','ChatGPT · Gemini · 后续','ChatGPT · Gemini · plus tard'),
'Android · later':('Android · sau này','Android · 今後','Android · 后续','Android · plus tard'),
}
IDX={'vi':0,'ja':1,'zh-cn':2,'fr':3}
def localize(l,text):
    i=IDX[l]
    for en,tr in S.items():
        for form in (en,en.replace('’','&#x27;'),en.replace('&','&amp;')):
            text=text.replace('>'+form+'<','>'+tr[i]+'<').replace('"'+form+'"','"'+tr[i]+'"')
    pref={'Status · checked ':('Trạng thái · kiểm tra ','状況 · 確認日 ','状态 · 核查于 ','Statut · vérifié le '),
          'iOS app ':('Ứng dụng iOS ','iOSアプリ ','iOS 应用 ','Appli iOS ')}
    text=re.sub(r'>Status · checked ([^<]*)<',lambda m:'>'+pref['Status · checked '][i]+m.group(1)+'<',text)
    live={'vi':'đã ra mắt','ja':'公開中','zh-cn':'已上线','fr':'disponible'}[l]
    text=re.sub(r'>iOS app ([\d.]+) · live<',lambda m:'>'+pref['iOS app '][i]+m.group(1)+' · '+live+'<',text)
    unit={'products':('sản phẩm','製品','款产品','produits'),'foods':('thực phẩm','食品','种食品','aliments')}
    def cnt(m):
        n,u=m.group(1),m.group(2)
        return '>'+(f'{n} {unit[u][i]}' if l in('vi','fr') else f'{n}{unit[u][i]}' if l!='fr' else '')+'<'
    text=re.sub(r'>(\d[\d.,]*[KM]?) (products|foods)<',cnt,text)
    return text
