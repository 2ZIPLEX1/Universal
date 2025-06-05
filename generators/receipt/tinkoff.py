import io
import os
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
import logging

logger = logging.getLogger(__name__)

class TinkoffReceiptGenerator:
    def __init__(self):
        # Дефолтные значения для квитанции по карте
        self.default_card_variables = {
            "transfer_amount": "5 500,50",
            "commission": "420,52",
            "recipient_card": "220220******1234",
            "recipient_bank": "Т-Банк",
            "recipient_name": "София Мармеладова М",
            "sender_name": "Валентин Дядька М",
            "status": "Успешно",
            "date_time": "22.05.2025 23:06:11",
            "receipt_number": "1-23-456-789-123"
        }
        
        # Пути к ресурсам
        self.assets_path = Path("static/assets/tinkoff")
        self.fonts_path = Path("static/fonts")
        
        # Создаем необходимые каталоги
        os.makedirs(self.assets_path, exist_ok=True)
        os.makedirs(self.fonts_path, exist_ok=True)
        
        # Регистрируем шрифты (если они доступны)
        self._register_fonts()

    def _register_fonts(self):
        """Регистрирует необходимые шрифты"""
        try:
            dejavu_path = self.fonts_path / "DejaVuSans.ttf"
            sfpro_path = self.fonts_path / "SFProDisplay-Semibold.ttf"
            
            if dejavu_path.exists():
                pdfmetrics.registerFont(TTFont('DejaVu', str(dejavu_path)))
            else:
                logger.warning(f"Шрифт DejaVu не найден по пути: {dejavu_path}")
                
            if sfpro_path.exists():
                pdfmetrics.registerFont(TTFont('SFPro-Semibold', str(sfpro_path)))
            else:
                logger.warning(f"Шрифт SFPro не найден по пути: {sfpro_path}")
                
        except Exception as e:
            logger.error(f"Ошибка при регистрации шрифтов: {e}")

    async def generate_card_receipt(self, variables=None):
        """Генерация квитанции по номеру карты"""
        # Объединяем дефолтные значения с переданными
        data = {**self.default_card_variables, **(variables or {})}
        
        try:
            # Создаем буфер для PDF
            buffer = io.BytesIO()
            
            # Создаем PDF
            self._create_pdf(buffer, data)
            
            # Получаем байты PDF
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Ошибка при создании PDF: {e}")
            # В случае ошибки создаем простой PDF с ошибкой
            return self._create_error_pdf(str(e))

    def _create_pdf(self, buffer, data):
        """Создает PDF с квитанцией"""
        # Размер чека
        custom_width = 365  
        custom_height = 640
        custom_page_size = (custom_width, custom_height)
        
        c = canvas.Canvas(buffer, pagesize=custom_page_size)
        width, height = custom_page_size

        # Логотип (если есть)
        logo_path = self.assets_path / "logo2.png"
        if logo_path.exists():
            logo_width, logo_height = 40, 40
            logo_x = (width - logo_width) / 2
            c.drawImage(str(logo_path), logo_x, height - 75, width=logo_width, height=logo_height, mask='auto')

        # Дата и время
        try:
            c.setFont("DejaVu", 9)
        except:
            c.setFont("Helvetica", 9)
            
        c.setFillColorRGB(0.5, 0.5, 0.5)  # Серый цвет
        c.drawString(25, height - 120, data["date_time"])

        # "Итого" и сумма
        c.setFillColorRGB(0, 0, 0)
        try:
            c.setFont("SFPro-Semibold", 20)
        except:
            c.setFont("Helvetica-Bold", 20)
            
        c.drawString(20, height - 145, "Итого")
        c.drawRightString(width - 20, height - 145, f"{data['transfer_amount']} ₽")

        # Желтая полоска после "Итого"
        c.setStrokeColorRGB(1, 0.8, 0)
        c.setLineWidth(1)
        c.line(20, height - 165, width - 20, height - 165)

        # Текстовые поля
        try:
            c.setFont("DejaVu", 10)
        except:
            c.setFont("Helvetica", 10)
            
        fields = [
            ("Перевод", "По номеру карты"),
            ("Статус", data["status"]),
            ("Сумма", f"{data['transfer_amount']} ₽"),
            ("Комиссия", f"{data['commission']} ₽"),
            ("Отправитель", data["sender_name"]),
            ("Карта получателя", data["recipient_card"]),
            ("Получатель", data["recipient_name"]),
            ("Банк получателя", data["recipient_bank"])
        ]

        y_position = height - 200
        line_spacing = 27

        for field, value in fields:
            c.drawString(20, y_position, field)
            c.drawRightString(width - 20, y_position, value)
            y_position -= line_spacing

        # Подпись (если есть)
        signature_path = self.assets_path / "signature2.png"
        if signature_path.exists():
            y_position -= 24
            c.drawImage(str(signature_path), width - 250, y_position - 60, width=230, height=95, mask='auto')
            y_position -= 90
        else:
            y_position -= 50

        # Желтая полоска перед "Квитанция"
        c.setStrokeColorRGB(1, 0.8, 0)
        c.setLineWidth(1)
        c.line(20, y_position, width - 20, y_position)

        # Квитанция
        try:
            c.setFont("DejaVu", 9.5)
        except:
            c.setFont("Helvetica", 9.5)
            
        c.setFillColorRGB(0, 0, 0)
        c.drawString(20, y_position - 30, f"Квитанция № {data['receipt_number']}")

        # "По вопросам зачисления"
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawString(20, y_position - 50, "По вопросам зачисления обращайтесь к получателю")

        # "Служба поддержки"
        support_text = "Служба поддержки "
        support_email = "fb@tbank.ru"
        text_width = c.stringWidth(support_text, "DejaVu" if "DejaVu" in c.getAvailableFonts() else "Helvetica", 9.5)

        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawString(20, y_position - 75, support_text)

        c.setFillColorRGB(0.2, 0.5, 1)
        c.drawString(20 + text_width, y_position - 75, support_email)

        # Сохранение PDF
        c.showPage()
        c.save()

    def _create_error_pdf(self, error_message):
        """Создает простой PDF с сообщением об ошибке"""
        try:
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=(400, 300))
            
            c.setFont("Helvetica", 12)
            c.drawString(50, 200, "Ошибка при создании квитанции:")
            c.drawString(50, 180, str(error_message))
            c.drawString(50, 160, "Обратитесь в службу поддержки")
            
            c.showPage()
            c.save()
            
            buffer.seek(0)
            return buffer.getvalue()
        except Exception as e:
            logger.error(f"Критическая ошибка при создании PDF с ошибкой: {e}")
            return b"Error creating PDF"

    async def generate_phone_receipt(self, variables=None):
        """Генерация квитанции по номеру телефона (заглушка)"""
        # Здесь можно реализовать аналогичную логику для квитанции по телефону
        return await self.generate_card_receipt(variables)