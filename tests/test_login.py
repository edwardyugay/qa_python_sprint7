# tests/test_login.py
import pytest
import allure

from src import courier

@allure.feature("Логин курьера")
@allure.story("Позитивный сценарий авторизации")
def test_login_courier_success(courier_fixture):
    data, courier_id = courier_fixture
    login_payload = {"login": data["login"], "password": data["password"]}
    login_response = courier.login_courier(login_payload)
    with allure.step("Проверяем, что статус 200 и присутствует поле id"):
        assert login_response.status_code == 200, f"Получен код {login_response.status_code}"
        assert "id" in login_response.json(), f"Ответ: {login_response.json()}"

@allure.feature("Логин курьера")
@allure.story("Негативный сценарий – отсутствие обязательного поля")
def test_login_courier_missing_field(courier_fixture):
    data, courier_id = courier_fixture
    login_payload = {"login": data["login"]}  # пропускаем пароль
    login_response = courier.login_courier(login_payload)
    with allure.step("Проверяем, что отсутствие пароля приводит к ошибке"):
        assert login_response.status_code in [400, 409], f"Получен код {login_response.status_code}"
