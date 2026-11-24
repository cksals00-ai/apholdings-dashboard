#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prices.json 생성 (맥 실행판 v2). 스키마는 앱 계약 그대로.
v1과 다른 점: asof에 date.today()가 아니라 실측 기준일을 넣는다(D-140 — 수기/추정 입력 금지).
사용: python3 gen_prices_v2.py [REPO_DIR]
"""
import json, os, sys, datetime as dt, time
import FinanceDataReader as fdr
from concurrent.futures import ThreadPoolExecutor

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/apdash")
OUT = os.path.join(REPO, "data", "prices.json")
SPARK_TOP = 400

def listing():
    for _ in range(4):
        try: return fdr.StockListing("KRX")
        except Exception: time.sleep(2)
    raise RuntimeError("StockListing 실패")

krx = listing()
bad = krx["Name"].str.contains("우$|우B$|우C$|스팩|리츠|홀딩스우", regex=True, na=False)
uni = krx[~bad]
uni = uni[uni["Market"].isin(["KOSPI", "KOSDAQ"])]

rows = []
for _, r in uni.iterrows():
    try:
        rows.append({"c": r["Code"], "n": r["Name"], "m": r["Market"][:6],
                     "p": round(float(r["Close"])),
                     "ch": round(float(r.get("ChagesRatio") or 0), 2),
                     "mc": round((r["Marcap"] or 0) / 1e8),
                     "a": round((r["Amount"] or 0) / 1e8, 1)})
    except Exception:
        pass
print("스냅샷 %d종목" % len(rows), flush=True)

ref = None
for probe in ("005930", "000660", "035420"):
    try:
        px = next(r["p"] for r in rows if r["c"] == probe)
        b = fdr.DataReader(probe, (dt.date.today() - dt.timedelta(days=14)).isoformat())
        m = b[b["Close"] == px]
        if len(m):
            ref = str(m.index[-1].date()); break
    except Exception:
        continue
if ref is None:
    ref = dt.date.today().isoformat()
    print("주의: 기준일 확인 실패 — today 사용", flush=True)
print("실측 기준일: %s" % ref, flush=True)

def spark(code):
    try:
        df = fdr.DataReader(code, (dt.date.fromisoformat(ref) - dt.timedelta(days=70)).isoformat(), ref)
        c = df["Close"].dropna().tolist()[-30:]
        return code, ([round(x) for x in c] if len(c) >= 5 else None)
    except Exception:
        return code, None

top = [r["c"] for r in sorted(rows, key=lambda x: -x["a"])[:SPARK_TOP]]
sp = {}
with ThreadPoolExecutor(max_workers=12) as ex:
    for i, (code, s) in enumerate(ex.map(spark, top), 1):
        if s: sp[code] = s
        if i % 100 == 0: print("  스파크 %d/%d" % (i, len(top)), flush=True)
for r in rows:
    if r["c"] in sp: r["s"] = sp[r["c"]]
print("스파크 %d종목" % len(sp), flush=True)

out = {"asof": ref, "basis": "종가",
       "generated": dt.datetime.now().isoformat()[:16],
       "disclaimer": "모의투자용 전일/당일 종가 스냅샷 — 실시간 아님, 투자 권유 아님",
       "stocks": rows}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
tmp = OUT + ".tmp"
with open(tmp, "w") as f:
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
os.replace(tmp, OUT)
print("저장: %s (%s bytes)" % (OUT, format(os.path.getsize(OUT), ",")))

chk = json.load(open(OUT, encoding="utf-8"))
assert set(chk.keys()) == {"asof", "basis", "generated", "disclaimer", "stocks"}
assert all({"c","n","m","p","ch","mc","a"} <= set(s.keys()) for s in chk["stocks"][:50])
print("검산 통과 — asof %s / %d종목 / 스파크 %d종목"
      % (chk["asof"], len(chk["stocks"]), sum("s" in s for s in chk["stocks"])))
