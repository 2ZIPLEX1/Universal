import os
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()

# ID администратора (для кнопки поддержки)
ADMIN_ID = 5657066026

# Токен бота
TOKEN = "7980749058:AAHCKw7AiWkok1aNt_zD6-p6uoU5CCb60ZQ"

# ID и URL канала
CHANNEL_ID = "-1002659449043"  # Замените на ID вашего канала
CHANNEL_URL = "https://t.me/+SN8kyI_Yd5w3Yzli"  # Замените на URL вашего канала

# URL изображений для меню
MENU_IMAGES = {
    "info": "file:///C:/Users/vania/OneDrive/Desktop/photo_2025-05-20_19-21-43.jpg",  # Замените на реальный URL
    "balance": "file:///C:/Users/vania/OneDrive/Desktop/photo_2025-05-20_19-21-43.jpg",  # Замените на реальный URL
    "checks": "file:///C:/Users/vania/OneDrive/Desktop/photo_2025-05-20_19-21-43.jpg",  # Замените на реальный URL
    "receipts": "file:///C:/Users/vania/OneDrive/Desktop/photo_2025-05-20_19-21-43.jpg"  # Замените на реальный URL
}
# Пути к файлам
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Настройки базы данных
DB_PATH = os.path.join(BASE_DIR, "db", "bot.db")

# Цены на услуги
PRICES = {
    "check": 50,  # Цена за чек в рублях
    "receipt": 70  # Цена за квитанцию в рублях
}

# Процент реферальных отчислений
REFERRAL_PERCENTAGE = 10  # 10% от суммы покупки

# Минимальная сумма для вывода
MIN_WITHDRAWAL = 2000  # Минимальная сумма для вывода в рублях