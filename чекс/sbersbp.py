from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader

# --- Параметры ---
pdf_file = "spb_check.pdf"
logo_path = "sber_logo.png"  # Логотип СПБ Банка
signature_path = "signature_sbp_sber_.png"  # Подпись "СПБ Банк Операция выполнена"

# --- Регистрация шрифтов ---
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'DejaVuSans-Bold.ttf'))

# --- Размер чека ---
custom_width = 420
custom_height = 1100  # Высота увеличена для подписи
custom_page_size = (custom_width, custom_height)
c = canvas.Canvas(pdf_file, pagesize=custom_page_size)
width, height = custom_page_size

# --- Логотип ---
logo_width, logo_height = 170, 35  # Размер логотипа
logo_x = (width - logo_width) / 2
c.drawImage(logo_path, logo_x, height - 60, width=logo_width, height=logo_height, mask='auto')

# --- Заголовок ---
c.setFont("DejaVu", 16)
c.setFillColorRGB(0.5, 0.5, 0.5)  # Серый цвет
c.drawCentredString(width / 2, height - 95, "Чек по операции")
c.drawCentredString(width / 2, height - 115, "31 января 2025 15:14:20 (МСК)")

# --- Пунктирная линия ---
c.setStrokeColorRGB(0.7, 0.7, 0.7)  
c.setLineWidth(1.5)
c.setDash(3, 3)  
c.line(30, height - 130, width - 30, height - 130)

# --- Основной текст ---
fields = [
    ("Операция", "Перевод по СБП"),
    ("ФИО получателя перевода", "Андрей Сергеевич П"),
    ("Номер телефона получателя", "+7 913 603-65-67"),
    ("Банк получателя", "ВТБ"),
    ("ФИО отправителя", "Семён Валерьевич Д"),
    ("Карта отправителя", "•••• 2315"),
    ("Сумма перевода", "3000.00 ₽"),
    ("Комиссия", "0.00 ₽"),
    ("Номер операции в СБП", "B5031121330042040000110011430703"),
]

y_position = height - 170
header_spacing = 20  # Отступ между серым и черным текстом
value_spacing = 36  # Увеличенный отступ между черными строками
special_spacing = 60  # Увеличенный отступ между ВТБ и ФИО, а также между 2315 и Сумма

for field, value in fields:
    c.setFillColorRGB(0.5, 0.5, 0.5)  # Серый цвет заголовков
    c.setFont("DejaVu", 14)
    c.drawString(31, y_position, field)
    
    y_position -= header_spacing  # Умеренный отступ между заголовком и значением
    
    c.setFillColorRGB(0, 0, 0)  # Чёрный цвет значений
    c.setFont("DejaVu", 16)
    c.drawString(31, y_position, value)
    
    if field in ["Банк получателя", "Карта отправителя"]:
        y_position -= special_spacing  # Больше места после ВТБ и 2315
    else:
        y_position -= value_spacing  # Обычный отступ между записями

# --- Подпись ---
y_position -= 20  # Отступ перед подписью
if signature_path:
    c.drawImage(signature_path, (width - 360) / 2, y_position - 130, width=360, height=140, mask='auto')

# --- Сохранение PDF ---
c.showPage()
c.save()

print(f"✅ PDF чек СПБ Банка сохранен: {pdf_file}")