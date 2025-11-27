import pytest
import allure
import requests
import uuid
from config.settings import Config

class TestOrderCreation:
    """Тесты создания заказа"""
    
    def create_valid_order_payload(self):
        """Создает валидный payload для заказа"""
        return {
            "firstName": f"Тест_{uuid.uuid4().hex[:4]}",
            "lastName": f"Тестовый_{uuid.uuid4().hex[:4]}",
            "address": "ул. Тестовая, 1",
            "metroStation": 1,
            "phone": "+79998887766",
            "rentTime": 1,
            "deliveryDate": "2024-12-31",
            "comment": "Тестовый заказ"
        }

    @pytest.mark.parametrize("color_data, test_name", [
        (["BLACK"], "черным цветом"),
        (["GREY"], "серым цветом"), 
        (["BLACK", "GREY"], "обоими цветами"),
        ([], "без указания цвета")
    ])
    @allure.title("Создание заказа с разными цветами - {test_name}")
    def test_create_order_with_different_colors(self, color_data, test_name):
        """Параметризованный тест создания заказа с разными цветами"""
        payload = self.create_valid_order_payload()
        if color_data:
            payload["color"] = color_data

        response = requests.post(Config.ORDER_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа без имени")
    def test_create_order_without_first_name(self):
        """Создание заказа без имени (API разрешает)"""
        payload = self.create_valid_order_payload()
        del payload["firstName"]
        response = requests.post(Config.ORDER_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа без фамилии")
    def test_create_order_without_last_name(self):
        """Создание заказа без фамилии (API разрешает)"""
        payload = self.create_valid_order_payload()
        del payload["lastName"]
        response = requests.post(Config.ORDER_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа без адреса")
    def test_create_order_without_address(self):
        """Создание заказа без адреса (API разрешает)"""
        payload = self.create_valid_order_payload()
        del payload["address"]
        response = requests.post(Config.ORDER_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа без станции метро")
    def test_create_order_without_metro_station(self):
        """Создание заказа без станции метро (API разрешает)"""
        payload = self.create_valid_order_payload()
        del payload["metroStation"]
        response = requests.post(Config.ORDER_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа без телефона")
    def test_create_order_without_phone(self):
        """Создание заказа без телефона (API разрешает)"""
        payload = self.create_valid_order_payload()
        del payload["phone"]
        response = requests.post(Config.ORDER_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа без времени аренды")
    def test_create_order_without_rent_time(self):
        """Создание заказа без времени аренды (API разрешает)"""
        payload = self.create_valid_order_payload()
        del payload["rentTime"]
        response = requests.post(Config.ORDER_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа без даты доставки")
    def test_create_order_without_delivery_date(self):
        """Создание заказа без даты доставки (API разрешает)"""
        payload = self.create_valid_order_payload()
        del payload["deliveryDate"]
        response = requests.post(Config.ORDER_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа с пустыми обязательными полями")
    def test_create_order_with_empty_required_fields(self):
        """Создание заказа с пустыми обязательными полями (API разрешает)"""
        payload = {
            "firstName": "",
            "lastName": "",
            "address": "",
            "metroStation": 4,
            "phone": "",
            "rentTime": 3,
            "deliveryDate": "2024-12-31",
            "comment": "Тестовый заказ"
        }
        response = requests.post(Config.ORDER_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа с неверным форматом телефона")
    def test_create_order_with_invalid_phone_format(self):
        """Создание заказа с неверным форматом телефона (API разрешает)"""
        payload = self.create_valid_order_payload()
        payload["phone"] = "invalid_phone"
        response = requests.post(Config.ORDER_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа с неверной датой доставки")
    def test_create_order_with_invalid_delivery_date(self):
        """Создание заказа с неверной датой доставки"""
        payload = self.create_valid_order_payload()
        payload["deliveryDate"] = "invalid_date"
        response = requests.post(Config.ORDER_URL, json=payload)
        # API возвращает 500 для неверной даты
        assert response.status_code == 500