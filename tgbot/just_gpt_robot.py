import requests
import aiogram
import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from auth.openaitokens import sandbox_tg_bot
from auth.tgtokens import just_gpt_robot

bot = Bot(token=just_gpt_robot)
dp = Dispatcher(bot)

openai.api_key = sandbox_tg_bot

# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Отправь мне свой вопрос, и я постараюсь дать ответ с помощью искусственного интеллекта.")

# Обработчик для всех текстовых сообщений
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    try:
        
        # Отправляем запрос в OpenAI API с использованием правильного конечного точки для chat
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}],
        )

        # Извлекаем текст ответа из ответа API
        if response.get('choices'):
            answer = response['choices'][0]['message']['content']
        else:
            answer = "Извините, не удалось получить ответ."

    except Exception as e:
        answer = f"Произошла ошибка при обращении к OpenAI API: {e}"

    # Отправляем ответ пользователю в телеграм
    await message.answer(answer)

# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)