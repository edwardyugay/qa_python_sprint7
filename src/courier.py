# src/courier.py
import requests
from src.base_api import get_full_url

def register_courier(payload: dict) -> requests.Response:
    """
    Регистрирует курьера с переданными данными.
    Возвращает объект response для проверки в тестах.
    """
    url = get_full_url("/courier")
    response = requests.post(url, data=payload)
    return response

def login_courier(payload: dict) -> requests.Response:
    """
    Авторизует курьера.
    """
    url = get_full_url("/courier/login")
    response = requests.post(url, data=payload)
    return response

def delete_courier(courier_id: int = None) -> requests.Response:
    """
    Удаляет курьера по его id.
    Если id не передан, запрос отправляется без него, что должно приводить к ошибке.
    """
    url = get_full_url(f"/courier/{courier_id}") if courier_id is not None else get_full_url("/courier")
    response = requests.delete(url)
    return response
