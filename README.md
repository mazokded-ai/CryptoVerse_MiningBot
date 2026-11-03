# CryptoVerse MiningBot — MVP
Учебная игра с виртуальными CV (не настоящая криптовалюта, выплаты не реализованы).

## Render deployment
Создайте GitHub repository и загрузите проект.
Для Render можно создать два Web Services:
- API: Build `pip install -r requirements.txt`; Start `uvicorn api:app --host 0.0.0.0 --port $PORT`
- Bot: Build `pip install -r requirements.txt`; Start `python bot.py`
У бота задайте environment variable `BOT_TOKEN`, а также `WEBAPP_URL` (HTTPS URL опубликованного web интерфейса).
Telegram Mini App должен быть доступен через HTTPS. Настройте URL через BotFather → /mybots → Bot Settings → Menu Button.
Примечание: Render free web services могут засыпать, а ephemeral filesystem не подходит для надёжного постоянного SQLite-хранения.
