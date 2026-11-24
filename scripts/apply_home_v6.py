#!/usr/bin/env python3
"""HOME v6 (2026-10-09): 임팩트 히어로. apply_home_v5 뒤에 실행(같은 폴더). 재실행해도 같음.
히어로를 어두운 전면 무대로 교체: 단어별 등장 헤드라인 + 「AI가 ___, 결정은 사람이」 회전 문장 + AP 중심 6부문 궤도 애니메이션(SVG/CSS) + 운영 중 제품 띠.
그 아래 「우리가 하는 일」 3단계 띠 삽입. 움직임 줄이기 설정이면 모두 정지. JS는 인라인 1개(회전 문장·스크롤 등장)."""
import re, html, importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent; E=lambda s:html.escape(str(s),quote=True)
spec=importlib.util.spec_from_file_location('h5',HERE/'apply_home_v5.py'); h5=importlib.util.module_from_spec(spec); spec.loader.exec_module(h5)
T6={
'ko':dict(h=['AI와','사람을','잇는','회사.'],pre='AI가',verbs=['성분을 대조하고','한국을 가르치고','순위를 매기고','상품을 골라 주고'],post='결정은 사람이 합니다.',what='무엇을 하나요',s1='공개 원본에 대조한다',s1d='식약처 자료처럼 누구나 확인할 수 있는 원본만',s2='근거와 함께 답한다',s2d='답마다 출처를 붙여 앱 · AI 비서 · 매장으로',s3='결정은 사람이 한다',s3d='고르고, 배우고, 겨루고, 사는 순간에',live='지금 운영 중',scroll='아래로'),
'en':dict(h=['Connecting','AI','and','people.'],pre='AI',verbs=['checks the ingredients,','teaches Korean,','ranks the players,','picks the products —'],post='people make the call.',what='What we do',s1='Check against public sources',s1d='Only originals anyone can verify, like Korea’s MFDS data',s2='Answer with evidence',s2d='Every answer carries its source — in apps, AI assistants and stores',s3='People decide',s3d='When choosing, learning, competing and buying',live='Live now',scroll='Scroll'),
'vi':dict(h=['Kết','nối','AI','và con người.'],pre='AI',verbs=['đối chiếu thành phần,','dạy tiếng Hàn,','xếp hạng người chơi,','chọn sản phẩm —'],post='con người quyết định.',what='Chúng tôi làm gì',s1='Đối chiếu nguồn công khai',s1d='Chỉ dữ liệu gốc ai cũng kiểm chứng được',s2='Trả lời kèm bằng chứng',s2d='Mỗi câu trả lời đều có nguồn — trong ứng dụng, trợ lý AI và cửa hàng',s3='Con người quyết định',s3d='Khi chọn, học, thi đấu và mua',live='Đang hoạt động',scroll='Cuộn xuống'),
'ja':dict(h=['AIと','人を','つなぐ','会社。'],pre='AIが',verbs=['成分を照合し、','韓国語を教え、','順位をつけ、','商品を選び、'],post='決めるのは人です。',what='私たちがすること',s1='公開された原本と照合する',s1d='誰でも確認できる原本データだけ',s2='根拠とともに答える',s2d='すべての答えに出典を — アプリ・AIアシスタント・店舗で',s3='決めるのは人',s3d='選ぶ・学ぶ・競う・買う瞬間に',live='運営中',scroll='スクロール'),
'zh-cn':dict(h=['连接','AI','与','人。'],pre='AI',verbs=['核对成分，','教授韩语，','排定名次，','挑选商品，'],post='由人做决定。',what='我们做什么',s1='对照公开原始数据',s1d='只用任何人都能核实的原始资料',s2='附上依据作答',s2d='每个回答都带出处——在应用、AI 助手和门店中',s3='由人决定',s3d='在挑选、学习、竞技和购买的时刻',live='正在运营',scroll='向下'),
'fr':dict(h=['Relier','l’IA','et','les humains.'],pre='L’IA',verbs=['vérifie les ingrédients,','enseigne le coréen,','classe les joueurs,','choisit les produits —'],post='l’humain décide.',what='Ce que nous faisons',s1='Vérifier sur sources publiques',s1d='Uniquement des originaux vérifiables par tous',s2='Répondre avec la preuve',s2d='Chaque réponse porte sa source — apps, assistants IA, boutiques',s3='L’humain décide',s3d='Au moment de choisir, apprendre, jouer et acheter',live='En service',scroll='Défiler'),
}
DIVS=['entertainment','edu','games','shop','intelligence']
def orbit(l):
    import math
    nodes=[];lines=[];dots=[]
    for i,d in enumerate(DIVS):
        a=-math.pi/2+i*2*math.pi/len(DIVS); x=300+210*math.cos(a); y=300+210*math.sin(a)
        lines.append(f'<line class="ob-l" style="--i:{i}" x1="300" y1="300" x2="{x:.0f}" y2="{y:.0f}"/>')
        dots.append(f'<circle class="ob-dot" r="4" style="--i:{i}"><animateMotion dur="3.2s" begin="{1.6+i*0.35:.2f}s" repeatCount="indefinite" path="M{x:.0f},{y:.0f} L300,300"/></circle>')
        nodes.append(f'<a href="/{l}/{d}/" class="ob-n" style="--i:{i}"><circle cx="{x:.0f}" cy="{y:.0f}" r="9"/><text x="{x:.0f}" y="{y+(34 if y>300 else -22):.0f}" text-anchor="middle">{d.capitalize()}</text></a>')
    return ('<svg class="hv6-orbit" viewBox="0 0 600 600" role="img" aria-label="AP: '+' · '.join(d.capitalize() for d in DIVS)+'">'
      '<circle class="ob-ring" cx="300" cy="300" r="210"/><circle class="ob-ring r2" cx="300" cy="300" r="120"/>'+''.join(lines)+''.join(dots)+
      '<circle class="ob-pulse" cx="300" cy="300" r="56"/><circle class="ob-core" cx="300" cy="300" r="56"/><text class="ob-ap" x="300" y="312" text-anchor="middle">AP</text>'+''.join(nodes)+'</svg>')
