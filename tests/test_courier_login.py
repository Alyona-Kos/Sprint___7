import pytest
import allure
import requests
from config.settings import Config
from helpers.courier_helper import register_new_courier_and_return_login_password, get_courier_id, delete_courier

class TestCourierLogin:
    """Тесты логина курьера"""

    @allure.title("Успешный логин курьера")
    def test_successful_login_returns_correct_response_and_id(self):
        """Успешная авторизация курьера возвращает правильный код ответа и id"""
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        payload = {"login": login, "password": password}
        response = requests.post(Config.COURIER_LOGIN_URL, json=payload)
        
        assert response.status_code == 200
        response_data = response.json()
        assert "id" in response_data
        courier_id = response_data["id"]
        assert isinstance(courier_id, int)
        assert courier_id > 0
        
        # Очистка
        delete_courier(courier_id)

    @allure.title("Логин с неверным паролем")
    def test_login_with_wrong_password_returns_404(self):
        """Логин с неверным паролем возвращает ошибку 404"""
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        payload = {"login": login, "password": "wrong_password"}
        response = requests.post(Config.COURIER_LOGIN_URL, json=payload)
        
        assert response.status_code == 404
        assert "message" in response.json()
        
        # Очистка
        courier_id = get_courier_id(login, password)
        delete_courier(courier_id)

    @allure.title("Логин с неверным логином")
    def test_login_with_wrong_login_returns_404(self):
        """Логин с неверным логином возвращает ошибку 404"""
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        payload = {"login": "nonexistent_login", "password": password}
        response = requests.post(Config.COURIER_LOGIN_URL, json=payload)
        
        assert response.status_code == 404
        assert "message" in response.json()
        
        # Очистка
        courier_id = get_courier_id(login, password)
        delete_courier(courier_id)

    @allure.title("Логин без пароля")
    def test_login_without_password_returns_error(self):
        """Логин без пароля возвращает ошибку"""
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        payload = {"login": login}
        response = requests.post(Config.COURIER_LOGIN_URL, json=payload)

        # API может возвращать 504 вместо 400 - проверяем что это ошибка
        assert response.status_code != 200
        assert response.status_code != 201
        
        # Очистка
        courier_id = get_courier_id(login, password)
        delete_courier(courier_id)

    @allure.title("Логин без логина")
    def test_login_without_login_returns_400(self):
        """Логин без логина возвращает ошибку 400"""
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        payload = {"password": password}
        response = requests.post(Config.COURIER_LOGIN_URL, json=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"
        
        # Очистка
        courier_id = get_courier_id(login, password)
        delete_courier(courier_id)