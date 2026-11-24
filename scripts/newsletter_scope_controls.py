"""Synthetic linguistic regressions only; never publication source material."""
import json
from pathlib import Path
from newsletter_speech_acts import classify
CASES=[
 '국내에서 인정되는 과정인지 확인한다.',
 '국내에서 인정되는 이 과정을 확인한다.',
 'AP가 기회를 얻었다면 활용을 검토한다.',
 'AP가 얻은 기회를 활용한다.',
 '학습 효과가 입증됐으므로 도입을 검토한다.',
 '도입한다면 모든 학생에게 효과가 입증된 기능을 사용하자.',
 '학습 효과가 입증됐는지 확인한다.',
 '학습 효과가 입증되지 않았다는 보고를 확인한다.',
]
def check(model,folder):
 story={'title':'새 도구를 발표했다.','summary':'새 도구를 발표했다.','fact':'새 도구를 발표했다.','insight':'필요하다면 적용을 검토할 수 있다.','action':' '.join(CASES)}
 receipt=classify(model,story)
 Path(folder,'scope-controls.json').write_text(json.dumps({'synthetic_regression_only':True,'draft':story,'receipt':receipt},ensure_ascii=False,indent=2))
 actual={r['id']:r['kind'] for r in receipt['inventory'] if r['field']=='action'}
 expected={i:'pure_proposal' if i in (0,2,6) else 'asserted_or_mixed' for i in range(len(CASES))}
 if actual!=expected:raise ValueError('Speech-act scope regression failed')
 negative=[p['text'] for p in receipt['facts']['action'] if p['sentence_id']==7]
 if len(negative)!=1 or '학습 효과가 입증되지 않았다는 보고를' not in negative[0]:raise ValueError('Negation or report attribution scope lost in asserted inventory')
 return receipt
