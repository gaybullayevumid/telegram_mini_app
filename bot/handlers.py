from aiogram import types, Router, F
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from bot.config import WEBAPP_URL

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
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

    await message.answer(
        f"Salom {message.from_user.first_name}! 👋\n\n"
        "Bu Hello World Mini App boti.\n"
        "Quyidagi tugma orqali mini appni oching:",
        reply_markup=keyboard
    )


@router.callback_query(F.data == "help")
async def help_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📱 <b>Mini App haqida:</b>\n\n"
        "• Bu oddiy Hello World dasturi\n"
        "• Django bilan yaratilgan\n"
        "• Telegram Web App texnologiyasi ishlatilgan\n\n"
        "Mini appni ochish uchun tugmani bosing! 👇",
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
        "Quyidagi tugma orqali mini appni oching:",
        reply_markup=keyboard
    )


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
            "Mini appni ochish uchun quyidagi tugmani bosing:",
            reply_markup=keyboard
        )
    else:
        await message.answer(
            "Mini appni ishlatish uchun /start buyrug'ini yuboring! 🚀"
        )
