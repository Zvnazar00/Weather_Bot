import requests
from config import open_weather_token, tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

but1 =KeyboardButton('Київ')
but2 =KeyboardButton('Львів')
but3 =KeyboardButton('Одеса')
but4 =KeyboardButton('Харків')
but5 =KeyboardButton('Дніпро')

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True). add(but1,but2,but3,but4,but5)


@dp.message_handler(commands=['weather'])
async def welcome(message: types.Message):
    await message.reply('Привіт! обирай своє місто, або апиши його, і я відправлю тобі погоду',  reply_markup=keyboard1)


@dp.message_handler()
async def get_weather(message: types.Message):

        smile_weather = {
            'Clear': '☀Ясно ☀ ',
            'Clouds': '☁Хмарно ☁',
            'Rain': '💧Дощ 💧',
            'Drizzle': '🌧Дощ 🌧',
            'Thurderstorm': '⚡Гроза ⚡',
            'Snow': '🌨Сніг 🌨',
            'Mist': '🌫Туманг 🌫'
        }

        try:
            a = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
                )
            data = a.json()
            city_name = data['name']  # виводимо назву
            country = data['sys']['country']  # виводмо країну
            if city_name == data['name']:
                chat_id = message.from_user.id
            photo_url = 'https://bit.ly/3DupBdl'
            await dp.bot.send_photo(chat_id=chat_id, photo=photo_url)

            weather = data['weather'][0]['main']
            if weather in smile_weather:
                wd = smile_weather[weather]
            else:
                wd = 'Незрозуміла погода, скоди подивись у вікно '

            temp = data['main']['temp']  # виводимо температуру
            humidity = data['main']['humidity']  # виводимо вологість
            pressure = data['main']['pressure']  # виводимо тиск
            wind = data['wind']['speed']  # виводимо швидкість вітру




            await message.reply(f'Погода в місті:⭐{city_name}⭐\n'
                                f'Країна:⭐{country}⭐\n|'
                                f'Температура:🌡️ {temp}C°🌡️\n'
                                f'Швидкість вітру:{wd}\n|'
                                f'Вологість:💧{humidity}%💧\n'
                                f'Тиск:🙂{pressure} мм рт.ст.🙂\n'
                                f'Швидкість вітру:🏎️{wind} м/с🏎️\n')
        except:
            await message.reply("Перевір назву міста:")

if __name__ == '__main__':
    executor.start_polling(dp)


