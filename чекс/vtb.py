from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from textwrap import wrap

# --- Parameters ---
pdf_file = "vtb_check.pdf"
logo_path = "vtb_logo.png"
podpis_path = "podvtb.png"

# --- Font Registration ---
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))

font_regular = 'DejaVuSans'
font_bold = 'DejaVuSans-Bold'

# --- Check Size and Margins ---
custom_width = 330
custom_height = 580
margin_x = 25
content_width = custom_width - (2 * margin_x)
custom_page_size = (custom_width, custom_height)
c = canvas.Canvas(pdf_file, pagesize=custom_page_size)
width, height = custom_page_size

# --- Wrap Text Function ---
def wrap_text(text, width, font_name, font_size):
    """Wrap text within a given width."""
    words = text.split()
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_width = stringWidth(word, font_name, font_size)
        space_width = stringWidth(' ', font_name, font_size)

        if current_width + word_width <= width:
            current_line.append(word)
            current_width += word_width + space_width
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width + space_width

    lines.append(' '.join(current_line))
    return lines

# --- Logo ---
logo_width = 90
logo_height = 90
logo_x = (width - logo_width) / 2.25
c.drawImage(logo_path, logo_x, height - 93, width=logo_width, height=logo_height, mask='auto')

# --- Blue Line ---
c.setStrokeColorRGB(0, 0.3, 1)
c.setLineWidth(0.85)
c.line(margin_x, height - 80, width - margin_x, height - 80)

# --- Header Text ---
c.setFont(font_regular, 11)
c.drawCentredString(width / 2, height - 110, "Исходящий перевод СБП")
c.drawCentredString(width / 2, height - 130, "Никита Сергеевич Д")

# --- Fields ---
fields = [
    ("Статус", "Выполнено", True),
    ("Дата операции", "18.11.2024, 17:23"),
    ("Счет списания", "*9889"),
    ("Имя плательщика", "Никита Сергеевич Д."),
    ("Получатель", "НИКИТА СЕРГЕЕВИЧ Д."),
    ("Телефон получателя", "+7 (996) 002-84-56"),
    ("Банк получателя", "Т-Банк (Тинькофф)"),
    ("ID операции в СБП", ""),
    ("Комиссия за перевод", "0 ₽"),
    ("Сумма перевода с   учетом комиссии", "17,24 ₽")
]

y_position = height - 165
line_spacing = 28

for field, value, *args in fields:
    c.setFont(font_regular, 9)
    c.setFillColorRGB(0, 0, 0)

    # Wrapping text
    field_lines = wrap_text(field, content_width / 2, font_regular, 9)
    value_lines = wrap_text(value, content_width / 2, font_regular, 9)

    # Special processing for operation ID and transfer amount
    if field == "ID операции в СБП":
        c.drawString(margin_x, y_position, field)
        id_part1 = "B432314231608414000011001"
        id_part2 = "1381101"
        c.drawRightString(width - margin_x, y_position, id_part1)
        c.drawRightString(width - margin_x, y_position - 15, id_part2)
        y_position -= 15
    elif field == "Сумма перевода с учетом комиссии":
        # Разделим длинный текст на две строки более аккуратно
        first_line = "Сумма перевода с      "
        second_line = "     учетом комиссии"
        c.drawString(margin_x, y_position, first_line)
        c.drawString(margin_x, y_position - 15, second_line)
        c.drawRightString(width - margin_x, y_position - 14, "17,24 ₽")
        y_position -= 20
    else:
        c.drawString(margin_x, y_position, field_lines[0])
        if args and args[0]:
            c.setFillColorRGB(0, 0.5, 0)
        c.drawRightString(width - margin_x, y_position, value_lines[0])

    extra_lines = max(len(field_lines), len(value_lines)) - 1
    if extra_lines > 0:
        for i in range(extra_lines):
            y_position -= 15
            if i + 1 < len(field_lines):
                c.drawString(margin_x, y_position, field_lines[i + 1])
            if i + 1 < len(value_lines):
                c.drawRightString(width - margin_x, y_position, value_lines[i + 1])

    y_position -= line_spacing

# --- Second Blue Line ---
y_position -= -10
c.setStrokeColorRGB(0, 0.3, 1)
c.setLineWidth(0.85)
c.line(margin_x, y_position, width - margin_x, y_position)

# --- Total Amount ---
y_position -= 40
c.setFont(font_regular, 15)
c.setFillColorRGB(0, 0, 0)
c.drawString(margin_x, y_position, "Сумма операции")
c.drawRightString(width - margin_x, y_position, "17.24 ₽")

# --- Signature ---
y_position -= 25
if podpis_path:
    c.drawImage(podpis_path, (width - 260) / 2, y_position - 40, width=250, height=50, mask='auto')

# --- Save PDF ---
c.showPage()
c.save()

print(f"✅ PDF receipt saved: {pdf_file}")