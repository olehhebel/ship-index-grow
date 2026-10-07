#!/usr/bin/env bash
set -euo pipefail

export DISPLAY=:99
export HOME=/vercel

PROFILE_DIR="/vercel/browser-profile"
LOG_DIR="/vercel/browser-logs"
VNC_DIR="/vercel/.vnc"

CHROME="${CHROME_PATH:-$(find /vercel/.cache/chrome -type f -path '*/chrome-linux64/chrome' | sort | tail -1)}"

if [ -z "$CHROME" ] || [ ! -x "$CHROME" ]; then
  echo "Chrome not found. Install it with:"
  echo "npx -y @puppeteer/browsers install chrome@stable --path /vercel/.cache/chrome"
  exit 1
fi

mkdir -p "$PROFILE_DIR" "$LOG_DIR" "$VNC_DIR"

pkill -f "playwright-mcp" >/dev/null 2>&1 || true
pkill -f "chrome.*browser-profile" >/dev/null 2>&1 || true
pkill -f "websockify.*6080" >/dev/null 2>&1 || true
pkill -f "x11vnc.*:99" >/dev/null 2>&1 || true
pkill -f "Xvfb :99" >/dev/null 2>&1 || true
sleep 1

# Snapshots can preserve Chromium's stale singleton lock.
rm -f "$PROFILE_DIR"/SingletonLock "$PROFILE_DIR"/SingletonSocket "$PROFILE_DIR"/SingletonCookie 2>/dev/null || true

if [ ! -f "$VNC_DIR/passwd" ]; then
  : "${VNC_PASSWORD:?Set VNC_PASSWORD for the first run}"
  x11vnc -storepasswd "$VNC_PASSWORD" "$VNC_DIR/passwd" >/dev/null
fi

nohup Xvfb :99 -screen 0 1440x900x24 -ac +extension RANDR >"$LOG_DIR/xvfb.log" 2>&1 &
sleep 1
nohup fluxbox -display :99 >"$LOG_DIR/fluxbox.log" 2>&1 &
sleep 1
nohup x11vnc -display :99 -forever -shared -rfbauth "$VNC_DIR/passwd" -rfbport 5900 -o "$LOG_DIR/x11vnc.log" >/dev/null 2>&1 &
nohup websockify --web /usr/share/novnc 6080 localhost:5900 >"$LOG_DIR/novnc.log" 2>&1 &

nohup "$CHROME" \
  --no-sandbox \
  --disable-dev-shm-usage \
  --remote-debugging-port=9222 \
  --remote-debugging-address=127.0.0.1 \
  --user-data-dir="$PROFILE_DIR" \
  --window-size=1440,900 \
  --no-first-run \
  --no-default-browser-check \
  "https://shipindexgrow.top" \
  "https://interfacereport.com" \
  "https://superprompt.pro" \
  "https://ridne.store" \
  >"$LOG_DIR/chrome.log" 2>&1 &

for _ in $(seq 1 30); do
  curl -fsS http://127.0.0.1:9222/json/version >/dev/null 2>&1 && break
  sleep 1
done

nohup npx -y @playwright/mcp@0.0.83 \
  --port 3080 \
  --host 0.0.0.0 \
  --cdp-endpoint "http://127.0.0.1:9222" \
  --allowed-hosts=* \
  >"$LOG_DIR/mcp.log" 2>&1 &

sleep 3

echo "Browser stack started"
echo "noVNC: :6080/vnc.html"
echo "MCP:   :3080/mcp"
