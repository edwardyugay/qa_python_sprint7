# src/order.py
import requests
from src.base_api import get_full_url

def create_order(payload: dict) -> requests.Response:
    """
    Создаёт заказ.
    Данные передаются в формате JSON.
    """
    url = get_full_url("/orders")
    response = requests.post(url, json=payload)
    return response

def list_orders() -> requests.Response:
    """
    Получает список заказов.
    """
    url = get_full_url("/orders")
    response = requests.get(url)
    return response

def accept_order(courier_id: int = None, order_id: int = None) -> requests.Response:
    """
    Курьер принимает заказ.
    Query-параметры:
      - courierId: id курьера
      - orderId: id заказа
    Если какого-либо параметра не передать, сервер возвращает ошибку.
    """
    url = get_full_url("/orders/accept")
    params = {}
    if courier_id is not None:
        params["courierId"] = courier_id
    if order_id is not None:
        params["orderId"] = order_id
    response = requests.put(url, params=params)
    return response

def get_order_by_track(track: str = None) -> requests.Response:
    """
    Получает заказ по его треку.
    Запрос отправляется с query-параметром track.
    Если параметр отсутствует или заказ не найден, возвращается ошибка.
    """
    url = get_full_url("/orders/track")
    params = {}
    if track is not None:
        params["track"] = track
    response = requests.get(url, params=params)
    return response
