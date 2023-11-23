from aiogram import Bot
from components.config import API_TOKEN
from database import Database

db = Database('db')
bot = Bot(token=API_TOKEN)

