import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from bot.utils.keyboards import get_create_bot_keyboard, get_my_bots_keyboard, get_add_bot_keyboard

logger = logging.getLogger(__name__)

async def bot_creation_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню создания бота"""
    # Заглушки для данных пользователя
    available_to_withdraw = 0
    earned_total = 0
    receipts_sold = 0
    checks_sold = 0
    
    creation_text = f"""💸 Создание личного бота

В пару кликов ты можешь создать своего бота и зарабатывать на продажах чеков и PDF квитанций. Минимальный вывод от 1500 ₽

— Твоя статистика:
Доступно к выводу: {available_to_withdraw} ₽
Заработано за все время: {earned_total} ₽
Продано квитанций: {receipts_sold}
Продано чеков: {checks_sold}

— Проценты заработка:
С 1 квитанции: 70% c квитанции
С 1 чека: 30% с чека"""
    
    # Отправляем новое сообщение с картинкой
    try:
        # Проверяем наличие изображения
        photo_path = "static/images/bot_creation.jpg"
        if os.path.exists(photo_path):
            await update.message.reply_photo(
                photo=open(photo_path, 'rb'),
                caption=creation_text,
                reply_markup=get_create_bot_keyboard(available_to_withdraw),
                parse_mode="Markdown"
            )
        else:
            # Если изображения нет, отправляем только текст
            await update.message.reply_text(
                creation_text,
                reply_markup=get_create_bot_keyboard(available_to_withdraw),
                parse_mode="Markdown"
            )
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        await update.message.reply_text(
            creation_text,
            reply_markup=get_create_bot_keyboard(available_to_withdraw),
            parse_mode="Markdown"
        )

async def withdraw_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик запроса на вывод средств"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text="🔄 Запрос на вывод средств принят. Наш менеджер свяжется с вами в ближайшее время.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="create_bot")]]),
        parse_mode="Markdown"
    )

async def my_bots_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик просмотра списка ботов"""
    query = update.callback_query
    await query.answer()
    
    bots_count = 0  # Заглушка
    
    bots_text = f"""🤖 Список твоих ботов:
{"У тебя пока нет ботов" if bots_count == 0 else "Список твоих ботов:"}"""
    
    # Редактируем текущее сообщение
    await query.edit_message_text(
        text=bots_text,
        reply_markup=get_my_bots_keyboard(),
        parse_mode="Markdown"
    )

async def add_bot_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик добавления нового бота"""
    query = update.callback_query
    await query.answer()
    
    # Устанавливаем состояние ожидания токена
    context.user_data["state"] = "waiting_bot_token"
    
    add_bot_text = """🤖 Добавление нового бота
Ты должен создать бота через @BotFather и получить его токен, затем прислать его в этот чат.
📖[Инструкция по созданию бота](https://core.telegram.org/bots#how-do-i-create-a-bot)"""
    
    # Редактируем текущее сообщение
    await query.edit_message_text(
        text=add_bot_text,
        reply_markup=get_add_bot_keyboard(),
        parse_mode="Markdown"
    )

async def process_bot_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка токена для создания бота"""
    token = update.message.text.strip()
    
    await update.message.reply_text(
        "✅ Токен получен! Ваш бот будет настроен в течение нескольких минут."
    )
    
    # Очищаем состояние
    if "state" in context.user_data:
        del context.user_data["state"]