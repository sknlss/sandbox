import d20

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import executor

from auth.tgtokens import just_roll_d20_bot

API_TOKEN = just_roll_d20_bot
bot = Bot(token=just_roll_d20_bot)
dp = Dispatcher(bot)

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