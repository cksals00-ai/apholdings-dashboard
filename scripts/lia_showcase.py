"""LIA's interactive portfolio; retain locale content and existing destinations."""
from html import escape as e

HANGEUL_APP_STORE_URL = 'https://apps.apple.com/app/apple-store/id6803749436?pt=129327962&ct=lia_bio_hc&mt=8'

COPY = {
 'ko': ['안녕하세요,<br>리아예요.', '한국의 이야기, 새로운 발견.<br>리아와 함께 만나보세요.', '커서를 움직여 보세요. 모바일에서는 리아를 눌러 보세요.', '리아에게 인사하기', '콘텐츠 보기', '브랜드 협업', 'AI 생성 캐릭터 · LIA', '리아의 콘텐츠', '선케어', '마스크', '립 틴트', '반응 켜기', '반응 끄기'],
 'en': ['Hi, I’m<br>LIA.', 'Stories from Korea. Something new to discover.<br>Come explore with LIA.', 'Move your cursor. On mobile, tap LIA to say hello.', 'Say hello to LIA', 'Watch content', 'Brand collaboration', 'AI-generated character · LIA', 'LIA’s content', 'Sun care', 'Mask', 'Lip tint', 'Enable reactions', 'Pause reactions'],
 'ja': ['こんにちは、<br>リアです。', '韓国の物語と、新しい発見。<br>リアと一緒に楽しみましょう。', 'カーソルを動かしてみてください。スマートフォンではリアをタップ。', 'リアに挨拶する', 'コンテンツを見る', 'ブランドとの協業', 'AI生成キャラクター · LIA', 'リアのコンテンツ', 'サンケア', 'マスク', 'リップティント', '反応を有効にする', '反応を止める'],
 'zh-cn': ['你好，<br>我是莉娅。', '韩国故事，新的发现。<br>和莉娅一起探索。', '移动鼠标试试看。在手机上，点击莉娅打个招呼。', '向莉娅打招呼', '观看内容', '品牌合作', 'AI生成角色 · LIA', '莉娅的内容', '防晒', '面膜', '唇彩', '开启互动', '暂停互动'],
 'vi': ['Xin chào,<br>mình là LIA.', 'Câu chuyện Hàn Quốc và những khám phá mới.<br>Cùng LIA khám phá nhé.', 'Di chuyển con trỏ. Trên điện thoại, chạm LIA để chào.', 'Chào LIA', 'Xem nội dung', 'Hợp tác thương hiệu', 'Nhân vật do AI tạo · LIA', 'Nội dung của LIA', 'Chống nắng', 'Mặt nạ', 'Son tint', 'Bật phản ứng', 'Tạm dừng phản ứng'],
 'fr': ['Bonjour,<br>c’est LIA.', 'Des histoires de Corée, de nouvelles découvertes.<br>Explorez avec LIA.', 'Déplacez le curseur. Sur mobile, touchez LIA pour la saluer.', 'Saluer LIA', 'Voir les contenus', 'Collaboration de marque', 'Personnage généré par IA · LIA', 'Les contenus de LIA', 'Soin solaire', 'Masque', 'Teinte à lèvres', 'Activer les réactions', 'Suspendre les réactions'],
}



def trip_install_links(locale):
 ko = locale == 'ko'
 title = '리아의 한국 여행 키트' if ko else 'Lia’s Korea trip kit'
 intro = '배우기 · 퀴즈 대결 · 공연 당일 준비. 세 개의 별도 앱입니다.' if ko else 'Learn Korean. Play a quiz. Plan your show day. Three separate apps.'
 apps = [('Hangeul Cubs','6803749436','hc','무료 71레슨 · 받침팩 별도 구매' if ko else '71 free lessons · optional paid Batchim pack'),('K-Ranker','6819796522','kr','무료 · 영어 퀴즈 · 상대가 있어야 실시간 대결 가능' if ko else 'Free English trivia · live duels need another player'),('K-Concert Trip','6803810106','kct','유료 · 공연장·체크리스트 · 티켓·아티스트 일정 제공 안 함' if ko else 'Paid app · venue guide and checklist · no ticket sales or artist schedules')]
 cards=[]
 for name,aid,ct,note in apps:
  url=f'https://apps.apple.com/app/apple-store/id{aid}?pt=129327962&ct=lia_bio_{ct}&mt=8'
  cards.append(f'<article class="card"><h3>{e(name)}</h3><p>{e(note)}</p><div class="actions"><a class="button primary" href="{e(url,quote=True)}" target="_blank" rel="noopener noreferrer">App Store</a></div></article>')
 return '<section class="section anchor" id="korea-trip-kit"><div class="wrap"><div class="section-head"><span class="eyebrow">LIA / KOREA TRIP KIT</span><h2>'+title+'</h2><p>'+intro+'</p></div><div class="grid-3">'+''.join(cards)+'</div></div></section>'

