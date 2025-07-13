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

# --- Размер чека (чуть-чуть вытянутый) ---
custom_width = 365  
custom_height = 640  # Увеличил высоту
custom_page_size = (custom_width, custom_height)
c = canvas.Canvas(pdf_file, pagesize=custom_page_size)
width, height = custom_page_size

# --- Логотип (поднял чуть выше) ---
logo_width, logo_height = 40, 40
logo_x = (width - logo_width) / 2
c.drawImage(logo_path, logo_x, height - 75, width=logo_width, height=logo_height, mask='auto')

# --- Дата и время ---
c.setFont("DejaVu", 9)
c.setFillColorRGB(0.5, 0.5, 0.5)  # Серый цвет
c.drawString(25, height - 120, "19.11.2024  23:24:20")  # Подвинул чуть ниже

# --- "Итого" и сумма ---
c.setFillColorRGB(0, 0, 0)
c.setFont("SFPro-Semibold", 20)  
c.drawString(20, height - 145, "Итого")
c.drawRightString(width - 20, height - 145, "840 ₽")

# --- Желтая полоска после "Итого" ---
c.setStrokeColorRGB(1, 0.8, 0)
c.setLineWidth(1)
c.line(20, height - 165, width - 20, height - 165)

# --- Текстовые поля ---
c.setFont("DejaVu", 10)
fields = [
    ("Перевод", "По номеру телефона"),
    ("Статус", "Успешно"),
    ("Сумма", "840 ₽"),
    ("Комиссия", "Без комиссии"),
    ("Отправитель", "Иван Ульяничев"),
    ("Телефон получателя", "+7 (904) 101-58-82"),
    ("Получатель", "Ярослав Е."),
    ("Сообщение", "Куку")
]

y_position = height - 200  # Поднял чуть выше
line_spacing = 27  # Увеличил немного расстояние между строками

for field, value in fields:
    c.drawString(20, y_position, field)
    c.drawRightString(width - 20, y_position, value)
    y_position -= line_spacing

# --- Подпись (убрано лишнее пространство) ---
y_position -= 24  # Чуть ближе к тексту

if signature_path:
    c.drawImage(signature_path, width - 250, y_position - 60, width=230, height=95, mask='auto')

# --- Желтая полоска перед "Квитанция" ---
y_position -= 90
c.setStrokeColorRGB(1, 0.8, 0)
c.setLineWidth(1)
c.line(20, y_position, width - 20, y_position)

# --- Квитанция ---
c.setFont("DejaVu", 9.5)
c.setFillColorRGB(0, 0, 0)  # Черный цвет
c.drawString(20, y_position - 30, "Квитанция  № 1-19-598-700-433")

# --- "По вопросам зачисления" ---
c.setFillColorRGB(0.5, 0.5, 0.5)
c.drawString(20, y_position - 50, "По вопросам зачисления обращайтесь к получателю")

# --- "Служба поддержки" ---
support_text = "Служба поддержки "
support_email = "fb@tbank.ru"
text_width = c.stringWidth(support_text, "DejaVu", 9.5)

c.setFillColorRGB(0.5, 0.5, 0.5)  # Серый цвет
c.drawString(20, y_position - 75, support_text)

c.setFillColorRGB(0.2, 0.5, 1)  # Голубой цвет
c.drawString(20 + text_width, y_position - 75, support_email)

# --- Финальный отступ ---
y_position -= 1  # Убрано лишнее белое пространство

# --- Сохранение PDF ---
c.showPage()
c.save()

print(f"✅ PDF чек сохранен: {pdf_file}")
