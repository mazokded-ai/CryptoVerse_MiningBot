import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
    BotCommand
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv(
    "WEBAPP_URL",
    "https://cryptoverse-miningbot.onrender.com"
)

if not BOT_TOKEN:
    raise ValueError("Не найден BOT_TOKEN в настройках Render")

bot = Bot(token=BOT_TOKEN)
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
        "⛏️ Здесь ты можешь добывать CV, "
        "получать ежедневные бонусы и улучшать уровень.\n\n"
        "Нажми кнопку ниже, чтобы начать!",
        reply_markup=keyboard
    )


@dp.message()
async def other_messages(message: Message):
    await message.answer(
        "Нажми /start, чтобы открыть CryptoVerse Mining."
    )


async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота")
    ])

    logging.info("CryptoVerse Mining Bot запущен!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
