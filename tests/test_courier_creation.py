import requests
import allure
from helpers.courier_helper import create_courier_payload
from config.settings import Config

BASE_URL = Config.COURIER_URL

@allure.title("Успешное создание курьера")
def test_successful_courier_creation():
    """Успешное создание курьера с использованием хелпера"""
    from helpers.courier_helper import register_new_courier_and_return_login_password
    courier_data = register_new_courier_and_return_login_password()
    
    # Проверяем что курьер создан успешно (3 элемента: логин, пароль, имя)
    assert len(courier_data) == 3, "Курьер не был создан"
    login, password, first_name = courier_data
    
    # Проверяем что все данные - строки
    assert isinstance(login, str), "Логин должен быть строкой"
    assert isinstance(password, str), "Пароль должен быть строкой"
    assert isinstance(first_name, str), "Имя должно быть строкой"

@allure.title("Успешное создание курьера без имени")
def test_successful_courier_creation_without_first_name():
    """Успешное создание курьера без имени (firstName не обязателен)"""
    payload = create_courier_payload(first_name=None)
    
    response = requests.post(BASE_URL, json=payload)
    
    # Создание должно быть успешным без firstName
    assert response.status_code == 201
    assert "ok" in response.json()

@allure.title("Создание курьера с дублирующимся логином")
def test_duplicate_courier_creation(create_test_courier):
    """Создание курьера с существующим логином возвращает ошибку"""
    login, password = create_test_courier
    
    # Пытаемся создать курьера с тем же логином
    payload = create_courier_payload(login=login, password="different_password", first_name=None)
    
    response = requests.post(BASE_URL, json=payload)
    
    # Должна быть ошибка дублирования
    assert response.status_code == 409
    assert "message" in response.json()

@allure.title("Создание курьера без логина")
def test_creation_without_login():
    """Создание курьера без логина возвращает ошибку"""
    payload = create_courier_payload()
    del payload["login"]  # Удаляем логин

    response = requests.post(BASE_URL, json=payload)
    
    assert response.status_code == 400
    assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

@allure.title("Создание курьера без пароля")
def test_creation_without_password():
    """Создание курьера без пароля возвращает ошибку"""
    payload = create_courier_payload()
    del payload["password"]  # Удаляем пароль

    response = requests.post(BASE_URL, json=payload)
    
    assert response.status_code == 400
    assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

@allure.title("Создание курьера с пустым логином")
def test_creation_with_empty_login():
    """Создание курьера с пустым логином возвращает ошибку"""
    payload = create_courier_payload(login="")

    response = requests.post(BASE_URL, json=payload)
    
    assert response.status_code == 400
    assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

@allure.title("Создание курьера с пустым паролем")
def test_creation_with_empty_password():
    """Создание курьера с пустым паролем возвращает ошибку"""
    payload = create_courier_payload(password="")

    response = requests.post(BASE_URL, json=payload)
    
    assert response.status_code == 400
    assert response.json()["message"] == "Недостаточно данных для создания учетной записи"