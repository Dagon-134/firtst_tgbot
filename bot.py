from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, CommandObject
from sql import isUserExist, delTask, addAll, addTgIdandName, watch, isTaskExist, changeTimeAndDate, returnJobId

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from datetime import datetime, timedelta
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


scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()



async def send_alert(user_id, text):
    await bot.send_message(
        chat_id=user_id,
        text=f"НАПОМИНАНИЕ: {text}"
    )
    delTask(text, user_id)
    
    

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(text=f'Привет, {message.from_user.first_name}, я бот напоминалка. Моя задача принимать твои задачи и время, в которое ты хочешь их выполнить, а потом напомнить тебе о них в нужное время.',
                         reply_markup=getMenu())


@dp.message(Command('instructions'))
async def instructions(message: Message):
    await message.answer(f'🤖Я бот напоминалка, а эта команда вызывают инструкцию, если вдруг ты запутаешся в использование бота. \n\nНачнём с основы, если ты хочешь создать новое задание, то нажми на команду /start, после чего нажми на кнопку "Создать задачу".\n\nПо той же команде ты сможешь просмотреть вс свои имеющиеся на данный момент задачи. \nЕсли у тебя есть просроченные или потеренные во времени задачи, то ты просто можешь их удалить. \n\n Потеренные задачи - это те задачи, которые потерялись из-за того, что ты отключил бота или заблокировал, а потом вернулся. \n\n❗️Если ты хочешь, чтобы твои задачи не терялись, то просто не нужно удалять бота❗️')


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
async def CreateTime(message: Message, state: FSMContext):
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
    
    job_id = f"alert_{message.from_user.id}_{int(utc_dt.timestamp())}"
        
    scheduler.add_job(
        func=send_alert, 
        trigger='date',
        run_date=utc_dt,         
        id=job_id,
        args=[message.from_user.id, task],
        replace_existing=True
    )
    
    addAll(task, utc_dt, tg_id, job_id)     
    
    await state.clear()                                                                                                                                                                                           
    # Сохранение всего в бд                                                 




                                                    
@dp.message(F.text == 'Просмотреть имеющиеся задачи')
async def watchTask(message: Message):
    tg_id = message.from_user.id
    
    result = watch(tg_id)
    formatted_tasks = [f"{item['task']} - {item['date_and_time']}" for item in result]
    final_change = []
    for i in formatted_tasks:
        i = i.replace(':00+03:00', '')
        final_change.append(i)
    fix_result = "\n".join(final_change)

    await message.answer(f'Ваши задачи: {fix_result}',
                             reply_markup=getChange()) 
    
    
class del_Task(StatesGroup):
    
    setTask = State()  
    
@dp.callback_query(F.data == 'delTask')
async def start(callback: CallbackQuery, state: FSMContext, ):
    await callback.answer('Удаление задачи')
    await callback.message.answer('Чтобы удалить задачу напишите её полностью')
    await state.set_state(del_Task.setTask)
    
@dp.message(del_Task.setTask)
async def del_task(message: Message, state: FSMContext):
    task = message.text
    tg_id = message.from_user.id
    if isTaskExist(task, tg_id) != 'Задание есть':
        await message.answer('Такого задания не существует')
        await state.clear()
    else:
        delTask(task, tg_id)
        await message.answer('Задание успешно удаленно')
        await state.clear()
    
    
    
    
class change_time_and_date(StatesGroup):
    
    setTask = State()
    setDate = State()
    setTime = State()
    setConfirm = State()
    
    
    
