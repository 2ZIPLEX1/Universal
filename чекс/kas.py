from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.units import mm
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate
from reportlab.platypus.frames import Frame
import math

# Register Cyrillic-compatible fonts
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))

class ScallopedBorderCanvas:
    """Class to draw scalloped (rounded) borders on the page background"""
    @staticmethod
    def draw_background(canvas, doc):
        # Draw light gray background for entire page
        canvas.setFillColor(colors.Color(0.94, 0.94, 0.94))  # Light gray
        canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)
        
        # Calculate coordinates for the white content area
        content_margin = 25*mm  # Margin for white content area
        left_x = content_margin
        bottom_y = content_margin
        width = doc.pagesize[0] - 2*content_margin
        height = doc.pagesize[1] - 2*content_margin
        
        # Store white content area dimensions for reference in other methods
        doc._white_content = {
            'x': left_x,
            'y': bottom_y,
            'width': width,
            'height': height
        }
        
        # Draw white background with scalloped borders
        canvas.setFillColor(colors.white)
        
        # Parameters for scalloped border
        num_scallops = 26  # Exactly 26 scallops per row as requested
        scallop_width = width / num_scallops
        scallop_height = 3*mm  # Height of scallop
        
        # Begin the path for the white content area
        path = canvas.beginPath()
        
        # Start at the top-left corner
        path.moveTo(left_x, bottom_y + height)
        
        # Top border with scallops
        for i in range(num_scallops):
            # Calculate points for bezier curve to simulate half-circle
            x1 = left_x + i * scallop_width
            y1 = bottom_y + height
            
            # Control points for bezier curve
            cx1 = x1 + scallop_width * 0.25
            cy1 = y1
            cx2 = x1 + scallop_width * 0.75
            cy2 = y1 - scallop_height
            
            # End point
            x2 = x1 + scallop_width
            y2 = y1
            
            # Draw line to start of scallop if this is not the first point
            if i > 0:
                path.lineTo(x1, y1)
                
            # Draw bezier curve for the scallop
            path.curveTo(cx1, cy1, cx2, cy2, x2, y2)
        
        # Right side (straight)
        path.lineTo(left_x + width, bottom_y)
        
        # Bottom border with scallops (reverse direction)
        for i in range(num_scallops):
            # Calculate points for bezier curve
            x1 = left_x + width - i * scallop_width
            y1 = bottom_y
            
            # Control points for bezier curve
            cx1 = x1 - scallop_width * 0.25
            cy1 = y1
            cx2 = x1 - scallop_width * 0.75
            cy2 = y1 + scallop_height
            
            # End point
            x2 = x1 - scallop_width
            y2 = y1
            
            # Draw line to start of scallop if this is not the first point
            if i > 0:
                path.lineTo(x1, y1)
                
            # Draw bezier curve for the scallop
            path.curveTo(cx1, cy1, cx2, cy2, x2, y2)
        
        # Left side (straight)
        path.lineTo(left_x, bottom_y + height)
        
        # Close and fill the path
        path.close()
        canvas.drawPath(path, fill=1, stroke=0)

