from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader

# --- Параметры ---
pdf_file = "check.pdf"
logo_path = "logo2.png"  # Логотип банка
signature_path = "signature2.png"  # Подпись

# --- Регистрация шрифтов ---
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('SFPro-Semibold', 'SFProDisplay-Semibold.ttf'))

# --- Размер чека (уменьшенный до размера примера) ---
custom_width = 355  
custom_height = 650  # Уменьшил до размера примера
custom_page_size = (custom_width, custom_height)
c = canvas.Canvas(pdf_file, pagesize=custom_page_size)
width, height = custom_page_size

# --- Логотип (центрированный, вверху) ---
logo_width, logo_height = 40, 40
logo_x = (width - logo_width) / 2
c.drawImage(logo_path, logo_x, height - 65, width=logo_width, height=logo_height, mask='auto')

# --- Дата и время (над "Итого") ---
c.setFont("DejaVu", 9)
c.setFillColorRGB(0.5, 0.5, 0.5)  # Серый цвет
c.drawString(25, height - 95, "19.11.2024 23:24:20")

# --- "Итого" и сумма (крупнее, как в примере) ---
c.setFillColorRGB(0, 0, 0)
c.setFont("SFPro-Semibold", 20)  # Подходящий размер шрифта
c.drawString(25, height - 120, "Итого")
c.drawRightString(width - 25, height - 120, "840 ₽")

# --- Желтая полоска после "Итого" (тоньше) ---
c.setStrokeColorRGB(1, 0.8, 0)
c.setLineWidth(0.8)  # Тоньше линия
c.line(25, height - 140, width - 20, height - 140)

# --- Текстовые поля с улучшенным форматированием ---
c.setFont("DejaVu", 9.5)
fields = [
    ("Перевод", "По номеру телефона"),
    ("Статус", "Успешно"),
    ("Сумма", "840 ₽"),
    ("Комиссия", "Без комиссии"),
    ("Отправитель", "Иван Ульяничев"),
    ("Телефон получателя", "+7 (904) 101-58-82"),
    ("Получатель", "Ярослав Е."),
    ("Сообщение", "Куку"),
    ("Банк получателя", "Т-Банк"),
    ("Счет списания", "400030007000****9876"),
    ("Идентификатор операции", "A10020030040060V00001000200")
]

y_position = height - 165
line_spacing = 25  # Компактное расстояние

for field, value in fields:
    # Названия полей черным цветом (не серым)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(25, y_position, field)
    
    # Значения черным цветом
    c.setFillColorRGB(0, 0, 0)
    c.drawRightString(width - 25, y_position, value)
    y_position -= line_spacing

# --- СБП на новой строке (ближе к строчке выше) ---
y_position -= -10  # Уменьшенный отступ вместо line_spacing
c.setFillColorRGB(0, 0, 0)
c.drawString(25, y_position, "СБП")
c.drawRightString(width - 25, y_position, "03000")
y_position -= line_spacing

# --- Подпись (оптимизированное размещение) ---
y_position -= 20

if signature_path:
    c.drawImage(signature_path, width - 250, y_position - 50, width=230, height=85, mask='auto')

# --- Желтая полоска перед "Квитанция" ---
y_position -= 60
c.setStrokeColorRGB(1, 0.8, 0)
c.setLineWidth(0.8)
c.line(25, y_position, width - 20, y_position)

# --- Квитанция (точно как в примере) ---
c.setFont("DejaVu", 10)
c.setFillColorRGB(0, 0, 0)
c.drawString(25, y_position - 25, "Квитанция № 1-19-598-700-433")

# --- Дополнительные строки внизу ---
c.setFillColorRGB(0.5, 0.5, 0.5)
c.setFont("DejaVu", 9)
c.drawString(25, y_position - 45, "По вопросам зачисления обращайтесь к получателю")

# --- "Служба поддержки" ---
support_text = "Служба поддержки "
support_email = "fb@tbank.ru"
text_width = c.stringWidth(support_text, "DejaVu", 9)

c.setFillColorRGB(0.5, 0.5, 0.5)
c.drawString(25, y_position - 65, support_text)

c.setFillColorRGB(0.2, 0.5, 1)  # Голубой цвет для email
c.drawString(25 + text_width, y_position - 65, support_email)

# --- Сохранение PDF ---
c.showPage()
c.save()

print(f"✅ PDF чек сохранен: {pdf_file}")