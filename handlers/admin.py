from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMIN_ID
from utils import admin_keyboard, main_keyboard
from services import database

router = Router()

@router.message(Command("admin"))
async def admin_panel(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer("👑 Панель администратора", reply_markup=admin_keyboard())

@router.message(F.text == "📊 Статистика")
async def admin_stats(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    
    data = database.load_users()
    total = len(data)
    processed = sum(u['total'] for u in data.values())
    
    await msg.answer(
        f"👥 Пользователей: {total}\n"
        f"📊 Обработок: {processed}"
    )

@router.message(F.text == "👥 Пользователи")
async def admin_users(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    
    data = database.load_users()
    if not data:
        await msg.answer("📭 Нет пользователей")
        return
    
    text = "👥 Последние:\n"
    for i, (uid, u) in enumerate(list(data.items())[-5:], 1):
        text += f"{i}. ID: {uid} ({u['total']})\n"
    
    await msg.answer(text)

@router.message(F.text == "🔙 В меню")
async def admin_back(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer("🔙 Главное меню", reply_markup=main_keyboard())