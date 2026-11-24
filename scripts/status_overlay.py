"""status.json → 제품 데이터 덮어쓰기 (build_site.py 에서 호출). 새 CSS·구조 없이 기존 블록(tags·note)만 쓴다."""
import json

def _n(x, ko):
    if not x: return None
    if ko: return f"{x/10000:.1f}".rstrip('0').rstrip('.') + '만 개'
    return f"{x/1000:,.0f}K" if x < 1_000_000 else f"{x/1_000_000:.1f}M"

def chips(pid, p, ko):
    f = p.get('facts', {}); out = []
    if f.get('appLive'):
        v = f.get('appVersion', '')
        out.append(f"iOS 앱 {v} · 출시" if ko else f"iOS app {v} · live")
    c = f.get('connector')
    if c:
        out.append(('Claude 커넥터 · ' + ('운영 중' if c == 'ok' else '점검 중')) if ko else ('Claude connector · ' + ('running' if c == 'ok' else 'maintenance')))
    n = _n(f.get('count'), ko)
    if n:
        what = {'safe': ('제품', 'products'), 'light': ('식품', 'foods')}[pid]
        s = (f"{what[0]} {n}" if ko else f"{n} {what[1]}")
        if f.get('asOf'):
            s += (f" · {f['asOf']} 기준" if ko else '')
        out.append(s)
    out += [m['ko' if ko else 'en'] for m in p.get('manual', [])]
    return out

def apply(DATA, ROOT):
    path = ROOT / 'site-source/status.json'
    if not path.exists(): return
    S = json.loads(path.read_text(encoding='utf-8'))
    for l, d in DATA.items():
        ko = l == 'ko'
        for pr in d.get('products', []):
            p = S['products'].get(pr['id'])
            if not p: continue
            if p.get('stage'): pr['status'] = p['stage']
            t = next((s for s in pr.get('sections', []) if s['id'] == 'today'), None)
            if not t: continue
            bl = [b for b in t['blocks'] if b.get('type') not in ('tags', 'note')]
            bl.insert(0, {'type': 'tags', 'items': chips(pr['id'], p, ko)})
            if S.get('checked'):
                bl.append({'type': 'note', 'text': (f"진행 현황 · {S['checked']} 확인" if ko else f"Status · checked {S['checked']}")})
            t['blocks'] = bl
