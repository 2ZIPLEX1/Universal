import os
import logging
import io
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from bot.utils.keyboards import (
    get_bank_keyboard, get_tinkoff_checks_keyboard, get_alfabank_checks_keyboard,
    get_sberbank_checks_keyboard, get_bank_selection_keyboard, get_back_keyboard
)
from generators.screenshot.tinkoff import TinkoffScreenshotGenerator
from db.models import Transaction, Stats

logger = logging.getLogger(__name__)

async def checks_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню выбора банка для чеков"""
    # Очищаем состояние пользователя при переходе в меню
    if "state" in context.user_data:
        del context.user_data["state"]
    
    # Проверяем, откуда вызвана функция: из callback или из текстового сообщения
    if update.callback_query:
        # Вызвана из callback - заменяем caption медиа-сообщения
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_caption(
            caption="💫 Выбери что хочешь отрисовать:",
            reply_markup=get_bank_keyboard("check"),
            parse_mode="Markdown"
        )
    else:
        # Вызвана из текстового сообщения - отправляем GIF + текст + кнопки в одном сообщении
        try:
            await update.message.reply_animation(
                animation="https://usagif.com/wp-content/uploads/gifs/starfall-gif-27.gif",
                caption="💫 Выбери что хочешь отрисовать:",
                reply_markup=get_bank_keyboard("check"),
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке GIF: {e}")
            # В случае ошибки отправляем только текст с меню
            await update.message.reply_text(
                "💫 Выбери что хочешь отрисовать:",
                reply_markup=get_bank_keyboard("check"),
                parse_mode="Markdown"
            )

# =============================================================================
# ТИНЬКОФФ БАНК
# =============================================================================

async def tinkoff_checks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню чеков Тинькофф"""
    query = update.callback_query
    await query.answer()
    
    # Очищаем состояние пользователя
    if "state" in context.user_data:
        del context.user_data["state"]
    
    # Заменяем caption медиа-сообщения
    await query.edit_message_caption(
        caption="🟡 Т-Банк → выбери что хочешь отрисовать:",
        reply_markup=get_tinkoff_checks_keyboard(),
        parse_mode="Markdown"
    )

async def tinkoff_balance_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для баланса Тинькофф (главная)"""
    query = update.callback_query
    await query.answer()
    
    # Устанавливаем состояние ожидания данных
    context.user_data["state"] = "waiting_tinkoff_balance_main_data"
    
    # Заменяем caption медиа-сообщения
    await query.edit_message_caption(
        caption="""🟡 Т-Банк → отправь данные по инструкции:

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
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="back_to_tinkoff")]]),
        parse_mode="Markdown"
    )

async def tinkoff_balance_card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для баланса Тинькофф (карта)"""
    query = update.callback_query
    await query.answer()
    
    # Устанавливаем состояние ожидания данных
    context.user_data["state"] = "waiting_tinkoff_balance_card_data"
    
    await query.edit_message_caption(
        caption="""🟡 Т-Банк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Баланс на карте
3️⃣ Последние 4 цифры карты
4️⃣ Расходы за месяц
▶️ Накоплено кэшбэка (необ.)

👇🏻 Пример введенных данных:

14:28
5 500,50
1234
10 000
0""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="back_to_tinkoff")]]),
        parse_mode="Markdown"
    )

async def tinkoff_send_card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню отправки на карту Тинькофф"""
    query = update.callback_query
    await query.answer()
    
    # Сохраняем информацию о том, из какого банка пришли
    context.user_data["source_bank"] = "tinkoff"
    context.user_data["action_type"] = "tinkoff_send_card"
    
    await query.edit_message_caption(
        caption="🟡 Т-Банк → Отправка на карту\nВыберите банк получателя:",
        reply_markup=get_bank_selection_keyboard("tinkoff_send_card"),
        parse_mode="Markdown"
    )

async def tinkoff_send_sbp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню отправки через СБП Тинькофф"""
    query = update.callback_query
    await query.answer()
    
    # Сохраняем информацию о том, из какого банка пришли
    context.user_data["source_bank"] = "tinkoff"
    context.user_data["action_type"] = "tinkoff_send_sbp"
    
    await query.edit_message_caption(
        caption="🟡 Т-Банк → Отправка через СБП\nВыберите банк получателя:",
        reply_markup=get_bank_selection_keyboard("tinkoff_send_sbp"),
        parse_mode="Markdown"
    )

