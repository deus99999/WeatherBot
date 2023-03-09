
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from config import token
from functions import get_weather_information

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Этот бот выводит информацию о погоде в любом городе,"
                        " который ты введешь. Чобы начать, введи название города!")


@dp.message_handler(commands=['contacts'])
async def process_contacts_command(message: types.Message):
    await message.reply("По всем вопросам и предложениям вы можете написать мне на почту rudenkoalexey@ukr.net")


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