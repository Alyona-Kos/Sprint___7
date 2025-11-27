import pytest
import requests
import allure
from helpers.courier_helper import register_new_courier_and_return_login_password, delete_courier, get_courier_id
from config.settings import Config

@pytest.fixture
def create_test_courier():
    """Фикстура для создания тестового курьера с последующей очисткой"""
    courier_data = register_new_courier_and_return_login_password()
    
    # Проверяем что курьер создан успешно
    assert len(courier_data) == 3, "Курьер не был создан"
    login, password, first_name = courier_data
    
    yield login, password  # Возвращаем логин и пароль для теста
    
    # Очистка после теста - удаляем созданного курьера
    courier_id = get_courier_id(login, password)
    if courier_id:
        delete_courier(courier_id)

@pytest.fixture
def courier_payload():
    """Фикстура для создания payload курьера"""
    from helpers.courier_helper import create_courier_payload
    return create_courier_payload()

@pytest.fixture  
def order_payload():
    """Фикстура для создания payload заказа"""
    from data.test_data import OrderData
    return OrderData.generate_order_payload()