async def tinkoff_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для истории платежей Тинькофф"""
    query = update.callback_query
    await query.answer()
    
    # Устанавливаем состояние ожидания данных
    context.user_data["state"] = "waiting_tinkoff_history_data"
    
    await query.edit_message_caption(
        caption="""🟡 Т-Банк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Расходы за месяц
3️⃣ Доходы за месяц

👇🏻 Пример введенных данных:

14:38
5 500,50
420,52""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="back_to_tinkoff")]]),
        parse_mode="Markdown"
    )

# Обработчики для отправки на разные банки из Тинькофф
async def tinkoff_send_card_to_bank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Универсальный обработчик для отправки на карту из Тинькофф"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем целевой банк из callback_data
    target_bank = query.data.split("_")[-1]  # Получаем последнюю часть после _
    
    # Устанавливаем состояние ожидания данных
    context.user_data["state"] = "waiting_tinkoff_send_card_data"
    context.user_data["target_bank"] = target_bank
    
    await query.edit_message_caption(
        caption="""🟡 Т-Банк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Сумма платежа
3️⃣ Баланс на карте
4️⃣ Номер карты получателя
▶️ Имя получателя (необ.)

👇🏻 Пример введенных данных:

14:32
420,52
5 500,50
4133216641213423
Кристина Л.""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="tinkoff_send_card")]]),
        parse_mode="Markdown"
    )

async def tinkoff_send_sbp_to_bank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Универсальный обработчик для отправки через СБП из Тинькофф"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем целевой банк из callback_data
    target_bank = query.data.split("_")[-1]  # Получаем последнюю часть после _
    
    # Устанавливаем состояние ожидания данных
    context.user_data["state"] = "waiting_tinkoff_send_sbp_data"
    context.user_data["target_bank"] = target_bank
    
    await query.edit_message_caption(
        caption="""🟡 Т-Банк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Сумма платежа
3️⃣ Баланс на карте
4️⃣ Номер телефона получателя
▶️ Имя получателя (необ.)

👇🏻 Пример введенных данных:

14:36
420,52
5 500,50
+7 (912) 924-14-52
Кристина Л.""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="tinkoff_send_sbp")]]),
        parse_mode="Markdown"
    )

# =============================================================================
# АЛЬФА-БАНК
# =============================================================================

