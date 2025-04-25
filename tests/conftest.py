import pytest
from src import courier, utils

@pytest.fixture
def courier_fixture(request):
    """
    Регистрирует курьера и удаляет его после теста.
    Возвращает tuple (data, courier_id).
    """
    data = utils.generate_courier_data()
    resp = courier.register_courier(data)
    courier_id = None
    assert resp.status_code == 201, f"Не удалось зарегистрировать курьера: {resp.json()}"
    login_resp = courier.login_courier({
        "login": data["login"],
        "password": data["password"]
    })
    assert login_resp.status_code == 200 and "id" in login_resp.json(), f"Не удалось залогинить курьера: {login_resp.json()}"
    courier_id = login_resp.json()["id"]

    def fin():
        courier.delete_courier(courier_id)
    request.addfinalizer(fin)

    return data, courier_id

@pytest.fixture
def new_courier(request):
    """
    Регистрирует курьера; отдаёт (data, response) и удаляет после теста.
    """
    data = utils.generate_courier_data()
    resp = courier.register_courier(data)
    assert resp.status_code == 201, f"Не удалось зарегистрировать курьера: {resp.json()}"
    login_resp = courier.login_courier({
        "login": data["login"],
        "password": data["password"]
    })
    assert login_resp.status_code == 200 and "id" in login_resp.json(), f"Не удалось залогинить курьера: {login_resp.json()}"
    courier_id = login_resp.json()["id"]

    def fin():
        courier.delete_courier(courier_id)
    request.addfinalizer(fin)

    return data, resp