def create_kaspi_receipt(output_file="kaspi_receipt.pdf", 
                        amount="7 370,90 ₸", 
                        name="Мармеладова София",
                        receipt_number="1426736812",
                        date_time="27.08.2024 03:45",
                        commission="0 ₸",
                        sender="Мармеладова София",
                        source="Kaspi Gold",
                        recipient="Kaspi"):
    
    # Настраиваемые параметры чека (можно изменять)
    # --------------------
    # Цвета
    dark_green = colors.Color(0.1, 0.45, 0.1)  # Более темный зеленый цвет для текста
    light_green = colors.Color(0.8, 0.93, 0.8)  # Светло-зеленый для фона
    
    # Размеры и отступы
    logo_width = 70  # Ширина логотипа
    logo_height = 70  # Высота логотипа
    logo_left_padding = 15  # Отступ логотипа слева
    logo_top_padding = 15   # Отступ логотипа сверху
    
    # Отступы текста
    text_left_padding = 30  # Отступ текста слева
    text_padding = 15       # Отступ между строками
    # --------------------
    
    # Create document with custom page template
    pagesize = A4
    doc = BaseDocTemplate(
        output_file, 
        pagesize=pagesize,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )
    
    # Create frame and page template
    frame = Frame(
        doc.leftMargin, 
        doc.bottomMargin, 
        doc.width, 
        doc.height,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0
    )
    
    # Add page template with scalloped background
    template = PageTemplate(
        id='normal',
        frames=[frame],
        onPage=ScallopedBorderCanvas.draw_background
    )
    
    doc.addPageTemplates([template])
    
    # Container for elements
    elements = []
    
    # Define styles - увеличенные размеры шрифтов
    title_style = ParagraphStyle(
        'TitleStyle',
        fontName='DejaVuSans-Bold',  # Жирный шрифт
        fontSize=20,  # Больше размер
        textColor=dark_green,
        alignment=TA_LEFT,
        leading=24,
    )
    
    amount_style = ParagraphStyle(
        'AmountStyle',
        fontName='DejaVuSans-Bold',
        fontSize=42,  # Еще больше размер
        textColor=dark_green,
        alignment=TA_LEFT,
        leading=46,
    )
    
    name_style = ParagraphStyle(
        'NameStyle',
        fontName='DejaVuSans',
        fontSize=22,  # Увеличенный размер
        textColor=colors.black,
        alignment=TA_LEFT,
        leading=26,
    )
    
    label_style = ParagraphStyle(
        'LabelStyle',
        fontName='DejaVuSans',
        fontSize=16,  # Увеличенный размер
        textColor=colors.gray,
        alignment=TA_LEFT,
    )
    
    value_style = ParagraphStyle(
        'ValueStyle',
        fontName='DejaVuSans',
        fontSize=16,  # Увеличенный размер
        textColor=colors.black,
        alignment=TA_RIGHT,
    )
    
    # Try to load logo - placed correctly within white area
    try:
        logo_img = Image('kaspi_logo.png', width=logo_width, height=logo_height)
    except:
        # If logo file not found, create a placeholder
        logo_img = Paragraph("LOGO", ParagraphStyle(
            'Logo',
            fontName='DejaVuSans-Bold',
            fontSize=20,
            textColor=colors.red
        ))
    
    # Logo positioned within the white area
    elements.append(Spacer(1, logo_top_padding))
    header_data = [[logo_img, '']]
    header_table = Table(header_data, colWidths=[logo_width, doc.width-logo_width])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (0, 0), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('LEFTPADDING', (0, 0), (0, 0), logo_left_padding),
        ('RIGHTPADDING', (0, 0), (0, 0), 0),
    ]))
    
    elements.append(header_table)
    elements.append(Spacer(1, 10))
    
    # Green background for success message and amount - full width
    # Зеленое поле должно быть выше
    elements.append(Spacer(1, 0))  # Уменьшен верхний отступ
    
    success_data = [
        [Paragraph("Перевод успешно совершен", title_style)],
        [Paragraph(amount, amount_style)],
    ]
    
    # Зеленый блок полной ширины
    success_table = Table(success_data, colWidths=[doc.width])
    success_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 1), light_green),
        ('ALIGN', (0, 0), (0, 1), 'LEFT'),
        ('VALIGN', (0, 0), (0, 1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (0, 1), text_left_padding),
        ('RIGHTPADDING', (0, 0), (0, 1), text_left_padding),
        ('TOPPADDING', (0, 0), (0, 0), 20),  # Больше верхний отступ
        ('BOTTOMPADDING', (0, 0), (0, 0), 5),
        ('TOPPADDING', (0, 1), (0, 1), 5),
        ('BOTTOMPADDING', (0, 1), (0, 1), 20),  # Больше нижний отступ
    ]))
    
    elements.append(success_table)
    elements.append(Spacer(1, 20))
    
    # Add name with proper alignment
    name_container = Table([[Paragraph(name, name_style)]], colWidths=[doc.width])
    name_container.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (0, 0), text_left_padding),
        ('RIGHTPADDING', (0, 0), (0, 0), 0),
        ('TOPPADDING', (0, 0), (0, 0), 0),
        ('BOTTOMPADDING', (0, 0), (0, 0), 0),
    ]))
    elements.append(name_container)
    elements.append(Spacer(1, 20))
    
    # Create details table - all rows aligned
    details_data = [
        [Paragraph("Тип перевода", label_style), Paragraph(f"Перевод клиенту<br/>{recipient}", value_style)],
        [Paragraph("№ квитанции", label_style), Paragraph(receipt_number, value_style)],
        [Paragraph("Дата и время<br/>по Астане", label_style), Paragraph(date_time, value_style)],
        [Paragraph("Комиссия", label_style), Paragraph(commission, value_style)],
        [Paragraph("Отправитель", label_style), Paragraph(sender, value_style)],
        [Paragraph("Откуда", label_style), Paragraph(source, value_style)],
    ]
    
    # Set column widths for details
    col_widths = [doc.width * 0.4, doc.width * 0.6]
    
    details_table = Table(details_data, colWidths=col_widths)
    details_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (1, 4), 0.5, colors.lightgrey),
        ('TOPPADDING', (0, 0), (1, -1), text_padding),
        ('BOTTOMPADDING', (0, 0), (1, -1), text_padding),
    ]))
    
    # Place details table in a container for consistent alignment
    details_container = Table([[details_table]], colWidths=[doc.width])
    details_container.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (0, 0), text_left_padding),
        ('RIGHTPADDING', (0, 0), (0, 0), text_left_padding),
        ('TOPPADDING', (0, 0), (0, 0), 0),
        ('BOTTOMPADDING', (0, 0), (0, 0), 0),
    ]))
    
    elements.append(details_container)
    
    # Build the document
    doc.build(elements)
    
    return output_file

if __name__ == "__main__":
    # Example usage with default values
    create_kaspi_receipt()
    print("PDF receipt has been generated!")
    
    # Пример с настройкой параметров
    # create_kaspi_receipt(
    #    output_file="custom_receipt.pdf",
    #    amount="10 000,00 ₸",
    #    name="Иванов Иван",
    #    receipt_number="9876543210",
    #    date_time="28.02.2023 14:30",
    #    commission="100 ₸",
    #    sender="Иванов Иван",
    #    source="Kaspi Gold",
    #    recipient="Kaspi"
    # )