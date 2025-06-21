from aiogram import types, Router, F, Bot
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, MenuButtonWebApp, MenuButtonDefault
from aiogram.filters import Command
from bot.config import WEBAPP_URL
import logging

router = Router()

# Menu buttonni sozlash funksiyasi
async def setup_bot_menu(bot: Bot):
    """Bot menu buttonni sozlash"""
    try:
        # URL ni tekshirish
        if not WEBAPP_URL or not WEBAPP_URL.startswith('https://'):
            print(f"❌ URL noto'g'ri: {WEBAPP_URL}")
            return False
            
        # Menu buttonni o'rnatish
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="🚀 Mini App",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        )
        print(f"✅ Bot menu button muvaffaqiyatli o'rnatildi: {WEBAPP_URL}")
        return True
    except Exception as e:
        print(f"❌ Menu button o'rnatishda xatolik: {e}")
        # Agar xatolik bo'lsa, default menuni o'rnatish
        try:
            await bot.set_chat_menu_button(menu_button=MenuButtonDefault())
            print("⚠️ Default menu button o'rnatildi")
        except Exception as e2:
            print(f"❌ Default menu ham ishlamadi: {e2}")
        return False

@router.message(Command("start"))
async def start_command(message: types.Message):
    # Menu buttonni har start da yangilash
    menu_success = False
    try:
        menu_success = await setup_bot_menu(message.bot)
    except Exception as e:
        logging.error(f"Menu button sozlashda xatolik: {e}")
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Hello World App ochish",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Yordam",
                    callback_data="help"
                )
            ]
        ]
    )

    # Menu button holati bo'yicha xabar
    menu_status = "💡 <i>Shuningdek, pastdagi menu tugmasidan ham foydalanishingiz mumkin!</i>" if menu_success else "⚠️ <i>Menu button hozircha ishlamayapti, inline tugmadan foydalaning.</i>"

    await message.answer(
        f"Salom {message.from_user.first_name}! 👋\n\n"
        "Bu Hello World Mini App boti.\n"
        "Quyidagi tugma orqali mini appni oching:\n\n"
        f"{menu_status}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.callback_query(F.data == "help")
async def help_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📱 <b>Mini App haqida:</b>\n\n"
        "• Bu oddiy Hello World dasturi\n"
        "• Django bilan yaratilgan\n"
        "• Telegram Web App texnologiyasi ishlatilgan\n\n"
        "Mini appni ochish uchun tugmani bosing! 👇\n\n"
        "💡 <i>Agar menu button ishlamasa, inline tugmadan foydalaning.</i>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🚀 Mini App ochish",
                        web_app=WebAppInfo(url=WEBAPP_URL)
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔙 Orqaga",
                        callback_data="back_to_start"
                    )
                ]
            ]
        )
    )


@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Hello World App ochish",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Yordam",
                    callback_data="help"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        f"Salom {callback.from_user.first_name}! 👋\n\n"
        "Bu Hello World Mini App boti.\n"
        "Quyidagi tugma orqali mini appni oching:\n\n"
        "💡 <i>Inline tugma ishonchli ishlaydi!</i>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


# Debug buyrug'i qo'shish
@router.message(Command("debug"))
async def debug_command(message: types.Message):
    debug_info = f"""
🔍 <b>Debug Ma'lumotlari:</b>

📱 <b>Bot ID:</b> {message.bot.id}
🌐 <b>WEBAPP_URL:</b> <code>{WEBAPP_URL}</code>
✅ <b>URL Format:</b> {'To\'g\'ri' if WEBAPP_URL.startswith('https://') else 'Noto\'g\'ri - https:// kerak'}
🔗 <b>URL Uzunligi:</b> {len(WEBAPP_URL)}

<b>Holat:</b>
• Inline button: ✅ Ishlaydi
• Menu button: ❓ Test qilib ko'ring

<b>Agar menu button ishlamasa:</b>
1. Ngrok yangi URL berganmi?
2. Config.py yangilangami?
3. Bot qayta ishga tushirilganmi?
    """
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🧪 Test Mini App",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Menu Button yangilash",
                    callback_data="refresh_menu"
                )
            ]
        ]
    )
    
    await message.answer(debug_info, parse_mode="HTML", reply_markup=keyboard)


@router.callback_query(F.data == "refresh_menu")
async def refresh_menu_callback(callback: types.CallbackQuery):
    """Menu buttonni qayta sozlash"""
    success = await setup_bot_menu(callback.bot)
    
    status = "✅ Menu button muvaffaqiyatli yangilandi!" if success else "❌ Menu button yangilanmadi. URL ni tekshiring."
    
    await callback.answer(status, show_alert=True)


@router.message()
async def echo_handler(message: types.Message):
    if "mini app" in message.text.lower() or "ochish" in message.text.lower():
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🚀 Hello World App ochish",
                        web_app=WebAppInfo(url=WEBAPP_URL)
                    )
                ]
            ]
        )
        await message.answer(
            "Mini appni ochish uchun quyidagi tugmani bosing:\n\n"
            "💡 <i>Inline tugma ishonchli ishlaydi!</i>",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "Mini appni ishlatish uchun /start buyrug'ini yuboring! 🚀\n\n"
            "🔧 <i>Debug uchun /debug buyrug'ini yuboring</i>",
            parse_mode="HTML"
        )

# Bot startup event handler (main.py da ishlatish uchun)
async def on_startup(bot: Bot):
    """Botni ishga tushirishda menu buttonni sozlash"""
    success = await setup_bot_menu(bot)
    if success:
        print("🤖 Bot ishga tushdi va menu button sozlandi!")
    else:
        print("🤖 Bot ishga tushdi, lekin menu button sozlanmadi!")
        print(f"🔗 Hozirgi WEBAPP_URL: {WEBAPP_URL}")
        print("❗ Ngrok URL ni tekshiring va config.py ni yangilang!")