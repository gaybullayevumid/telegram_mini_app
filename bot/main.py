import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.handlers import router, on_startup
from bot.config import BOT_TOKEN

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    # Bot va Dispatcher yaratish
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Router qo'shish
    dp.include_router(router)
    
    # Startup da menu button sozlash
    await on_startup(bot)
    
    print("🚀 Bot ishga tushmoqda...")
    
    try:
        # Botni ishga tushirish
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Bot ishga tushirishda xatolik: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())