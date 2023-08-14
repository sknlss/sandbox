from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import executor

from auth.tgtokens import direkta_bot

from log_message import log_message

# Путь к файлу с логами
log_path = 'tgbot/log/messages.csv'

bot = Bot(token=direkta_bot)
dp = Dispatcher(bot)

# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer('Этот бот делает вещи\n'
                        'Описание расширенного функционала бота /help')
    await log_message(await bot.get_me(), message, log_path)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)