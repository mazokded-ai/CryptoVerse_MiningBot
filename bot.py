import os, asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
TOKEN=os.getenv("BOT_TOKEN")
WEBAPP_URL=os.getenv("WEBAPP_URL","https://example.com")
if not TOKEN: raise RuntimeError("Set BOT_TOKEN environment variable")
bot=Bot(TOKEN); dp=Dispatcher()
@dp.message(CommandStart())
async def start(message: Message):
    kb=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⛏ Открыть CryptoVerse",web_app=WebAppInfo(url=WEBAPP_URL))]],resize_keyboard=True)
    await message.answer("Добро пожаловать в CryptoVerse! Это игровая симуляция виртуального майнинга CV.",reply_markup=kb)
async def main(): await dp.start_polling(bot)
if __name__=="__main__": asyncio.run(main())