async def alfabank_checks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню чеков Альфа-Банка"""
    query = update.callback_query
    await query.answer()
    
    # Очищаем состояние пользователя
    if "state" in context.user_data:
        del context.user_data["state"]
    
    await query.edit_message_caption(
        caption="🅰️ Альфа-Банк → выбери что хочешь отрисовать:",
        reply_markup=get_alfabank_checks_keyboard(),
        parse_mode="Markdown"
    )

async def alfabank_balance_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для баланса Альфа-Банка (главная)"""
    query = update.callback_query
    await query.answer()
    
    context.user_data["state"] = "waiting_alfabank_balance_main_data"
    
    await query.edit_message_caption(
        caption="""🅰️ Альфа-Банк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Баланс на карте
3️⃣ Последние 4 цифры карты
4️⃣ Имя держателя карты

👇🏻 Пример введенных данных:

14:59
5 500,50
1234
Кристина""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="back_to_alfabank")]]),
        parse_mode="Markdown"
    )

async def alfabank_balance_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для баланса Альфа-Банка (платежный счет)"""
    query = update.callback_query
    await query.answer()
    
    context.user_data["state"] = "waiting_alfabank_balance_account_data"
    
    await query.edit_message_caption(
        caption="""🅰️ Альфа-Банк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Баланс на карте
3️⃣ Последние 4 цифры карты
4️⃣ Последние 4 цифры счета

👇🏻 Пример введенных данных:

14:59
5 500,50
1234
9872""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="back_to_alfabank")]]),
        parse_mode="Markdown"
    )

async def alfabank_send_card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню отправки на карту Альфа-Банк"""
    query = update.callback_query
    await query.answer()
    
    context.user_data["source_bank"] = "alfabank"
    context.user_data["action_type"] = "alfabank_send_card"
    
    await query.edit_message_caption(
        caption="🅰️ Альфа-Банк → Отправка на карту\nВыберите банк получателя:",
        reply_markup=get_bank_selection_keyboard("alfabank_send_card"),
        parse_mode="Markdown"
    )

async def alfabank_send_sbp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню отправки через СБП Альфа-Банк"""
    query = update.callback_query
    await query.answer()
    
    context.user_data["source_bank"] = "alfabank"
    context.user_data["action_type"] = "alfabank_send_sbp"
    
    await query.edit_message_caption(
        caption="🅰️ Альфа-Банк → Отправка через СБП\nВыберите банк получателя:",
        reply_markup=get_bank_selection_keyboard("alfabank_send_sbp"),
        parse_mode="Markdown"
    )

# =============================================================================
# СБЕРБАНК
# =============================================================================

async def sberbank_checks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню чеков Сбербанка"""
    query = update.callback_query
    await query.answer()
    
    # Очищаем состояние пользователя
    if "state" in context.user_data:
        del context.user_data["state"]
    
    await query.edit_message_caption(
        caption="🟢 Сбербанк → выбери что хочешь отрисовать:",
        reply_markup=get_sberbank_checks_keyboard(),
        parse_mode="Markdown"
    )

async def sberbank_balance_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для баланса Сбербанка (главная)"""
    query = update.callback_query
    await query.answer()
    
    context.user_data["state"] = "waiting_sberbank_balance_main_data"
    
    await query.edit_message_caption(
        caption="""🟢 Сбербанк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Баланс на карте
3️⃣ Баланс на счету
4️⃣ Последние 4 цифры карты
5️⃣ Последние 4 цифры счета
6️⃣ Расходы за месяц
7️⃣ Переводы людям
▶️ Сумма комиссии (необ.)
▶️ СберСпасибо (необ.)

👇🏻 Пример введенных данных:

19:05
5 500,50
420,52
1234
9876
10 000
500
500
0""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="back_to_sberbank")]]),
        parse_mode="Markdown"
    )

async def sberbank_balance_card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для баланса Сбербанка (карта)"""
    query = update.callback_query
    await query.answer()
    
    context.user_data["state"] = "waiting_sberbank_balance_card_data"
    
    await query.edit_message_caption(
        caption="""🟢 Сбербанк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Сумма перевода
3️⃣ Последние 4 цифры карты
4️⃣ Последние 4 цифры счета

👇🏻 Пример введенных данных:

19:10
5 500,50
1234
9876""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="back_to_sberbank")]]),
        parse_mode="Markdown"
    )

async def sberbank_balance_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для баланса Сбербанка (платежный счет)"""
    query = update.callback_query
    await query.answer()
    
    context.user_data["state"] = "waiting_sberbank_balance_account_data"
    
    await query.edit_message_caption(
        caption="""🟢 Сбербанк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Баланс на счету
3️⃣ Последние 4 цифры карты
4️⃣ Последние 4 цифры счёта
5️⃣ Расходы за месяц

👇🏻 Пример введенных данных:

19:12
420,52
1234
9876
420 520""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="back_to_sberbank")]]),
        parse_mode="Markdown"
    )

async def sberbank_transfer_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для перевода выполнен Сбербанк"""
    query = update.callback_query
    await query.answer()
    
    context.user_data["state"] = "waiting_sberbank_transfer_done_data"
    
    await query.edit_message_caption(
        caption="""🟢 Сбербанк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Сумма перевода
3️⃣ Последние 4 цифры карты получателя

👇🏻 Пример введенных данных:

19:12
420,52
1234""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="back_to_sberbank")]]),
        parse_mode="Markdown"
    )

async def sberbank_transfer_sbp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для перевода отправлен СБП Сбербанк"""
    query = update.callback_query
    await query.answer()
    
    context.user_data["state"] = "waiting_sberbank_transfer_sbp_data"
    
    await query.edit_message_caption(
        caption="""🟢 Сбербанк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Сумма перевода
3️⃣ Номер телефона получателя
4️⃣ ФИО получателя
5️⃣ Банк получателя

👇🏻 Пример введенных данных:

19:14
420,52
+7 (922) 914-24-34
София Мармеладова С
Т-Банк""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="back_to_sberbank")]]),
        parse_mode="Markdown"
    )