@dp.callback_query(F.data == 'changeDateAndtime')
async def start(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Изменение времени и даты')
    await callback.message.answer('Для начала напишите задание, в котором хотите изменить время и дату')
    await state.set_state(change_time_and_date.setTask)
    
@dp.message(change_time_and_date.setTask)
async def task(message: Message, state: FSMContext):
    task = message.text
    tg_id = message.from_user.id
    if isTaskExist(task, tg_id) != 'Задание есть':
        await message.answer('Такого задания не существует')
        await state.clear()
    else:
        await state.update_data(task=task)
        await message.answer('Нашёл задание, теперь напишите дату в формате DD.MM.YYYY')
        await state.set_state(change_time_and_date.setDate)
        
@dp.message(change_time_and_date.setDate)
async def startCreate(message: Message, state: FSMContext):
    list = []
    date_text = message.text
    
    for i in date_text:
        list.append(i)
    
    if len(list) != 10:
        await message.answer("Дата введена не правильно")
            
    elif list[2] != '.' and list[5] != '.':
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /start")
        await state.clear()
       
    elif ((list[3] + list[4] != '01') or (list[3] + list[4] !='03') or (list[3] + list[4] !='05') or (list[3] + list[4] !='07') or (list[3] + list[4] !='08') or (list[3] + list[4] !='10') or (list[3] + list[4] !='12') or (list[3] + list[4] !='04') or (list[3] + list[4] !='06') or (list[3] + list[4] !='09') or (list[3] + list[4] !='11')) and (int(list[0]) >= 2 and int(list[1]) > 8):
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /start")
        await state.clear()
    
    elif ((int(list[0]) >= 3 and int(list[1]) >= 2) and ((list[3] + list[4] != '02') or (list[3] + list[4] !='04') or (list[3] + list[4] !='06') or (list[3] + list[4] !='09') or (list[3] + list[4] !='11'))):
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /start")
        await state.clear()    

    elif ((int(list[0]) >= 3 and int(list[1]) >= 1) and ((list[3] + list[4] != '01') or (list[3] + list[4] !='03') or (list[3] + list[4] !='05') or (list[3] + list[4] !='07') or (list[3] + list[4] !='08') or (list[3] + list[4] !='10') or (list[3] + list[4] !='12') or (list[3] + list[4] !='02'))):
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /start")
        await state.clear()
        
    elif int(list[6] + list[7] + list[8] + list[9]) <= 2025:
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /start")
        await state.clear()      
         
    else:
        await state.update_data(Date=date_text)
        await state.set_state(change_time_and_date.setTime)
        await message.answer("Дату запомнил, теперь введите время дедлайна в формате HH:MM")
        
        
@dp.message(change_time_and_date.setTime)
async def chahge_time(message: Message, state: FSMContext):
    time = message.text
    list = []

    for i in time:
        list.append(i)
        
    if len(list) != 5:
        await message.answer('Врема введенно не правильно')
        await state.clear()
   
    elif list[2] != ':':
        await message.answer('Врема введенно не правильно')
        await state.clear()
        
    elif ((int(list[0]) >= 2) and (int(list[1]) >= 4)) or (int(list[3]) >= 6):
        await message.answer('Врема введенно не правильно')
        await state.clear()
        
    else:
        await message.answer("Время запомнил, чтобы продолжить напишите что угодно")
        await state.update_data(Time=time)
        await state.set_state(change_time_and_date.setConfirm)
        
@dp.message(change_time_and_date.setConfirm)
async def startCreate(message: Message, state: FSMContext):
    data = await state.get_data()
    task = data.get('task')
    date = data.get('Date')                                                 
    time = data.get('Time')  
    tg_id = message.from_user.id 
    
    user_tz_str = 'Europe/Moscow'
    user_tz = pytz.timezone(user_tz_str)
    
    native_dt = datetime(int(date[6] + date[7] + date[8] + date[9]), int(date[3] + date[4]), int(date[0] + date[1]), int(time[0] + time[1]), int(time[3] + time[4]))
    aware_dt = user_tz.localize(native_dt)
    utc_dt = aware_dt.astimezone(pytz.UTC)
    print(utc_dt)
    
    find_job_id = returnJobId(task, tg_id)
    job = scheduler.get_job(find_job_id)
    job.reschedule(trigger='date', run_date=native_dt)
 
    changeTimeAndDate(task, utc_dt, tg_id)
            
    await message.answer('Время и дата изменнены')
    await state.clear()     
                                                        
                                                            
async def main():
    scheduler.start()                                                   
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
                                                    
                                                    
                                                    