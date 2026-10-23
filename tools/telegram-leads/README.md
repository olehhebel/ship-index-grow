# Заявки с сайта в Telegram (бесплатно)

Сайт на GitHub Pages — это только статичные файлы, спрятать там ключ бота нельзя.
Поэтому заявку принимает маленький скрипт в твоём Google-аккаунте (Google Apps Script),
он и отправляет её в Telegram. Бесплатно, карта не нужна.
Если скрипт не ответит, сайт сам отправит заявку на почту через formsubmit.co, как раньше.

## 1. Бот в Telegram

1. Открой [@BotFather](https://t.me/BotFather), отправь `/newbot`, придумай имя.
   BotFather пришлёт **токен** вида `123456789:AA...`. Никому его не показывай.
2. Открой своего нового бота и нажми **Start** (без этого бот не сможет тебе писать).
3. Открой [@userinfobot](https://t.me/userinfobot) и нажми **Start**. Он пришлёт твой **Id** (число).

## 2. Скрипт в Google

1. Зайди на [script.google.com](https://script.google.com) → **New project**.
2. Удали всё в окне кода и вставь содержимое файла `Code.gs` из этой папки. Нажми 💾.
3. Слева ⚙️ **Project Settings** → внизу **Script Properties** → **Add script property**, добавь две:
   - `TELEGRAM_BOT_TOKEN` = токен от BotFather
   - `TELEGRAM_CHAT_ID` = твой Id от userinfobot
4. Вернись в редактор, вверху выбери функцию `testLead` → **Run**. Google попросит разрешения — разреши
   (на экране «Google hasn't verified this app» нажми **Advanced** → **Go to … (unsafe)**: это твой собственный скрипт).
   В Telegram должна прийти тестовая заявка.
5. Справа вверху **Deploy** → **New deployment** → ⚙️ **Web app**:
   - **Execute as:** Me
   - **Who has access:** Anyone
   
   → **Deploy**. Скопируй **Web app URL** (заканчивается на `/exec`).

## 3. Подключить к сайту

Вставь этот URL в `app.js` в строку `const TELEGRAM_RELAY_URL='';` (между кавычками)
или просто пришли его Claude — он сам вставит. Этот адрес не секретный.
