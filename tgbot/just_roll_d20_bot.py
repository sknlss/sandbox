import d20
import csv
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from auth.tgtokens import just_roll_d20_bot
from log_message import log_message

# Путь к файлу с логами
log_path = 'tgbot/log/messages.csv'
bot_owner = 'sknlss'
bot = Bot(token=just_roll_d20_bot)
dp = Dispatcher(bot)

# Список вариантов кубиков для обработчиков
dice_variants = [4, 6, 8, 10, 12, 100, 20]

# Обобщенная функция для обработки команд кубиков
async def send_dice(message: types.Message, num_sides: int):
    await message.answer(str(d20.roll(f'd{num_sides}')))
    await log_message(await bot.get_me(), message, log_path)

# Создание обработчиков для каждой команды кубика
for num_sides in dice_variants:
    command = f'd{num_sides}'
    dp.register_message_handler(lambda message, ns=num_sides: send_dice(message, ns), commands=command)

# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Этот бот кидает кубы\n"
                         "/roll Популярные варианты кубиков\n"
                         "/help Описание расширенного функционала бота")
    await log_message(await bot.get_me(), message, log_path)

# Обработчик для команды /roll
@dp.message_handler(commands=['roll'])
async def send_roll(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = [
        types.InlineKeyboardButton(f"d{num}", callback_data=f"d{num}") for num in dice_variants
    ]
    markup.add(*buttons)
    await message.answer("Выберите вариант кубика:", reply_markup=markup)
    await log_message(await bot.get_me(), message, log_path)

# Обработчик для команды /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer("Можно бросать кубы, нажимая на кнопки через команду /roll\n\n"
                         "Можно бросать кубы через команды\n"
                         "/d4 /d6 /d8 /d10 /d12 /d100 /d20\n\n"
                         "Можно ввести количество кубов и модификаторы текстом\n"
                         "Примеры: `d20` / `1d20+5` / `3d4+3` / `10d6` / `1d8+2d6+5`"
                         , parse_mode=types.ParseMode.MARKDOWN)
    await log_message(await bot.get_me(), message, log_path)

# Обработчик для команды /dialogs
@dp.message_handler(commands=['dialogs'])
async def list_dialogs(message: types.Message):
    if message.from_user.username == 'sknlss':
        try:
            bot_info = await bot.get_me()
            bot_username = bot_info.username
            bot_id = bot_info.id

            bot_dialogs = {}
            with open(log_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Пропустить заголовок
                for row in reader:
                    if row[0] == bot_username and row[1] == str(bot_id):
                        username, user_id = row[3], row[4]
                        if (username, user_id) not in bot_dialogs:
                            bot_dialogs[(username, user_id)] = 1
                        else:
                            bot_dialogs[(username, user_id)] += 1
            
            response = f"Диалоги с `{bot_username}` (id: `{bot_id}`):\n"
            for (username, user_id), message_count in bot_dialogs.items():
                response += f"user\_id: `{user_id}` username: `{username}` messages: `{message_count}`\n"
            
            await message.answer(response, parse_mode=types.ParseMode.MARKDOWN)
        except FileNotFoundError:
            await message.answer("Файл с логами не найден.")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {str(e)}")
    else:
        await message.answer("Error 403: Доступ запрещен.")


# Обработчик для кнопок выбора кубика
@dp.callback_query_handler(lambda c: c.data.startswith("d"))
async def process_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, str(d20.roll(callback_query.data)))

# Обработчик для любого текстового ввода
@dp.message_handler(lambda message: True)
async def send_dice_roll_from_text(message: types.Message):
    try:
        await message.answer(str(d20.roll(message.text.lower())))
        await log_message(await bot.get_me(), message, log_path)
    except:
        pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
