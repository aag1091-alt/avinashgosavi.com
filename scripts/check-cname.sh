#!/usr/bin/env bash
# Check CNAME for www.avinashgosavi.com until it points to aag1091-alt.github.io
# Usage: ./scripts/check-cname.sh
# Run in background: nohup ./scripts/check-cname.sh > cname-check.log 2>&1 &

TARGET="aag1091-alt.github.io"
DOMAIN="www.avinashgosavi.com"
INTERVAL=60
MAX_ATTEMPTS=60   # 60 * 60 sec = 1 hour max

attempt=0
while [ $attempt -lt $MAX_ATTEMPTS ]; do
  attempt=$((attempt + 1))
  result=$(dig "$DOMAIN" CNAME +short 2>/dev/null | head -1)
  now=$(date '+%Y-%m-%d %H:%M:%S')
  if echo "$result" | grep -q "$TARGET"; then
    echo "[$now] CNAME updated! $DOMAIN -> $result"
    exit 0
  fi
  echo "[$now] Attempt $attempt: still $result (waiting ${INTERVAL}s)"
  sleep $INTERVAL
done
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Stopped after $MAX_ATTEMPTS attempts (1 hour)"
exit 1
