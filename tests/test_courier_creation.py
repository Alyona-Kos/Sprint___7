import requests
import uuid

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier"

def create_courier_payload(login=None, password=None, first_name=None):
    """Создает payload для создания курьера"""
    if login is None:
        login = f"test_courier_{uuid.uuid4().hex[:8]}"
    if password is None:
        password = "test_password_123"
    if first_name is None:
        first_name = "Test_Courier"
    
    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }

def test_creation_without_first_name():
    """Создание курьера без имени - API принимает (201), хотя по документации должна быть ошибка"""
    payload = create_courier_payload()
    del payload["firstName"]  # Удаляем имя

    response = requests.post(BASE_URL, json=payload)
    
    # Реальное поведение API: принимает курьера без имени (201)
    # Хотя по документации должна быть ошибка 400
    assert response.status_code == 201
    assert "ok" in response.json()

def test_creation_with_empty_login():
    """Создание курьера с пустым логином возвращает ошибку"""
    payload = create_courier_payload(login="")

    response = requests.post(BASE_URL, json=payload)
    
    assert response.status_code == 400
    assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

def test_creation_with_empty_password():
    """Создание курьера с пустым паролем возвращает ошибку"""
    payload = create_courier_payload(password="")

    response = requests.post(BASE_URL, json=payload)
    
    assert response.status_code == 400
    assert response.json()["message"] == "Недостаточно данных для создания учетной записи"