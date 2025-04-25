import allure
import pytest
from src import courier, order
from src.data import generate_order_payload
from src.utils import generate_courier_data

@allure.feature("Удаление курьера")
class TestDeleteCourier:

    @allure.title("Успешное удаление курьера")
    @allure.story("Позитивный сценарий – удаление курьера")
    def test_delete_courier_success(self):
        data = generate_courier_data()
        r1 = courier.register_courier(data); assert r1.status_code==201
        r2 = courier.login_courier({"login":data["login"],"password":data["password"]}); assert r2.status_code==200
        cid = r2.json()["id"]
        rd = courier.delete_courier(cid)
        assert rd.status_code==200 and rd.json().get("ok") is True

    @allure.title("Ошибка при отсутствии id курьера")
    @allure.story("Негативный сценарий – без courierId")
    def test_delete_courier_without_id(self):
        rd = courier.delete_courier(None)
        assert rd.status_code in (400,404)
        j = rd.json(); assert "message" in j and j["message"].strip()

    @allure.title("Ошибка при несуществующем id курьера")
    @allure.story("Негативный сценарий – неверный courierId")
    def test_delete_courier_nonexistent_id(self):
        rd = courier.delete_courier(999999)
        assert rd.status_code in (400,404)
        j = rd.json(); assert "message" in j and j["message"].strip()

@allure.feature("Принятие заказа")
class TestAcceptOrder:

    @allure.title("Успешное принятие заказа")
    @allure.story("Позитивный сценарий – принять заказ")
    def test_accept_order_success(self, courier_fixture):
        _, cid = courier_fixture
        create = order.create_order(generate_order_payload())
        assert create.status_code==201
        track = create.json()["track"]
        oid = order.get_order_by_track(track).json()["order"]["id"]
        ra = order.accept_order(cid, oid)
        assert ra.status_code==200 and ra.json().get("ok") is True

    @allure.title("Ошибка при отсутствии courierId")
    @allure.story("Негативный сценарий – без courierId")
    def test_accept_order_missing_courier_id(self):
        create = order.create_order(generate_order_payload()); assert create.status_code==201
        oid = order.get_order_by_track(create.json()["track"]).json()["order"]["id"]
        ra = order.accept_order(None, oid)
        assert ra.status_code in (400,404)
        j=ra.json(); assert "message" in j and j["message"].strip()

    @allure.title("Ошибка при неверном courierId")
    @allure.story("Негативный сценарий – неверный courierId")
    def test_accept_order_invalid_courier_id(self):
        create = order.create_order(generate_order_payload()); assert create.status_code==201
        oid = order.get_order_by_track(create.json()["track"]).json()["order"]["id"]
        ra = order.accept_order(999999, oid)
        assert ra.status_code in (400,404)
        j=ra.json(); assert "message" in j and j["message"].strip()

    @allure.title("Ошибка при отсутствии orderId")
    @allure.story("Негативный сценарий – без orderId")
    def test_accept_order_missing_order_id(self, courier_fixture):
        _, cid = courier_fixture
        ra = order.accept_order(cid, None)
        assert ra.status_code in (400,404)
        j=ra.json(); assert "message" in j and j["message"].strip()

    @allure.title("Ошибка при неверном orderId")
    @allure.story("Негативный сценарий – неверный orderId")
    def test_accept_order_invalid_order_id(self, courier_fixture):
        _, cid = courier_fixture
        ra = order.accept_order(cid, 999999)
        assert ra.status_code in (400,404)
        j=ra.json(); assert "message" in j and j["message"].strip()

@allure.feature("Получение заказа по треку")
class TestGetOrderByTrack:

    @allure.title("Успешное получение заказа по треку")
    @allure.story("Позитивный сценарий – получить заказ")
    def test_get_order_by_track_success(self):
        create = order.create_order(generate_order_payload()); assert create.status_code==201
        track = create.json()["track"]
        gr = order.get_order_by_track(track)
        assert gr.status_code==200
        j=gr.json(); assert "order" in j and isinstance(j["order"], dict)

    @allure.title("Ошибка при отсутствии track")
    @allure.story("Негативный сценарий – без track")
    def test_get_order_by_track_missing_track(self):
        gr = order.get_order_by_track(None)
        assert gr.status_code in (400,404)
        j=gr.json(); assert "message" in j and j["message"].strip()

    @allure.title("Ошибка при несуществующем track")
    @allure.story("Негативный сценарий – неверный track")
    def test_get_order_by_track_invalid_track(self):
        gr = order.get_order_by_track("invalid")
        assert gr.status_code in (400,404)
        j=gr.json(); assert "message" in j and j["message"].strip()
