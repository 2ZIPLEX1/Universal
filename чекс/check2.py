from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader

# --- Параметры ---
pdf_file = "sberbank_check.pdf"
logo_path = "sber_logo.png"  # Логотип СберБанка
signature_path = "signature_sber_.png"  # Подпись "ПАО Сбербанк Операция выполнена"

# --- Регистрация шрифтов ---
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'DejaVuSans-Bold.ttf'))

# --- Размер чека (увеличен, чтобы не обрезался) ---
custom_width = 400  
custom_height = 910  # Увеличил высоту для подписи
custom_page_size = (custom_width, custom_height)
c = canvas.Canvas(pdf_file, pagesize=custom_page_size)
width, height = custom_page_size

# --- Логотип (уменьшена высота, сделан сплюснутым) ---
logo_width, logo_height = 170, 35  # Сделал ниже
logo_x = (width - logo_width) / 2
c.drawImage(logo_path, logo_x, height - 70, width=logo_width, height=logo_height, mask='auto')

# --- Заголовок (по центру, большой, но НЕ жирный) ---
c.setFont("DejaVu", 15.5)
c.setFillColorRGB(0.5, 0.5, 0.5)  # Серый цвет
c.drawCentredString(width / 2, height - 105, "Чек по операции")
c.drawCentredString(width / 2, height - 125, "6 февраля 2025 07:56:34 (МСК)")

# --- Пунктирная линия (серого цвета) ---
c.setStrokeColorRGB(0.7, 0.7, 0.7)  
c.setDash(3, 3)  
c.line(30, height - 135, width - 30, height - 135)

# --- Основной текст (серый заголовок, чёрные данные под ним) ---
fields = [
    ("Операция", "Перевод клиенту СберБанка"),
    ("ФИО получателя", "Максим Павлович З."),
    ("Телефон получателя", "+7(908) 574-21-78"),
    ("Номер карты получателя", "**** 4001"),
    ("", ""),  # Пропуск перед "ФИО отправителя"
    ("ФИО отправителя", "Семён Валерьевич Д."),
    ("Счёт отправителя", "**** 2315"),
    ("Сумма перевода", "38,00 ₽"),
    ("Комиссия", "0,00 ₽"),
]

y_position = height - 170
line_spacing = 20  # Уменьшил отступы между строками

for field, value in fields:
    if field:  
        c.setFillColorRGB(0.5, 0.5, 0.5)  # Серый цвет заголовков
        c.setFont("DejaVu", 13.5)  # Увеличил шрифт заголовков
        c.drawString(31, y_position, field)

    y_position -= 22  # Отступ перед чёрным текстом

    c.setFillColorRGB(0, 0, 0)  # Чёрный цвет значений
    c.setFont("DejaVu", 14)  # Значения ещё больше
    c.drawString(31, y_position, value)
    
    y_position -= line_spacing

# --- Дополнительный отступ после "0,00 ₽" ---
y_position -= 25  # Добавил отступ перед "Номер документа"

# --- Оставшиеся данные ---
fields_continued = [
    ("Номер документа", "1000000000546882360"),
    ("Код авторизации", "804014"),
]

for field, value in fields_continued:
    c.setFillColorRGB(0.5, 0.5, 0.5)  
    c.setFont("DejaVu", 13.5)  
    c.drawString(30, y_position, field)

    y_position -= 18  

    c.setFillColorRGB(0, 0, 0)  
    c.setFont("DejaVu", 14)  
    c.drawString(30, y_position, value)
    
    y_position -= line_spacing

# --- Пунктирная линия (серого цвета) ---
c.setStrokeColorRGB(0.7, 0.7, 0.7)  
c.setDash(3, 3)  
c.line(30, y_position - 15, width - 30, y_position - 15)

# --- Блок "Дополнительная информация" (по макету) ---
y_position -= 40
c.setFont("DejaVu", 12)
c.setFillColorRGB(0.5, 0.5, 0.5)  # Серый цвет заголовка
c.drawString(30, y_position, "Дополнительная информация")

y_position -= 20
c.setFont("DejaVu", 14)  # Сделал больше
c.setFillColorRGB(0, 0, 0)  # Чёрный цвет текста
c.drawString(30, y_position, "Если вы отправили деньги не тому человеку,")
y_position -= 20
c.drawString(30, y_position, "обратитесь к получателю перевода.")
y_position -= 20
c.drawString(30, y_position, "Деньги может вернуть только получатель.")

# --- Подпись "ПАО Сбербанк Операция выполнена" (по центру, больше и растянута) ---
y_position -= 55  # Добавил больше места перед подписью
if signature_path:
    c.drawImage(signature_path, (width - 260) / 2, y_position - 70, width=260, height=79, mask='auto')  # Увеличил и растянул

# --- Сохранение PDF ---
c.showPage()
c.save()

print(f"✅ PDF чек СберБанка сохранен: {pdf_file}")
