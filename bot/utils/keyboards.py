from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard():
    """Возвращает основную обычную клавиатуру для главного меню"""
    keyboard = [
        [KeyboardButton("🗒️ Чеки"), KeyboardButton("🧾 Pdf Квитанции")],
        [KeyboardButton("💼 Баланс"), KeyboardButton("ℹ️ Инфо")],
        [KeyboardButton("🆘 Поддержка"), KeyboardButton("💰 Создать своего бота")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_bank_keyboard(type_id):
    """Возвращает клавиатуру выбора банка для чеков или квитанций"""
    if type_id == "check":
        keyboard = [
            [InlineKeyboardButton("🍁 Каспи", callback_data="check_kaspi")],
            [InlineKeyboardButton("🅰️ Альфа банк", callback_data="check_alfabank")],
            [InlineKeyboardButton("🔶 Binance", callback_data="check_binance")],
            [InlineKeyboardButton("🟢 Cбербанк", callback_data="check_sberbank")],
            [InlineKeyboardButton("🟡 Т-банк", callback_data="check_tinkoff")],
            [InlineKeyboardButton("🔵 ВТБ", callback_data="check_vtb")],
        ]
    else:  # receipt
        keyboard = [
            [InlineKeyboardButton("🗒️ Т-банк", callback_data="receipt_tinkoff")],
            [InlineKeyboardButton("🗒️ Каспи", callback_data="receipt_kaspi")],
            [InlineKeyboardButton("🗒️ ВТБ", callback_data="receipt_vtb")],
            [InlineKeyboardButton("🧾 СБЕРБАНК", callback_data="receipt_sberbank")],
        ]
    return InlineKeyboardMarkup(keyboard)

def get_tinkoff_checks_keyboard():
    """Возвращает клавиатуру выбора типа чека Тинькофф"""
    keyboard = [
        [InlineKeyboardButton("🟡 Баланс(Главная)", callback_data="tinkoff_balance_main")],
        [InlineKeyboardButton("🟡 Баланс(Карта)", callback_data="tinkoff_balance_card")],
        [InlineKeyboardButton("🟡 Отправка на карту", callback_data="tinkoff_send_card")],
        [InlineKeyboardButton("🟡 Отправка через СБП", callback_data="tinkoff_send_sbp")],
        [InlineKeyboardButton("🟡 История платежей", callback_data="tinkoff_history")],
        [InlineKeyboardButton("« Назад", callback_data="checks")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_alfabank_checks_keyboard():
    """Возвращает клавиатуру выбора типа чека Альфа-Банка"""
    keyboard = [
        [InlineKeyboardButton("🅰️ Баланс (главная)", callback_data="alfabank_balance_main")],
        [InlineKeyboardButton("🅰️ Баланс(Платежный счет)", callback_data="alfabank_balance_account")],
        [InlineKeyboardButton("🅰️ Отправка на карту", callback_data="alfabank_send_card")],
        [InlineKeyboardButton("🅰️ Отправка через СБП", callback_data="alfabank_send_sbp")],
        [InlineKeyboardButton("« Назад", callback_data="checks")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_sberbank_checks_keyboard():
    """Возвращает клавиатуру выбора типа чека Сбербанка"""
    keyboard = [
        [InlineKeyboardButton("🟢 Баланс (Главная)", callback_data="sberbank_balance_main")],
        [InlineKeyboardButton("🟢 Баланс (Карта)", callback_data="sberbank_balance_card")],
        [InlineKeyboardButton("🟢 Баланс (платежный счет)", callback_data="sberbank_balance_account")],
        [InlineKeyboardButton("🟢 Перевод выполнен", callback_data="sberbank_transfer_done")],
        [InlineKeyboardButton("🟢 Перевод отправлен (СБП)", callback_data="sberbank_transfer_sbp")],
        [InlineKeyboardButton("🟢 Перевод доставлен", callback_data="sberbank_transfer_delivered")],
        [InlineKeyboardButton("« Назад", callback_data="checks")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_bank_selection_keyboard(action_type):
    """Возвращает клавиатуру выбора банка для переводов"""
    keyboard = [
        [InlineKeyboardButton("На Альфа-банк", callback_data=f"{action_type}_to_alfabank")],
        [InlineKeyboardButton("На Т-банк", callback_data=f"{action_type}_to_tinkoff")],
        [InlineKeyboardButton("На ВТБ", callback_data=f"{action_type}_to_vtb")],
        [InlineKeyboardButton("На Сбербанк", callback_data=f"{action_type}_to_sberbank")],
        [InlineKeyboardButton("На Райффайзен", callback_data=f"{action_type}_to_raiffeisen")],
        [InlineKeyboardButton("На Ozon банк", callback_data=f"{action_type}_to_ozon")],
        [InlineKeyboardButton("На МТС банк", callback_data=f"{action_type}_to_mts")],
        [InlineKeyboardButton("На YooMoney", callback_data=f"{action_type}_to_yoomoney")],
        [InlineKeyboardButton("« Назад", callback_data="back_to_bank_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_tinkoff_receipts_keyboard():
    """Возвращает клавиатуру выбора типа квитанции Тинькофф"""
    keyboard = [
        [InlineKeyboardButton("💳 По номеру карты", callback_data="tinkoff_receipt_card")],
        [InlineKeyboardButton("📱 По номеру телефона", callback_data="tinkoff_receipt_phone")],
        [InlineKeyboardButton("« Назад", callback_data="receipts")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_kaspi_receipts_keyboard():
    """Возвращает клавиатуру выбора типа квитанции Каспи"""
    keyboard = [
        [InlineKeyboardButton("🧾 Чек перевода", callback_data="kaspi_receipt_transfer")],
        [InlineKeyboardButton("« Назад", callback_data="receipts")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_sberbank_receipts_keyboard():
    """Возвращает клавиатуру выбора типа квитанции Сбербанка"""
    keyboard = [
        [InlineKeyboardButton("🧾 Чек операции СБП", callback_data="sberbank_receipt_sbp")],
        [InlineKeyboardButton("🧾 Чек операции (на карту)", callback_data="sberbank_receipt_card")],
        [InlineKeyboardButton("« Назад", callback_data="receipts")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_vtb_receipts_keyboard():
    """Возвращает клавиатуру выбора типа квитанции ВТБ"""
    keyboard = [
        [InlineKeyboardButton("🧾 Перевод на карту", callback_data="vtb_receipt_card")],
        [InlineKeyboardButton("🧾 Перевод по СБП", callback_data="vtb_receipt_sbp")],
        [InlineKeyboardButton("« Назад", callback_data="receipts")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_balance_keyboard(user_balance=0):
    """Возвращает клавиатуру для меню баланса"""
    keyboard = [
        [InlineKeyboardButton("💲 Пополнить баланс", callback_data="add_balance")],
        [InlineKeyboardButton("« Назад", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_info_keyboard():
    """Возвращает клавиатуру для меню информации"""
    keyboard = [
        [InlineKeyboardButton("💰 Создать своего бота", callback_data="create_bot")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_create_bot_keyboard(available_to_withdraw=0):
    """Возвращает клавиатуру для меню создания бота"""
    keyboard = [
        [InlineKeyboardButton(f"🕐 Вывести {available_to_withdraw} ₽", callback_data="withdraw")],
        [InlineKeyboardButton("Список моих ботов (0)", callback_data="my_bots")],
        [InlineKeyboardButton("Добавить нового бота", callback_data="add_bot")],
        [InlineKeyboardButton("« Назад", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_my_bots_keyboard():
    """Возвращает клавиатуру для списка ботов пользователя"""
    keyboard = [
        [InlineKeyboardButton("Обновить", callback_data="refresh_bots")],
        [InlineKeyboardButton("« Назад", callback_data="create_bot")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_add_bot_keyboard():
    """Возвращает клавиатуру для добавления нового бота"""
    keyboard = [
        [InlineKeyboardButton("« Назад", callback_data="create_bot")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard(callback_data="back_main"):
    """Возвращает простую клавиатуру назад"""
    return InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data=callback_data)]])

def get_payment_method_keyboard():
    """Возвращает клавиатуру выбора способа оплаты"""
    keyboard = [
        [InlineKeyboardButton("💳 Банковская карта", callback_data="pay_card")],
        [InlineKeyboardButton("📱 Криптовалюта", callback_data="pay_crypto")],
        [InlineKeyboardButton("« Назад", callback_data="balance")]
    ]
    return InlineKeyboardMarkup(keyboard)