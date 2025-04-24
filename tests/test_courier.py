# tests/test_courier.py
import pytest
import allure
from src import courier, utils

@allure.feature("Создание курьера")
@allure.story("Позитивный сценарий регистрации курьера")
def test_create_courier_success():
    data = utils.generate_courier_data()
    response = courier.register_courier(data)
    with allure.step("Проверяем, что статус 201 и в ответе {'ok': true}"):
        assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"
        response_json = response.json()
        assert response_json.get("ok") is True, f"Ответ: {response_json}"
    # Удаляем созданного курьера для очистки базы
    login_payload = {"login": data["login"], "password": data["password"]}
    login_response = courier.login_courier(login_payload)
    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]
        courier.delete_courier(courier_id)

@allure.feature("Создание курьера")
@allure.story("Негативный сценарий – отсутствие обязательного поля")
def test_create_courier_missing_field():
    data = utils.generate_courier_data()
    data.pop("password")  # удаляем обязательное поле
    response = courier.register_courier(data)
    with allure.step("Проверка, что отсутствие поля приводит к ошибке"):
        assert response.status_code in [400, 409], f"Получен код {response.status_code}"

@allure.feature("Создание курьера")
@allure.story("Негативный сценарий – дублирование курьера")
def test_create_duplicate_courier():
    data = utils.generate_courier_data()
    # Регистрируем первый раз
    response1 = courier.register_courier(data)
    assert response1.status_code == 201, "Первый курьер не зарегистрирован"
    # Регистрируем второй раз с теми же данными
    response2 = courier.register_courier(data)
    with allure.step("Проверяем, что повторная регистрация возвращает ошибку"):
        assert response2.status_code in [400, 409], f"Получен код {response2.status_code}"
    # Очистка – удаляем курьера, если он был создан
    login_payload = {"login": data["login"], "password": data["password"]}
    login_response = courier.login_courier(login_payload)
    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]
        courier.delete_courier(courier_id)
