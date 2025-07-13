import os
import logging
import io
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from bot.utils.keyboards import (
    get_bank_keyboard, get_tinkoff_receipts_keyboard, 
    get_kaspi_receipts_keyboard, get_sberbank_receipts_keyboard, 
    get_back_keyboard
)
from generators.receipt.tinkoff import TinkoffReceiptGenerator
from db.models import Transaction, Stats

logger = logging.getLogger(__name__)

async def receipts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню выбора банка для квитанций"""
    # Очищаем состояние пользователя при переходе в меню
    if "state" in context.user_data:
        del context.user_data["state"]
    
    # Проверяем, откуда вызвана функция: из callback или из текстового сообщения
    if update.callback_query:
        # Вызвана из callback - заменяем caption медиа-сообщения
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_caption(
            caption="💫 Выбери какую квитанцию хочешь создать:",
            reply_markup=get_bank_keyboard("receipt"),
            parse_mode="Markdown"
        )
    else:
        # Вызвана из текстового сообщения - отправляем GIF + текст + кнопки в одном сообщении
        try:
            await update.message.reply_animation(
                animation="https://usagif.com/wp-content/uploads/gifs/starfall-gif-27.gif",
                caption="💫 Выбери какую квитанцию хочешь создать:",
                reply_markup=get_bank_keyboard("receipt"),
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке GIF: {e}")
            # В случае ошибки отправляем только текст с меню
            await update.message.reply_text(
                "💫 Выбери какую квитанцию хочешь создать:",
                reply_markup=get_bank_keyboard("receipt"),
                parse_mode="Markdown"
            )

async def tinkoff_receipts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню квитанций Тинькофф"""
    query = update.callback_query
    await query.answer()
    
    # Очищаем состояние пользователя
    if "state" in context.user_data:
        del context.user_data["state"]
    
    # Заменяем caption медиа-сообщения
    await query.edit_message_caption(
        caption="🧾 Тинькофф - выбери тип перевода в квитанции:",
        reply_markup=get_tinkoff_receipts_keyboard(),
        parse_mode="Markdown"
    )

async def process_tinkoff_card_receipt_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка введенных данных для квитанции Тинькофф по карте"""
    # Разбираем введенные данные
    data = update.message.text.strip().split('\n')
    
    if len(data) < 8:
        await update.message.reply_text(
            "❌ Недостаточно данных. Пожалуйста, введите все необходимые данные согласно инструкции."
        )
        return
    
    # Создаем словарь с данными
    variables = {
        "transfer_amount": data[0],
        "commission": data[1],
        "recipient_card": data[2],
        "recipient_bank": data[3],
        "recipient_name": data[4],
        "sender_name": data[5],
        "status": data[6],
        "date_time": data[7],
        "receipt_number": data[8] if len(data) > 8 else "1-23-456-789-123"
    }
    
    # Генерируем квитанцию
    try:
        generator = TinkoffReceiptGenerator()
        pdf_bytes = await generator.generate_card_receipt(variables)
        
        # Сохраняем в статистику
        user_id = update.effective_user.id
        Transaction.create(user_id, "receipt", -150, "Tinkoff card receipt")
        Stats.increment("receipt")
        
        # Отправляем квитанцию
        await update.message.reply_document(
            document=io.BytesIO(pdf_bytes),
            filename="tinkoff_receipt_card.pdf",
            caption="✅ Готово! Вот ваша квитанция Тинькофф по карте."
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ Произошла ошибка при генерации квитанции: {str(e)}"
        )
    
    # Очищаем состояние
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_tinkoff_phone_receipt_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка введенных данных для квитанции Тинькофф по телефону"""
    # Аналогично process_tinkoff_card_receipt_data, но для квитанции по телефону
    await update.message.reply_text("Функция обработки квитанции по телефону еще не реализована.")
    
    # Очищаем состояние
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_kaspi_transfer_receipt_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка введенных данных для квитанции Каспи"""
    await update.message.reply_text("Функция обработки квитанции Каспи еще не реализована.")
    
    # Очищаем состояние
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_sberbank_sbp_receipt_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка введенных данных для квитанции Сбербанка СБП"""
    await update.message.reply_text("Функция обработки квитанции Сбербанка СБП еще не реализована.")
    
    # Очищаем состояние
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_sberbank_card_receipt_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка введенных данных для квитанции Сбербанка по карте"""
    await update.message.reply_text("Функция обработки квитанции Сбербанка по карте еще не реализована.")
    
    # Очищаем состояние
    if "state" in context.user_data:
        del context.user_data["state"]

# Заглушки для других обработчиков
async def kaspi_receipts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню квитанций Каспи"""
    query = update.callback_query
    await query.answer()
    
    # Очищаем состояние пользователя
    if "state" in context.user_data:
        del context.user_data["state"]
    
    await query.edit_message_caption(
        caption="🍁 Каспи - выбери тип перевода в квитанции:",
        reply_markup=get_kaspi_receipts_keyboard(),
        parse_mode="Markdown"
    )

async def vtb_receipts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню квитанций ВТБ"""
    query = update.callback_query
    await query.answer()
    
    # Очищаем состояние пользователя
    if "state" in context.user_data:
        del context.user_data["state"]
    
    await query.edit_message_caption(
        caption="🔵 ВТБ - выбери тип перевода в квитанции:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="receipts")]]),
        parse_mode="Markdown"
    )

async def sberbank_receipts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню квитанций Сбербанка"""
    query = update.callback_query
    await query.answer()
    
    # Очищаем состояние пользователя
    if "state" in context.user_data:
        del context.user_data["state"]
    
    await query.edit_message_caption(
        caption="🟢 Сбербанк - выбери тип перевода в квитанции:",
        reply_markup=get_sberbank_receipts_keyboard(),
        parse_mode="Markdown"
    )

# Добавьте новый обработчик для квитанции по карте
async def tinkoff_receipt_card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для квитанции Тинькофф по карте"""
    query = update.callback_query
    await query.answer()
    
    # Устанавливаем состояние ожидания данных
    context.user_data["state"] = "waiting_tinkoff_card_receipt_data"
    
    await query.edit_message_caption(
        caption="""🧾 Т-Банк → отправь данные по инструкции:

1️⃣ Сумма перевода
2️⃣ Сумма комиссии
3️⃣ Карта получателя
4️⃣ Банк получателя
5️⃣ Имя получателя
6️⃣ Имя отправителя
7️⃣ Статус перевода
8️⃣ Дата и время перевода
▶️ Номер квитанции

👇🏻 Пример введенных данных:

5 500,50
420,52
220220******1234
Т-Банк
София Мармеладова М
Валентин Дядька М
Успешно
22.05.2025 23:06:11
1-23-456-789-123""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="receipt_tinkoff")]]),
        parse_mode="Markdown"
    )