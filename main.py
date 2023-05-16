import pprint
from datetime import datetime
import requests
from aiogram import Bot, Dispatcher, executor, types
from config import *
bot = Bot(tg_token)

dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=f'Привет, {message.chat.first_name}!\nДля продолжения просто напишите город который вас интересует')


@dp.message_handler()
async def send_info_about_city(message: types.Message):
    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric'
        )

        data = r.json()
        city_name = message.text.capitalize()
        temp = int(data['main']['temp'])
        feels_like = int(data['main']['feels_like'])
        humidity = int(data['main']['humidity'])
        wind_speed = int(data['wind']['speed'])
        sunrise =  datetime.fromtimestamp(data['sys']['sunrise'])
        await bot.send_message(chat_id=message.chat.id, text=f'Сегодня {datetime.now().strftime("%m.%d.%Y")}\n\n'
                                                             f'Вы выбрали город: {city_name}\n\n'
                                                             f'В текущем городе сейчас: {temp} ℃\n'
                                                             f'По ощущениям: {feels_like} ℃\n\n'
                                                             f'Влажность воздуха: {humidity} %\n'
                                                             f'Скорость ветра: {wind_speed} м/с\n')



    except Exception:
        await bot.send_message(chat_id=message.chat.id, text='Неправильно введен город')
executor.start_polling(dp)