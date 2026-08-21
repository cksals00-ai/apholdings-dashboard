#!/bin/bash
# A.P Holdings 대시보드 배포 v2 (D-124) — site 폴더 전체 동기화 (index.html + data/*)
SRC="$HOME/Library/CloudStorage/GoogleDrive-cksals00@gmail.com/내 드라이브/AP_HOLDINGS_QUEUE/site"
REPO="$HOME/apdash"; LOG="$REPO/deploy.log"
[ -d "$SRC" ] || exit 0
[ -d "$REPO/.git" ] || exit 0
cd "$REPO" || exit 0
rsync -a --exclude '.git' --exclude 'deploy.log' --exclude 'deploy_dashboard.sh' "$SRC/" "$REPO/"
git add -A
git diff --cached --quiet && exit 0
git -c user.name="AP Holdings" -c user.email="cksals00@gmail.com" commit -m "site update $(date '+%Y-%m-%d %H:%M')" >> "$LOG" 2>&1
git push origin main >> "$LOG" 2>&1 && echo "$(date '+%F %T') pushed" >> "$LOG" || echo "$(date '+%F %T') PUSH FAIL" >> "$LOG"
