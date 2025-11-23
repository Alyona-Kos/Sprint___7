import requests
import uuid
import allure
import pytest
from config.settings import Config
from data.test_data import OrderData

BASE_URL = Config.ORDER_URL

def create_valid_order_payload():
    """Создает валидный payload для заказа"""
    return OrderData.generate_order_payload()

# Параметризованный тест для создания заказа с разными цветами
@allure.title("Создание заказа с разными цветами")
@pytest.mark.parametrize("color", [
    ["BLACK"],
    ["GREY"], 
    ["BLACK", "GREY"],
    []
], ids=[
    "black_color",
    "grey_color",
    "both_colors",
    "without_color"
])
def test_create_order_with_different_colors(color):
    """Параметризованный тест создания заказа с разными цветами"""
    payload = create_valid_order_payload()
    if color:  # Добавляем цвет только если он не пустой
        payload["color"] = color

    response = requests.post(BASE_URL, json=payload)
    
    assert response.status_code == 201
    assert "track" in response.json()

@allure.title("Создание заказа без имени")
def test_create_order_without_first_name():
    """Создание заказа без имени"""
    payload = create_valid_order_payload()
    del payload["firstName"]

    response = requests.post(BASE_URL, json=payload)
    
    # API принимает заказы без обязательных полей
    assert response.status_code == 201
    assert "track" in response.json()

@allure.title("Создание заказа без фамилии")
def test_create_order_without_last_name():
    """Создание заказа без фамилии"""
    payload = create_valid_order_payload()
    del payload["lastName"]

    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert "track" in response.json()

@allure.title("Создание заказа без адреса")
def test_create_order_without_address():
    """Создание заказа без адреса"""
    payload = create_valid_order_payload()
    del payload["address"]

    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert "track" in response.json()

@allure.title("Создание заказа без станции метро")
def test_create_order_without_metro_station():
    """Создание заказа без станции метро"""
    payload = create_valid_order_payload()
    del payload["metroStation"]

    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert "track" in response.json()

@allure.title("Создание заказа без телефона")
def test_create_order_without_phone():
    """Создание заказа без телефона"""
    payload = create_valid_order_payload()
    del payload["phone"]

    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert "track" in response.json()

@allure.title("Создание заказа без времени аренды")
def test_create_order_without_rent_time():
    """Создание заказа без времени аренды"""
    payload = create_valid_order_payload()
    del payload["rentTime"]

    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert "track" in response.json()

@allure.title("Создание заказа без даты доставки")
def test_create_order_without_delivery_date():
    """Создание заказа без даты доставки"""
    payload = create_valid_order_payload()
    del payload["deliveryDate"]

    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert "track" in response.json()

@allure.title("Создание заказа с пустыми обязательными полями")
def test_create_order_with_empty_required_fields():
    """Создание заказа с пустыми обязательными полями"""
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

    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert "track" in response.json()

@allure.title("Создание заказа с неверным форматом телефона")
def test_create_order_with_invalid_phone_format():
    """Создание заказа с неверным форматом телефона"""
    payload = create_valid_order_payload()
    payload["phone"] = "invalid_phone"

    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert "track" in response.json()

@allure.title("Создание заказа с неверной датой доставки")
def test_create_order_with_invalid_delivery_date():
    """Создание заказа с неверной датой доставки возвращает ошибку"""
    payload = create_valid_order_payload()
    payload["deliveryDate"] = "invalid_date"

    response = requests.post(BASE_URL, json=payload)

    # Для неверной даты API возвращает 500
    assert response.status_code == 500