from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4

# --- Параметры ---
pdf_file = "alfabank_check.pdf"
logo_path = "alfalogo.png"  # Логотип банка
signature_path = "alfapodp.png"  # Подпись
footer_image_path = "adralfa.png"  # Адрес внизу

# --- Регистрация шрифтов ---
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('SFPro-Semibold', 'SFProDisplay-Semibold.ttf'))

# --- Размер чека ---
custom_width = 750
custom_height = 970
c = canvas.Canvas(pdf_file, pagesize=(custom_width, custom_height))
width, height = custom_width, custom_height

# --- Логотип ---
logo_width, logo_height = 70, 70
c.drawImage(logo_path, 20, height - 125, width=logo_width, height=logo_height, mask='auto')

# --- Дата и время формирования ---
c.setFont("DejaVu", 13)
c.setFillColorRGB(0.5, 0.5, 0.5)
c.drawRightString(width - 50, height - 60, "Сформирована")
c.drawRightString(width - 50, height - 80, "16.02.2025 14:44 мск")

# --- Заголовок ---
c.setFont("SFPro-Semibold", 25)
c.setFillColorRGB(0, 0, 0)
c.drawString(40, height - 160, "Квитанция о переводе по СБП")

# --- Данные чека ---
fields_left = [
    ("Сумма перевода", "1 017 RUR"),
    ("Комиссия", "0 RUR"),
    ("Дата и время перевода", "03.01.2025 14:01:06 мск"),
    ("Номер операции", "C160301250535614"),
    ("Получатель", "Семен Валерьевич Д")
]

fields_right = [
    ("Номер телефона получателя", "79085742810"),
    ("Банк получателя", "Сбербанк"),
    ("Счёт списания", "40817810017490000072"),
    ("Идентификатор операции в СБП", "B50031101073650D0000180011410901"),
    ("Сообщение получателю", "Перевод денежных средств")
]

# --- Отрисовка полей ---
y_position = height - 200
line_spacing = 50

for left, right in zip(fields_left, fields_right):
    # Левая колонка
    c.setFont("DejaVu", 13)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(40, y_position, left[0])
    c.setFont("DejaVu", 14.5)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(40, y_position - 20, left[1])

    # Правая колонка
    c.setFont("DejaVu", 13)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(width/2 - 16, y_position, right[0])
    c.setFont("DejaVu", 14.5)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(width/2 - 16, y_position - 20, right[1])

    y_position -= line_spacing

# --- Подпись ---
y_position -= 50
c.drawImage(signature_path, 27, y_position - 70, width=260, height=115, mask='auto')

# --- Адрес и контакты банка ---
c.drawImage(footer_image_path, width - 420, 30, width=380, height=57, mask='auto')

# --- Сохранение PDF ---
c.showPage()
c.save()

print(f"✅ PDF чек сохранен: {pdf_file}")
