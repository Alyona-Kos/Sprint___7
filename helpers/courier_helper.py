import requests
from config.settings import Config
from data.test_data import CourierData

def register_new_courier_and_return_login_password():
    """Метод регистрации нового курьера возвращает список из логина, пароля и имени"""
    
    # ИСПРАВЛЕНО: инициализируем список
    login_pass = []
    
    # используем данные из test_data
    login = CourierData.generate_random_string(10)
    password = CourierData.generate_random_string(10)
    first_name = CourierData.generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(Config.COURIER_URL, data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass


def create_courier_payload(login=None, password=None, first_name=None):
    """Создает payload для создания курьера"""
    
    # используем данные из test_data
    if login is None:
        login = CourierData.generate_login()
    if password is None:
        password = CourierData.DEFAULT_PASSWORD
    if first_name is None:
        first_name = CourierData.DEFAULT_FIRST_NAME
    
    payload = {
        "login": login,
        "password": password
    }
    # firstName не является обязательным, добавляем только если указано
    if first_name is not None:
        payload["firstName"] = first_name
    
    return payload