import requests
import datetime

from config import open_weather_token, token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import emoji

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Этот бот выводит информацию о погоде в любом городе,"
                        " который ты введешь. Чобы начать, введи название города!")

cities = []


@dp.message_handler()
async def get_weather(message: types.Message):

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    flags = {
        "UA": ":Ukraine:",

    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        name = data["name"]
        cities.append(name)
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Что-то непонятное"

        country = data["sys"]["country"]
        if country in flags:
            flag = flags[country]
        else:
            flag = ""
        humidity = data["main"]["humidity"]
        # wind_speed = data["wind"]["speed"]
        feels_like = data["main"]["feels_like"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text=f"{name}", callback_data="city"))
        await message.answer(f"{datetime.datetime.now().strftime('%Y-%m-%d')}       "
                             f"                    {datetime.datetime.now().strftime('%H:%M')}"
                             f"\nГород: {name} {emoji.emojize(flag)}"
                             f"\nТемпература: {cur_weather} С°"
                             f"\n{wd}"
                             f"\nОщущается как {feels_like} градусов"
                             f"\nВлажность: {humidity} %"
                             f"\nВосход в {sunrise_timestamp.strftime('%H:%M:%S')}"
                             f"\nЗакат в {sunset_timestamp.strftime('%H:%M:%S')}",
                             reply_markup=keyboard)

    except Exception:
        await message.reply("Проверьте название или введите название более крупного города\U00002620")


@dp.callback_query_handler(text="city")
async def send_city(call: types.CallbackQuery):
    await call.message.answer("роботаю над этим..")


if __name__ == "__main__":
    executor.start_polling(dp)