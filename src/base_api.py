# src/base_api.py
BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

def get_full_url(endpoint: str) -> str:
    """Возвращает полный URL для заданного эндпоинта."""
    return f"{BASE_URL}{endpoint}"
