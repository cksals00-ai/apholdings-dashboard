#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""리아 「한국 여행 실전 한글」 하루 한 편 — GitHub Actions 에서 매일 실행.

data/lia_daily_queue.json 의 순서대로, 아직 안 올라간 첫 편을 인스타 릴로 게시한다.
  · 이미 올라갔는지는 인스타 전체 게시물로 판정(상태 파일을 고치지 않음)
    - 캡션 첫 줄이 같으면 중복
    - 단일 표현 편은 같은 표현이 「표현 (발음)」 형태로 이미 올라갔으면 중복(다른 경로로 올라간 것 포함)
  · 이 시리즈가 최근 18시간 안에 올라갔으면 건너뜀(다른 시리즈 게시물은 무시)
  · 토큰은 절대 출력하지 않는다. API 원본 응답도 출력하지 않는다.
"""
import os, sys, json, time, datetime, urllib.request, urllib.parse, urllib.error

TOK = os.environ["IG_TOKEN"]
G = "https://graph.instagram.com/v23.0/"
QUEUE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "lia_daily_queue.json")


def call(path, data=None, **q):
    if data is not None:
        req = urllib.request.Request(G + path, data=urllib.parse.urlencode(dict(data, access_token=TOK)).encode())
    else:
        req = G + path + "?" + urllib.parse.urlencode(dict(q, access_token=TOK))
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        msg = json.loads(e.read().decode(errors="replace") or "{}").get("error", {}).get("message", "")
        sys.exit(f"API 오류 {e.code} ({path.split('?')[0]}): {msg[:200]}")


def first_line(s):
    return (s or "").strip().splitlines()[0].strip() if (s or "").strip() else ""


def all_media(max_items=500):
    out, r = [], call("me/media", fields="timestamp,caption", limit=100)
    while True:
        out += r.get("data", [])
        nxt = r.get("paging", {}).get("next")
        if not nxt or len(out) >= max_items:
            return out
        try:   # next URL 에 토큰이 들어 있으므로 출력하지 않는다
            r = json.load(urllib.request.urlopen(nxt, timeout=60))
        except urllib.error.HTTPError as e:
            sys.exit(f"API 오류 {e.code} (paging)")


def already_posted(it, captions, lines):
    if first_line(it["caption"]) in lines:
        return True
    ko = (it.get("ko") or "").strip()
    if it.get("id", "").startswith("p") and ko:
        key = ko + " ("   # 단일 표현 편 캡션 형식: 「표현 (발음)」
        return any(key in c for c in captions)
    return False


def main():
    queue = json.load(open(QUEUE, encoding="utf-8"))
    history = all_media()
    recent = history[:40]
    ours = {first_line(x["caption"]) for x in queue}
    now = datetime.datetime.now(datetime.timezone.utc)
    for m in recent:   # 다른 시리즈 게시물은 상관하지 않는다 — 이 시리즈가 최근 18시간 안에 올라갔을 때만 건너뜀
        t = datetime.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        if first_line(m.get("caption")) in ours and (now - t).total_seconds() < 18 * 3600:
            print("이 시리즈 오늘 편 이미 게시됨 — 건너뜀"); return 0
    captions = [m.get("caption") or "" for m in history]
    lines = {first_line(c) for c in captions}
    for x in queue:
        if already_posted(x, captions, lines):
            print("중복이라 건너뜀:", x["id"], "·", x.get("ko", ""))
    it = next((x for x in queue if not already_posted(x, captions, lines)), None)
    if not it:
        print("큐 소진 — 올릴 편 없음. 새 편 제작 필요"); return 1
    print("게시:", it["id"], "·", it.get("ko", ""))
    c = call("me/media", data={"media_type": "REELS", "video_url": it["video_url"],
                                "caption": it["caption"], "share_to_feed": "true"})
    for _ in range(50):
        s = call(c["id"], fields="status_code")["status_code"]
        if s == "FINISHED": break
        if s == "ERROR": sys.exit("컨테이너 처리 오류")
        time.sleep(6)
    p = call("me/media_publish", data={"creation_id": c["id"]})
    print("완료:", call(p["id"], fields="permalink")["permalink"])
    left = len([x for x in queue if not already_posted(x, captions, lines)]) - 1
    print(f"남은 재고: {left}편")
    return 0


if __name__ == "__main__":
    sys.exit(main())
