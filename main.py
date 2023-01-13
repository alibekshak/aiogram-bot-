import csv 
from os import system
from time import sleep
from datetime import datetime


import requests
import logging
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from core.config import TOKEN, ADMIN_ID, WEATHER_IP
from core.weather import weather_city

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# with open(f"core/admin/data/UserInfo.csv", "a", encoding="UTF-8") as file:
#     writer = csv.writer(file)
#     ID = "ID"
#     USERNAME = "USERNAME"
#     FIRST_NAME = "FIRST_NAME"
#     LAST_NAME = "LAST_NAME"
#     PHONE = "PHONE"
#     writer.writerow((ID, USERNAME, FIRST_NAME, LAST_NAME, PHONE))

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Зарегистрироваться", request_contact=True)
    )
    photo_start = open("core/static/image/f53d3f8a2b09f6431df49140c39ba639.jpg", "rb")
    await message.answer_photo(photo=photo_start, caption="Привет я бот, для работы пройдите регистрацию", reply_markup=markup)
        

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contact_start(message : types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Алматы"), KeyboardButton("Астана"), KeyboardButton("Талдыкорган"),
        KeyboardButton("Шымкент"), KeyboardButton("Караганда"), KeyboardButton("Актау"),
        KeyboardButton("Кызылорда"), KeyboardButton("Актобе"), KeyboardButton("Семей"),
    )

    user_id = message.contact.user_id
    username = message.chat.username
    first_name = message.contact.first_name
    last_name = message.contact.last_name
    phone = message.contact.phone_number
    with open(f"core/admin/data/UserInfo.csv", "a", encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                user_id,
                username,
                first_name, 
                last_name,
                phone
            )
        )

        Informations = f"""
id: {user_id},
first_name: {first_name}
last_name: {last_name}
phone: {phone}
created: {datetime.now().strftime("%Y-%m-%d %H %M ")}
        """
        registration_photo = open("core/static/image/f53d3f8a2b09f6431df49140c39ba639.jpg", "rb")
        await bot.send_photo(ADMIN_ID, registration_photo, Informations)
        await message.answer("Вы успешно зарегистрированы, напишите название любого города", reply_markup=markup)

@dp.message_handler(content_types=["text"])
async def weather_city_author(message: types.Message):
    get_weather_def = weather_city(message.text)
    await message.answer(get_weather_def)


if __name__ == "__main__":  
    executor.start_polling(dp)