def hero(l):
    t=T6[l]; t5=h5.T[l]
    words=''.join(f'<span class="w" style="--i:{i}">{E(w)}</span> ' for i,w in enumerate(t['h']))
    verbs=''.join(f'<span class="v{" on" if i==0 else ""}">{E(v)}</span>' for i,v in enumerate(t['verbs']))
    live=''.join(f'<a href="{u}" target="_blank" rel="noopener noreferrer"><i></i>{n}</a>' for n,u in [('AP Safe',h5.SAFE),('AP Light',h5.LIGHT),('AP Games',f'https://games.apholdings.kr/{"ko" if l=="ko" else "en"}/'),('Lia Select Shop','https://shop.apholdings.kr/')])
    return (f'<section class="hv6" aria-label="AP Holdings"><div class="wrap hv6-in"><div class="hv6-copy">'
      f'<span class="eyebrow">AP HOLDINGS · AI PEOPLE</span><h1>{words}</h1>'
      f'<p class="hv6-rot"><span class="pre">{E(t["pre"])}</span> <span class="verbs" aria-live="off">{verbs}</span><br><b>{E(t["post"])}</b></p>'
      f'<div class="actions"><a class="button primary" href="/{l}/about/">{E(t5["about"])}</a><a class="button ghost" href="/{l}/ir/">IR / INVESTORS</a></div></div>'
      f'<div class="hv6-art">{orbit(l)}</div></div>'
      f'<div class="hv6-live"><div class="wrap"><span>{E(t["live"])}</span>{live}</div></div></section>'
      f'<section class="hv6-what"><div class="wrap"><span class="eyebrow">{E(t["what"])}</span><ol>'
      + ''.join(f'<li class="rv" style="--i:{i}"><span class="n">0{i+1}</span><h3>{E(t[f"s{i+1}"])}</h3><p>{E(t[f"s{i+1}d"])}</p></li>' for i in range(3))
      + '</ol></div></section>')
JS='<script data-v6>(()=>{const r=matchMedia("(prefers-reduced-motion: reduce)").matches;const v=[...document.querySelectorAll(".hv6-rot .v")];let k=0;if(!r&&v.length>1)setInterval(()=>{v[k].classList.remove("on");k=(k+1)%v.length;v[k].classList.add("on")},2400);const io=new IntersectionObserver(e=>e.forEach(x=>{if(x.isIntersecting){x.target.classList.add("in");io.unobserve(x.target)}}),{threshold:.15});document.querySelectorAll("main .rv, main section:not(.hv6) h2, .hflow, .use-list, .hn-list, .hc-in").forEach(el=>{el.classList.add("rv");io.observe(el)})})();</script>'
def main():
    n=0
    for l in h5.LOCS:
        f=ROOT/l/'index.html'
        if not f.exists(): continue
        s=f.read_text(); o=s
        s=re.sub(r'<section class="hv6".*?</section><section class="hv6-what">.*?</section>','',s,flags=re.S)
        s=re.sub(r'<section class="hero home-hero hv5">.*?</section>','',s,count=1,flags=re.S)
        s=s.replace('<main id="main">','<main id="main">'+hero(l),1)
        s=re.sub(r'<script data-v6>.*?</script>','',s,flags=re.S).replace('</body>',JS+'</body>',1)
        s=s.replace('<body','<body data-home="v6"',1) if 'data-home="v6"' not in s else s
        if s!=o: f.write_text(s); n+=1
    print({'home_v6':n})
if __name__=='__main__':
    main()
    from apply_website_copy import main as apply_copy
    apply_copy()
