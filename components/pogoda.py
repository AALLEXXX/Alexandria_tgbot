import requests
from bs4 import BeautifulSoup as BS
from create_bot import bot
from aiogram import types

def get_weather(url_from_user):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/88.0.4324.182 Safari/537.36"}
    url = url_from_user
    response = requests.get(url, headers=headers)
    bs = BS(response.content, 'html.parser')
    temp = bs.find('div', id="weather-now-number")
    return temp.text


async def show_pogoda(callback_query):
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)

    keyboard = types.InlineKeyboardMarkup()

    pog_moscow_but = types.InlineKeyboardButton(text="Москва🏙", callback_data="pogoda_moscow")
    pog_sp_but = types.InlineKeyboardButton(text="Санкт-Питербург🌉", callback_data="pogoda_sp")
    pog_sev_but = types.InlineKeyboardButton(text="Севастополь🏝", callback_data="pogoda_sev")
    return_but = types.InlineKeyboardButton(text="вернуться↩️", callback_data="return")

    keyboard.add(pog_moscow_but, pog_sp_but, pog_sev_but, return_but)

    await bot.send_message(callback_query.from_user.id, "🌐Выберите город:", reply_markup=keyboard)