#!/usr/bin/env bash
set -euo pipefail

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  xvfb \
  x11vnc \
  novnc \
  websockify \
  fluxbox \
  dbus-x11 \
  curl

npm install
npx playwright install chromium
npx playwright install-deps chromium

mkdir -p /vercel/browser-profile /vercel/browser-logs /vercel/browser-output /vercel/.vnc
chmod 700 /vercel/browser-profile /vercel/.vnc

echo "Cloud-browser dependencies installed."
