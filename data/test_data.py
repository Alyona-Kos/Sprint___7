"""Тестовые данные для автотестов"""

import uuid

class CourierData:
    """Данные для тестов курьеров"""
    
    # Базовые тестовые данные
    DEFAULT_PASSWORD = "test_password_123"
    DEFAULT_FIRST_NAME = "Test_Courier"
    
    @staticmethod
    def generate_login():
        """Генерирует уникальный логин для курьера"""
        return f"test_courier_{uuid.uuid4().hex[:8]}"
    
    @staticmethod
    def generate_random_string(length=10):
        """Генерирует случайную строку указанной длины"""
        import random
        import string
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))


class OrderData:
    """Данные для тестов заказов"""
    
    # Базовые данные заказа
    DEFAULT_FIRST_NAME = "Тест"
    DEFAULT_LAST_NAME = "Тестовый"
    DEFAULT_ADDRESS = "ул. Тестовая, 1"
    DEFAULT_PHONE = "+79998887766"
    DEFAULT_COMMENT = "Тестовый заказ"
    
    @staticmethod
    def generate_order_payload():
        """Генерирует payload для создания заказа"""
        return {
            "firstName": f"{OrderData.DEFAULT_FIRST_NAME}_{uuid.uuid4().hex[:4]}",
            "lastName": f"{OrderData.DEFAULT_LAST_NAME}_{uuid.uuid4().hex[:4]}",
            "address": OrderData.DEFAULT_ADDRESS,
            "metroStation": 1,
            "phone": OrderData.DEFAULT_PHONE,
            "rentTime": 1,
            "deliveryDate": "2024-12-31",
            "comment": OrderData.DEFAULT_COMMENT
        }