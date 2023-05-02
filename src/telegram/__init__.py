from pyrogram import Client
from config import telegram


telegram_vars = telegram()
app = Client(
    "secretchessclub_bot",
    api_id=telegram_vars[0],
    api_hash=telegram_vars[1],
    bot_token=telegram_vars[2],
)

# app.run()
