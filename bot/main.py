import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.handlers import router

async def main():
    # Bot va Dispatcher yaratish
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Router qo'shish
    dp.include_router(router)
    
    try:
        # Webhook o'chirish (agar oldin ishlatilgan bo'lsa)
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Polling boshlash
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())