import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from bot.utils.keyboards import get_balance_keyboard, get_payment_method_keyboard
from db.models import User

logger = logging.getLogger(__name__)

async def balance_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню баланса пользователя"""
    user_id = update.effective_user.id
    username = update.effective_user.username or "Не указан"
    
    # Получение баланса пользователя (добавьте собственную логику)
    user_balance = 0  # Заглушка, замените на реальную логику получения баланса
    
    balance_text = f"💼 Твой баланс\nUserID: {user_id}\nUserName: {username}\nБаланс: {user_balance} руб."
    
    if user_balance < 50:
        balance_text += "\n\nПополни свой баланс для создания чеков и квитанций в нашем боте.\n🏦Чтобы пополнить нажми кнопку ниже."
    else:
        balance_text += "\n\n🪙Ты можешь пополнить баланс кнопкой ниже."
    
    # Отправляем новое сообщение с картинкой
    try:
        # Проверяем наличие изображения
        photo_path = "static/images/balance.jpg"
        if os.path.exists(photo_path):
            await update.message.reply_photo(
                photo=open(photo_path, 'rb'),
                caption=balance_text,
                reply_markup=get_balance_keyboard(user_balance),
                parse_mode="Markdown"
            )
        else:
            # Если изображения нет, отправляем только текст
            await update.message.reply_text(
                balance_text,
                reply_markup=get_balance_keyboard(user_balance),
                parse_mode="Markdown"
            )
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        await update.message.reply_text(
            balance_text,
            reply_markup=get_balance_keyboard(user_balance),
            parse_mode="Markdown"
        )

async def add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик пополнения баланса"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text="💰 Выберите способ пополнения баланса:",
        reply_markup=get_payment_method_keyboard(),
        parse_mode="Markdown"
    )

async def pay_card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик оплаты картой"""
    query = update.callback_query
    await query.answer()
    
    # Тут должна быть ваша логика для оплаты картой
    # Например, формирование счета, ссылки на оплату и т.д.
    
    await query.edit_message_text(
        text="💳 Оплата банковской картой\n\nДля оплаты перейдите по ссылке: [ссылка на оплату](https://example.com)\n\nПосле оплаты баланс будет пополнен автоматически.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="add_balance")]]),
        parse_mode="Markdown"
    )

async def pay_crypto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик оплаты криптовалютой"""
    query = update.callback_query
    await query.answer()
    
    # Тут должна быть ваша логика для оплаты криптовалютой
    
    await query.edit_message_text(
        text="📱 Оплата криптовалютой\n\nДля оплаты отправьте средства на следующий адрес:\n\nBTC: bc1q...\nETH: 0x...\n\nПосле отправки средств свяжитесь с администратором для подтверждения.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="add_balance")]]),
        parse_mode="Markdown"
    )