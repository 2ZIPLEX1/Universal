import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Состояния
LANGUAGE, BANK, TRANSFER_TYPE, STATUS, CURRENCY, AMOUNT, COMMISSION, SENDER, RECIPIENT_PHONE, RECIPIENT, MESSAGE, GENERATE_PDF = range(12)

# Пути к логотипам и подписям
BANKS = {
    "Тинькофф": {
        "logo": "banks/tinka/tinkoff_logo.png",
        "signature": "banks/tinka/t_ros.png"
    },
    "Сбербанк": {
        "logo": "banks/sber/sberbank_logo.png",
        "signature": "banks/sber/s_ros.png"
    },
    "ВТБ": {
        "logo": "banks/VTB/vtb_logo.png",
        "signature": "banks/VTB/vtb_ros.png"
    },
    "Альфа Банк": {
        "logo": "banks/alfa/alfa_logo.png",
        "signature": "banks/alfa/alfa_ros.png"
    }
}

async def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [["Русский", "English"]]
    await update.message.reply_text(
        "Выберите язык / Choose language:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return LANGUAGE

async def language(update: Update, context: CallbackContext) -> int:
    user_language = update.message.text
    context.user_data['language'] = user_language
    reply_keyboard = [["Тинькофф", "Сбербанк", "ВТБ", "Альфа Банк"]]
    await update.message.reply_text(
        "Выберите банк / Choose bank:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return BANK

async def bank(update: Update, context: CallbackContext) -> int:
    user_bank = update.message.text
    context.user_data['bank'] = user_bank
    reply_keyboard = [["По номеру телефона", "По номеру карты", "Назад"]]
    await update.message.reply_text(
        "Выберите тип перевода:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return TRANSFER_TYPE

async def transfer_type(update: Update, context: CallbackContext) -> int:
    transfer_type = update.message.text
    context.user_data['transfer_type'] = transfer_type
    if transfer_type == "Назад":
        return await bank(update, context)
    reply_keyboard = [["Вписать статус самому", "Холд 15 дней", "Холд 7 дней", "Назад"]]
    await update.message.reply_text(
        "Выберите статус:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return STATUS

async def status(update: Update, context: CallbackContext) -> int:
    status = update.message.text
    context.user_data['status'] = status
    if status == "Назад":
        return await transfer_type(update, context)
    reply_keyboard = [["EUR", "RUB", "USD", "Назад"]]
    await update.message.reply_text(
        "Выберите валюту:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return CURRENCY

async def currency(update: Update, context: CallbackContext) -> int:
    currency = update.message.text
    context.user_data['currency'] = currency
    if currency == "Назад":
        return await status(update, context)
    await update.message.reply_text("Введите сумму:")
    return AMOUNT

async def amount(update: Update, context: CallbackContext) -> int:
    amount = update.message.text
    context.user_data['amount'] = amount
    reply_keyboard = [["Указать комиссию", "Без комиссии", "Назад"]]
    await update.message.reply_text(
        "Выберите комиссию:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return COMMISSION

async def commission(update: Update, context: CallbackContext) -> int:
    commission = update.message.text
    context.user_data['commission'] = commission
    if commission == "Назад":
        return await currency(update, context)
    await update.message.reply_text("Введите имя отправителя:")
    return SENDER

async def sender(update: Update, context: CallbackContext) -> int:
    sender = update.message.text
    context.user_data['sender'] = sender
    reply_keyboard = [["Пропустить", "Ввести самому", "Назад"]]
    await update.message.reply_text(
        "Введите телефон получателя:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return RECIPIENT_PHONE

async def recipient_phone(update: Update, context: CallbackContext) -> int:
    recipient_phone = update.message.text
    context.user_data['recipient_phone'] = recipient_phone
    if recipient_phone == "Назад":
        return await sender(update, context)
    await update.message.reply_text("Введите имя получателя:")
    return RECIPIENT

async def recipient(update: Update, context: CallbackContext) -> int:
    recipient = update.message.text
    context.user_data['recipient'] = recipient
    reply_keyboard = [["Ввести сообщение", "Пропустить", "Назад"]]
    await update.message.reply_text(
        "Введите сообщение:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return MESSAGE

async def message(update: Update, context: CallbackContext) -> int:
    message = update.message.text
    context.user_data['message'] = message
    if message == "Назад":
        return await recipient(update, context)
    await generate_pdf(update, context)
    return ConversationHandler.END

async def generate_pdf(update: Update, context: CallbackContext):
    user_data = context.user_data
    bank_data = BANKS[user_data['bank']]
    
    pdf_filename = "receipt.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()
    
    elements = []
    
    # Логотип банка
    logo = Image(bank_data['logo'], width=50*mm, height=20*mm)
    elements.append(logo)
    elements.append(Spacer(1, 12))
    
    # Тип перевода
    elements.append(Paragraph(f"Тип перевода: {user_data['transfer_type']}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Статус
    elements.append(Paragraph(f"Статус: {user_data['status']}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Валюта и сумма
    elements.append(Paragraph(f"Сумма: {user_data['amount']} {user_data['currency']}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Комиссия
    elements.append(Paragraph(f"Комиссия: {user_data['commission']}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Отправитель
    elements.append(Paragraph(f"Отправитель: {user_data['sender']}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Телефон получателя
    elements.append(Paragraph(f"Телефон получателя: {user_data['recipient_phone']}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Получатель
    elements.append(Paragraph(f"Получатель: {user_data['recipient']}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Сообщение
    elements.append(Paragraph(f"Сообщение: {user_data['message']}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Подпись
    signature = Image(bank_data['signature'], width=50*mm, height=20*mm)
    elements.append(signature)
    
    doc.build(elements)
    
    with open(pdf_filename, "rb") as file:
        await update.message.reply_document(document=file, caption="Ваш чек готов!")

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Операция отменена.")
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token("7709895492:AAFUWFF0R44IDD8kbLUCVbcdmc1J24KlTDg").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, language)],
            BANK: [MessageHandler(filters.TEXT & ~filters.COMMAND, bank)],
            TRANSFER_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, transfer_type)],
            STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, status)],
            CURRENCY: [MessageHandler(filters.TEXT & ~filters.COMMAND, currency)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount)],
            COMMISSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, commission)],
            SENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, sender)],
            RECIPIENT_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, recipient_phone)],
            RECIPIENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, recipient)],
            MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, message)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()