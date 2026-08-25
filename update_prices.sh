#!/bin/bash
# A.P Holdings — prices.json 일일 자동 갱신 + 게시 검증 (D-144)
# 설치: cp "$D/update_prices.sh" ~/apdash/update_prices.sh && chmod +x ~/apdash/update_prices.sh
# cron: 0 16 * * 1-5 /bin/bash $HOME/apdash/update_prices.sh >> $HOME/apdash/prices.log 2>&1

set -uo pipefail
REPO="$HOME/apdash"
URL="https://cksals00-ai.github.io/apholdings-dashboard/data/prices.json"
DRIVE="$HOME/Library/CloudStorage/GoogleDrive-cksals00@gmail.com/내 드라이브/AP_HOLDINGS_QUEUE/reports"
TODAY=$(date +%Y-%m-%d)
STAMP=$(date +%Y%m%d-%H%M)
RPT="$DRIVE/PRICES-$STAMP.md"
FAIL=""

log(){ echo "[$(date '+%F %T')] $*"; }

log "=== prices 갱신 시작 ==="
cd "$REPO" || { FAIL="레포 없음: $REPO"; }

# 1) 생성
if [ -z "$FAIL" ]; then
  python3 "$REPO/gen_prices_v2.py" "$REPO" || FAIL="생성 실패"
fi

# 2) 스파크 포함 여부 검사 — 빠지면 게시하지 않는다
if [ -z "$FAIL" ]; then
  SPARK=$(python3 -c "
import json;d=json.load(open('$REPO/data/prices.json'))
print(sum('s' in s for s in d['stocks']))
" 2>/dev/null || echo 0)
  ASOF=$(python3 -c "
import json;print(json.load(open('$REPO/data/prices.json'))['asof'])
" 2>/dev/null || echo "?")
  log "생성 완료 — asof=$ASOF spark=$SPARK"
  [ "${SPARK:-0}" -lt 200 ] && FAIL="스파크 부족($SPARK) — 게시 중단"
fi

# 3) 푸시
if [ -z "$FAIL" ]; then
  git add data/prices.json
  if git diff --cached --quiet; then
    log "변경 없음 — 커밋 생략"
  else
    git commit -m "prices: $ASOF (spark $SPARK)" && git push || FAIL="푸시 실패"
  fi
fi

# 4) 게시 검증 — 푸시 성공 != 게시 완료 (D-130)
LIVE_ASOF=""
if [ -z "$FAIL" ]; then
  for i in 1 2 3 4 5 6; do
    sleep 30
    BODY=$(curl -s --max-time 20 "$URL" | head -c 200)
    LIVE_ASOF=$(echo "$BODY" | sed -n 's/.*"asof":"\([0-9-]*\)".*/\1/p')
    log "검증 $i회차 — live asof=$LIVE_ASOF (기대 $ASOF)"
    [ "$LIVE_ASOF" = "$ASOF" ] && break
  done
  [ "$LIVE_ASOF" != "$ASOF" ] && FAIL="게시 미반영 (live=$LIVE_ASOF, 기대=$ASOF)"
fi

# 5) 결과를 드라이브에 기록 — 클라우드 세션이 이 파일로 성공/실패를 감시한다
mkdir -p "$DRIVE"
{
  echo "# prices.json 갱신 보고"
  echo
  echo "run_at: $(date '+%F %T %Z')"
  echo "asof: ${ASOF:-?}"
  echo "spark: ${SPARK:-0}"
  echo "live_asof: ${LIVE_ASOF:-?}"
  echo "url: $URL"
  if [ -z "$FAIL" ]; then
    echo "status: OK"
    echo
    echo "게시 확인됨. asof가 live와 일치한다."
  else
    echo "status: FAIL"
    echo "reason: $FAIL"
    echo
    echo "조치 필요. ~/apdash/prices.log 확인."
  fi
} > "$RPT"
log "보고 기록: $RPT"

if [ -n "$FAIL" ]; then
  log "!! 실패: $FAIL"
  command -v osascript >/dev/null && osascript -e "display notification \"prices.json 갱신 실패: $FAIL\" with title \"A.P Holdings\"" || true
  exit 1
fi
log "=== 완료 (asof $ASOF · spark $SPARK · 게시 확인) ==="
