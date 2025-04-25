from faker import Faker

fake = Faker('ru_RU')

def generate_order_payload(colors=None) -> dict:
    """
    Генерирует данные для создания заказа.
    Принимает список цветов или None.
    """
    payload = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.address(),
        "metroStation": str(fake.random_int(min=1, max=200)),
        "phone": fake.phone_number(),
        "rentTime": fake.random_int(min=1, max=10),
        "deliveryDate": fake.date_between(start_date="+1d", end_date="+30d").strftime("%Y-%m-%d"),
        "comment": fake.sentence(nb_words=5)
    }
    if colors is not None:
        payload["color"] = colors
    return payload
