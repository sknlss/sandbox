import re

import d20

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import executor

from auth.tgtokens import just_gpt_robot

bot = Bot(token=just_gpt_robot)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer('Этот бот кидает кубы\n'
                        '/roll Популярные варианты кубиков\n'
                        '/help Описание расширенного функционала бота')

@dp.message_handler(commands=['roll'])
async def send_roll(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = [
        types.InlineKeyboardButton("d4", callback_data="d4"),
        types.InlineKeyboardButton("d6", callback_data="d6"),
        types.InlineKeyboardButton("d8", callback_data="d8"),
        types.InlineKeyboardButton("d10", callback_data="d10"),
        types.InlineKeyboardButton("d12", callback_data="d12"),
        types.InlineKeyboardButton("d100", callback_data="d100"),
        types.InlineKeyboardButton("d20", callback_data="d20"),
    ]
    markup.add(*buttons)
    await message.answer("Выберите вариант кубика:", reply_markup=markup)

@dp.message_handler(commands=['d4'])
async def send_d4(message: types.Message):
    await message.answer(str(d20.roll('d4')))

@dp.message_handler(commands=['d6'])
async def send_d6(message: types.Message):
    await message.answer(str(d20.roll('d6')))

@dp.message_handler(commands=['d8'])
async def send_d8(message: types.Message):
    await message.answer(str(d20.roll('d8')))

@dp.message_handler(commands=['d10'])
async def send_d10(message: types.Message):
    await message.answer(str(d20.roll('d10')))

@dp.message_handler(commands=['d12'])
async def send_d12(message: types.Message):
    await message.answer(str(d20.roll('d12')))

@dp.message_handler(commands=['d100'])
async def send_d100(message: types.Message):
    await message.answer(str(d20.roll('d100')))

@dp.message_handler(commands=['d20'])
async def send_d20(message: types.Message):
    await message.answer(str(d20.roll('d20')))

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer('Можно бросать кубы, нажимая на кнопки через команду /roll\n\n'
                         'Можно бросать кубы через команды\n'
                          '/d4 /d6 /d8 /d10 /d12 /d100 /d20\n\n'
                         'Можно ввести количество кубов и модификаторы текстом\n'
                         'Примеры: `d20` / `1d20+5` / `3d4+3` / `10d6` / `1d8+2d6+5`'
                         , parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data in ["d4", "d6", "d8", "d10", "d12", "d100", "d20"])
async def process_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, str(d20.roll(callback_query.data)))

@dp.message_handler()
async def echo(message: types.Message):
    try:
        await message.answer(str(d20.roll(message.text)))
    except Exception as e:
        if message.chat.type == types.ChatType.GROUP or message.chat.type == types.ChatType.SUPERGROUP:
            pass
        else:
            await message.answer('Примеры корректных запросов: "d20" "1d20+5" "3d4+3" "10d6" "1d8+2d6+5"')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)