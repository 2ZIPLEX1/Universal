#!/usr/bin/env python
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import logging
from bot.handlers import start
from bot.handlers import checks
from bot.handlers import receipts
# from bot.handlers import balance, info, bot_creation
from bot.handlers.common import ensure_directories_exist
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
    
    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start.process_message))
    
    # Обработчики для возврата в соответствующие меню (только рабочие)
    application.add_handler(CallbackQueryHandler(checks.checks_menu, pattern="^checks$"))
    application.add_handler(CallbackQueryHandler(receipts.receipts_menu, pattern="^receipts$"))
    application.add_handler(CallbackQueryHandler(start.support_handler, pattern="^support$"))

    # Обработчики для банков в меню чеков
    application.add_handler(CallbackQueryHandler(checks.tinkoff_checks, pattern="^check_tinkoff$"))
    application.add_handler(CallbackQueryHandler(checks.alfabank_checks, pattern="^check_alfabank$"))
    application.add_handler(CallbackQueryHandler(checks.binance_checks, pattern="^check_binance$"))
    application.add_handler(CallbackQueryHandler(checks.sberbank_checks, pattern="^check_sberbank$"))
    application.add_handler(CallbackQueryHandler(checks.kaspi_checks, pattern="^check_kaspi$"))
    application.add_handler(CallbackQueryHandler(checks.vtb_checks, pattern="^check_vtb$"))

    # Обработчики для Тинькофф чеков
    application.add_handler(CallbackQueryHandler(checks.tinkoff_balance_main, pattern="^tinkoff_balance_main$"))
    application.add_handler(CallbackQueryHandler(checks.tinkoff_balance_card, pattern="^tinkoff_balance_card$"))
    application.add_handler(CallbackQueryHandler(checks.tinkoff_send_card, pattern="^tinkoff_send_card$"))
    application.add_handler(CallbackQueryHandler(checks.tinkoff_send_sbp, pattern="^tinkoff_send_sbp$"))
    application.add_handler(CallbackQueryHandler(checks.tinkoff_history, pattern="^tinkoff_history$"))
    
    # Обработчики для Альфа-банк чеков
    application.add_handler(CallbackQueryHandler(checks.alfabank_balance_main, pattern="^alfabank_balance_main$"))
    application.add_handler(CallbackQueryHandler(checks.alfabank_balance_account, pattern="^alfabank_balance_account$"))
    application.add_handler(CallbackQueryHandler(checks.alfabank_send_card, pattern="^alfabank_send_card$"))
    application.add_handler(CallbackQueryHandler(checks.alfabank_send_sbp, pattern="^alfabank_send_sbp$"))
    
    # Обработчики для Сбербанк чеков
    application.add_handler(CallbackQueryHandler(checks.sberbank_balance_main, pattern="^sberbank_balance_main$"))
    application.add_handler(CallbackQueryHandler(checks.sberbank_balance_card, pattern="^sberbank_balance_card$"))
    application.add_handler(CallbackQueryHandler(checks.sberbank_balance_account, pattern="^sberbank_balance_account$"))
    application.add_handler(CallbackQueryHandler(checks.sberbank_transfer_done, pattern="^sberbank_transfer_done$"))
    application.add_handler(CallbackQueryHandler(checks.sberbank_transfer_sbp, pattern="^sberbank_transfer_sbp$"))
    application.add_handler(CallbackQueryHandler(checks.sberbank_transfer_delivered, pattern="^sberbank_transfer_delivered$"))
    
    # Обработчики для переводов на другие банки (Тинькофф)
    application.add_handler(CallbackQueryHandler(checks.tinkoff_send_card_to_bank, pattern="^tinkoff_send_card_to_"))
    application.add_handler(CallbackQueryHandler(checks.tinkoff_send_sbp_to_bank, pattern="^tinkoff_send_sbp_to_"))
    
    # Обработчики для переводов на другие банки (Альфа-банк)
    application.add_handler(CallbackQueryHandler(checks.alfabank_send_card_to_bank, pattern="^alfabank_send_card_to_"))
    application.add_handler(CallbackQueryHandler(checks.alfabank_send_sbp_to_bank, pattern="^alfabank_send_sbp_to_"))
    
    # Обработчики для возврата в меню банков
    application.add_handler(CallbackQueryHandler(checks.back_to_tinkoff_menu, pattern="^back_to_tinkoff$"))
    application.add_handler(CallbackQueryHandler(checks.back_to_alfabank_menu, pattern="^back_to_alfabank$"))
    application.add_handler(CallbackQueryHandler(checks.back_to_sberbank_menu, pattern="^back_to_sberbank$"))
    application.add_handler(CallbackQueryHandler(checks.back_to_bank_menu, pattern="^back_to_bank_menu$"))
    
    # Обработчики для раздела "Квитанции"
    application.add_handler(CallbackQueryHandler(receipts.tinkoff_receipts, pattern="^receipt_tinkoff$"))
    application.add_handler(CallbackQueryHandler(receipts.kaspi_receipts, pattern="^receipt_kaspi$"))
    application.add_handler(CallbackQueryHandler(receipts.vtb_receipts, pattern="^receipt_vtb$"))
    application.add_handler(CallbackQueryHandler(receipts.sberbank_receipts, pattern="^receipt_sberbank$"))
    
    # Обработчики для квитанций Тинькофф
    application.add_handler(CallbackQueryHandler(receipts.tinkoff_receipt_card, pattern="^tinkoff_receipt_card$"))
    
    # Обработчик для возврата в главное меню
    application.add_handler(CallbackQueryHandler(start.back_to_main, pattern="^back_main$"))
    
    # Запуск бота
    application.run_polling(allowed_updates=["message", "callback_query"])
    
    logger.info("Бот запущен")

if __name__ == "__main__":
    main()