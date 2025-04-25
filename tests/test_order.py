import pytest
import allure
from src import order
from src.data import generate_order_payload

@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Позитивные сценарии создания заказа с разными цветами")
    @allure.story("Параметризованное создание заказа")
    @pytest.mark.parametrize("colors", [["BLACK"], ["GREY"], ["BLACK","GREY"], None])
    def test_create_order(self, colors):
        payload = generate_order_payload(colors)
        resp = order.create_order(payload)
        assert resp.status_code == 201
        j = resp.json()
        assert "track" in j and isinstance(j["track"], int)

@allure.feature("Список заказов")
class TestListOrders:

    @allure.title("Получение списка заказов")
    @allure.story("Проверка списка заказов")
    def test_list_orders(self):
        resp = order.list_orders()
        assert resp.status_code == 200
        j = resp.json()
        assert "orders" in j and isinstance(j["orders"], list)
