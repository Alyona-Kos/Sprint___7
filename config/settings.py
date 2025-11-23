"""Конфигурация проекта и URL endpoints"""

class Config:
    # Базовые URL для разных стендов
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    # Endpoints
    COURIER_URL = f"{BASE_URL}/api/v1/courier"
    ORDER_URL = f"{BASE_URL}/api/v1/orders"
    
    # Дополнительные endpoints (если понадобятся)
    COURIER_LOGIN_URL = f"{COURIER_URL}/login"
    ORDER_TRACK_URL = f"{ORDER_URL}/track"
    ORDER_ACCEPT_URL = f"{ORDER_URL}/accept"
    ORDER_CANCEL_URL = f"{ORDER_URL}/cancel"
    ORDER_FINISH_URL = f"{ORDER_URL}/finish"
    
    # Таймауты
    REQUEST_TIMEOUT = 10
