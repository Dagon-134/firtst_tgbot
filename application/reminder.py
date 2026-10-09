from sql import delTask

from aiogram import Bot

from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))

class Reminder:
    
    def __init__(self, bot):
        self.bot = bot
        
    async def send_alert(self, user_id, text):
        await bot.send_message(
            chat_id=user_id,
            text=f"НАПОМИНАНИЕ: {text}"
        )
        delTask(text, user_id)