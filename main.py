import asyncio
import logging
from config import TOKEN
from aiogram import Bot, Dispatcher

from app.database.init import init_db

from app.handlers.start_handlers import router as start_router
from app.handlers.leave_bid_handlers import router as leave_request_router
from app.handlers.call_handlers import router as call_router
from app.handlers.settings_handlers import router as settings_router
from app.handlers.contact_handlers import router as contact_router
from app.handlers.admin_handlers import router as admin_router

async def on_startup(dp: Dispatcher):
    await init_db()

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    await on_startup(dp)

    dp.include_routers(admin_router, start_router, leave_request_router, call_router, settings_router, contact_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())