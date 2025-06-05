import io
import asyncio
from pyppeteer import launch

class BaseScreenshotGenerator:
    async def html_to_image(self, html_content, options=None):
        """Преобразование HTML в изображение"""
        default_options = {
            "width": 390,
            "height": 844,
            "deviceScaleFactor": 2,
            "fullPage": False
        }
        
        # Объединяем дефолтные опции с переданными
        opts = {**default_options, **(options or {})}
        
        # Запускаем браузер
        browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        page = await browser.newPage()
        
        # Устанавливаем размер вьюпорта
        await page.setViewport({
            "width": opts["width"],
            "height": opts["height"],
            "deviceScaleFactor": opts["deviceScaleFactor"]
        })
        
        # Устанавливаем содержимое страницы
        await page.setContent(html_content, {"waitUntil": "networkidle0"})
        
        # Делаем скриншот
        screenshot = await page.screenshot({
            "type": "png",
            "fullPage": opts["fullPage"]
        })
        
        # Закрываем браузер
        await browser.close()
        
        return screenshot