async def sberbank_transfer_delivered(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для перевода доставлен Сбербанк"""
    query = update.callback_query
    await query.answer()
    
    context.user_data["state"] = "waiting_sberbank_transfer_delivered_data"
    
    await query.edit_message_caption(
        caption="""🟢 Сбербанк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Сумма перевода
3️⃣ Сумма комиссии
4️⃣ ФИО получателя

👇🏻 Пример введенных данных:

19:15
5 500,50
420,52
София Мармеладова С""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="back_to_sberbank")]]),
        parse_mode="Markdown"
    )

# =============================================================================
# ОСТАЛЬНЫЕ БАНКИ (заглушки)
# =============================================================================

async def binance_checks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню чеков Binance"""
    query = update.callback_query
    await query.answer()
    
    # Очищаем состояние пользователя
    if "state" in context.user_data:
        del context.user_data["state"]
    
    await query.edit_message_caption(
        caption="🔶 Binance → выбери что хочешь отрисовать:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="checks")]]),
        parse_mode="Markdown"
    )

async def kaspi_checks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню чеков Каспи"""
    query = update.callback_query
    await query.answer()
    
    # Очищаем состояние пользователя
    if "state" in context.user_data:
        del context.user_data["state"]
    
    await query.edit_message_caption(
        caption="🍁 Каспи → выбери что хочешь отрисовать:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="checks")]]),
        parse_mode="Markdown"
    )

