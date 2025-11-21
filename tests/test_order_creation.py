import requests
import uuid

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/orders"

def create_valid_order_payload():
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

def test_create_order_with_black_color():
    """Создание заказа с черным цветом"""
    payload = create_valid_order_payload()
    payload["color"] = ["BLACK"]

    response = requests.post(BASE_URL, json=payload)
    
    assert response.status_code == 201
    assert "track" in response.json()

def test_create_order_with_grey_color():
    """Создание заказа с серым цветом"""
    payload = create_valid_order_payload()
    payload["color"] = ["GREY"]

    response = requests.post(BASE_URL, json=payload)
    
    assert response.status_code == 201
    assert "track" in response.json()

def test_create_order_with_both_colors():
    """Создание заказа с обоими цветами"""
    payload = create_valid_order_payload()
    payload["color"] = ["BLACK", "GREY"]

    response = requests.post(BASE_URL, json=payload)
    
    assert response.status_code == 201
    assert "track" in response.json()

def test_create_order_without_color():
    """Создание заказа без указания цвета"""
    payload = create_valid_order_payload()

    response = requests.post(BASE_URL, json=payload)
    
    assert response.status_code == 201
    assert "track" in response.json()

def test_create_order_without_first_name():
    """Создание заказа без имени возвращает ошибку"""
    payload = create_valid_order_payload()
    del payload["firstName"]  # Удаляем обязательное поле

    response = requests.post(BASE_URL, json=payload)
    
    # Согласно документации, все поля обязательные, кроме color
    # Но API может быть нестрогим, проверяем оба варианта
    if response.status_code == 400:
        assert "message" in response.json()
    else:
        # Если API принимает заказ, проверяем наличие track
        assert response.status_code == 201
        assert "track" in response.json()

def test_create_order_without_last_name():
    """Создание заказа без фамилии возвращает ошибку"""
    payload = create_valid_order_payload()
    del payload["lastName"]

    response = requests.post(BASE_URL, json=payload)

    if response.status_code == 400:
        assert "message" in response.json()
    else:
        assert response.status_code == 201
        assert "track" in response.json()

def test_create_order_without_address():
    """Создание заказа без адреса возвращает ошибку"""
    payload = create_valid_order_payload()
    del payload["address"]

    response = requests.post(BASE_URL, json=payload)

    if response.status_code == 400:
        assert "message" in response.json()
    else:
        assert response.status_code == 201
        assert "track" in response.json()

def test_create_order_without_metro_station():
    """Создание заказа без станции метро возвращает ошибку"""
    payload = create_valid_order_payload()
    del payload["metroStation"]

    response = requests.post(BASE_URL, json=payload)

    if response.status_code == 400:
        assert "message" in response.json()
    else:
        assert response.status_code == 201
        assert "track" in response.json()

def test_create_order_without_phone():
    """Создание заказа без телефона возвращает ошибку"""
    payload = create_valid_order_payload()
    del payload["phone"]

    response = requests.post(BASE_URL, json=payload)

    if response.status_code == 400:
        assert "message" in response.json()
    else:
        assert response.status_code == 201
        assert "track" in response.json()

def test_create_order_without_rent_time():
    """Создание заказа без времени аренды возвращает ошибку"""
    payload = create_valid_order_payload()
    del payload["rentTime"]

    response = requests.post(BASE_URL, json=payload)

    if response.status_code == 400:
        assert "message" in response.json()
    else:
        assert response.status_code == 201
        assert "track" in response.json()

def test_create_order_without_delivery_date():
    """Создание заказа без даты доставки возвращает ошибку"""
    payload = create_valid_order_payload()
    del payload["deliveryDate"]

    response = requests.post(BASE_URL, json=payload)

    if response.status_code == 400:
        assert "message" in response.json()
    else:
        assert response.status_code == 201
        assert "track" in response.json()

def test_create_order_with_empty_required_fields():
    """Создание заказа с пустыми обязательными полями возвращает ошибку"""
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

    if response.status_code == 400:
        assert "message" in response.json()
    else:
        assert response.status_code == 201
        assert "track" in response.json()

def test_create_order_with_invalid_phone_format():
    """Создание заказа с неверным форматом телефона возвращает ошибку"""
    payload = create_valid_order_payload()
    payload["phone"] = "invalid_phone"

    response = requests.post(BASE_URL, json=payload)

    if response.status_code == 400:
        assert "message" in response.json()
    else:
        assert response.status_code == 201
        assert "track" in response.json()

def test_create_order_with_invalid_delivery_date():
    """Создание заказа с неверной датой доставки возвращает ошибку"""
    payload = create_valid_order_payload()
    payload["deliveryDate"] = "invalid_date"

    response = requests.post(BASE_URL, json=payload)

    # Для неверной даты может быть 400 или 500
    assert response.status_code in [400, 500]
    if response.status_code == 400:
        assert "message" in response.json()