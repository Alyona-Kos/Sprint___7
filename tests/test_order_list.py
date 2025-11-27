import requests
import pytest
import allure
from config.settings import Config

class TestOrderList:
    """Тесты получения списка заказов"""

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        """Получение списка заказов"""
        response = requests.get(Config.ORDER_URL)
        assert response.status_code == 200
        assert "orders" in response.json()

    @allure.title("Получение списка заказов с лимитом")
    def test_orders_list_with_limit(self):
        """Получение списка заказов с лимитом"""
        response = requests.get(f"{Config.ORDER_URL}?limit=5")
        assert response.status_code == 200
        assert "orders" in response.json()
        assert "pageInfo" in response.json()