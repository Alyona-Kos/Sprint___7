import requests
from config.settings import Config
from data.test_data import CourierData

def create_courier_payload(login=None, password=None, first_name=None):
    """Создает payload для создания курьера"""
    if login is None:
        login = CourierData.generate_login()
    if password is None:
        password = CourierData.DEFAULT_PASSWORD
    
    payload = {
        "login": login,
        "password": password
    }
    
    # firstName не является обязательным, добавляем только если указано
    if first_name is not None:
        payload["firstName"] = first_name
    
    return payload

def register_new_courier_and_return_login_password():
    """Метод регистрации нового курьера возвращает список из логина и пароля"""
    login = CourierData.generate_login()
    password = CourierData.DEFAULT_PASSWORD
    first_name = CourierData.DEFAULT_FIRST_NAME

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(Config.COURIER_URL, json=payload)

    login_pass = []
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass

def delete_courier(courier_id):
    """Удаляет курьера по ID"""
    if courier_id:
        response = requests.delete(f"{Config.COURIER_URL}/{courier_id}")
        if response.status_code != 200:
            print(f"Не удалось удалить курьера {courier_id}: {response.status_code}")

def get_courier_id(login, password):
    """Получает ID курьера по логину и паролю"""
    payload = {"login": login, "password": password}
    response = requests.post(Config.COURIER_LOGIN_URL, json=payload)
    if response.status_code == 200:
        return response.json()["id"]
    return None