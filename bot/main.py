#!/usr/bin/env python
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import logging
from bot.handlers import start, checks, receipts, balance, info, bot_creation
from bot.handlers.common import ensure_directories_exist  # Убираем create_placeholder_images
from bot.config import TOKEN

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Запуск бота"""
    # Создание необходимых директорий и заглушек для изображений
    ensure_directories_exist()
    
    # Создание приложения
    application = Application.builder().token(TOKEN).build()
    
    # Обработчики команд
    application.add_handler(CommandHandler("start", start.start_command))
    
    # Обработчики для квитанций Тинькофф
    application.add_handler(CallbackQueryHandler(receipts.tinkoff_receipt_card, pattern="^tinkoff_receipt_card$"))

    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start.process_message))
    
        # Обработчики для возврата в соответствующие меню
    application.add_handler(CallbackQueryHandler(checks.checks_menu, pattern="^checks$"))
    application.add_handler(CallbackQueryHandler(receipts.receipts_menu, pattern="^receipts$"))
    application.add_handler(CallbackQueryHandler(balance.balance_menu, pattern="^balance$"))
    application.add_handler(CallbackQueryHandler(info.info_menu, pattern="^info$"))
    application.add_handler(CallbackQueryHandler(start.support_handler, pattern="^support$"))
    application.add_handler(CallbackQueryHandler(bot_creation.bot_creation_menu, pattern="^create_bot$"))

        # Обработчики для банков в меню чеков
    application.add_handler(CallbackQueryHandler(checks.tinkoff_checks, pattern="^check_tinkoff$"))
    application.add_handler(CallbackQueryHandler(checks.alfabank_checks, pattern="^check_alfabank$"))
    application.add_handler(CallbackQueryHandler(checks.binance_checks, pattern="^check_binance$"))
    application.add_handler(CallbackQueryHandler(checks.sberbank_checks, pattern="^check_sberbank$"))
    application.add_handler(CallbackQueryHandler(checks.kaspi_checks, pattern="^check_kaspi$"))
    application.add_handler(CallbackQueryHandler(checks.vtb_checks, pattern="^check_vtb$"))

    # Обработчики для Тинькофф
    application.add_handler(CallbackQueryHandler(checks.tinkoff_balance_main, pattern="^tinkoff_balance_main$"))
    
    # Обработчики для возврата в соответствующие меню
    application.add_handler(CallbackQueryHandler(start.back_to_main, pattern="^back_main$"))
    application.add_handler(CallbackQueryHandler(checks.checks_menu, pattern="^checks$"))
    application.add_handler(CallbackQueryHandler(receipts.receipts_menu, pattern="^receipts$"))
    application.add_handler(CallbackQueryHandler(bot_creation.bot_creation_menu, pattern="^create_bot$"))

    # Обработчики для раздела "Квитанции"
    application.add_handler(CallbackQueryHandler(receipts.tinkoff_receipts, pattern="^receipt_tinkoff$"))
    application.add_handler(CallbackQueryHandler(receipts.kaspi_receipts, pattern="^receipt_kaspi$"))
    application.add_handler(CallbackQueryHandler(receipts.vtb_receipts, pattern="^receipt_vtb$"))
    application.add_handler(CallbackQueryHandler(receipts.sberbank_receipts, pattern="^receipt_sberbank$"))
    
    # Обработчики для баланса
    application.add_handler(CallbackQueryHandler(balance.add_balance, pattern="^add_balance$"))
    application.add_handler(CallbackQueryHandler(balance.pay_card, pattern="^pay_card$"))
    application.add_handler(CallbackQueryHandler(balance.pay_crypto, pattern="^pay_crypto$"))
    
    # Обработчики для раздела "Создать своего бота"
    application.add_handler(CallbackQueryHandler(bot_creation.withdraw_handler, pattern="^withdraw$"))
    application.add_handler(CallbackQueryHandler(bot_creation.my_bots_handler, pattern="^my_bots$"))
    application.add_handler(CallbackQueryHandler(bot_creation.add_bot_handler, pattern="^add_bot$"))
    application.add_handler(CallbackQueryHandler(start.back_to_main, pattern="^back_main$"))
    
    # Запуск бота
    application.run_polling(allowed_updates=["message", "callback_query"])
    
    logger.info("Бот запущен")

if __name__ == "__main__":
    main()