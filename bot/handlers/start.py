from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
import logging
import os
from bot.config import CHANNEL_ID, CHANNEL_URL, ADMIN_ID

# Импортируем модули других обработчиков
from bot.utils.subscription import check_subscription
from bot.utils.keyboards import get_main_keyboard
from db.models import User

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Регистрируем пользователя в базе данных
    User.get_or_create(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    # Очищаем предыдущие состояния пользователя
    if "state" in context.user_data:
        del context.user_data["state"]
    
    # Проверка подписки только если CHANNEL_ID задан
    is_subscribed = True
    if CHANNEL_ID:
        is_subscribed = await check_subscription(context.bot, user.id, CHANNEL_ID)
    
    if not is_subscribed:
        # Пользователь не подписан на канал - отправляем GIF с инструкцией подписки
        try:
            await update.message.reply_animation(
                animation="https://usagif.com/wp-content/uploads/gifs/starfall-gif-27.gif",
                caption=f"🛑 Привет! Чтобы начать пользоваться нашим ботом, нужно подписаться на [наш канал]({CHANNEL_URL}). \n\n⚡️ Подписался? Напиши боту команду /start или любое сообщение в чат!",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке GIF: {e}")
            # В случае ошибки отправляем только текст
            await update.message.reply_text(
                f"🛑 Привет! Чтобы начать пользоваться нашим ботом, нужно подписаться на [наш канал]({CHANNEL_URL}). \n\n⚡️ Подписался? Напиши боту команду /start или любое сообщение в чат!",
                parse_mode="Markdown"
            )
    else:
        # Пользователь подписан на канал - отправляем эмодзи, затем GIF с клавиатурой
        # Сначала отправляем эмодзи отдельным сообщением
        await update.message.reply_text("💫")
        
        # Затем отправляем GIF с приветствием и клавиатурой в одном сообщении
        try:
            await update.message.reply_animation(
                animation="https://media1.tenor.com/m/5hCo-bxm3mUAAAAC/gojo-gojo-annoyed.gif",
                caption="Привет, добро пожаловать в нашего бота\n\nВ нашем боте ты можешь создать точную копию скриншотов переводов, чеков по операциям, истории переводов и покупок! Используй нашего бота только для розыгрышей и в личных целях, ответственность за все действия несешь только ты.\n\n📑 Инструкция и описание боты\n📖 Пользовательское соглашение",
                reply_markup=get_main_keyboard(),
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке GIF: {e}")
            # В случае ошибки отправляем только текст с клавиатурой
            await update.message.reply_text(
                "Привет, добро пожаловать в нашего бота\n\nВ нашем боте ты можешь создать точную копию скриншотов переводов, чеков по операциям, истории переводов и покупок! Используй нашего бота только для розыгрышей и в личных целях, ответственность за все действия несешь только ты.\n\n📑 Инструкция и описание боты\n📖 Пользовательское соглашение",
                reply_markup=get_main_keyboard(),
                parse_mode="Markdown"
            )

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    user = update.effective_user
    
    # Проверка подписки только если CHANNEL_ID задан
    is_subscribed = True
    if CHANNEL_ID:
        is_subscribed = await check_subscription(context.bot, user.id, CHANNEL_ID)
    
    if not is_subscribed:
        # Если не подписан, отправляем сообщение с предложением подписаться (без клавиатуры)
        await start_command(update, context)
        return
    
    message_text = update.message.text
    
    # Если пользователь в режиме ввода данных, обрабатываем их
    user_state = context.user_data.get("state", None)
    
    # Тинькофф обработчики
    if user_state == "waiting_tinkoff_balance_main_data":
        from bot.handlers import checks
        await checks.process_tinkoff_balance_main_data(update, context)
    elif user_state == "waiting_tinkoff_balance_card_data":
        from bot.handlers import checks
        await checks.process_tinkoff_balance_card_data(update, context)
    elif user_state == "waiting_tinkoff_send_card_data":
        from bot.handlers import checks
        await checks.process_tinkoff_send_card_data(update, context)
    elif user_state == "waiting_tinkoff_send_sbp_data":
        from bot.handlers import checks
        await checks.process_tinkoff_send_sbp_data(update, context)
    elif user_state == "waiting_tinkoff_history_data":
        from bot.handlers import checks
        await checks.process_tinkoff_history_data(update, context)
    # Альфа-банк обработчики
    elif user_state == "waiting_alfabank_balance_main_data":
        from bot.handlers import checks
        await checks.process_alfabank_balance_main_data(update, context)
    elif user_state == "waiting_alfabank_balance_account_data":
        from bot.handlers import checks
        await checks.process_alfabank_balance_account_data(update, context)
    elif user_state == "waiting_alfabank_send_card_data":
        from bot.handlers import checks
        await checks.process_alfabank_send_card_data(update, context)
    elif user_state == "waiting_alfabank_send_sbp_data":
        from bot.handlers import checks
        await checks.process_alfabank_send_sbp_data(update, context)
    # Сбербанк обработчики
    elif user_state == "waiting_sberbank_balance_main_data":
        from bot.handlers import checks
        await checks.process_sberbank_balance_main_data(update, context)
    elif user_state == "waiting_sberbank_balance_card_data":
        from bot.handlers import checks
        await checks.process_sberbank_balance_card_data(update, context)
    elif user_state == "waiting_sberbank_balance_account_data":
        from bot.handlers import checks
        await checks.process_sberbank_balance_account_data(update, context)
    elif user_state == "waiting_sberbank_transfer_done_data":
        from bot.handlers import checks
        await checks.process_sberbank_transfer_done_data(update, context)
    elif user_state == "waiting_sberbank_transfer_sbp_data":
        from bot.handlers import checks
        await checks.process_sberbank_transfer_sbp_data(update, context)
    elif user_state == "waiting_sberbank_transfer_delivered_data":
        from bot.handlers import checks
        await checks.process_sberbank_transfer_delivered_data(update, context)
    # Старые обработчики (для совместимости)
    elif user_state == "waiting_tinkoff_balance_data":
        from bot.handlers import checks
        await checks.process_tinkoff_balance_data(update, context)
    elif user_state == "waiting_tinkoff_card_receipt_data":
        from bot.handlers import receipts
        await receipts.process_tinkoff_card_receipt_data(update, context)
    elif user_state == "waiting_tinkoff_phone_receipt_data":
        from bot.handlers import receipts
        await receipts.process_tinkoff_phone_receipt_data(update, context)
    elif user_state == "waiting_kaspi_transfer_receipt_data":
        from bot.handlers import receipts
        await receipts.process_kaspi_transfer_receipt_data(update, context)
    elif user_state == "waiting_sberbank_sbp_receipt_data":
        from bot.handlers import receipts
        await receipts.process_sberbank_sbp_receipt_data(update, context)
    elif user_state == "waiting_sberbank_card_receipt_data":
        from bot.handlers import receipts
        await receipts.process_sberbank_card_receipt_data(update, context)
    elif user_state == "waiting_bot_token":
        from bot.handlers import bot_creation
        await bot_creation.process_bot_token(update, context)
    else:
        # Обрабатываем нажатия на кнопки меню
        if message_text == "🗒️ Чеки":
            from bot.handlers import checks
            await checks.checks_menu(update, context)
        elif message_text == "🧾 Pdf Квитанции":
            from bot.handlers import receipts
            await receipts.receipts_menu(update, context)
        elif message_text == "💼 Баланс":
            # Временно закомментировано до исправления модуля balance
            await update.message.reply_text(
                "💼 Баланс - функция временно недоступна",
                reply_markup=get_main_keyboard()
            )
        elif message_text == "ℹ️ Инфо":
            # Временно закомментировано до исправления модуля info
            await update.message.reply_text(
                "ℹ️ Инфо - функция временно недоступна", 
                reply_markup=get_main_keyboard()
            )
        elif message_text == "🆘 Поддержка":
            await support_handler(update, context)
        elif message_text == "💰 Создать своего бота":
            # Временно закомментировано до исправления модуля bot_creation
            await update.message.reply_text(
                "💰 Создать своего бота - функция временно недоступна",
                reply_markup=get_main_keyboard()
            )
        else:
            # Если нет активного состояния и не распознана команда, отправляем главное меню
            await update.message.reply_text(
                "Выберите действие из меню:",
                reply_markup=get_main_keyboard()
            )

async def support_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик кнопки поддержки - открывает чат с админом"""
    # ID администратора
    admin_id = ADMIN_ID
    
    # Создаем URL для перехода в чат с админом
    support_url = f"tg://user?id={admin_id}"
    
    # Отправляем новое сообщение с кнопкой поддержки
    try:
        # Проверяем наличие изображения
        photo_path = "static/images/support.jpg"
        if os.path.exists(photo_path):
            await update.message.reply_photo(
                photo=open(photo_path, 'rb'),
                caption="🆘 Поддержка\n\nЕсли у вас возникли вопросы или проблемы с использованием бота, обратитесь к администратору.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Написать в поддержку", url=support_url)]
                ]),
                parse_mode="Markdown"
            )
        else:
            # Если изображения нет, отправляем только текст
            await update.message.reply_text(
                "🆘 Поддержка\n\nЕсли у вас возникли вопросы или проблемы с использованием бота, обратитесь к администратору.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Написать в поддержку", url=support_url)]
                ]),
                parse_mode="Markdown"
            )
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        await update.message.reply_text(
            "🆘 Поддержка\n\nЕсли у вас возникли вопросы или проблемы с использованием бота, обратитесь к администратору.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Написать в поддержку", url=support_url)]
            ]),
            parse_mode="Markdown"
        )

async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Возврат в главное меню"""
    query = update.callback_query
    
    if query:
        await query.answer()
        
        # Очистка состояния пользователя
        if "state" in context.user_data:
            del context.user_data["state"]
        
        # Отправляем сообщение с главным меню
        await query.message.reply_text(
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )
    else:
        # Если функция вызвана не из callback, просто отправляем главное меню
        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )