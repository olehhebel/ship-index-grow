// Ship Index Grow: free relay from the site's join form to Telegram.
// Runs as a Google Apps Script web app so the bot token stays hidden
// (GitHub Pages serves static files only and cannot keep secrets).
// Setup steps: see README.md in this folder.

var MAX_FIELD = 500;

function clean(value) {
  return String(value == null ? '' : value).trim().slice(0, MAX_FIELD);
}

function escapeHtml(value) {
  return clean(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function reply(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  var props = PropertiesService.getScriptProperties();
  var botToken = props.getProperty('TELEGRAM_BOT_TOKEN');
  var chatId = props.getProperty('TELEGRAM_CHAT_ID');
  if (!botToken || !chatId) return reply({ ok: false, error: 'Lead delivery is not configured' });

  var body;
  try {
    body = JSON.parse((e && e.postData && e.postData.contents) || '{}');
  } catch (err) {
    return reply({ ok: false, error: 'Invalid JSON' });
  }

  var name = clean(body.name);
  var email = clean(body.email);
  if (clean(body._honey)) return reply({ ok: true });
  if (!name || !/^\S+@\S+\.\S+$/.test(email)) {
    return reply({ ok: false, error: 'Valid name and email are required' });
  }

  var text = [
    '🚀 <b>SHIP INDEX GROW — NEW LEAD</b>',
    '',
    '👤 <b>Name:</b> ' + escapeHtml(name),
    '✉️ <b>Email:</b> ' + escapeHtml(email),
    '📦 <b>Course:</b> ' + escapeHtml(body.course || 'Ship Index Grow'),
    '💳 <b>Price:</b> ' + escapeHtml(body.price || '—'),
    '🌐 <b>Language:</b> ' + escapeHtml(body.language || '—'),
    '🔗 <b>Source:</b> ' + escapeHtml(body._url || '—'),
    '🕒 <b>Time:</b> ' + new Date().toISOString()
  ].join('\n');

  var response = UrlFetchApp.fetch('https://api.telegram.org/bot' + botToken + '/sendMessage', {
    method: 'post',
    contentType: 'application/json',
    muteHttpExceptions: true,
    payload: JSON.stringify({ chat_id: chatId, text: text, parse_mode: 'HTML', disable_web_page_preview: true })
  });
  if (response.getResponseCode() !== 200) {
    console.error('Telegram API error', response.getContentText());
    return reply({ ok: false, error: 'Telegram delivery failed' });
  }
  return reply({ ok: true });
}

// Run once from the editor to check the setup: a test lead should arrive in Telegram.
function testLead() {
  var result = doPost({ postData: { contents: JSON.stringify({ name: 'Test', email: 'test@example.com', language: 'test' }) } });
  console.log(result.getContent());
}
