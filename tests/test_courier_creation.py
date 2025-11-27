import pytest
import allure
import requests
from config.settings import Config
from helpers.courier_helper import create_courier_payload
from data.test_data import CourierData

class TestCourierCreation:
    """Тесты создания курьера"""

    @allure.title("Успешное создание курьера")
    def test_successful_courier_creation_returns_correct_response(self):
        """Успешное создание курьера возвращает правильный код ответа и {"ok":true}"""
        payload = create_courier_payload()
        response = requests.post(Config.COURIER_URL, json=payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Успешное создание курьера без имени")
    def test_successful_courier_creation_without_first_name(self):
        """Успешное создание курьера без имени (firstName не обязателен)"""
        payload = create_courier_payload(first_name=None)
        
        # Убедимся что firstName не в payload
        assert "firstName" not in payload
        
        response = requests.post(Config.COURIER_URL, json=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Создание дубликата курьера")
    def test_cannot_create_duplicate_couriers(self):
        """Нельзя создать двух одинаковых курьеров"""
        payload = create_courier_payload()
        
        # Первое создание
        response1 = requests.post(Config.COURIER_URL, json=payload)
        assert response1.status_code == 201
        assert response1.json() == {"ok": True}
        
        # Второе создание с тем же логином
        response2 = requests.post(Config.COURIER_URL, json=payload)
        assert response2.status_code == 409
        assert "message" in response2.json()

    @allure.title("Создание курьера без логина")
    def test_creation_without_login_returns_error(self):
        """Создание курьера без логина возвращает ошибку"""
        payload = create_courier_payload()
        del payload["login"]
        
        response = requests.post(Config.COURIER_URL, json=payload)
        assert response.status_code == 400
        assert "message" in response.json()

    @allure.title("Создание курьера без пароля")
    def test_creation_without_password_returns_error(self):
        """Создание курьера без пароля возвращает ошибку"""
        payload = create_courier_payload()
        del payload["password"]
        
        response = requests.post(Config.COURIER_URL, json=payload)
        assert response.status_code == 400
        assert "message" in response.json()

    @allure.title("Создание курьера с пустым логином")
    def test_creation_with_empty_login_returns_error(self):
        """Создание курьера с пустым логином возвращает ошибку"""
        payload = create_courier_payload(login="")
        response = requests.post(Config.COURIER_URL, json=payload)
        assert response.status_code == 400
        assert "message" in response.json()

    @allure.title("Создание курьера с пустым паролем")
    def test_creation_with_empty_password_returns_error(self):
        """Создание курьера с пустым паролем возвращает ошибку"""
        payload = create_courier_payload(password="")
        response = requests.post(Config.COURIER_URL, json=payload)
        assert response.status_code == 400
        assert "message" in response.json()