import datetime

from aiogram import Bot, Dispatcher, types, executor
from config import *
import requests
from colorama import init, Fore, Style

init() #инциализация бибилотеки colorama для цветого вывода состояния бота

async def on_startup(_):
    """Эта функция нужна для вывода в консоль запущен ли бот или нет + цветной вывод"""
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Бот запущен')

def time_part():
    """определение части дня"""
    time_now = int(datetime.datetime.now().strftime('%H'))
    night_part = 00
    morning_part = 6
    day_part = 13
    evening_part = 18
    if time_now >= night_part and time_now < morning_part:
        return 'ночь' + '🌃'
    elif time_now >= morning_part and time_now < day_part:
        return 'утро' + '☀️'
    elif time_now >= day_part and time_now < evening_part:
        return 'день' + '✨'
    else:
        return 'вечер' + '🌆'


def bye_message(part, name):
    """сообщения для прощания с пользователем"""
    if part == 'утро☀️' or part == 'день✨':
        return f'Хорошего и продуктивного вам дня, {name}!\n'
    elif part == 'вечер🌆':
        return f'Хорошего вам вечера, {name}!\n'
    else:
        return f'Доброй ночи, {name}!\n'

def heart_dispay(part):
    """вывод сердца в конце после прощания в зависимости от того
        какая часть дня у пользователя
    """
    if part == 'утро☀️':
        return '💛'
    elif part == 'день✨':
        return '💚'
    elif part == 'вечер🌆':
        return '🧡'
    else:
        return '🖤'

bot = Bot(tg_token)

dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def hello_message(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=f'прив, {message.from_user.first_name}\n'
                                                         f'этот бот показывает погоду, просто напишите ваш город на английском')

@dp.message_handler()
async def get_weather(message: types.Message):
    try: #если пользователь введет несуществующий город, то ему выдаст исключение - 'вы неправильно ввели город'
        global wd
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric' #получени информации со страницы
        )
        statuses = {
            """статусы для обозначения погоды визуального и текстового обозначения статуса погоды"""
            'Drizzle': 'Мелкий дождь' + '💧',
            'Rain': 'Дождь' + '💦',
            'Thunderstorm': 'Гроза' + '⚡️',
            'Mist': 'Туман' + '🌫',
            'Snow': 'Снег' + '❄️',
            'Clear': 'Ясно' + '☀️',
            'Clouds': 'Облачно' + '☁️',
        }


        data = r.json() #конвертирование в json формат
        weather_description = data['weather'][0]['main']


        if weather_description in statuses:
            wd = statuses[weather_description] #если текущая погода есть в статусах, то переменная получается значение этого статуса
        else:
            await bot.send_message(chat_id=message.chat.id, text='Не могу распознать погоду, посмотри в окно')

        feel = int(data['main']['feels_like']) #сколько градусов по ощущениям
        humidity = data['main']['humidity'] #влажность
        temp = int(data['main']['temp']) #температура
        wind = data['wind']['speed'] #скорость ветра
        part = time_part() #часть дня

        """выводим пользователю всю информацию"""
        await bot.send_message(chat_id=message.chat.id, text=f"Вы выбрали город: {message.text}\n\n"
                                                             f"Сегодня {datetime.datetime.now().strftime('%d.%m.%y')}\n\n"
                                                             f"Температура в указанном городе {temp} °C, {wd}\n"
                                                             f"По ощущению {feel} °C\n"
                                                             f"Ветер сегодня до {wind} м/c\nВлажность воздуха составляет {humidity}%\n\n"
                                                             f"Скорее всего у вас сейчас {part}\n\n"
                                                             f"{bye_message(part, message.from_user.first_name)}")


        await bot.send_message(chat_id=message.chat.id, text=f'{heart_dispay(part)}') #после главной информации кидаем сердечко, в зависимости от текущей части дня
    except Exception:
        await bot.send_message(chat_id=message.chat.id, text='☠️' + 'должно быть, вы отправили неверное название города' + '☠️')


executor.start_polling(dp, on_startup=on_startup, skip_updates=True) #пропуск апдейтов и вывод в консоль состояние бота