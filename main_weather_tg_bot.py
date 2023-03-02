import emoji
import requests
import datetime
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from config import open_weather_token, token


bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Этот бот выводит информацию о погоде в любом городе,"
                        " который ты введешь. Чобы начать, введи название города!")


@dp.message_handler(commands=['contacts'])
async def process_contacts_command(message: types.Message):
    await message.reply("По всем вопросам и предложениям вы можете написать мне на почту rudenkoalexey@ukr.net")


def get_weather_information(message_text):

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
            f"https://api.openweathermap.org/data/2.5/weather?q={message_text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        name = data["name"]

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

        information = f"{datetime.datetime.now().strftime('%Y-%m-%d')}" \
                             f"                             {datetime.datetime.now().strftime('%H:%M')}" \
                             f"\nГород: {name} {emoji.emojize(flag)}" \
                             f"\nТемпература: {cur_weather} С°" \
                             f"\n{wd}" \
                             f"\nОщущается как {feels_like} градусов" \
                             f"\nВлажность: {humidity} %" \
                             f"\nВосход в {sunrise_timestamp.strftime('%H:%M:%S')}" \
                             f"\nЗакат в {sunset_timestamp.strftime('%H:%M:%S')}"



        return information

    except Exception:
        return ("Проверьте название или введите название более крупного города\U00002620")


@dp.message_handler()
async def request_weather(message: types.Message):
    message_text = message.text
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text=f"{message.text}", callback_data=f"city_name|{message_text}|{chat_id}"))

    # , callback_data=f"city_name|{message}"))
    message_text = message.text
    await message.answer(get_weather_information(message_text), reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('city_name'))
async def send_city(callback_query: types.CallbackQuery):
    city_name, message_text, chat_id = callback_query.data.split("|")

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text=f"{message_text}", callback_data=f"city_name|{message_text}|{chat_id}"))

    await bot.send_message(chat_id, text = f"{get_weather_information(message_text)}", reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dp)