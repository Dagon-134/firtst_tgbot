from sql import Repo

from aiogram import Bot

from dotenv import load_dotenv
import os

load_dotenv()

bot_url = os.getenv("BOT_TOKEN")
if bot_url is None:
    raise ValueError("Переменная окружения BOT_TOKEN не задана!")
bot = Bot(token=bot_url)

class Reminder:
    
    def __init__(self, bot):
        self.bot = bot
        
    async def send_alert(self, user_id, text):
        repo = Repo()
        await bot.send_message(
            chat_id=user_id,
            text=f"НАПОМИНАНИЕ: {text}"
        )
        repo.delTask(text, user_id)