# tests/test_additional.py
import pytest
import allure
from src import courier, order, utils

@allure.feature("Удаление курьера")
class TestDeleteCourier:
    @allure.story("Позитивный сценарий – успешное удаление курьера")
    def test_delete_courier_success(self):
        # Регистрируем курьера
        data = utils.generate_courier_data()
        reg_response = courier.register_courier(data)
        assert reg_response.status_code == 201, "Ошибка регистрации курьера"
        login_payload = {"login": data["login"], "password": data["password"]}
        login_response = courier.login_courier(login_payload)
        courier_id = login_response.json().get("id")
        delete_response = courier.delete_courier(courier_id)
        with allure.step("Проверяем, что удаление возвращает {'ok': true}"):
            assert delete_response.status_code == 200, f"Получен код {delete_response.status_code}"
            assert delete_response.json().get("ok") is True

    @allure.story("Негативный сценарий – запрос без id")
    def test_delete_courier_without_id(self):
        delete_response = courier.delete_courier(None)
        with allure.step("Проверяем, что отсутствие id приводит к ошибке"):
            assert delete_response.status_code in [400, 404]

    @allure.story("Негативный сценарий – запрос с несуществующим id")
    def test_delete_courier_nonexistent_id(self):
        delete_response = courier.delete_courier(999999)
        with allure.step("Проверяем, что несуществующий id приводит к ошибке"):
            assert delete_response.status_code in [400, 404]

@allure.feature("Принятие заказа")
class TestAcceptOrder:
    @allure.story("Позитивный сценарий – успешное принятие заказа")
    def test_accept_order_success(self, courier_fixture):
        # Используем зарегистрированного курьера
        data, courier_id = courier_fixture
        # Создаем заказ
        order_payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test Address",
            "metroStation": "5",
            "phone": "1234567890",
            "rentTime": 5,
            "deliveryDate": "2025-04-20",
            "comment": "Test order"
        }
        create_response = order.create_order(order_payload)
        assert create_response.status_code == 201, "Ошибка создания заказа"
        track = create_response.json().get("track")
        assert track is not None, "Отсутствует track"
        # Получаем order_id по track
        track_response = order.get_order_by_track(track)
        assert track_response.status_code == 200, "Ошибка получения заказа по треку"
        order_obj = track_response.json().get("order", {})
        order_id = order_obj.get("id")
        accept_response = order.accept_order(courier_id=courier_id, order_id=order_id)
        with allure.step("Проверяем, что заказ принят и возвращается {'ok': true}"):
            assert accept_response.status_code == 200, f"Получен код {accept_response.status_code}"
            assert accept_response.json().get("ok") is True

    @allure.story("Негативный сценарий – отсутствие id курьера")
    def test_accept_order_missing_courier_id(self):
        # Создаем заказ
        order_payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test Address",
            "metroStation": "5",
            "phone": "1234567890",
            "rentTime": 5,
            "deliveryDate": "2025-04-20",
            "comment": "Test order"
        }
        create_response = order.create_order(order_payload)
        track = create_response.json().get("track")
        track_response = order.get_order_by_track(track)
        order_id = track_response.json().get("order", {}).get("id")
        accept_response = order.accept_order(courier_id=None, order_id=order_id)
        with allure.step("Проверяем, что отсутствие id курьера приводит к ошибке"):
            assert accept_response.status_code in [400, 404]

    @allure.story("Негативный сценарий – неверный id курьера")
    def test_accept_order_invalid_courier_id(self):
        # Создаем заказ
        order_payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test Address",
            "metroStation": "5",
            "phone": "1234567890",
            "rentTime": 5,
            "deliveryDate": "2025-04-20",
            "comment": "Test order"
        }
        create_response = order.create_order(order_payload)
        track = create_response.json().get("track")
        track_response = order.get_order_by_track(track)
        order_id = track_response.json().get("order", {}).get("id")
        accept_response = order.accept_order(courier_id=999999, order_id=order_id)
        with allure.step("Проверяем, что неверный id курьера возвращает ошибку"):
            assert accept_response.status_code in [400, 404]

    @allure.story("Негативный сценарий – отсутствие id заказа")
    def test_accept_order_missing_order_id(self, courier_fixture):
        data, courier_id = courier_fixture
        accept_response = order.accept_order(courier_id=courier_id, order_id=None)
        with allure.step("Проверяем, что отсутствие id заказа приводит к ошибке"):
            assert accept_response.status_code in [400, 404]

    @allure.story("Негативный сценарий – неверный id заказа")
    def test_accept_order_invalid_order_id(self, courier_fixture):
        data, courier_id = courier_fixture
        accept_response = order.accept_order(courier_id=courier_id, order_id=999999)
        with allure.step("Проверяем, что неверный id заказа приводит к ошибке"):
            assert accept_response.status_code in [400, 404]

@allure.feature("Получение заказа по треку")
class TestGetOrderByTrack:
    @allure.story("Позитивный сценарий получения заказа")
    def test_get_order_by_track_success(self):
        order_payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test Address",
            "metroStation": "5",
            "phone": "1234567890",
            "rentTime": 5,
            "deliveryDate": "2025-04-20",
            "comment": "Test order"
        }
        create_response = order.create_order(order_payload)
        assert create_response.status_code == 201, "Ошибка создания заказа"
        track = create_response.json().get("track")
        get_response = order.get_order_by_track(track)
        with allure.step("Проверяем, что заказ получен и в ответе присутствует объект order"):
            assert get_response.status_code == 200, f"Получен код {get_response.status_code}"
            order_obj = get_response.json().get("order")
            assert order_obj is not None, "Объект заказа отсутствует"

    @allure.story("Негативный сценарий – запрос без трека")
    def test_get_order_by_track_missing_track(self):
        get_response = order.get_order_by_track(None)
        with allure.step("Проверяем, что отсутствие трека приводит к ошибке"):
            assert get_response.status_code in [400, 404]

    @allure.story("Негативный сценарий – запрос с несуществующим треком")
    def test_get_order_by_track_invalid_track(self):
        get_response = order.get_order_by_track("invalid_track")
        with allure.step("Проверяем, что несуществующий трек приводит к ошибке"):
            assert get_response.status_code in [400, 404]
