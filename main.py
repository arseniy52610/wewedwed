import os
import asyncio
from pathlib import Path
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)

TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
APP_URL = os.getenv("APP_URL", "").rstrip("/")
PORT = int(os.getenv("PORT", "8080"))

bot = Bot(token=TOKEN) if TOKEN else None
dp = Dispatcher()

BASE_DIR = Path(__file__).resolve().parent


@dp.message(CommandStart())
async def start(message: Message):
    if not APP_URL:
        await message.answer(
            "Приложение ещё настраивается. Попробуй немного позже."
        )
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть BynexVPN",
                    web_app=WebAppInfo(url=APP_URL),
                )
            ]
        ]
    )

    await message.answer(
        "Нажми кнопку, чтобы открыть BynexVPN:",
        reply_markup=keyboard,
    )


async def index(request):
    file_path = BASE_DIR / "index.html"

    if not file_path.exists():
        return web.Response(text="index.html не найден", status=404)

    return web.FileResponse(file_path)


async def health(request):
    return web.Response(text="BynexVPN Mini App работает")


async def main():
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    if bot:
        await dp.start_polling(bot)
    else:
        print("Не задан BOT_TOKEN: веб-сервер работает, бот не запущен.")
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
