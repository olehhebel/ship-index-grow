# Oleh Vercel Cloud Browser

A zero-extra-subscription browser automation setup for Vercel Sandbox.

## Stack

- Vercel Sandbox (persistent named sandbox)
- Chromium / Chrome for Testing
- Xvfb + Fluxbox
- x11vnc + noVNC for a visible browser in the web
- Microsoft Playwright MCP for agent/browser control
- Persistent Chrome user data stored inside the sandbox filesystem snapshot

The implementation is adapted from the architecture used by:
- Microsoft Playwright MCP — Apache-2.0
- xtr-dev/mcp-playwright-novnc — MIT

## Runtime endpoints

The sandbox publishes two ports:
- 6080 — noVNC browser UI
- 3080 — Playwright MCP HTTP endpoint

The browser opens the four project tabs on startup:
- https://shipindexgrow.top
- https://interfacereport.com
- https://superprompt.pro
- https://ridne.store

## Provisioning

On a fresh Ubuntu-based Vercel Sandbox:

```bash
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
  xvfb x11vnc novnc websockify fluxbox dbus-x11

npx -y @puppeteer/browsers install chrome@stable --path /vercel/.cache/chrome
```

Copy `start-browser.sh` to `/vercel/start-browser.sh`, make it executable and run it.

The named sandbox must publish ports 6080 and 3080 at creation time.

## Persistence

Use a persistent named Vercel Sandbox and snapshot its filesystem. The Chrome profile lives at:

```
/vercel/browser-profile
```

This preserves cookies and local browser state across sandbox snapshots/resumes.

## Security

The VNC connection is password protected. Do not commit passwords, TikTok credentials, passkeys, cookies or browser profile data to Git.
