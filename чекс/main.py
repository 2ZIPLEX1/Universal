import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from datetime import datetime
import pytz

# Состояния для ConversationHandler
LANGUAGE, BANK, TRANSFER_TYPE, STATUS, CURRENCY, AMOUNT, COMMISSION, SENDER, RECIPIENT_PHONE, RECIPIENT, MESSAGE, GENERATE = range(12)

# Логотипы и подписи
bank_data = {
    "Тинькофф": {"logo": "tinkoff_logo.png", "signature": "t_ros.png"},
    "Сбербанк": {"logo": "sberbank_logo.png", "signature": "s_ros.png"},
    "ВТБ": {"logo": "vtb_logo.png", "signature": "vtb_ros.png"},
    "Альфа-Банк": {"logo": "alfa_logo.png", "signature": "alfa_ros.png"}
}

def start(update: Update, context: CallbackContext) -> int:
    buttons = [[KeyboardButton("Русский")], [KeyboardButton("English")]]
    update.message.reply_text("Выберите язык / Choose language:", reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
    return LANGUAGE

def choose_language(update: Update, context: CallbackContext) -> int:
    language = update.message.text
    context.user_data['language'] = language
    buttons = [[KeyboardButton(bank)] for bank in bank_data.keys()]
    update.message.reply_text("Выберите банк / Choose bank:", reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
    return BANK

def choose_bank(update: Update, context: CallbackContext) -> int:
    bank = update.message.text
    context.user_data['bank'] = bank
    buttons = [[KeyboardButton("По номеру телефона")], [KeyboardButton("По номеру карты")], [KeyboardButton("Назад")]]
    update.message.reply_text("Выберите тип перевода:", reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
    return TRANSFER_TYPE

def transfer_type(update: Update, context: CallbackContext) -> int:
    transfer_type = update.message.text
    if transfer_type == "Назад":
        return choose_bank(update, context)
    context.user_data['transfer_type'] = transfer_type
    buttons = [[KeyboardButton("Вписать статус самому")], [KeyboardButton("Холд 15 дней")], [KeyboardButton("Холд 7 дней")], [KeyboardButton("Назад")]]
    update.message.reply_text("Выберите статус:", reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
    return STATUS

def status(update: Update, context: CallbackContext) -> int:
    status = update.message.text
    if status == "Назад":
        return transfer_type(update, context)
    context.user_data['status'] = status
    buttons = [[KeyboardButton("RUB")], [KeyboardButton("USD")], [KeyboardButton("EUR")], [KeyboardButton("Назад")]]
    update.message.reply_text("Выберите валюту:", reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
    return CURRENCY

def currency(update: Update, context: CallbackContext) -> int:
    currency = update.message.text
    if currency == "Назад":
        return status(update, context)
    context.user_data['currency'] = currency
    update.message.reply_text("Введите сумму:")
    return AMOUNT

def amount(update: Update, context: CallbackContext) -> int:
    amount = update.message.text
    context.user_data['amount'] = amount
    buttons = [[KeyboardButton("Указать комиссию")], [KeyboardButton("Без комиссии")], [KeyboardButton("Назад")]]
    update.message.reply_text("Выберите комиссию:", reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
    return COMMISSION

def commission(update: Update, context: CallbackContext) -> int:
    commission = update.message.text
    if commission == "Назад":
        return currency(update, context)
    context.user_data['commission'] = commission
    update.message.reply_text("Введите имя отправителя:")
    return SENDER

def sender(update: Update, context: CallbackContext) -> int:
    sender = update.message.text
    context.user_data['sender'] = sender
    buttons = [[KeyboardButton("Пропустить")], [KeyboardButton("Ввести самому")], [KeyboardButton("Назад")]]
    update.message.reply_text("Введите телефон получателя:", reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
    return RECIPIENT_PHONE

def recipient_phone(update: Update, context: CallbackContext) -> int:
    recipient_phone = update.message.text
    if recipient_phone == "Назад":
        return sender(update, context)
    context.user_data['recipient_phone'] = recipient_phone
    update.message.reply_text("Введите имя получателя:")
    return RECIPIENT

def recipient(update: Update, context: CallbackContext) -> int:
    recipient = update.message.text
    context.user_data['recipient'] = recipient
    buttons = [[KeyboardButton("Ввести сообщение")], [KeyboardButton("Пропустить")], [KeyboardButton("Назад")]]
    update.message.reply_text("Введите сообщение:", reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
    return MESSAGE

def message(update: Update, context: CallbackContext) -> int:
    message = update.message.text
    if message == "Назад":
        return recipient(update, context)
    context.user_data['message'] = message
    update.message.reply_text("Генерация чека...")
    return generate_receipt(update, context)

def generate_receipt(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    bank = user_data['bank']
    logo = bank_data[bank]['logo']
    signature = bank_data[bank]['signature']

    pdf_filename = f"receipt_{update.message.from_user.id}.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Image(logo, width=100, height=50))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Итого: {user_data['amount']} {user_data['currency']}", styles['Heading2']))
    story.append(Paragraph(f"Время создания: {datetime.now(pytz.timezone('Europe/London')).strftime('%d.%m.%Y %H:%M:%S')}", styles['BodyText']))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Тип перевода: {user_data['transfer_type']}", styles['BodyText']))
    story.append(Paragraph(f"Статус: {user_data['status']}", styles['BodyText']))
    story.append(Paragraph(f"Отправитель: {user_data['sender']}", styles['BodyText']))
    story.append(Paragraph(f"Телефон получателя: {user_data['recipient_phone']}", styles['BodyText']))
    story.append(Paragraph(f"Получатель: {user_data['recipient']}", styles['BodyText']))
    story.append(Paragraph(f"Сообщение: {user_data['message']}", styles['BodyText']))
    story.append(Spacer(1, 12))

    story.append(Image(signature, width=100, height=50))
    story.append(Paragraph("По вопросам зачисления обращайтесь к получателю", styles['BodyText']))
    story.append(Paragraph(f"Служба поддержки {bank}", styles['BodyText']))

    doc.build(story)
    update.message.reply_document(document=open(pdf_filename, 'rb'))
    os.remove(pdf_filename)
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Операция отменена.")
    return ConversationHandler.END

def main():
    updater = Updater("7709895492:AAFUWFF0R44IDD8kbLUCVbcdmc1J24KlTDg")
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE: [MessageHandler(Filters.text & ~Filters.command, choose_language)],
            BANK: [MessageHandler(Filters.text & ~Filters.command, choose_bank)],
            TRANSFER_TYPE: [MessageHandler(Filters.text & ~Filters.command, transfer_type)],
            STATUS: [MessageHandler(Filters.text & ~Filters.command, status)],
            CURRENCY: [MessageHandler(Filters.text & ~Filters.command, currency)],
            AMOUNT: [MessageHandler(Filters.text & ~Filters.command, amount)],
            COMMISSION: [MessageHandler(Filters.text & ~Filters.command, commission)],
            SENDER: [MessageHandler(Filters.text & ~Filters.command, sender)],
            RECIPIENT_PHONE: [MessageHandler(Filters.text & ~Filters.command, recipient_phone)],
            RECIPIENT: [MessageHandler(Filters.text & ~Filters.command, recipient)],
            MESSAGE: [MessageHandler(Filters.text & ~Filters.command, message)],
            GENERATE: [MessageHandler(Filters.text & ~Filters.command, generate_receipt)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()