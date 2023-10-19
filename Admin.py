from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = '6378511203:AAF-Pj5t4kmUJtFLaQi1vDmuWniHxnG0-qU'  # Replace with your bot token

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def add_token_to_file(token):
    with open('bot_tokens.txt', 'a') as file:
        file.write(token + '\n')



@dp.message_handler(commands=['addtoken'])
async def add_token(message: types.Message):
    token = message.text.split(' ')[1]
    add_token_to_file(token)
    await message.reply("Token has been added successfully.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
