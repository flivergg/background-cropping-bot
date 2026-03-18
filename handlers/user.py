from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import ADMIN_ID
from utils import main_keyboard, bg_keyboard, show_progress
from services import database, image

router = Router()
sessions = {}  

@router.message(Command("start"))
async def start(msg: Message):
    await msg.answer(
        "✨ <b>AI Фоторедактор</b>\n\n"
        "🎯 Удаляю фон с любых фото\n"
        "🎨 Меняю фон на любой цвет",
        parse_mode='HTML',
        reply_markup=main_keyboard()
    )

@router.message(F.text == "🎯 Удалить фон")
async def remove_start(msg: Message):
    await msg.answer("📸 Отправьте фото", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Отмена")]], resize_keyboard=True
    ))

@router.message(F.text == "🎨 Изменить фон")
async def change_start(msg: Message):
    if msg.from_user.id not in sessions:
        await msg.answer("❌ Сначала удалите фон")
        return
    await msg.answer("🎨 Выберите фон:", reply_markup=bg_keyboard())

@router.message(F.text == "📊 Статистика")
async def stats(msg: Message):
    data = database.load_users()
    uid = str(msg.from_user.id)
    if uid in data:
        await msg.answer(f"📊 Обработано: {data[uid]['total']} фото")
    else:
        await msg.answer("📊 Статистики пока нет")

@router.message(F.text == "🆘 Помощь")
async def help(msg: Message):
    await msg.answer(
        "1. Нажми «Удалить фон»\n"
        "2. Отправь фото\n"
        "3. Получи результат\n"
        "4. Нажми «Изменить фон»"
    )

@router.message(F.text == "⚪ Белый")
async def white_bg(msg: Message):
    await apply_color_bg(msg, "white")

@router.message(F.text == "⚫ Черный")
async def black_bg(msg: Message):
    await apply_color_bg(msg, "black")

async def apply_color_bg(msg: Message, color):
    uid = msg.from_user.id
    if uid not in sessions:
        await msg.answer("❌ Сессия устарела", reply_markup=main_keyboard())
        return
    
    await show_progress(msg, [("Создание фона", 30), ("Наложение", 60), ("Готово", 100)])
    
    s = sessions[uid]
    bg = image.create_bg(s["size"][0], s["size"][1], color)
    result = image.apply_bg(s["no_bg"], bg, s["mask"])
    
    file = BufferedInputFile(result, filename=f"{color}.png")
    await msg.reply_document(file, caption="✅ Готово!", reply_markup=main_keyboard())

@router.message(F.text == "📸 Свое фото")
async def custom_bg(msg: Message):
    uid = msg.from_user.id
    if uid not in sessions:
        await msg.answer("❌ Ошибка")
        return
    sessions[uid]["step"] = "waiting_bg"
    await msg.answer("📸 Отправьте фото для фона")

@router.message(F.text == "🔙 Назад")
async def back(msg: Message):
    await msg.answer("🔙 Главное меню", reply_markup=main_keyboard())

@router.message(F.text == "🔙 Отмена")
async def cancel(msg: Message):
    await msg.answer("❌ Отменено", reply_markup=main_keyboard())

@router.message(F.photo | F.document)
async def handle_photo(msg: Message):
    uid = msg.from_user.id
    
    # Получаем файл
    if msg.photo:
        file_id = msg.photo[-1].file_id
    else:
        file_id = msg.document.file_id
    
    file = await msg.bot.get_file(file_id)
    bytes = await msg.bot.download_file(file.file_path)
    
    # Если ждем фоновое фото
    if uid in sessions and sessions[uid].get("step") == "waiting_bg":
        await show_progress(msg, [("Анализ", 20), ("Наложение", 60), ("Готово", 100)])
        s = sessions[uid]
        result = image.apply_bg(s["no_bg"], bytes.getvalue(), s["mask"])
        file = BufferedInputFile(result, filename="result.png")
        await msg.reply_document(file, caption="✅ Готово!", reply_markup=main_keyboard())
        database.update_stats(uid)
        del sessions[uid]
        return
    
    # Удаляем фон
    await show_progress(msg, [
        ("Загрузка", 10), ("Анализ", 30), ("Удаление фона", 70), ("Готово", 100)
    ])
    
    no_bg = image.remove_bg(bytes.getvalue())
    mask, size = image.get_mask(no_bg)
    
    sessions[uid] = {
        "no_bg": no_bg,
        "mask": mask,
        "size": size
    }
    
    file = BufferedInputFile(no_bg, filename="no_bg.png")
    await msg.reply_document(
        file, 
        caption="✅ Фон удален! Теперь можете изменить фон",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🎨 Изменить фон")]],
            resize_keyboard=True
        )
    )
    
    database.update_stats(uid)