#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""리아 인스타그램 지표 → Supabase 동기화.

GitHub Actions 에서 매일 실행된다. 표준 라이브러리만 쓴다 (pip 설치 없음).

필요한 시크릿 (Settings → Secrets and variables → Actions)
  IG_TOKEN               인스타그램 장기 액세스 토큰
  SUPABASE_SERVICE_KEY   Supabase service_role 키

원칙
  · 조회 실패를 0 으로 메우지 않는다. 실패는 실패로 남기고 종료 코드를 올린다
  · 토큰을 절대 출력하지 않는다 (로그는 공개된다)
  · ai_note 는 건드리지 않는다. 사람이 쓴 판독만 들어가는 칸이다
"""
import os, sys, json, time, urllib.request, urllib.parse, urllib.error, datetime

IG_TOKEN   = os.environ["IG_TOKEN"]
SB_URL     = os.environ.get("SUPABASE_URL", "https://cgijpcimixaregbpvqbf.supabase.co").rstrip("/")
SB_KEY     = os.environ["SUPABASE_SERVICE_KEY"]
CHANNEL_ID = os.environ.get("IG_CHANNEL_ID", "23ff8bd5-67ab-4c8d-9ef1-b164ef0f3795")

GRAPH = "https://graph.instagram.com/v23.0"
UTC   = datetime.timezone.utc


def ig(path, **params):
    params["access_token"] = IG_TOKEN
    url = f"{GRAPH}/{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=40) as r:
        return json.loads(r.read())


def ig_url(url):
    with urllib.request.urlopen(url, timeout=40) as r:
        return json.loads(r.read())


def sb(method, path, body=None, **params):
    url = f"{SB_URL}/rest/v1/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("apikey", SB_KEY)
    req.add_header("Authorization", f"Bearer {SB_KEY}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Prefer", "resolution=merge-duplicates,return=representation")
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            raw = r.read()
            return json.loads(raw) if raw else []
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"[supabase {method} {path}] {e.code} {e.read()[:300].decode(errors='replace')}\n")
        raise


def fetch_media(limit_total=200):
    out = []
    d = ig("me/media",
           fields="id,timestamp,media_type,media_product_type,permalink,caption",
           limit=50)
    out += d.get("data", [])
    nxt = d.get("paging", {}).get("next")
    while nxt and len(out) < limit_total:
        d = ig_url(nxt)
        out += d.get("data", [])
        nxt = d.get("paging", {}).get("next")
    return out


def insights(media_id, product_type):
    metrics = "reach,likes,comments,saved,shares"
    if product_type == "REELS":
        metrics += ",views,ig_reels_avg_watch_time"
    try:
        d = ig(f"{media_id}/insights", metric=metrics)
    except urllib.error.HTTPError:
        return None
    return {i["name"]: i["values"][0]["value"] for i in d.get("data", [])}


def account_snapshot():
    """계정 30일 스냅샷. reach 의 팔로워/비팔로워 분해가 핵심이다."""
    until = int(datetime.datetime.now(UTC).timestamp())
    since = until - 29 * 86400
    out = {}
    try:
        me = ig("me", fields="followers_count,media_count")
        out["followers"] = me.get("followers_count")
    except urllib.error.HTTPError:
        pass
    for metric, key in (("reach", "reach_total"), ("profile_views", "profile_views"),
                        ("accounts_engaged", "accounts_engaged"),
                        ("total_interactions", "total_interactions")):
        try:
            d = ig("me/insights", metric=metric, period="day",
                   metric_type="total_value", since=since, until=until)
            out[key] = d["data"][0]["total_value"]["value"]
        except Exception:
            out[key] = None
    try:
        d = ig("me/insights", metric="reach", period="day", metric_type="total_value",
               breakdown="follow_type", since=since, until=until)
        for b in d["data"][0]["total_value"].get("breakdowns", []):
            for r in b.get("results", []):
                dim = r["dimension_values"][0]
                if dim == "FOLLOWER":
                    out["reach_follower"] = r["value"]
                elif dim == "NON_FOLLOWER":
                    out["reach_non_follower"] = r["value"]
    except Exception:
        pass
    return out


def main():
    started = datetime.datetime.now(UTC)
    media = fetch_media()
    if not media:
        sys.stderr.write("게시물 0건 — 토큰 또는 권한 확인 필요. 중단한다.\n")
        return 1
    print(f"게시물 {len(media)}건")

    items, rows, failed = [], [], 0
    for m in media:
        pt = m.get("media_product_type") or m.get("media_type")
        cap = (m.get("caption") or "").strip()
        items.append({
            "channel_id": CHANNEL_ID,
            "platform_media_id": m["id"],
            "title": cap.splitlines()[0][:200] if cap else None,
            "media_format": pt,
            "published_url": m.get("permalink"),
            "published_at": m["timestamp"],
            "stage": "published",
        })
        v = insights(m["id"], pt)
        if v is None:
            failed += 1
            continue
        aw = v.get("ig_reels_avg_watch_time")
        rows.append({
            "pid": m["id"],
            "reach": v.get("reach"), "views": v.get("views"),
            "likes": v.get("likes"), "comments": v.get("comments"),
            "saved": v.get("saved"), "shares": v.get("shares"),
            "avg_watch_seconds": round(aw / 1000, 3) if isinstance(aw, (int, float)) else None,
        })
        time.sleep(0.12)

    sb("POST", "admin_media_items", items, on_conflict="platform_media_id")
    print(f"게시물 적재 {len(items)}건")

    mapping = {}
    for chunk in range(0, len(items), 100):
        ids = [i["platform_media_id"] for i in items[chunk:chunk + 100]]
        got = sb("GET", "admin_media_items",
                 select="id,platform_media_id",
                 platform_media_id="in.(" + ",".join(ids) + ")")
        mapping.update({g["platform_media_id"]: g["id"] for g in got})

    observed = started.replace(minute=0, second=0, microsecond=0).isoformat()
    payload = []
    for r in rows:
        iid = mapping.get(r.pop("pid"))
        if not iid:
            continue
        r.update({"item_id": iid, "observed_at": observed,
                  "source": "instagram_graph_api"})
        payload.append(r)
    if payload:
        sb("POST", "admin_media_metrics", payload, on_conflict="item_id,observed_at")
    print(f"지표 적재 {len(payload)}건 · 조회실패 {failed}건")

    acc = account_snapshot()
    if acc.get("reach_total") is not None:
        acc.update({"channel_id": CHANNEL_ID,
                    "observed_on": started.date().isoformat(),
                    "window_days": 30, "source": "instagram_graph_api"})
        sb("POST", "admin_media_account_daily", [acc],
           on_conflict="channel_id,observed_on,window_days")
        print(f"계정 스냅샷 · 팔로워도달 {acc.get('reach_follower')} / "
              f"비팔로워도달 {acc.get('reach_non_follower')}")
    else:
        sys.stderr.write("계정 인사이트 조회 실패 — 추정치로 채우지 않고 건너뛴다.\n")

    if failed and failed == len(media):
        sys.stderr.write("전 건 지표 조회 실패. 실패로 종료한다.\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
