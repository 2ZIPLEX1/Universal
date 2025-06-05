import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def ensure_directories_exist():
    """Создает необходимые директории для изображений"""
    dirs = [
        "static",
        "static/images",
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
    
    # Создаем заглушки для изображений
    create_not_subscribed_image()

def create_not_subscribed_image():
    """Создает изображение для экрана 'не подписан на канал'"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Проверяем, существует ли уже изображение
        image_path = "static/images/not_subscribed.jpg"
        if os.path.exists(image_path) and os.path.getsize(image_path) > 100:  # Проверяем, что файл не пустой
            return
        
        # Создаем новое изображение
        width, height = 600, 400
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Добавляем текст
        try:
            # Пытаемся загрузить шрифт
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            # Если шрифт не найден, используем стандартный
            font = ImageFont.load_default()
        
        draw.text((50, 150), "Пожалуйста, подпишитесь на наш канал", fill='black', font=font)
        draw.text((50, 200), "чтобы начать использовать бота", fill='black', font=font)
        
        # Сохраняем изображение
        image.save(image_path)
    except Exception as e:
        logger.error(f"Ошибка при создании изображения: {e}")
        # Создаем пустой файл, чтобы не пытаться создать его снова
        with open("static/images/not_subscribed.jpg", "w") as f:
            f.write("Placeholder for not_subscribed image")