import allure
import pytest
from src import courier

@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Успешная авторизация курьера")
    @allure.story("Позитивный сценарий авторизации")
    def test_login_courier_success(self, courier_fixture):
        data, courier_id = courier_fixture
        resp = courier.login_courier({"login": data["login"], "password": data["password"]})
        assert resp.status_code == 200
        j = resp.json()
        assert "id" in j and isinstance(j["id"], int)

    @allure.title("Ошибка при отсутствии обязательного поля при авторизации")
    @allure.story("Негативный сценарий – отсутствие поля password")
    def test_login_courier_missing_field(self, courier_fixture):
        data, _ = courier_fixture
        resp = courier.login_courier({"login": data["login"]})
        assert resp.status_code in (400, 409)
        j = resp.json()
        assert "message" in j and j["message"].strip()
