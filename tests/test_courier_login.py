import requests
import allure
from config.settings import Config

BASE_URL = Config.COURIER_URL

# УДАЛЕНО: функция create_test_courier

@allure.title("Логин с неверным паролем")
def test_login_with_wrong_password(create_test_courier):  # ИСПРАВЛЕНО: используем фикстуру
    """Логин с неверным паролем возвращает ошибку 404"""
    login, password = create_test_courier  # ИСПРАВЛЕНО: распаковываем фикстуру
    
    payload = {
        "login": login,
        "password": "wrong_password"
    }

    response = requests.post(f'{BASE_URL}/login', json=payload)
    
    # Согласно документации: неверный пароль = 404
    assert response.status_code == 404
    assert response.json()["message"] == "Учетная запись не найдена"

@allure.title("Логин с неверным логином")
def test_login_with_wrong_login(create_test_courier):  # ИСПРАВЛЕНО: используем фикстуру
    """Логин с неверным логином возвращает ошибку 404"""
    login, password = create_test_courier  # ИСПРАВЛЕНО: распаковываем фикстуру
    
    payload = {
        "login": "nonexistent_login",
        "password": password
    }

    response = requests.post(f'{BASE_URL}/login', json=payload)
    
    # Согласно документации: неверный логин = 404
    assert response.status_code == 404
    assert response.json()["message"] == "Учетная запись не найдена"

@allure.title("Логин без пароля")
def test_login_without_password(create_test_courier):  # ИСПРАВЛЕНО: используем фикстуру
    """Логин без пароля возвращает ошибку 504"""
    login, password = create_test_courier  # ИСПРАВЛЕНО: распаковываем фикстуру
    
    payload = {
        "login": login
    }

    response = requests.post(f'{BASE_URL}/login', json=payload)

    # 504 указывает на проблему сервера
    assert response.status_code == 504