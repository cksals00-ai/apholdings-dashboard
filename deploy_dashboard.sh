#!/bin/bash
# A.P Holdings 배포 v3 (D-125) — 공개 사이트/내부 대시보드 분리
#  site/     → apholdings-dashboard (공개: 문샷 랜딩·privacy·data)
#  site_ops/ → ap-ops-7k2m9x       (내부: 대표 계좌 대시보드, PIN 게이트)
BASE="$HOME/Library/CloudStorage/GoogleDrive-cksals00@gmail.com/내 드라이브/AP_HOLDINGS_QUEUE"
PUB_SRC="$BASE/site";      PUB_REPO="$HOME/apdash"
OPS_SRC="$BASE/site_ops";  OPS_REPO="$HOME/apops"
LOG="$PUB_REPO/deploy.log"

sync_repo() {
  local SRC="$1" REPO="$2"
  [ -d "$SRC" ] || return 0
  [ -d "$REPO/.git" ] || return 0
  cd "$REPO" || return 0
  rsync -a --exclude '.git' --exclude 'deploy.log' --exclude 'deploy_dashboard.sh' "$SRC/" "$REPO/"
  git pull --rebase -X theirs origin main >/dev/null 2>&1 || true
  git add -A
  git diff --cached --quiet && return 0
  git -c user.name="AP Holdings" -c user.email="cksals00@gmail.com" commit -m "update $(date '+%Y-%m-%d %H:%M')" >> "$LOG" 2>&1
  git push origin main >> "$LOG" 2>&1 && echo "$(date '+%F %T') pushed $(basename "$REPO")" >> "$LOG" || echo "$(date '+%F %T') PUSH FAIL $(basename "$REPO")" >> "$LOG"
}

# 내부 저장소가 없으면 공개 저장소의 인증 URL을 재사용해 자동 클론
if [ ! -d "$OPS_REPO/.git" ] && [ -d "$PUB_REPO/.git" ]; then
  URL=$(git -C "$PUB_REPO" remote get-url origin)
  OPS_URL="${URL/apholdings-dashboard/ap-ops-7k2m9x}"
  git clone "$OPS_URL" "$OPS_REPO" >> "$LOG" 2>&1
fi

sync_repo "$PUB_SRC" "$PUB_REPO"
sync_repo "$OPS_SRC" "$OPS_REPO"
