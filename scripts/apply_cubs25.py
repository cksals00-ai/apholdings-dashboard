"""Apply approved 2.5 copy and screenshots without regenerating other site surfaces."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1]
def apply():
 for lang in ('ko','en','vi','fr','ja','zh-cn'):
  data=json.loads((ROOT/f'site-source/locales/{lang}.json').read_text());p=next(x for x in data['products'] if x['id']=='cubs');a=next(x for x in p['sections'] if x['id']=='first-letters-25');tags=a['blocks'][0]['items'];note=a['blocks'][1]['text']
  f=ROOT/f'{lang}/products/cubs/index.html';s=f.read_text()
  s=re.sub(r'<section[^>]*id="first-letters-25".*?</section>','',s,flags=re.S)
  block='<section class="section soft anchor" id="first-letters-25"><div class="wrap"><span class="eyebrow">NEW · VERSION 2.5</span><h2>'+a['title']+'</h2><p class="lead">'+a['desc']+'</p><div class="tags">'+''.join('<span>'+x+'</span>' for x in tags)+'</div><div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;max-width:760px;margin:30px auto"><img src="/media/cubs/v25/letter.png" width="390" height="844" alt="First Letters: ㅏ + ㅇ = 아" style="width:100%;height:auto;border-radius:16px" loading="lazy"><img src="/media/cubs/v25/word.png" width="390" height="844" alt="Word lesson: 아빠 · dad" style="width:100%;height:auto;border-radius:16px" loading="lazy"></div><p>'+note+'</p><a class="button primary" href="https://apps.apple.com/app/id6803749436">App Store · 2.5</a></div></section>'
  s=s.replace('<section class="section">',block+'<section class="section">',1)
  s=re.sub(r'(?<!\d)42(?=\s*(?:레슨|lessons|leçons|bài|レッスン|课))','71',s)
  s=s.replace('한국어를 처음 만나는 외국인과 아이.\n한 에피소드에 받침 하나. 영어 · 베트남어 · 프랑스어.','처음 배우는 모음·자음부터 받침까지.\n무료 71레슨 · 영어 · 베트남어 · 프랑스어 힌트.')
  s=s.replace('Android · YouTube 채널 — 추후 출시 예정','Android 정식 출시 준비 중 · YouTube 채널 운영 중')
  s=s.replace('YouTube 채널에서 EP1 공개 중. 레슨팩 확장은 준비 중.','2.5 공개: 무료 71레슨. 받침 마스터 팩 18레슨은 별도 구매입니다.')
  f.write_text(s)
if __name__=='__main__':apply()
