#!/bin/bash
SRC="$HOME/Library/CloudStorage/GoogleDrive-cksals00@gmail.com/내 드라이브/AP_HOLDINGS_QUEUE/site/index.html"
REPO="$HOME/apdash"
LOG="$REPO/deploy.log"
[ -f "$SRC" ] || exit 0
[ -d "$REPO/.git" ] || exit 0
cd "$REPO" || exit 0
cmp -s "$SRC" index.html && exit 0
cp "$SRC" index.html
git add index.html
git -c user.name="AP Holdings" -c user.email="cksals00@gmail.com" commit -m "dashboard update $(date '+%Y-%m-%d %H:%M')" >> "$LOG" 2>&1
git push origin main >> "$LOG" 2>&1 && echo "$(date '+%F %T') pushed" >> "$LOG" || echo "$(date '+%F %T') PUSH FAIL" >> "$LOG"
