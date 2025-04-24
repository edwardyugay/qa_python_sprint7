# tests/conftest.py
import pytest
from src import courier, utils

@pytest.fixture
def courier_fixture():
    """
    Фикстура для создания курьера и очистки (удаления) после выполнения теста.
    Возвращает кортеж (данные курьера, courier_id) если регистрация успешна, иначе (данные, None).
    """
    data = utils.generate_courier_data()
    reg_response = courier.register_courier(data)
    courier_id = None
    if reg_response.status_code == 201:
        login_payload = {"login": data["login"], "password": data["password"]}
        login_response = courier.login_courier(login_payload)
        if login_response.status_code == 200 and "id" in login_response.json():
            courier_id = login_response.json()["id"]
    yield data, courier_id
    # Очистка: если курьер был успешно создан, удаляем его
    if courier_id:
        courier.delete_courier(courier_id)
