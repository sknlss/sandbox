import csv
import os
import time
from datetime import datetime
from aiogram import Bot
from aiogram import types

# Функция для логирования сообщений
async def log_message(bot: Bot, message: types.Message, log_path):
    # Проверяем, что сообщение - это текстовое сообщение или команда
    if message.text or message.is_command():
        # Проверяем, существует ли файл или он пуст
        if not os.path.exists(log_path) or os.path.getsize(log_path) == 0:
            with open(log_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['bot_username', 'bot_id', 'datetime', 'username', 'user_id', 'text_message'])
        
        with open(log_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([bot.username,
                             bot.id,
                             datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'),
                             message.from_user.username,
                             message.from_user.id,
                             message.text
                             ])