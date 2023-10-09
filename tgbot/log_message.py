import os
import time
from datetime import datetime
import pandas as pd
from aiogram import Bot
from aiogram import types

# Функция для логирования сообщений
async def log_message(bot: Bot, message: types.Message, log_path):
    # Проверяем, что сообщение - это текстовое сообщение или команда
    if message.text or message.is_command():
        # Проверяем, существует ли файл или он пуст
        if not os.path.exists(log_path) or os.path.getsize(log_path) == 0:
            # Создаем пустой DataFrame с заголовками столбцов
            df = pd.DataFrame(columns=['bot_username', 'bot_id', 'datetime', 'username', 'user_id', 'text_message'])
            df.to_csv(log_path, index=False, encoding='utf-8')
        
        # Создаем DataFrame с новой строкой для логирования
        new_row = {
            'bot_username': bot.username,
            'bot_id': bot.id,
            'datetime': datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'),
            'username': message.from_user.username,
            'user_id': message.from_user.id,
            'text_message': message.text
        }
        df = pd.DataFrame([new_row])
        
        # Добавляем новую строку в существующий файл с логами
        df.to_csv(log_path, mode='a', header=False, index=False, encoding='utf-8')