async def vtb_checks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню чеков ВТБ"""
    query = update.callback_query
    await query.answer()
    
    # Очищаем состояние пользователя
    if "state" in context.user_data:
        del context.user_data["state"]
    
    await query.edit_message_caption(
        caption="🔵 ВТБ → выбери что хочешь отрисовать:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="checks")]]),
        parse_mode="Markdown"
    )

# =============================================================================
# УНИВЕРСАЛЬНЫЕ ОБРАБОТЧИКИ ДЛЯ ПЕРЕВОДОВ
# =============================================================================

async def alfabank_send_card_to_bank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Универсальный обработчик для отправки на карту из Альфа-Банка"""
    query = update.callback_query
    await query.answer()
    
    target_bank = query.data.split("_")[-1]
    context.user_data["state"] = "waiting_alfabank_send_card_data"
    context.user_data["target_bank"] = target_bank
    
    await query.edit_message_caption(
        caption="""🅰️ Альфа-Банк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Сумма платежа
3️⃣ Последние 4 цифры карты получателя
4️⃣ Последние 4 цифры карты списания

👇🏻 Пример введенных данных:

18:37
5 500,50
1234
9876""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="alfabank_send_card")]]),
        parse_mode="Markdown"
    )

async def alfabank_send_sbp_to_bank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Универсальный обработчик для отправки через СБП из Альфа-Банка"""
    query = update.callback_query
    await query.answer()
    
    target_bank = query.data.split("_")[-1]
    context.user_data["state"] = "waiting_alfabank_send_sbp_data"
    context.user_data["target_bank"] = target_bank
    
    await query.edit_message_caption(
        caption="""🅰️ Альфа-Банк → отправь данные по инструкции:

1️⃣ Время на телефоне
2️⃣ Сумма платежа
3️⃣ Номер телефона получателя
4️⃣ ФИО получателя
5️⃣ Счет списания

👇🏻 Пример введенных данных:

18:41
5 500,50
+7 (922) 914-24-34
Кристина Ладынская К.
1234""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="alfabank_send_sbp")]]),
        parse_mode="Markdown"
    )

# =============================================================================
# ФУНКЦИИ ВОЗВРАТА В МЕНЮ БАНКОВ
# =============================================================================

async def back_to_tinkoff_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Возврат в меню Тинькофф с очисткой состояния"""
    query = update.callback_query
    await query.answer()
    
    if "state" in context.user_data:
        del context.user_data["state"]
    
    await query.edit_message_caption(
        caption="🟡 Т-Банк → выбери что хочешь отрисовать:",
        reply_markup=get_tinkoff_checks_keyboard(),
        parse_mode="Markdown"
    )

async def back_to_alfabank_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Возврат в меню Альфа-Банка с очисткой состояния"""
    query = update.callback_query
    await query.answer()
    
    if "state" in context.user_data:
        del context.user_data["state"]
    
    await query.edit_message_caption(
        caption="🅰️ Альфа-Банк → выбери что хочешь отрисовать:",
        reply_markup=get_alfabank_checks_keyboard(),
        parse_mode="Markdown"
    )

async def back_to_sberbank_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Возврат в меню Сбербанка с очисткой состояния"""
    query = update.callback_query
    await query.answer()
    
    if "state" in context.user_data:
        del context.user_data["state"]
    
    await query.edit_message_caption(
        caption="🟢 Сбербанк → выбери что хочешь отрисовать:",
        reply_markup=get_sberbank_checks_keyboard(),
        parse_mode="Markdown"
    )

async def back_to_bank_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Универсальный возврат в меню банка"""
    query = update.callback_query
    await query.answer()
    
    # Определяем, в какой банк вернуться на основе source_bank
    source_bank = context.user_data.get("source_bank", "tinkoff")
    
async def back_to_bank_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Универсальный возврат в меню банка"""
    query = update.callback_query
    await query.answer()
    
    # Определяем, в какой банк вернуться на основе source_bank
    source_bank = context.user_data.get("source_bank", "tinkoff")
    
    if source_bank == "tinkoff":
        await back_to_tinkoff_menu(update, context)
    elif source_bank == "alfabank":
        await back_to_alfabank_menu(update, context)
    elif source_bank == "sberbank":
        await back_to_sberbank_menu(update, context)
    else:
        # По умолчанию возвращаемся в главное меню чеков
        await checks_menu(update, context)

# =============================================================================
# ОБРАБОТЧИКИ ДАННЫХ (заглушки для генерации скриншотов)
# =============================================================================

async def process_tinkoff_balance_main_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка данных для баланса Тинькофф (главная)"""
    await update.message.reply_text("✅ Скриншот баланса Тинькофф (главная) будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_tinkoff_balance_card_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка данных для баланса Тинькофф (карта)"""
    await update.message.reply_text("✅ Скриншот баланса Тинькофф (карта) будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_tinkoff_send_card_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка данных для отправки на карту Тинькофф"""
    target_bank = context.user_data.get("target_bank", "unknown")
    await update.message.reply_text(f"✅ Скриншот отправки на карту Тинькофф → {target_bank} будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_tinkoff_send_sbp_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка данных для отправки через СБП Тинькофф"""
    target_bank = context.user_data.get("target_bank", "unknown")
    await update.message.reply_text(f"✅ Скриншот отправки через СБП Тинькофф → {target_bank} будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_tinkoff_history_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка данных для истории Тинькофф"""
    await update.message.reply_text("✅ Скриншот истории платежей Тинькофф будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

# Функции для Альфа-банка
async def process_alfabank_balance_main_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Скриншот баланса Альфа-Банка (главная) будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_alfabank_balance_account_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Скриншот баланса Альфа-Банка (платежный счет) будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_alfabank_send_card_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    target_bank = context.user_data.get("target_bank", "unknown")
    await update.message.reply_text(f"✅ Скриншот отправки на карту Альфа-Банк → {target_bank} будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_alfabank_send_sbp_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    target_bank = context.user_data.get("target_bank", "unknown")
    await update.message.reply_text(f"✅ Скриншот отправки через СБП Альфа-Банк → {target_bank} будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

# Функции для Сбербанка
async def process_sberbank_balance_main_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Скриншот баланса Сбербанка (главная) будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_sberbank_balance_card_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Скриншот баланса Сбербанка (карта) будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_sberbank_balance_account_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Скриншот баланса Сбербанка (платежный счет) будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_sberbank_transfer_done_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Скриншот перевода выполнен Сбербанк будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_sberbank_transfer_sbp_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Скриншот перевода отправлен СБП Сбербанк будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

async def process_sberbank_transfer_delivered_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Скриншот перевода доставлен Сбербанк будет сгенерирован здесь")
    if "state" in context.user_data:
        del context.user_data["state"]

# Старые функции для совместимости
async def process_tinkoff_balance_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка введенных данных для баланса Тинькофф (старая версия)"""
    await process_tinkoff_balance_main_data(update, context)