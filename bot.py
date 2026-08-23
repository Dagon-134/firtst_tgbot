from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, CommandObject
from sql import isUserExist, delTask, changeTask, changeDate, addAll, addTgIdandName, watch

from datetime import datetime, time
import pytz

from keyboards import getChange, getMenu, getSome

from dotenv import load_dotenv
import os

import asyncio



class Dialog(StatesGroup):
    
    setId = State()
    setTask = State()
    setDate = State()
    setTime = State()
    confirm = State()


load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()



@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(text=f'Привет, {message.from_user.first_name}, я бот напоминалка. Моя задача принимать твои задачи и время, в которое ты хочешь их выполнить.',
                         reply_markup=getMenu())





@dp.message(F.text == 'Создать задачу')
async def start(message: Message, state: FSMContext):
    await message.answer('Для того чтобы начать напишите что угодно')
    name = message.from_user.first_name
    tg_id = message.from_user.id
    if isUserExist(tg_id) == "Пользователь есть":
        await state.update_data(taskId=tg_id)
        await state.set_state(Dialog.setId)
        
    else:
        addTgIdandName(name, tg_id)
        await state.update_data(taskId=tg_id)
        await state.set_state(Dialog.setId)
            
@dp.message(Dialog.setId)
async def what_should_i_make(message: Message, state: FSMContext):
    await message.answer('Теперь можете ввести то, что вы хотите сделать в будущем')
    await state.set_state(Dialog.setTask)
    
@dp.message(Dialog.setTask)
async def time_and_date(message: Message, state: FSMContext):
    task_text = message.text
    if task_text == ' ':
        await message.answer("Задача пуста, ведите её заново, нажав на /start")
    else:
        await message.answer("Название запомнил, теперь введите дату дедлайна в формате DD.MM.YYYY")
        await state.update_data(taskName=task_text)
        await state.set_state(Dialog.setDate)
       
@dp.message(Dialog.setDate)
async def startCreate(message: Message, state: FSMContext):
    list = []
    data_text = message.text
    
    for i in data_text:
        list.append(i)
    
    if len(list) != 10:
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /start")
            
    elif list[2] != '.' and list[5] != '.':
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /start")
       
    #Проверка, если месяц февраль и в нём введён день больше 28, то будет выводится ошибка
    elif ((list[3] + list[4] != '01') or (list[3] + list[4] !='03') or (list[3] + list[4] !='05') or (list[3] + list[4] !='07') or (list[3] + list[4] !='08') or (list[3] + list[4] !='10') or (list[3] + list[4] !='12') or (list[3] + list[4] !='04') or (list[3] + list[4] !='06') or (list[3] + list[4] !='09') or (list[3] + list[4] !='11')) and (int(list[0]) >= 2 and int(list[1]) > 8):
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /start")
    
    #Проверка, если введённый день равняется или является больше 32 и при этом месяц, в котором максимум 31 день(январь, март, май и т.д.), то будет выводится ошибка  
    elif ((int(list[0]) >= 3 and int(list[1]) >= 2) and ((list[3] + list[4] != '02') or (list[3] + list[4] !='04') or (list[3] + list[4] !='06') or (list[3] + list[4] !='09') or (list[3] + list[4] !='11'))):
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /start")
    
    #Проверка, если введённый день равняется или является больше 31 и при этом месяц, в котором максимум 30 дней(апрель, июнь, сентябрь и т.д.), то будет выводится ошибка
    elif ((int(list[0]) >= 3 and int(list[1]) >= 1) and ((list[3] + list[4] != '01') or (list[3] + list[4] !='03') or (list[3] + list[4] !='05') or (list[3] + list[4] !='07') or (list[3] + list[4] !='08') or (list[3] + list[4] !='10') or (list[3] + list[4] !='12') or (list[3] + list[4] !='02'))):
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /start")

    #Проверка, если определённые суммированный объекты выводят год меньше или равно 2025, то будет выдоваться ошибка    
    elif int(list[6] + list[7] + list[8] + list[9]) <= 2025:
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /start")
       
    else:
        await state.update_data(taskDate=data_text)
        await state.set_state(Dialog.setTime)
        await message.answer("Дату запомнил, теперь введите время дедлайна в формате HH:MM")

@dp.message(Dialog.setTime)
async def startCreate(message: Message, state: FSMContext):
    time_text = message.text
    list = []
    data = await state.get_data()

    for i in time_text:
        list.append(i)
        
    if len(list) != 5:
        await message.answer('введите время правильно, начав заново и нажав на /start')
   
    elif list[2] != ':':
        await message.answer('введите время правильно, начав заново и нажав на /start')
        
    elif ((int(list[0]) >= 2) and (int(list[1]) >= 4)) or (int(list[3]) >= 6):
        await message.answer('введите время правильно, начав заново и нажав на /start')
        
    else:
        await message.answer("Время запомнил")
        
        time_text = message.text
        await state.update_data(taskTime=time_text)

        await message.answer(f"Итого задача:\n {data["taskName"]} которую нужно сделать {data["taskDate"]} в {time_text}")
        await message.answer("Напишите любое сообщение, чтобы подтвердить задачу")
        
        await state.set_state(Dialog.confirm)
    
@dp.message(Dialog.confirm)
async def startCreate(message: Message, state: FSMContext):
    await message.answer("Задача поставлена!")
    data = await state.get_data()
    task = data.get('taskName')
    date = data.get('taskDate')                                                 
    time = data.get('taskTime')  
    tg_id = data.get('taskId')   
    
    user_tz_str = 'Europe/Moscow'
    user_tz = pytz.timezone(user_tz_str)
    
    native_dt = datetime(int(date[6] + date[7] + date[8] + date[9]), int(date[3] + date[4]), int(date[0] + date[1]), int(time[0] + time[1]), int(time[3] + time[4]))
    aware_dt = user_tz.localize(native_dt)
    utc_dt = aware_dt.astimezone(pytz.UTC)
    
    addAll(task, utc_dt, tg_id)                                                                                                                                                                                                   
    # Сохранение всего в бд                                                 




                                                    
@dp.message(F.text == 'Просмотреть имеющиеся задачи')
async def watchTask(message: Message, state: FSMContext):
    data = await state.get_data() 
    tg_id = data.get('taskId')
    print(watch(tg_id))

    
    await message.answer('Ваши задачи:',
                             reply_markup=getChange()) 
    
    
# @dp.message(F.text.isdigit())
# async def some(message: Message):
#     await message.answer("g", 
#                          reply_markup=getSome(int(message.text)))
                                                        
                                                            
async def main():                                                   
    await dp.start_polling(bot)  
    
   
    
    
# import datetime
# import os.path

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# # If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


# def main():
#   """Shows basic usage of the Google Calendar API.
#   Prints the start and name of the next 10 events on the user's calendar.
#   """
#   creds = None
#   # The file token.json stores the user's access and refresh tokens, and is
#   # created automatically when the authorization flow completes for the first
#   # time.
#   if os.path.exists("token.json"):
#     creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#   # If there are no (valid) credentials available, let the user log in.
#   if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#       creds.refresh(Request())
#     else:
#       flow = InstalledAppFlow.from_client_secrets_file(
#           "credentials.json", SCOPES
#       )
#       creds = flow.run_local_server(port=0)
#     # Save the credentials for the next run
#     with open("token.json", "w") as token:
#       token.write(creds.to_json())

# if __name__ == "__main__":
#   main()
  
  
  
  
                                                 
                                                    
asyncio.run(main())                                                 
                                                    
                                                    
                                                    