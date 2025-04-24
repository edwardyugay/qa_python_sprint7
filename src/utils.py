# src/utils.py
from faker import Faker

# Используем локаль 'ru_RU' для получения данных на русском языке
fake = Faker('ru_RU')

def generate_courier_data() -> dict:
    """
    Генерирует уникальные тестовые данные для курьера.
    Используются методы Faker:
      - user_name для логина,
      - password для пароля,
      - first_name для имени.
    """
    return {
        "login": fake.user_name(),
        "password": fake.password(length=10),
        "firstName": fake.first_name()
    }
