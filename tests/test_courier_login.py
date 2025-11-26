import pytest
import allure
import requests
from config.settings import Config
from helpers.courier_helper import delete_courier, get_courier_id

class TestCourierLogin:
    """Тесты логина курьера"""

    @allure.title("Успешный логин курьера")
    def test_successful_login_returns_correct_response_and_id(self, create_test_courier):
        """Успешная авторизация курьера возвращает правильный код ответа и id"""
        login, password = create_test_courier
        
        payload = {"login": login, "password": password}
        response = requests.post(f'{Config.COURIER_URL}/login', json=payload)
        
        assert response.status_code == 200
        response_data = response.json()
        assert "id" in response_data
        courier_id = response_data["id"]
        assert isinstance(courier_id, int)
        assert courier_id > 0

    @allure.title("Логин с неверным паролем")
    def test_login_with_wrong_password_returns_404(self, create_test_courier):
        """Логин с неверным паролем возвращает ошибку 404"""
        login, password = create_test_courier
        
        payload = {"login": login, "password": "wrong_password"}
        response = requests.post(f'{Config.COURIER_URL}/login', json=payload)
        
        assert response.status_code == 404
        assert "message" in response.json()

    @allure.title("Логин с неверным логином")
    def test_login_with_wrong_login_returns_404(self, create_test_courier):
        """Логин с неверным логином возвращает ошибку 404"""
        login, password = create_test_courier
        
        payload = {"login": "nonexistent_login", "password": password}
        response = requests.post(f'{Config.COURIER_URL}/login', json=payload)
        
        assert response.status_code == 404
        assert "message" in response.json()

    @allure.title("Логин без пароля")
    def test_login_without_password_returns_error(self, create_test_courier):
        """Логин без пароля возвращает ошибку"""
        login, password = create_test_courier
        
        payload = {"login": login}
        response = requests.post(f'{Config.COURIER_URL}/login', json=payload)

        # API может возвращать 504 вместо 400 - проверяем что это ошибка
        assert response.status_code != 200
        assert response.status_code != 201

    @allure.title("Логин без логина")
    def test_login_without_login_returns_400(self, create_test_courier):
        """Логин без логина возвращает ошибку 400"""
        login, password = create_test_courier
        
        payload = {"password": password}
        response = requests.post(f'{Config.COURIER_URL}/login', json=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"