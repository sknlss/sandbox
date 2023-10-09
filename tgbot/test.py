import pandas as pd
import mysql.connector
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.utils import executor
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from aiogram.dispatcher.filters.state import State, StatesGroup

from auth.tgtokens import witty_robot
from auth.mysql import tgbot

# Инициализируем бота и диспетчера
bot = Bot(token=witty_robot)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Инициализируем подключение к базе данных
db_url = f"mysql+pymysql://{tgbot['username']}:{tgbot['password']}@{tgbot['host']}:{tgbot['port']}/{tgbot['database']}"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
db = Session()
metadata = MetaData()

# Определяем таблицы в базе данных
users_table = Table('user', metadata, autoload_with=engine)
messages_table = Table('message', metadata, autoload_with=engine)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user = await get_user(message.from_user)
    await message.answer(f"Привет, {message.from_user.first_name}! Этот бот сохраняет твои сообщения. Просто напиши что-нибудь, и я запишу.")

# Обработчик текстовых сообщений
@dp.message_handler(lambda message: message.text and not message.text.startswith('/'), state='*')
async def process_message(message: types.Message, state: FSMContext):
    # Сохраняем сообщение в базе данных
    user = await get_user(message.from_user)
    await save_message(message, user)

    await message.answer("Сообщение сохранено!")

# Функция для получения пользователя из базы данных или создания нового
async def get_user(user: types.User):
    existing_user = db.query(users_table).filter(users_table.c.tg_user_id == user.id).first()
    if existing_user:
        return existing_user

    new_user = users_table.insert().values(
        type='new',
        tg_user_id=user.id,
    )
    db.execute(new_user)
    db.commit()
    return db.query(users_table).filter(users_table.c.tg_user_id == user.id).first()

# Функция для сохранения сообщения в базе данных
async def save_message(message: types.Message, user):
    new_message = messages_table.insert().values(
        tg_message_id=message.message_id,
        text=message.text,
        user_id=user.id,
        tg_user_id=message.from_user.id,
        tg_username=message.from_user.username,
        tg_firstname=message.from_user.first_name,
        tg_lastname=message.from_user.last_name,
        tg_lang=message.from_user.language_code,
        conversation_id=None,  # Здесь должен быть идентификатор беседы, если нужно
    )
    db.execute(new_message)
    db.commit()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)