def app_install_links(locale):
 ko = locale == 'ko'
 apps = [
  ('Hangeul Cubs', '6803749436', '무료 71레슨 · 받침팩 별도 구매' if ko else '71 free lessons · optional paid Batchim pack'),
  ('IRON GRADE', '6808070870', '유료 운동 기록 앱' if ko else 'Paid workout record app'),
  ('나의 첫투자 / First Invest', '6803763681', '유료 · 한국어 · 모의투자' if ko else 'Paid · Korean UI · simulated investing'),
  ('Dawn Grace', '6803325336', '무료 · 아침 묵상' if ko else 'Free · morning reflection'),
  ('세이프리스트 / Safelist', '6805684034', '무료 · 선택 유료 기능 · 진단·안전 판정 아님' if ko else 'Free · optional purchases · no diagnosis or safety guarantee'),
  ('퀴즈랭커 / QuizRanker', '6810908071', '무료 · 앱 내 구매 · 한국어 게임 화면' if ko else 'Free · in-app purchases · Korean game screens'),
  ('아빠랑 나랑 / Dad & Me', '6821352092', '무료 약속 도장판 · Family Pass 별도 구매' if ko else 'Free promise board · optional Family Pass'),
 ]
 cards = []
 for name, app_id, note in apps:
  apple = HANGEUL_APP_STORE_URL if app_id == '6803749436' else f'https://apps.apple.com/{"kr/" if app_id in ("6805684034", "6821352092") else ""}app/id{app_id}'
  if app_id in ('6805684034', '6821352092'):
   note += ' · 한국 App Store' if ko else ' · Korean App Store; regional availability applies'
  buttons = f'<a class="button primary" href="{e(apple,quote=True)}" target="_blank" rel="noopener noreferrer">App Store ↗</a>'
  if app_id == '6803749436':
   buttons += '<a class="button" href="https://play.google.com/store/apps/details?id=com.aplocalift.hangeulcubs" target="_blank" rel="noopener noreferrer">Google Play ↗</a>'
  cards.append(f'<article class="card"><h3>{e(name)}</h3><p>{e(note)}</p><div class="actions">{buttons}</div></article>')
 title = '영상에서 본 앱, 여기서 설치하세요.' if ko else 'Get the apps you saw in our videos.'
 note = 'AP Holdings 자사 앱 · 가격과 이용 조건은 스토어에서 확인하세요.' if ko else 'Apps by AP Holdings. Check pricing and availability in your store.'
 return '<section class="section anchor" id="apps"><div class="wrap"><div class="section-head"><span class="eyebrow">AP APPS</span><h2>'+title+'</h2><p>'+note+'</p></div><div class="grid-3">'+''.join(cards)+'</div></div></section>'

def render(locale, product, sections, mail):
 t=COPY[locale]
 external='target="_blank" rel="noopener noreferrer"'
 app_pitch = '무료 71레슨으로 한국어 읽기를 시작하세요. 18개 레슨의 받침 마스터 팩은 별도 구매입니다.' if locale == 'ko' else '71 free lessons to start reading Korean. Optional 18-lesson Batchim Master Pack sold separately.'
 app_cta = '한글컵스 · App Store' if locale == 'ko' else 'Hangeul Cubs · App Store'
 return f'''<link rel="stylesheet" href="/assets/v2/lia-interactive.css?v=3"><script defer src="/assets/v2/lia-interactive.js?v=1"></script>
 <section class="lia-hero" data-lia-hero><div class="wrap lia-hero-grid">
 <div class="lia-intro"><span class="eyebrow">AP ENTERTAINMENT / LIA</span><h1>{t[0]}</h1><p class="lia-lead">{t[1]}</p>
 <p class="lia-lead"><strong>Hangeul Cubs</strong> · {e(app_pitch)}</p>
 <div class="lia-actions"><a class="button primary" href="{e(HANGEUL_APP_STORE_URL,quote=True)}" {external}>{e(app_cta)} ↗</a><a class="button" href="#korea-trip-kit">{("한국 여행 키트 앱 3종" if locale == "ko" else "Korea trip kit · 3 apps")} ↘</a><a class="button" href="#apps">{("영상 속 앱 설치" if locale == "ko" else "Get the apps")} ↘</a><a class="button" href="#lia-content" data-lia-greet>{e(t[4])} ↘</a><a class="button" href="{e(mail('LIA collaboration'),quote=True)}" data-lia-greet>{e(t[5])} ↗</a></div>
 <div class="lia-social"><a href="https://www.instagram.com/lia_park55/" {external} data-lia-greet>Instagram ↗</a><a href="https://www.tiktok.com/@lia_park55" {external} data-lia-greet>TikTok ↗</a><a href="https://www.youtube.com/@APHoldings" {external} data-lia-greet>YouTube / AP Holdings ↗</a></div><p class="lia-disclosure">{e(t[6])}</p></div>
 <div class="lia-portrait"><button type="button" class="lia-stage" data-lia-stage data-pose="neutral" aria-label="{e(t[3],quote=True)}" aria-pressed="false"><span class="lia-sprite" aria-hidden="true"><img src="/media/lia/lia-interactive-atlas-v3.png" width="1536" height="1024" alt="" fetchpriority="high"></span><span class="lia-stage-label">LIA <span>●</span></span></button>
 <div class="lia-controls"><p>{e(t[2])}</p><button type="button" data-lia-toggle aria-pressed="true" data-on="{e(t[12],quote=True)}" data-off="{e(t[11],quote=True)}">{e(t[12])}</button></div></div>
 </div></section>
 {trip_install_links(locale)}
 {app_install_links(locale)}
 <section class="section lia-content anchor" id="lia-content"><div class="wrap"><div class="section-head"><span class="eyebrow">WATCH / LIA</span><h2>{e(t[7])}</h2></div><div class="lia-video-grid">''' + ''.join(f'<figure><video controls playsinline preload="none" poster="/media/lia/review_ep{i}_{slug}_poster.jpg" src="/media/lia/review_ep{i}_{slug}.mp4" aria-label="LIA · {e(label,quote=True)}"></video><figcaption><span>0{i}</span> {e(label)}</figcaption></figure>' for i,slug,label in [(1,'suncream',t[8]),(2,'mask',t[9]),(3,'tint',t[10])]) + '</div></div></section>' + sections(product.get('sections',[]))

