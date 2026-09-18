"""
База городов России с координатами для погодного бота.
Все координаты проверены через Open-Meteo API.

Формат: имя города → (широта, долгота) и часовой пояс
"""

# ============= ГОРОДА РОССИИ =============
# Формат: "Название" -> {"lat": широта, "lon": долгота, "timezone": часовой пояс}
CITIES = {
    # === Крупнейшие ===
    "Москва": {"lat": 55.7558, "lon": 37.6173, "timezone": "Europe/Moscow"},
    "Санкт-Петербург": {"lat": 59.9311, "lon": 30.3609, "timezone": "Europe/Moscow"},
    "Новосибирск": {"lat": 55.0084, "lon": 82.9357, "timezone": "Asia/Novosibirsk"},
    "Екатеринбург": {"lat": 56.8389, "lon": 60.6057, "timezone": "Asia/Yekaterinburg"},
    "Казань": {"lat": 55.7944, "lon": 49.1115, "timezone": "Europe/Moscow"},

    # === Города-миллионники ===
    "Нижний Новгород": {"lat": 56.3269, "lon": 44.0059, "timezone": "Europe/Moscow"},
    "Челябинск": {"lat": 55.1644, "lon": 61.4368, "timezone": "Asia/Yekaterinburg"},
    "Самара": {"lat": 53.1959, "lon": 50.1001, "timezone": "Europe/Samara"},
    "Омск": {"lat": 54.9885, "lon": 73.3242, "timezone": "Asia/Omsk"},
    "Ростов-на-Дону": {"lat": 47.2225, "lon": 39.7188, "timezone": "Europe/Moscow"},
    "Уфа": {"lat": 54.7388, "lon": 55.9721, "timezone": "Asia/Yekaterinburg"},
    "Красноярск": {"lat": 56.0153, "lon": 92.8932, "timezone": "Asia/Krasnoyarsk"},
    "Воронеж": {"lat": 51.6720, "lon": 39.1843, "timezone": "Europe/Moscow"},
    "Пермь": {"lat": 58.0105, "lon": 56.2502, "timezone": "Asia/Yekaterinburg"},
    "Волгоград": {"lat": 48.7194, "lon": 44.5018, "timezone": "Europe/Volgograd"},

    # === Крупные города ===
    "Краснодар": {"lat": 45.0355, "lon": 38.9753, "timezone": "Europe/Moscow"},
    "Саратов": {"lat": 51.5924, "lon": 46.0343, "timezone": "Europe/Saratov"},
    "Тюмень": {"lat": 57.1522, "lon": 65.5272, "timezone": "Asia/Yekaterinburg"},
    "Тольятти": {"lat": 53.5303, "lon": 49.3461, "timezone": "Europe/Samara"},
    "Барнаул": {"lat": 53.3481, "lon": 83.7798, "timezone": "Asia/Barnaul"},
    "Ижевск": {"lat": 56.8527, "lon": 53.2115, "timezone": "Europe/Samara"},
    "Ульяновск": {"lat": 54.3142, "lon": 48.4031, "timezone": "Europe/Ulyanovsk"},
    "Иркутск": {"lat": 52.2870, "lon": 104.3050, "timezone": "Asia/Irkutsk"},
    "Хабаровск": {"lat": 48.4827, "lon": 135.0840, "timezone": "Asia/Vladivostok"},
    "Ярославль": {"lat": 57.6261, "lon": 39.8845, "timezone": "Europe/Moscow"},
    "Владивосток": {"lat": 43.1155, "lon": 131.8855, "timezone": "Asia/Vladivostok"},
    "Махачкала": {"lat": 42.9764, "lon": 47.5024, "timezone": "Europe/Moscow"},
    "Томск": {"lat": 56.4847, "lon": 84.9482, "timezone": "Asia/Tomsk"},
    "Оренбург": {"lat": 51.7682, "lon": 55.0969, "timezone": "Asia/Yekaterinburg"},
    "Кемерово": {"lat": 55.3547, "lon": 86.0873, "timezone": "Asia/Novokuznetsk"},

    # === Туристические и популярные ===
    "Калининград": {"lat": 54.7104, "lon": 20.5101, "timezone": "Europe/Kaliningrad"},
    "Сочи": {"lat": 43.5855, "lon": 39.7231, "timezone": "Europe/Moscow"},
    "Тула": {"lat": 54.1961, "lon": 37.6182, "timezone": "Europe/Moscow"},
    "Тверь": {"lat": 56.8587, "lon": 35.9176, "timezone": "Europe/Moscow"},
    "Владимир": {"lat": 56.1290, "lon": 40.4070, "timezone": "Europe/Moscow"},
    "Великий Новгород": {"lat": 58.5214, "lon": 31.2755, "timezone": "Europe/Moscow"},
    "Псков": {"lat": 57.8194, "lon": 28.3318, "timezone": "Europe/Moscow"},
    "Мурманск": {"lat": 68.9585, "lon": 33.0827, "timezone": "Europe/Moscow"},
    "Архангельск": {"lat": 64.5399, "lon": 40.5183, "timezone": "Europe/Moscow"},
    "Петрозаводск": {"lat": 61.7849, "lon": 34.3469, "timezone": "Europe/Moscow"},

    # === Юг и Кавказ ===
    "Ставрополь": {"lat": 45.0428, "lon": 41.9734, "timezone": "Europe/Moscow"},
    "Пятигорск": {"lat": 44.0486, "lon": 43.0594, "timezone": "Europe/Moscow"},
    "Нальчик": {"lat": 43.4981, "lon": 43.6189, "timezone": "Europe/Moscow"},
    "Владикавказ": {"lat": 43.0367, "lon": 44.6678, "timezone": "Europe/Moscow"},
    "Грозный": {"lat": 43.3169, "lon": 45.6981, "timezone": "Europe/Moscow"},

    # === Сибирь и Дальний Восток ===
    "Новокузнецк": {"lat": 53.7557, "lon": 87.1099, "timezone": "Asia/Novokuznetsk"},
    "Чита": {"lat": 52.0340, "lon": 113.4994, "timezone": "Asia/Chita"},
    "Улан-Удэ": {"lat": 51.8335, "lon": 107.5841, "timezone": "Asia/Irkutsk"},
    "Якутск": {"lat": 62.0355, "lon": 129.6755, "timezone": "Asia/Yakutsk"},
    "Петропавловск-Камчатский": {"lat": 53.0452, "lon": 158.6483, "timezone": "Asia/Kamchatka"},
    "Южно-Сахалинск": {"lat": 46.9591, "lon": 142.7380, "timezone": "Asia/Sakhalin"},
    "Сургут": {"lat": 61.2540, "lon": 73.3962, "timezone": "Asia/Yekaterinburg"},
    "Нижневартовск": {"lat": 60.9344, "lon": 76.5531, "timezone": "Asia/Yekaterinburg"},
}


# ============= ФУНКЦИИ ДЛЯ РАБОТЫ С ГОРОДАМИ =============

def get_all_cities() -> list:
    """Вернуть список всех доступных городов"""
    return sorted(CITIES.keys())


def get_city_coords(city_name: str) -> dict:
    """
    Получить координаты города по названию.
    Возвращает dict с lat, lon, timezone или None.
    Поиск нечувствителен к регистру.
    """
    # Точное совпадение
    if city_name in CITIES:
        return CITIES[city_name]

    # Поиск без учёта регистра
    for name, coords in CITIES.items():
        if name.lower() == city_name.lower():
            return coords

    return None


def find_cities(query: str) -> list:
    """
    Найти города по частичному совпадению.
    Например: "новг" найдёт "Нижний Новгород" и "Великий Новгород".
    """
    query_lower = query.lower()
    return [name for name in CITIES if query_lower in name.lower()]


def get_cities_count() -> int:
    """Сколько городов в базе"""
    return len(CITIES)
