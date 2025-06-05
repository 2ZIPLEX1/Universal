import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from bot.utils.keyboards import get_info_keyboard
from db.models import Stats

logger = logging.getLogger(__name__)

async def info_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню информации о боте"""
    # Получение статистики бота (добавьте собственную логику)
    # Используем заглушки для примера
    users_count = 1
    total_checks = 0
    total_receipts = 0
    today_checks = 0
    today_receipts = 0
    
    # В реальном боте, вы бы получали эти данные из базы данных
    try:
        stats = Stats.get_stats()
        users_count = stats["users_count"]
        total_checks = stats["total_checks"]
        total_receipts = stats["total_receipts"]
        today_checks = stats["today_checks"]
        today_receipts = stats["today_receipts"]
    except Exception as e:
        print(f"Ошибка при получении статистики: {e}")
    
    info_text = f"""💫 Информация о боте

Купить рекламу - ""
Инфо-канал - ""
Поддержка - ""

-Статистика бота:
 
Пользователей в ботах: {users_count}
Чеков за все время: {total_checks}
Квитанций за все время: {total_receipts}
Чеков за сегодня: {today_checks}
Квитанций за сегодня: {today_receipts}"""
    
    # Отправляем новое сообщение с картинкой
    try:
        # Проверяем наличие изображения
        photo_path = "static/images/info.jpg"
        if os.path.exists(photo_path):
            await update.message.reply_photo(
                photo=open(photo_path, 'rb'),
                caption=info_text,
                reply_markup=get_info_keyboard(),
                parse_mode="Markdown"
            )
        else:
            # Если изображения нет, отправляем только текст
            await update.message.reply_text(
                info_text,
                reply_markup=get_info_keyboard(),
                parse_mode="Markdown"
            )
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        await update.message.reply_text(
            info_text,
            reply_markup=get_info_keyboard(),
            parse_mode="Markdown"
        )