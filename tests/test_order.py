# tests/test_order.py
import pytest
import allure
from src import order

@allure.feature("Создание заказа")
@allure.story("Позитивные сценарии создания заказа с разными вариантами color")
@pytest.mark.parametrize("colors", [
    (["BLACK"]),
    (["GREY"]),
    (["BLACK", "GREY"]),
    (None)  # когда поле color не передаётся
])
def test_create_order(colors):
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
    if colors is not None:
        order_payload["color"] = colors

    response = order.create_order(order_payload)
    with allure.step("Проверяем статус 201 и наличие поля track в ответе"):
        assert response.status_code == 201, f"Получен код {response.status_code}"
        response_json = response.json()
        assert "track" in response_json, f"Ответ: {response_json}"

@allure.feature("Список заказов")
@allure.story("Получение списка заказов")
def test_list_orders():
    response = order.list_orders()
    with allure.step("Проверяем, что статус 200 и orders — это список"):
        assert response.status_code == 200, f"Получен код {response.status_code}"
        orders = response.json().get("orders")
        assert isinstance(orders, list), f"Ожидается список, получено: {orders}"
