#!/usr/bin/env python3
"""세이프리스트·라이트리스트 진행 현황 사실 확인 → site-source/status.json 갱신.
App Store 버전·출시일(iTunes lookup) · 커넥터 /health. 바뀐 게 없으면 파일을 건드리지 않는다(checked 날짜 제외).
사용: python3 scripts/update_status.py   → 표준출력에 요약, 종료코드 0
"""
import json, urllib.request, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'site-source/status.json'
KST = datetime.timezone(datetime.timedelta(hours=9))

def get(url, timeout=90):
    req = urllib.request.Request(url, headers={'User-Agent': 'apholdings-status/1.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))

S = json.loads(P.read_text(encoding='utf-8'))
before = json.dumps(S['products'], ensure_ascii=False, sort_keys=True)
for pid, p in S['products'].items():
    f = dict(p.get('facts') or {})
    try:
        r = get(f"https://itunes.apple.com/lookup?id={p['appId']}&country=kr")['results']
        if r:
            r = r[0]
            f['appVersion'] = r.get('version')
            d = r.get('currentVersionReleaseDate')
            if d:
                f['appDate'] = datetime.datetime.fromisoformat(d.replace('Z', '+00:00')).astimezone(KST).strftime('%Y-%m-%d')
            f['appLive'] = True
        else:
            f['appLive'] = False
    except Exception as ex:
        print(pid, 'appstore check failed:', ex)   # 실패하면 이전 사실 유지
    try:
        h = get(p['health'])
        f['connector'] = 'ok' if h.get('ok') else 'down'
        f['count'] = h.get('products') or h.get('foods') or f.get('count')
        if h.get('asOf'): f['asOf'] = h['asOf']
    except Exception as ex:
        f['connector'] = 'down'
        print(pid, 'health failed:', ex)
    p['facts'] = f
after = json.dumps(S['products'], ensure_ascii=False, sort_keys=True)
changed = before != after
S['checked'] = datetime.datetime.now(KST).strftime('%Y-%m-%d')
P.write_text(json.dumps(S, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
for pid, p in S['products'].items():
    print(pid, json.dumps(p['facts'], ensure_ascii=False))
print('CHANGED' if changed else 'UNCHANGED')
