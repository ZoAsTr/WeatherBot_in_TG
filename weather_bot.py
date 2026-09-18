import asyncio
import aiohttp
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
import os
from dotenv import load_dotenv
from cities import get_all_cities, get_city_coords, find_cities

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

USER_CITIES = {}

class CityForm(StatesGroup):
    searching = State()

async def get_weather(city_data: dict):
    """Получаем текущую погоду и прогноз с Open-Meteo API"""
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": city_data["lat"],
        "longitude": city_data["lon"],
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": city_data["timezone"],
        "forecast_days": 7
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                logger.debug(f"API status: {response.status}")
                
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    logger.error(f"API error: {response.status} - {error_text}")
                    return None
    except Exception as e:
        logger.error(f"Request error: {e}")
        return None

def interpret_weather_code(code: int) -> str:
    """Переводит WMO код в понятное описание"""
    weather_codes = {
        0: "☀️ Ясно",
        1: "🌤️ Облачно",
        2: "⛅ Переменная облачность",
        3: "☁️ Пасмурно",
        45: "🌫️ Туман",
        48: "🌫️ Туман с инеем",
        51: "🌦️ Лёгкий морось",
        53: "🌦️ Морось",
        55: "🌧️ Сильная морось",
        61: "🌧️ Небольшой дождь",
        63: "🌧️ Дождь",
        65: "⛈️ Сильный дождь",
        71: "❄️ Небольшой снег",
        73: "❄️ Снег",
        75: "❄️ Сильный снег",
        77: "❄️ Снежные зёрна",
        80: "🌧️ Ливни",
        81: "⛈️ Сильные ливни",
        82: "⛈️ Экстремальные ливни",
        85: "❄️ Снежные ливни",
        86: "❄️ Сильные снежные ливни",
        95: "⛈️ Гроза",
        96: "⛈️ Гроза с градом",
        99: "⛈️ Гроза с сильным градом"
    }
    return weather_codes.get(code, "❓ Неизвестно")

def get_weather_advice(code: int, temp: float, wind_speed: float) -> str:
    """Даёт советы на основе погоды"""
    advice = []
    
    if temp > 30:
        advice.append("☀️ Очень жарко! Не забудь защиту от солнца.")
    elif temp < -10:
        advice.append("🧤 Мороз! Одевайся теплее.")
    elif temp < 5:
        advice.append("🧥 Холодно! Тёплая куртка обязательна.")
    
    if wind_speed > 15:
        advice.append("💨 Сильный ветер! Будь осторожнее.")
    
    if code in [95, 96, 99]:
        advice.append("⚡ Гроза! Лучше остаться дома.")
    
    return "\n".join(advice) if advice else "✅ Никаких особых предупреждений"

def format_current_weather(data: dict, city_name: str) -> str:
    """Форматирует текущую погоду"""
    current = data.get("current", {})
    
    temp = current.get("temperature_2m", "N/A")
    feels_like = current.get("apparent_temperature", "N/A")
    humidity = current.get("relative_humidity_2m", "N/A")
    wind = current.get("wind_speed_10m", "N/A")
    weather = interpret_weather_code(current.get("weather_code", 0))
    
    return f"""🌍 <b>Погода в {city_name}</b>

{weather}

🌡️ Температура: <b>{temp}°C</b>
🤔 Ощущается как: <b>{feels_like}°C</b>
💧 Влажность: <b>{humidity}%</b>
💨 Ветер: <b>{wind} км/ч</b>
"""

def format_week_forecast(data: dict, city_name: str) -> str:
    """Форматирует прогноз на неделю"""
    daily = data.get("daily", {})
    times = daily.get("time", [])
    temps_max = daily.get("temperature_2m_max", [])
    temps_min = daily.get("temperature_2m_min", [])
    weather_codes = daily.get("weather_code", [])
    precipitation = daily.get("precipitation_sum", [])
    
    forecast = f"📅 <b>Прогноз на 7 дней ({city_name})</b>\n\n"
    
    for i in range(min(7, len(times))):
        date = datetime.fromisoformat(times[i]).strftime("%a, %d.%m")
        weather = interpret_weather_code(weather_codes[i])
        max_t = temps_max[i]
        min_t = temps_min[i]
        rain = precipitation[i] if i < len(precipitation) else 0
        
        rain_text = f" 🌧️ {rain}мм" if rain > 0 else ""
        forecast += f"{date}: {weather} {min_t}..{max_t}°C{rain_text}\n"
    
    return forecast

