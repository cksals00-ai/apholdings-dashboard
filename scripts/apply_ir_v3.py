#!/usr/bin/env python3
"""IR 본문을 IA v3(5부문) 기준으로 다시 쓴다 — AP Revenue·Travel 서술 제거 (2026-10-09 대표 결정). 여러 번 실행해도 같은 결과."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
R = json.loads((ROOT / 'site-source/ir-v3.json').read_text())
report = {}
for l, pairs in R.items():
    loc, _, page = l.partition('@'); p = ROOT / loc / (page or 'ir') / 'index.html'; s = p.read_text(); hit = 0; miss = []
    for old, new in pairs:
        forms = [(old, new), (old.replace('\n', '\\n'), new.replace('\n', '\\n'))]
        found = False
        for o, n in forms:
            if o in s:
                s = s.replace(o, n); found = True
        if found or new in s:
            hit += 1
        else:
            miss.append(old[:40])
    p.write_text(s); report[l] = {'applied': hit, 'missing': miss}
print(json.dumps(report, ensure_ascii=False, indent=1))
