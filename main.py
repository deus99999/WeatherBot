import requests
import datetime
from pprint import pprint
from config import open_weather_token


def get_weather(city, open_weather_token):

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds" : "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        pprint(data)

        name = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Что-то непонятное"

        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        feels_like = data["main"]["feels_like"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])


        print(f"{datetime.datetime.now().strftime('%Y-%m-%d')}\nГород: {name}\nТемпература: {cur_weather} С°\n{wd}\nОщущается как {feels_like} градусов\nВосход в {sunrise_timestamp.strftime('%H:%M:%S')}\nЗакат в {sunset_timestamp.strftime('%H:%M:%S')}")

    except Exception as ex:
        print(ex)
        print("Проверьте название города")


def main():
    city = input("Введите название вашего города: ")
    get_weather(city, open_weather_token)


if __name__ == "__main__":
    main()