def format_advice(data: dict) -> str:
    """Даёт полезные советы"""
    current = data.get("current", {})
    
    temp = current.get("temperature_2m", 0)
    wind = current.get("wind_speed_10m", 0)
    code = current.get("weather_code", 0)
    
    advice = get_weather_advice(code, temp, wind)
    
    return f"""💡 <b>Советы для сегодня</b>\n\n{advice}"""

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт основное меню"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="☀️ Сейчас"), KeyboardButton(text="📅 На неделю")],
            [KeyboardButton(text="💡 Советы"), KeyboardButton(text="🏙️ Выбрать город"), KeyboardButton(text="🔍 Найти город")],
            [KeyboardButton(text="ℹ️ О боте")]
        ],
        resize_keyboard=True
    )

def get_popular_cities_keyboard() -> InlineKeyboardMarkup:
    """Кнопки с самыми популярными городами"""
    popular = [
        "Москва", "Санкт-Петербург", "Нижний Новгород",
        "Казань", "Новосибирск", "Екатеринбург",
        "Краснодар", "Сочи", "Владивосток"
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=city, callback_data=f"pick_{city}")]
            for city in popular
        ]
    )

def get_all_cities_keyboard() -> InlineKeyboardMarkup:
    """Кнопки со всеми городами (по 2 в строке)"""
    cities = get_all_cities()
    rows = []
    
    for i in range(0, len(cities), 2):
        if i + 1 < len(cities):
            row = [
                InlineKeyboardButton(text=cities[i], callback_data=f"pick_{cities[i]}"),
                InlineKeyboardButton(text=cities[i + 1], callback_data=f"pick_{cities[i + 1]}")
            ]
        else:
            row = [InlineKeyboardButton(text=cities[i], callback_data=f"pick_{cities[i]}")]
        rows.append(row)
    
    return InlineKeyboardMarkup(inline_keyboard=rows)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Команда /start"""
    user_id = message.from_user.id
    current = USER_CITIES.get(user_id, None)

    if current:
        text = f"👋 Привет! Текущий город: <b>{current}</b>.\n\nВыбери, что хочешь узнать:"
    else:
        text = "👋 Привет! Я погодный бот.\n\nВыбери город:"

    await message.answer(text, parse_mode="HTML", reply_markup=get_main_keyboard())

@dp.message(F.text == "🏙️ Выбрать город")
async def choose_city(message: types.Message):
    """Выбор популярного города"""
    await message.answer(
        "🏙️ <b>Популярные города:</b>\n\n"
        "Или напиши /all_cities чтобы увидеть все города из базы.",
        parse_mode="HTML",
        reply_markup=get_popular_cities_keyboard())

@dp.message(Command("all_cities"))
async def all_cities_cmd(message: types.Message):
    """Показать все города"""
    await message.answer(
        "🏙️ <b>Все доступные города:</b>\n\n",
        parse_mode="HTML",
        reply_markup=get_all_cities_keyboard()
    )

@dp.callback_query(F.data.startswith("pick_"))
async def pick_city(callback: types.CallbackQuery):
    """Пользователь выбрал город из кнопок"""
    user_id = callback.from_user.id
    city_name = callback.data.removeprefix("pick_")

    coords = get_city_coords(city_name)
    if not coords:
        await callback.answer("❌ Город не найден")
        return

    USER_CITIES[user_id] = city_name
    await callback.answer(f"✅ Выбран: {city_name}")

    await callback.message.edit_text(
        f"✅ Город <b>{city_name}</b> выбран!\n\n"
        f"Теперь нажми «☀️ Сейчас» чтобы увидеть погоду.",
        parse_mode="HTML"
    )

@dp.message(F.text == "🔍 Найти город")
async def search_city(message: types.Message, state: FSMContext):
    """Начать поиск города"""
    await state.set_state(CityForm.searching)
    await message.answer(
        "🔍 Напиши название города (или его часть):\n"
        "Например: <i>Новгород</i>",
        parse_mode="HTML"
    )

@dp.message(CityForm.searching)
async def search_process(message: types.Message, state: FSMContext):
    """Обработка поиска города"""
    query = message.text.strip()
    results = find_cities(query)

    if not results:
        await message.answer("❌ Город не найден. Попробуй ещё раз.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=city, callback_data=f"pick_{city}")]
            for city in results
        ]
    )

    await message.answer(
        f"🔍 Найдено городов: <b>{len(results)}</b>",
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await state.clear()

@dp.message(F.text == "☀️ Сейчас")
async def current_weather(message: types.Message):
    """Текущая погода"""
    user_id = message.from_user.id
    city_name = USER_CITIES.get(user_id, None)

    if not city_name:
        await message.answer(
            "❌ Город не выбран. Сначала выбери город.",
            reply_markup=get_main_keyboard()
        )
        return

    msg = await message.answer("⏳ Получаю данные...")

    coords = get_city_coords(city_name)
    data = await get_weather(coords)

    await msg.delete()
    
    if data:
        await message.answer(format_current_weather(data, city_name), parse_mode="HTML")
    else:
        await message.answer("❌ Не удалось получить данные о погоде. Попробуй позже.")

@dp.message(F.text == "📅 На неделю")
async def week_forecast(message: types.Message):
    """Прогноз на неделю"""
    user_id = message.from_user.id
    city_name = USER_CITIES.get(user_id, None)

    if not city_name:
        await message.answer(
            "❌ Город не выбран. Сначала выбери город.",
            reply_markup=get_main_keyboard()
        )
        return

    msg = await message.answer("⏳ Получаю прогноз...")
    
    coords = get_city_coords(city_name)
    data = await get_weather(coords)

    await msg.delete()
    
    if data:
        await message.answer(format_week_forecast(data, city_name), parse_mode="HTML")
    else:
        await message.answer("❌ Не удалось получить прогноз. Попробуй позже.")

@dp.message(F.text == "💡 Советы")
async def weather_advice(message: types.Message):
    """Советы на основе погоды"""
    user_id = message.from_user.id
    city_name = USER_CITIES.get(user_id, None)
    
    if not city_name:
        await message.answer(
            "❌ Город не выбран. Сначала выбери город.",
            reply_markup=get_main_keyboard()
        )
        return
    
    msg = await message.answer("⏳ Анализирую погоду...")
    
    coords = get_city_coords(city_name)
    data = await get_weather(coords)

    await msg.delete()

    if data:
        text = format_advice(data)
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer("❌ Не удалось получить данные. Попробуй позже.")

@dp.message(F.text == "ℹ️ О боте")
async def about_bot(message: types.Message):
    """Информация о боте"""
    user_id = message.from_user.id
    city_name = USER_CITIES.get(user_id, "не выбран")
    await message.answer(
        "ℹ️ <b>О боте</b>\n\n"
        "Это учебный погодный бот.\n\n"
        "Функции:\n"
        "• Текущая температура и условия\n"
        "• Прогноз на 7 дней\n"
        "• Советы на основе погоды\n\n"
        "📍 Локация: " + city_name + "\n"
        "🌐 Данные: Open-Meteo API",
        parse_mode="HTML"
    )

@dp.message()
async def echo(message: types.Message):
    """Обработчик всех остальных сообщений"""
    await message.answer(
        "🤔 Не понял команду. Используй кнопки меню!",
        reply_markup=get_main_keyboard()
    )

async def main():
    """Запуск бота"""
    logger.info("🤖 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен")

