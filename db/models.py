class User:
    @staticmethod
    def get_or_create(user_id, username=None, first_name=None, last_name=None):
        """Заглушка для получения или создания пользователя"""
        return {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "balance": 0
        }
    
    @staticmethod
    def update_balance(user_id, amount):
        """Заглушка для обновления баланса пользователя"""
        return 0
    
    @staticmethod
    def get_balance(user_id):
        """Заглушка для получения баланса пользователя"""
        return 0

class Transaction:
    @staticmethod
    def create(user_id, type, amount, description=None):
        """Заглушка для создания транзакции"""
        pass

class Stats:
    @staticmethod
    def increment(type, count=1):
        """Заглушка для увеличения счетчика статистики"""
        pass
    
    @staticmethod
    def get_stats():
        """Заглушка для получения статистики"""
        return {
            "today_checks": 0,
            "today_receipts": 0,
            "total_checks": 0,
            "total_receipts": 0,
            "users_count": 1
        }