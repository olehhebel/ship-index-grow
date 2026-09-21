const MAX_FIELD = 500;

function clean(value = '') {
  return String(value).trim().slice(0, MAX_FIELD);
}

function escapeHtml(value = '') {
  return clean(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'Method not allowed' });
  }

  const botToken = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;

  if (!botToken || !chatId) {
    console.error('Telegram lead delivery is not configured');
    return res.status(503).json({ ok: false, error: 'Lead delivery is not configured' });
  }

  const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  const name = clean(body.name);
  const email = clean(body.email);
  const website = clean(body.website);

  if (website) {
    return res.status(200).json({ ok: true });
  }

  if (!name || !email || !/^\S+@\S+\.\S+$/.test(email)) {
    return res.status(400).json({ ok: false, error: 'Valid name and email are required' });
  }

  const requestType = clean(body.request_type || 'Ship Index Grow join request');
  const course = clean(body.course || 'Ship Index Grow');
  const price = clean(body.price || '$490');
  const source = clean(body.source || req.headers.referer || 'shipindexgrow.top');
  const submittedAt = new Date().toISOString();

  const text = [
    '🚀 <b>SHIP INDEX GROW — NEW LEAD</b>',
    '',
    `👤 <b>Name:</b> ${escapeHtml(name)}`,
    `✉️ <b>Email:</b> ${escapeHtml(email)}`,
    `🎓 <b>Request:</b> ${escapeHtml(requestType)}`,
    `📦 <b>Course:</b> ${escapeHtml(course)}`,
    `💳 <b>Price:</b> ${escapeHtml(price)}`,
    `🔗 <b>Source:</b> ${escapeHtml(source)}`,
    `🕒 <b>Time:</b> ${escapeHtml(submittedAt)}`
  ].join('\n');

  try {
    const telegramResponse = await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text,
        parse_mode: 'HTML',
        disable_web_page_preview: true
      })
    });

    const telegramResult = await telegramResponse.json();

    if (!telegramResponse.ok || !telegramResult.ok) {
      console.error('Telegram API error', telegramResult);
      return res.status(502).json({ ok: false, error: 'Telegram delivery failed' });
    }

    return res.status(200).json({ ok: true });
  } catch (error) {
    console.error('Lead delivery error', error);
    return res.status(500).json({ ok: false, error: 'Lead delivery failed' });
  }
}
