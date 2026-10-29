"""Register FoldBlock without changing existing game routes or release status."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
def apply():
 for lang in ('ko','en'):
  ko=lang=='ko'
  route=f'/{lang}/products/foldblock/'
  hub=ROOT/f'{lang}/games/index.html'
  template=hub.read_text()
  name='폴드블록' if ko else 'FoldBlock'
  title='접으면 가볍게. 펼치면 더 크게.' if ko else 'A little break. A bigger board.'
  desc='조각 세 개를 놓고, 줄을 완성하세요. 시간 제한 없이 나만의 리듬으로 즐기는 8×8 블록퍼즐.' if ko else 'Place three pieces and complete rows and columns. An 8×8 block puzzle at your own pace, with no timer.'
  labels=['무료','광고 없음','계정 없음','오프라인'] if ko else ['Free','No ads','No account','Offline']
  features=[('한 줄을 채우는 즐거움','가로·세로를 완성하면 블록이 사라집니다. 콤보를 이어가고 판을 모두 비워 보세요.'),('매일 새로운 도전','날짜마다 정해진 조각 순서로 오늘의 도전에 참여하세요. 출석과 일일 임무로 크레딧을 모을 수 있어요.'),('함께 자라는 파트너','토끼부터 사자까지 여덟 파트너의 능력을 만나세요. 플레이하며 숙련도를 쌓고 새 파트너를 영입하세요.'),('화면에 맞춰 이어지는 플레이','작은 화면에서는 간결하게, 넓은 화면에서는 판과 정보를 함께 봅니다. 화면 크기를 바꿔도 진행 중인 판은 이어집니다.')] if ko else [('Make room for one more move','Complete a row or column to clear blocks. Keep a combo going and aim for an all-clear.'),('A fresh challenge each day','Try a daily seeded piece sequence. Earn local credits through attendance and daily missions.'),('Eight partners to grow with','Meet eight animal partners with different abilities. Play to build mastery and recruit more partners.'),('A board that fits your screen','Compact on small screens; more room for your board and information on larger screens. Resizing keeps your current game intact.')]
  shots=['첫 화면과 오늘의 도전','블록을 놓고 줄 완성하기','파트너와 함께 플레이'] if ko else ['Home and daily challenge','Place blocks and complete lines','Play with a partner']
  status='<div class="release" id="install"><h2>'+('출시 소식' if ko else 'Release status')+'</h2><p><strong>App Store</strong> · '+('심사 대기 중' if ko else 'Waiting for review')+'</p><p><strong>Google Play</strong> · '+('출시 준비 중' if ko else 'Preparing for release')+'</p><p class="muted">'+('스토어에서 실제 공개되면 이곳에 설치 링크가 열립니다.' if ko else 'Install links will appear here after the app becomes publicly available.')+'</p></div>'
  body='<main id="main"><section class="fb-hero"><div><a href="/'+lang+'/games/">← AP Games</a><p class="eyebrow">AP GAMES · FOLDBLOCK</p><h1>'+name+'</h1><h2>'+title+'</h2><p class="lead">'+desc+'</p><div class="badges">'+''.join('<span>'+x+'</span>' for x in labels)+'</div><a class="button primary" href="#install">'+('출시 현황 보기' if ko else 'Release status')+'</a></div><img class="feature" src="/media/games/foldblock/feature.png" width="1024" height="500" alt="'+name+' · 8×8 블록퍼즐"></section><section class="fb-features">'+''.join('<article><span class="eyebrow">0'+str(i+1)+'</span><h2>'+a+'</h2><p>'+b+'</p></article>' for i,(a,b) in enumerate(features))+'</section><section class="fb-screens"><h2>'+('미리 만나보세요' if ko else 'Take a closer look')+'</h2><div class="screens">'+''.join('<figure><img loading="lazy" src="/media/games/foldblock/screen-'+str(i+1)+'.png" width="1206" height="2622" alt="'+s+'"><figcaption>'+s+'</figcaption></figure>' for i,s in enumerate(shots))+'</div></section>'+status+'<section class="fb-notes"><h2>'+('시작하기 전에' if ko else 'Before you play')+'</h2><p>'+('진행 기록과 크레딧은 이 기기에 저장됩니다. 앱을 삭제하면 기록이 지워질 수 있으며, 기기 간 동기화·온라인 순위표는 제공하지 않습니다. 크레딧은 플레이로 얻는 게임 내 재화이며 현금 결제 상품이 아닙니다.' if ko else 'Progress and credits are stored on your device. Uninstalling may erase them. Cloud sync and online leaderboards are not provided. Credits are earned through play, with no real-money purchases.')+'</p><a href="/foldblock_privacy.html">'+('개인정보처리방침' if ko else 'Privacy policy')+'</a></section></main>'
  css='<style>.fb-hero,.fb-features,.fb-screens,.release,.fb-notes{max-width:1120px;margin:0 auto;padding:64px 24px}.fb-hero{display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:36px}.fb-hero h1{font-size:clamp(44px,7vw,80px);margin:16px 0}.fb-hero h2{font-size:clamp(24px,3vw,36px)}.feature{width:100%;border-radius:24px}.badges{display:flex;gap:8px;flex-wrap:wrap;margin:24px 0}.badges span{border:1px solid #ccd6d0;border-radius:99px;padding:6px 12px}.fb-features{display:grid;grid-template-columns:1fr 1fr;gap:36px;border-top:1px solid #d9dfda}.fb-features p,.fb-notes p{line-height:1.8}.screens{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}.screens figure{margin:0}.screens img{width:100%;height:auto;border-radius:24px}.screens figcaption{padding-top:12px}.release{background:#edf4ed;border-radius:24px;margin:24px auto}.muted{color:#526357}.fb-notes{padding-bottom:80px}.foldblock-card img{width:100%;border-radius:12px}@media(max-width:700px){.fb-hero,.fb-features{grid-template-columns:1fr}.fb-hero,.fb-features,.fb-screens,.release,.fb-notes{padding:36px 20px}.screens{gap:10px}.screens img{border-radius:12px}.screens figcaption{font-size:12px}.release{margin:16px}.fb-hero .feature{order:-1}}</style>'
  page=re.sub(r'<main\b.*?</main>',lambda m:body,template,flags=re.S)
  page=re.sub(r'<title>.*?</title>','<title>'+name+' — AP Games</title>',page)
  page=page.replace(f'https://www.apholdings.kr/{lang}/games/',f'https://www.apholdings.kr{route}')
  page=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+desc+'">',page)
  page=re.sub(r'<meta property="og:title" content="[^"]*">','<meta property="og:title" content="'+name+' — AP Games">',page)
  page=re.sub(r'<meta property="og:description" content="[^"]*">','<meta property="og:description" content="'+desc+'">',page)
  page=page.replace('</head>','<meta property="og:image" content="https://www.apholdings.kr/media/games/foldblock/feature.png">'+css+'</head>')
  target=ROOT/route.strip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(page)
  card='<article class="product-card hub-card foldblock-card" data-foldblock><img src="/media/games/foldblock/feature.png" width="1024" height="500" alt="'+name+'"><span class="status">'+('출시 준비 중' if ko else 'Coming soon')+'</span><h3>'+name+'</h3><p>'+desc+'</p><a class="text-link" href="'+route+'">'+('게임 소개 보기 →' if ko else 'Discover FoldBlock →')+'</a></article>'
  for f in (hub,ROOT/f'{lang}/index.html'):
   s=f.read_text();s=re.sub(r'<article[^>]*data-foldblock.*?</article>','',s,flags=re.S)
   marker='<div class="grid-3 hub-grid">' if f==hub else '<div class="compact-grid games-grid">'
   if marker not in s and f!=hub:
    s=s.replace('</main>','<section class="section"><div class="wrap"><h2>AP Games · FoldBlock</h2><div class="grid-3 hub-grid">'+card+'</div></div></section></main>');f.write_text(s);continue
   if marker not in s:raise RuntimeError(f'Missing Games insertion: {f}')
   s=s.replace(marker,marker+card,1);f.write_text(s)
 sitemap=ROOT/'sitemap.xml';s=sitemap.read_text()
 for lang in ('ko','en'):
  url=f'https://www.apholdings.kr/{lang}/products/foldblock/'
  if url not in s:s=s.replace('</urlset>',f'<url><loc>{url}</loc><lastmod>2026-10-29</lastmod></url></urlset>')
 sitemap.write_text(s)
if __name__=='__main__':apply()
