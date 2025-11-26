import requests
import pytest
import allure

class TestOrderList:
    """Тесты получения списка заказов"""
    
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/orders"

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        """Получение списка заказов"""
        response = requests.get(self.BASE_URL)
        assert response.status_code == 200
        assert "orders" in response.json()

    @allure.title("Получение списка заказов с лимитом")
    def test_orders_list_with_limit(self):
        """Получение списка заказов с лимитом"""
        response = requests.get(f"{self.BASE_URL}?limit=5")
        assert response.status_code == 200
        assert "orders" in response.json()
        assert "pageInfo" in response.json()