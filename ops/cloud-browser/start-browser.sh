#!/usr/bin/env bash
set -euo pipefail

export DISPLAY=:99
export HOME=/vercel

PROFILE_DIR="${PROFILE_DIR:-/vercel/browser-profile}"
LOG_DIR="${LOG_DIR:-/vercel/browser-logs}"
OUTPUT_DIR="${OUTPUT_DIR:-/vercel/browser-output}"
VNC_DIR="${VNC_DIR:-/vercel/.vnc}"

if [[ -z "${VNC_PASSWORD:-}" ]]; then
  echo "VNC_PASSWORD is required." >&2
  exit 1
fi

CHROME="${CHROME:-${CHROME_PATH:-}}"
if [[ -z "$CHROME" ]]; then
  CHROME="$(find /vercel/.cache/chrome/chrome /vercel/.cache/ms-playwright -type f -path '*/chrome-linux64/chrome' 2>/dev/null | sort | tail -1 || true)"
fi
if [[ -z "$CHROME" || ! -x "$CHROME" ]]; then
  echo "No executable Chromium/Chrome found. Run bootstrap.sh first." >&2
  exit 1
fi

mkdir -p "$PROFILE_DIR" "$LOG_DIR" "$OUTPUT_DIR" "$VNC_DIR"
chmod 700 "$PROFILE_DIR" "$VNC_DIR"

pkill -f "Xvfb :99" >/dev/null 2>&1 || true
pkill -f "x11vnc.*:99" >/dev/null 2>&1 || true
pkill -f "websockify.*6080" >/dev/null 2>&1 || true
pkill -f "playwright-mcp" >/dev/null 2>&1 || true
pkill -f "remote-debugging-port=9222" >/dev/null 2>&1 || true
rm -f "$PROFILE_DIR/SingletonLock" "$PROFILE_DIR/SingletonCookie" "$PROFILE_DIR/SingletonSocket" "$PROFILE_DIR/DevToolsActivePort"
sleep 1

x11vnc -storepasswd "$VNC_PASSWORD" "$VNC_DIR/passwd" >/dev/null
chmod 600 "$VNC_DIR/passwd"

nohup Xvfb :99 -screen 0 1440x900x24 -ac +extension RANDR >"$LOG_DIR/xvfb.log" 2>&1 &
sleep 1
nohup fluxbox -display :99 >"$LOG_DIR/fluxbox.log" 2>&1 &
sleep 1
nohup x11vnc -display :99 -forever -shared -rfbauth "$VNC_DIR/passwd" -rfbport 5900 -noxdamage >"$LOG_DIR/x11vnc.log" 2>&1 &
nohup websockify --web /usr/share/novnc 6080 localhost:5900 >"$LOG_DIR/novnc.log" 2>&1 &

nohup "$CHROME" \
  --no-sandbox \
  --disable-dev-shm-usage \
  --no-first-run \
  --no-default-browser-check \
  --password-store=basic \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --user-data-dir="$PROFILE_DIR" \
  --window-size=1440,900 \
  --start-maximized \
  "https://accounts.google.com/" \
  "https://github.com/" \
  "https://vercel.com/dashboard" \
  "https://www.facebook.com/" \
  "https://www.tiktok.com/" \
  "https://www.linkedin.com/" \
  "https://www.freelancer.com/" \
  "https://shipindexgrow.top/" \
  "https://superprompt.pro/" \
  "https://interfacereport.com/" \
  "https://ridne.store/" \
  >"$LOG_DIR/chromium.log" 2>&1 &

for _ in $(seq 1 45); do
  curl -fsS http://127.0.0.1:9222/json/version >/dev/null 2>&1 && break
  sleep 1
done

nohup npx -y @playwright/mcp@0.0.83 \
  --port 3080 \
  --host 127.0.0.1 \
  --cdp-endpoint http://127.0.0.1:9222 \
  --shared-browser-context \
  --viewport-size 1440x900 \
  --no-sandbox \
  --output-dir "$OUTPUT_DIR" \
  >"$LOG_DIR/mcp.log" 2>&1 &

sleep 3
curl -fsS http://127.0.0.1:9222/json/version >/dev/null

echo "Oleh Cloud Browser is running."
echo "noVNC local port: 6080"
echo "Playwright MCP local endpoint: http://127.0.0.1:3080/mcp"
