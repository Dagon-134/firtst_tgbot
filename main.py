from aiogram import Bot, Dispatcher

from application.create_task import createTask
from application.get_list_of_tasks import what_we_have
from application.scheduelr_stuff import scheduler_job
from application.reminder import Reminder

from dotenv import load_dotenv
import os

import asyncio

from handlers import rt_handler

from scheduler import scheduler

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()                                           
                                                            
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(rt_handler)
    job_manager = scheduler_job(bot)
    dp['main_functions'] = createTask
    dp['all_tasks'] = what_we_have
    dp['scheduler'] = scheduler_job
    dp['remind'] = Reminder
    scheduler.start()                                                   
    await dp.start_polling(bot)                                   
                                                    
asyncio.run(main())         