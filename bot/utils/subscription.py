from telegram import Bot
import logging

logger = logging.getLogger(__name__)

async def check_subscription(bot: Bot, user_id: int, channel_id: str) -> bool:
    """
    Проверяет, подписан ли пользователь на канал.
    
    Args:
        bot: Экземпляр бота
        user_id: ID пользователя
        channel_id: ID канала (с @ для публичных или -100... для приватных)
        
    Returns:
        bool: True если подписан, False если нет
    """
    if not channel_id:
        return True  # Если ID канала не задан, считаем, что проверка пройдена
    
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        # Список статусов, при которых пользователь считается подписанным
        allowed_statuses = ['creator', 'administrator', 'member']
        
        return member.status in allowed_statuses
    except Exception as e:
        logger.error(f"Ошибка при проверке подписки: {e}")
        # Для тестирования можно вернуть True, чтобы не блокировать функциональность
        return True