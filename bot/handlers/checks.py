import os
import logging
import io
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from bot.utils.keyboards import get_bank_keyboard, get_tinkoff_checks_keyboard, get_back_keyboard
from generators.screenshot.tinkoff import TinkoffScreenshotGenerator
from db.models import Transaction, Stats

logger = logging.getLogger(__name__)

async def checks_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню выбора банка для чеков"""
    query = update.callback_query
    await query.answer()
    
    # Редактируем текущее сообщение
    await query.edit_message_text(
        text="💫 Выбери что хочешь отрисовать:",
        reply_markup=get_bank_keyboard("check"),
        parse_mode="Markdown"
    )

async def tinkoff_checks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню чеков Тинькофф"""
    query = update.callback_query
    await query.answer()
    
    # Редактируем текущее сообщение
    await query.edit_message_text(
        text="🟡 Т-Банк → выбери что хочешь отрисовать:",
        reply_markup=get_tinkoff_checks_keyboard(),
        parse_mode="Markdown"
    )

async def process_tinkoff_balance_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка введенных данных для баланса Тинькофф"""
    # Разбираем введенные данные
    data = update.message.text.strip().split('\n')
    
    if len(data) < 5:
        await update.message.reply_text(
            "❌ Недостаточно данных. Пожалуйста, введите все необходимые данные согласно инструкции."
        )
        return
    
    # Создаем словарь с данными
    variables = {
        "phoneTime": data[0],
        "userName": data[1],
        "cardBalance": data[2],
        "cardLastDigits": data[3],
        "monthlyExpenses": data[4],
        "cashbackAmount": data[5] if len(data) > 5 else "0"
    }
    
    # Генерируем скриншот
    try:
        generator = TinkoffScreenshotGenerator()
        screenshot_bytes = await generator.generate_balance_main(variables)
        
        # Сохраняем в статистику
        user_id = update.effective_user.id
        Transaction.create(user_id, "check", -100, "Tinkoff balance screenshot")
        Stats.increment("check")
        
        # Отправляем скриншот
        await update.message.reply_photo(
            photo=io.BytesIO(screenshot_bytes),
            caption="✅ Готово! Вот ваш скриншот баланса Тинькофф."
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ Произошла ошибка при генерации скриншота: {str(e)}"
        )
    
    # Очищаем состояние
    if "state" in context.user_data:
        del context.user_data["state"]

async def tinkoff_balance_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для баланса Тинькофф (главная)"""
    query = update.callback_query
    await query.answer()
    
    # Устанавливаем состояние ожидания данных
    context.user_data["state"] = "waiting_tinkoff_balance_data"
    
    # Редактируем текущее сообщение
    await query.edit_message_text(
        text="""🟡 Т-Банк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Имя держателя карты
3️⃣ Баланс на карте
4️⃣ Последние 4 цифры карты
5️⃣ Расходы за месяц
▶️ Накоплено кэшбэка (необ.)

👇🏻 Пример введенных данных:

20:27
София
5 500,50
1234
10 000
0""",
        reply_markup=get_back_keyboard("check_tinkoff"),
        parse_mode="Markdown"
    )

# Другие обработчики чеков
async def alfabank_checks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню чеков Альфа-Банка"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text="🅰️ Альфа банк → выбери что хочешь отрисовать:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="checks")]]),
        parse_mode="Markdown"
    )

async def binance_checks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню чеков Binance"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text="🔶 Binance → выбери что хочешь отрисовать:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="checks")]]),
        parse_mode="Markdown"
    )

async def sberbank_checks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню чеков Сбербанка"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text="🟢 Сбербанк → выбери что хочешь отрисовать:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="checks")]]),
        parse_mode="Markdown"
    )

async def kaspi_checks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню чеков Каспи"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text="🍁 Каспи → выбери что хочешь отрисовать:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="checks")]]),
        parse_mode="Markdown"
    )

async def vtb_checks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню чеков ВТБ"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text="🔵 ВТБ → выбери что хочешь отрисовать:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="checks")]]),
        parse_mode="Markdown"
    )
async def checks_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню выбора банка для чеков"""
    # Проверяем, откуда вызвана функция: из callback или из текстового сообщения
    if update.callback_query:
        # Вызвана из callback
        query = update.callback_query
        await query.answer()
        
        # Редактируем текущее сообщение
        try:
            await query.edit_message_text(
                text="💫 Выбери что хочешь отрисовать:",
                reply_markup=get_bank_keyboard("check"),
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Ошибка при редактировании сообщения: {e}")
            # Если не удалось отредактировать, отправляем новое сообщение
            await query.message.reply_text(
                "💫 Выбери что хочешь отрисовать:",
                reply_markup=get_bank_keyboard("check"),
                parse_mode="Markdown"
            )
    else:
        # Вызвана из текстового сообщения
        # Отправляем новое сообщение с картинкой
        try:
            # Проверяем наличие изображения
            photo_path = "static/images/checks.jpg"
            if os.path.exists(photo_path):
                await update.message.reply_photo(
                    photo=open(photo_path, 'rb'),
                    caption="💫 Выбери что хочешь отрисовать:",
                    reply_markup=get_bank_keyboard("check"),
                    parse_mode="Markdown"
                )
            else:
                # Если изображения нет, отправляем только текст
                await update.message.reply_text(
                    "💫 Выбери что хочешь отрисовать:",
                    reply_markup=get_bank_keyboard("check"),
                    parse_mode="Markdown"
                )
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
            await update.message.reply_text(
                "💫 Выбери что хочешь отрисовать:",
                reply_markup=get_bank_keyboard("check"),
                parse_mode="Markdown"
            )