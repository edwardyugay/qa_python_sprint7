import allure
import pytest
from src import courier, utils

@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешная регистрация курьера")
    @allure.story("Позитивный сценарий регистрации курьера")
    def test_create_courier_success(self, new_courier):
        data, response = new_courier
        assert response.status_code == 201
        assert response.json().get("ok") is True

    @allure.title("Ошибка при отсутствии обязательного поля при регистрации")
    @allure.story("Негативный сценарий – отсутствие поля password")
    def test_create_courier_missing_field(self):
        data = utils.generate_courier_data()
        data.pop("password")
        resp = courier.register_courier(data)
        assert resp.status_code in (400, 409)
        j = resp.json()
        assert "message" in j and isinstance(j["message"], str) and j["message"].strip()

    @allure.title("Ошибка при дублировании курьера")
    @allure.story("Негативный сценарий – регистрация дублирующегося курьера")
    def test_create_duplicate_courier(self, new_courier):
        data, _ = new_courier
        resp2 = courier.register_courier(data)
        assert resp2.status_code in (400, 409)
        j = resp2.json()
        assert "message" in j and j["message"].strip()
