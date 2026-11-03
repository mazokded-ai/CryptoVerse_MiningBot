import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://cryptoverse-miningbot.onrender.com")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в Render")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="⛏️ Открыть CryptoVerse Mining",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🚀 Добро пожаловать в CryptoVerse Mining!\n\n"
        "Нажми кнопку ниже, чтобы открыть игру.",
        reply_markup=keyboard
    )


@dp.message()
async def other_messages(message: Message):
    await message.answer("Напиши /start, чтобы запустить бота.")


async def main():
    logging.info("Бот запускается...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
