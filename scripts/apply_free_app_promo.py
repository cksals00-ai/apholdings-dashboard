"""Keep verified Hangeul Cubs and FoldBlock install links after generation."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
STORES = {
    'cubs': ('https://apps.apple.com/app/id6803749436', 'https://play.google.com/store/apps/details?id=com.aplocalift.hangeulcubs'),
    'foldblock': ('https://apps.apple.com/app/id6828323490', 'https://play.google.com/store/apps/details?id=com.apholdings.foldblock'),
}

def buttons(app, ko):
    apple, google = STORES[app]
    return (f'<a class="button primary" href="{google}" target="_blank" rel="noopener noreferrer">'
            + ('Google Play에서 설치' if ko else 'Get it on Google Play') + '</a>'
            + f'<a class="button" href="{apple}" target="_blank" rel="noopener noreferrer">'
            + ('App Store에서 다운로드' if ko else 'Download on the App Store') + '</a>')

def apply():
    for lang in ('ko', 'en'):
        ko = lang == 'ko'
        p = ROOT / lang / 'products/cubs/index.html'
        s = p.read_text()
        # Insert once in the hero, retaining the existing education-site link.
        s = re.sub(r'<div class="actions hero-actions">.*?</div>',
            lambda m: '<div class="actions hero-actions">' + buttons('cubs', ko)
            + f'<a class="button" href="https://edu.apholdings.kr/{lang}/">'
            + ('학습 사이트 보기' if ko else 'Explore the learning site') + '</a></div>', s, count=1, flags=re.S)
        s = s.replace('>iOS 앱과 교육 영상을 이용할 수 있습니다.<', '>Android·iOS 앱과 교육 영상을 이용할 수 있습니다.<')
        s = s.replace('Android 정식 출시 준비 중', 'Android·iOS 정식 출시')
        s = s.replace('Android release coming soon', 'Available on Android and iOS')
        s = s.replace('Android · coming soon', 'Android · available on Google Play')
        # Avoid implying that external YouTube viewing works offline.
        s = s.replace('<span>완전 오프라인</span>', '<span>기기 내 학습 · 영상은 인터넷 필요</span>')
        today = '<section class="section anchor" id="today"><div class="wrap"><div class="cta-block"><span class="number">05 · '
        today += ('지금' if ko else 'Today') + '</span><h2>'
        today += ('Android·iOS에서 한글 학습을 시작하세요.' if ko else 'Start learning on Android and iOS.') + '</h2><p>'
        today += ('무료 71레슨으로 첫 글자부터 연습하세요. 받침 마스터 팩 18레슨은 별도 앱 내 구매입니다.' if ko else 'Start with 71 free lessons. The 18-lesson Batchim Master pack is a separate in-app purchase.')
        today += '</p><div class="actions">' + buttons('cubs', ko) + '</div><p class="note">'
        today += ('Android · iPhone · iPad · 학습 영상 시청에는 인터넷이 필요합니다.' if ko else 'Android · iPhone · iPad. Internet is required to watch learning videos.')
        today += '</p></div></div></section>'
        s, n = re.subn(r'<section class="section anchor" id="today">.*?</section>', lambda m: today, s, count=1, flags=re.S)
        assert n == 1, p
        p.write_text(s)

        p = ROOT / lang / 'products/foldblock/index.html'
        s = p.read_text()
        status = '<div class="release" id="install"><h2>' + ('지금 무료로 플레이하세요' if ko else 'Play for free')
        status += '</h2><div class="actions">' + buttons('foldblock', ko) + '</div><p class="muted">'
        status += ('Android · iPhone · iPad에서 이용할 수 있습니다. 광고·인앱 구매·계정 없이 즐기세요.' if ko
                   else 'Available on Android, iPhone and iPad. No ads, in-app purchases or account.') + '</p></div>'
        s, n = re.subn(r'<div class="release" id="install">.*?<p class="muted">.*?</p></div>', lambda m: status, s, count=1, flags=re.S)
        assert n == 1, p
        s = s.replace('출시 현황 보기', '무료로 설치하기').replace('>Release status</a>', '>Get the app</a>')
        p.write_text(s)
        for p in (ROOT / lang / 'games/index.html', ROOT / lang / 'index.html'):
            s = p.read_text()
            def card(m):
                c = m[0].replace('출시 준비 중', 'Android · iOS 출시').replace('Coming soon', 'Available on Android &amp; iOS')
                c = re.sub(r'<div class="actions" data-foldblock-install>.*?</div>', '', c, flags=re.S)
                return c.replace('</article>', '<div class="actions" data-foldblock-install>' + buttons('foldblock', ko) + '</div></article>')
            s, n = re.subn(r'<article[^>]*data-foldblock.*?</article>', card, s, flags=re.S)
            assert n == 1, p
            p.write_text(s)

if __name__ == '__main__':
    apply()
