import io
import asyncio
from pyppeteer import launch

class BaseReceiptGenerator:
    async def html_to_pdf(self, html_content, options=None):
        """Преобразование HTML в PDF"""
        default_options = {
            "format": "A4",
            "printBackground": True,
            "margin": {
                "top": "1cm",
                "right": "1cm",
                "bottom": "1cm",
                "left": "1cm"
            }
        }
        
        # Объединяем дефолтные опции с переданными
        opts = {**default_options, **(options or {})}
        
        # Запускаем браузер
        browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        page = await browser.newPage()
        
        # Устанавливаем содержимое страницы
        await page.setContent(html_content, {"waitUntil": "networkidle0"})
        
        # Генерируем PDF
        pdf = await page.pdf(opts)
        
        # Закрываем браузер
        await browser.close()
        
        return pdf