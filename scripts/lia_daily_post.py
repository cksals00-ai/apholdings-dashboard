#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""리아 「한국 여행 실전 한글」 하루 한 편 — GitHub Actions 에서 매일 실행.

data/lia_daily_queue.json 의 순서대로, 아직 안 올라간 첫 편을 인스타 릴로 게시한다.
  · 이미 올라갔는지는 최근 게시물 캡션 첫 줄로 판정(상태 파일을 고치지 않음)
  · 최근 6시간 안에 게시물이 있으면 건너뜀(하루 1건 원칙)
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


def main():
    queue = json.load(open(QUEUE, encoding="utf-8"))
    recent = call("me/media", fields="timestamp,caption", limit=40).get("data", [])
    if recent:
        last = datetime.datetime.strptime(recent[0]["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        if (datetime.datetime.now(datetime.timezone.utc) - last).total_seconds() < 6 * 3600:
            print("최근 6시간 안에 게시물 있음 — 오늘은 건너뜀"); return 0
    posted = {first_line(m.get("caption")) for m in recent}
    it = next((x for x in queue if first_line(x["caption"]) not in posted), None)
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
    left = len([x for x in queue if first_line(x["caption"]) not in posted]) - 1
    print(f"남은 재고: {left}편")
    return 0


if __name__ == "__main__":
    sys.exit(main())
