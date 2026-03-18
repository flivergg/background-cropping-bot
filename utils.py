import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎯 Удалить фон"), KeyboardButton(text="🎨 Изменить фон")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="🆘 Помощь")]
        ],
        resize_keyboard=True
    )

def bg_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚪ Белый"), KeyboardButton(text="⚫ Черный")],
            [KeyboardButton(text="📸 Свое фото"), KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )

def admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="👥 Пользователи")],
            [KeyboardButton(text="🔙 В меню")]
        ],
        resize_keyboard=True
    )

async def show_progress(message, steps):
    msg = await message.answer("🔄 Обработка...")
    for text, percent in steps:
        bar = "█" * (percent//10) + "░" * (10 - percent//10)
        await msg.edit_text(f"🔄 {text} [{bar}] {percent}%")
        await asyncio.sleep(0.5)
    await msg.delete()