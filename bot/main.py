import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.handlers import router

# Logging sozlash
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Bot ishga tushmoqda...")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    # webhook bo‘lsa, tozalab yuboramiz
    await bot.delete_webhook(drop_pending_updates=True)

    # polling orqali ishlatamiz
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to‘xtatildi")
    except Exception as e:
        logger.error(f"Xatolik: {e}")
