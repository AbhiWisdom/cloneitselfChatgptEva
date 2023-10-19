import logging
import openai
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
import datetime
import os
import threading

current_date_time = datetime.datetime.now()
current_date = current_date_time.date()
current_time = current_date_time.time()
owner = "@abhiraj_singh"

INTRO = "you are web browsing bot\n"


def load_bot_tokens(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

BOT_TOKENS = load_bot_tokens('bot_tokens.txt')


logging.basicConfig(level=logging.INFO)

def save_api_key(user_id, api_key):
    with open(f'Api{user_id}.txt', 'a') as f:
        f.write(f'{user_id}:{api_key}\n')

def load_api_key(user_id):
    try:
        with open(f'Api{user_id}.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                user_id_str, api_key = line.strip().split(':')
                if int(user_id_str) == user_id:
                    return api_key
    except FileNotFoundError:
        return None
    return None

async def reset_conversation(message: types.Message):
    user_id = message.from_user.id
    try:
        os.remove(f'{user_id}.txt')
        await message.reply("Your conversation history has been reset.")
    except FileNotFoundError:
        await message.reply("There is no conversation history to reset.")

async def set_api_key(message: types.Message):
    api_key = message.text.split(' ')[1]
    user_id = message.from_user.id
    
    # Delete any existing API key file
    try:
        os.remove(f'Api{user_id}.txt')
    except FileNotFoundError:
        pass

    # Save the new API key
    save_api_key(user_id, api_key)
    await message.reply("API key has been set successfully.")

def get_response(user_message, user_api_key):
    openai.api_key = user_api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": INTRO},
            {"role": "user", "content": user_message},
        ],
    )
    response_message = response['choices'][0]['message']['content']
    if response_message.startswith("Eva:"):
        response_message = response_message[len("Eva:"):]
    return response_message

async def handle_message(message: types.Message, bot: Bot):
    user_message = message.text
    chat_type = message.chat.type

    if chat_type == "group" or chat_type == "supergroup":
        if "Eva" not in user_message and "eva" not in user_message:
            return
        user_message = user_message.replace("Eva", "").replace("eva", "")
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    user_api_key = load_api_key(user_id)
    if user_api_key is None:
        await message.reply("Please set your OpenAI API key \n\n/setapi *your api key* \n\n[ Note :- remove * , And send api key personally to bot :- @Abhikritibot , \nIt wont work if you dont start the bot in personal message.]")
        return
  
    with open(f'{user_id}.txt', 'a+' , encoding='utf-8') as f:
        f.seek(0)
        previous_messages = f.readlines()

    previous_messages.append(f"{first_name}: {user_message}\n")

    with open(f'{user_id}.txt', 'a', encoding='utf-8') as f:
        f.write(user_message + '\n')

    user_messages = []
    ai_messages = []

    for i, msg in enumerate(previous_messages):
        if i % 2 == 0:
            user_messages.append(msg)
        else:
            ai_messages.append(msg)

    conversation = ''
    for user_message, ai_message in zip(user_messages, ai_messages):
        conversation += f"User: {user_message.strip()}\n"
        conversation += f"AI: {ai_message.strip()}\n"
        
    await bot.send_chat_action(chat_id=user_id, action="typing")
    response = get_response(f"Hey {first_name}" + INTRO + ''.join(previous_messages[-20:]), user_api_key)
    with open(f'{user_id}.txt', 'a', encoding='utf-8') as f:
        f.write(response + '\n')
   
    await message.reply(response)

import asyncio

def start_bot(token):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    bot = Bot(token=token)
    dp = Dispatcher(bot, loop=loop)
    dp.middleware.setup(LoggingMiddleware())
    
    # Register handlers
    dp.message_handler(commands=['reset'])(reset_conversation)
    dp.message_handler(commands=['setapi'])(set_api_key)
    dp.message_handler()(lambda message: handle_message(message, bot))

    executor.start_polling(dp, loop=loop, skip_updates=True)

if __name__ == '__main__':
    threads = []
    for token in BOT_TOKENS:
        t = threading.Thread(target=start_bot, args=(token,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
