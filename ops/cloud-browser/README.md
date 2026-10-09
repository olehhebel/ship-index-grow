# Oleh Cloud Browser

Private browser-automation runtime for the Oleh Hebel project ecosystem.

## Purpose

One persistent browser profile for operational work across:

- Ship Index Grow — https://shipindexgrow.top
- SuperPrompt / Oleh Hebel & Co — https://superprompt.pro
- Interface Report — https://interfacereport.com
- RIDNE — https://ridne.store
- Gmail / Google
- GitHub
- Vercel
- Facebook
- TikTok
- LinkedIn
- Freelancer

The browser runs in a persistent Vercel Sandbox in the `fra1` region. A virtual X11 desktop is exposed through noVNC for one-time logins and human confirmation. Automation uses Microsoft Playwright MCP connected to the same Chrome instance through CDP, so manual login state and automated actions share one profile.

## Open-source base

This setup is intentionally thin and reuses maintained upstream projects instead of reimplementing browser automation:

- `microsoft/playwright-mcp` — browser automation / MCP
- `xtr-dev/mcp-playwright-novnc` — reference architecture for headed Playwright + Xvfb + noVNC
- `noVNC/noVNC` — browser-based VNC client
- `LibVNC/x11vnc` — X11 VNC bridge

The runtime scripts in this directory are project-specific orchestration only.

## Runtime layout

- persistent Chrome profile: `/vercel/browser-profile`
- logs: `/vercel/browser-logs`
- noVNC: port `6080`
- Chrome DevTools Protocol: `127.0.0.1:9222`
- Playwright MCP: `127.0.0.1:3080/mcp`

The MCP port should remain private; only noVNC needs to be temporarily exposed for interactive sign-in.

## Security

Never commit passwords, cookies, passkeys, session state, OAuth tokens, or the browser profile. Set `VNC_PASSWORD` at runtime. The persistent browser profile lives only in the Vercel Sandbox snapshot.

## Bootstrap

```bash
cd ops/cloud-browser
sudo ./bootstrap.sh
VNC_PASSWORD='<temporary-password>' ./start-browser.sh
```

After services are authenticated, snapshot/stop the Vercel Sandbox. Resume it only when automation is needed. This avoids leaving a logged-in browser continuously exposed.

## Update policy

Every Wednesday at 08:00 Europe/Kyiv, review upstream browser-automation projects and Vercel Sandbox changes. Update only when the replacement is materially safer, more reliable, or more capable. Preserve browser-profile compatibility and verify noVNC, CDP, and MCP before adopting changes.
