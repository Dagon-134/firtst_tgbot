from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, CommandObject
from sql import isUserExist, delTask, addAll, addTgIdandName, watch, isTaskExist, changeTimeAndDate, returnJobId, isDateTimeExist, DeleteAll

from calendare import addAllInCalendare

from functions_for_bot import creat_date, creat_time, get_time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from datetime import datetime, timedelta
import pytz

from keyboards import getChange, getMenu, confirm, RightorNot

from dotenv import load_dotenv
import os

import asyncio

from models import Task



class Dialog(StatesGroup):

    setTask = State()
    setDate = State()
    setTime = State()
    confirm = State()
    overlap = State()


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
    

###
#Начальная команда, первое знакомство с ботом
###    

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(text=f'👋Привет, {message.from_user.first_name}, я бот напоминалка. Моя задача принимать твои задачи и время, в которое ты хочешь их выполнить, а потом напомнить тебе о них в нужное время.',
                         reply_markup=getMenu())



###
#Команда выводит инструкцию
###

@dp.message(Command('instructions'))
async def instructions(message: Message):
    await message.answer(f'🤖Я бот напоминалка, а эта команда вызывают инструкцию, если вдруг ты запутаешся в использование бота. \n\nНачнём с основы, если ты хочешь создать новое задание, то нажми на команду /start, после чего нажми на кнопку "Создать задачу".\n\nПо той же команде ты сможешь просмотреть вс свои имеющиеся на данный момент задачи. \nЕсли у тебя есть просроченные или потеренные во времени задачи, то ты просто можешь их удалить. \n\n Потеренные задачи - это те задачи, которые потерялись из-за того, что ты отключил бота или заблокировал, а потом вернулся. \n\n❗️Если ты хочешь, чтобы твои задачи не терялись, то просто не нужно удалять бота❗️')



###
#Создадим здачу
###

@dp.message(F.text == '📖Создать задачу')
async def start(message: Message, state: FSMContext):
    await message.answer('♿️Для того чтобы начать напишите задачу')
    name = message.from_user.first_name
    tg_id = message.from_user.id
    if isUserExist(tg_id) == True:
        await state.update_data(userId=tg_id)
        await state.set_state(Dialog.setTask)
        
    else:
        addTgIdandName(name, tg_id)
        await state.update_data(taskId=tg_id)
        await state.set_state(Dialog.setTask)

    
@dp.message(Dialog.setTask) #Запомним название и перейдём к дате
async def time_and_date(message: Message, state: FSMContext):
    task_text = message.text
    await message.answer("✅Задачу запомнил, теперь введите дату дедлайна в формате DD.MM.YYYY")
    await state.update_data(taskName=task_text)
    await state.set_state(Dialog.setDate)
       
@dp.message(Dialog.setDate) #Запомним дату и перейдём ко времени
async def CreateDate(message: Message, state: FSMContext):
    list = []
    data_text = message.text
    verification = creat_date(data_text)
    
    for i in data_text:
        list.append(i)
        
    if verification == False:
        await message.answer("❗️Введите дату дедлайна в формате DD.MM.YYYY❗️")
        await state.set_state(Dialog.setDate)  
      
    else:
        await state.update_data(taskDate=data_text)
        await state.set_state(Dialog.setTime)
        await message.answer("✅Дату запомнил, теперь введите время дедлайна в формате HH:MM")

@dp.message(Dialog.setTime) #Запомним время и перейдём к подтверждению задачи
async def CreateTime(message: Message, state: FSMContext):
    time_text = message.text
    verification = creat_time(time_text)
    list = []
    data = await state.get_data()

    for i in time_text:
        list.append(i)
   
    if verification == False:
        await message.answer('❗️Введите время правильно❗️')
        await state.set_state(Dialog.setTime)
                
    else:
        
        time_text = message.text
        await state.update_data(taskTime=time_text)

        await message.answer(f"Итого задача:\n\n{data["taskName"]} которую нужно сделать {data["taskDate"]} в {time_text}")
        await message.answer("👀Всё ли правильно?",
                             reply_markup=RightorNot())
        
        await state.set_state(Dialog.confirm)
        
    
@dp.message(Dialog.confirm, F.text == '✅Всё правильно') #Всё было правильно - сохраняем в бд(Проверки: 1.Если пользователь ввёл уже существующую дату и время, предложим перенести на другое число или время; 2.Если была введена прошедшая дата, то выберем другую дату)
async def startCreate(message: Message, state: FSMContext):
    data = await state.get_data()
    task = data.get('taskName')
    date = data.get('taskDate')                                                 
    time = data.get('taskTime')  
    tg_id = data.get('userId')   

    date_time, native_dt = get_time(time, date)
    
    check_time = isDateTimeExist(date_time, tg_id)
    if check_time is not None:
        formatted_tasks = [f"{item['time']} - {item['task']}" for item in check_time]
        final_change = []
        for i in formatted_tasks:
            i = i.replace(':00+03:00', '')
            final_change.append(i)
        fix_result = "\n".join(final_change)
        await message.answer(f'❕Время и дата соответсвует с уже существующими:\n{fix_result}',
                            reply_markup=confirm())
        await state.set_state(Dialog.overlap)
        
    if date_time == False:
        await message.answer(f'❌Введенна не верная дата или время \n\n❗️Введите дату дедлайна в формате DD.MM.YYYY')
        await state.get_state(Dialog.setDate)
    
    else:
        job_id = f"alert_{message.from_user.id}_{int(date_time.timestamp())}"
            
        scheduler.add_job(
            func=send_alert, 
            trigger='date',
            run_date=date_time,         
            id=job_id,
            args=[message.from_user.id, task],
            replace_existing=True
        )
        
        task_model = Task(UserId=tg_id, TaskName=task, Time=date_time, JobId=job_id)
        
        addAll(task_model.TaskName, task_model.Time, task_model.UserId, task_model.JobId)
        addAllInCalendare(task, date_time, tg_id)
        await state.clear()                
        await message.answer("🟢Задача поставлена!")        
                                                                                                                                                                           

@dp.callback_query(Dialog.overlap, F.data == 'nothingGhange') #Пользователь решил не менять дату и время, всё сохраняется в бд
async def cancel(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task = data.get('taskName')
    date = data.get('taskDate')                                                 
    time = data.get('taskTime')  
    tg_id = data.get('userId')   
    
    date_time, native_dt = get_time(time, date)
    
    if date_time == False:
        await callback.answer(f'❌Введенна не верная дата или время \n\n ❗️Введите дату дедлайна в формате DD.MM.YYYY')
        await state.get_state(Dialog.setDate)
    
    else:
        job_id = f"alert_{callback.from_user.id}_{int(date_time.timestamp())}"
            
        scheduler.add_job(
            func=send_alert, 
            trigger='date',
            run_date=date_time,         
            id=job_id,
            args=[callback.from_user.id, task],
            replace_existing=True
        )
        
        task_model = Task(UserId=tg_id, TaskName=task, Time=date_time, JobId=job_id)
                
        addAll(task_model.TaskName, task_model.Time, task_model.UserId, task_model.JobId)
        addAllInCalendare(task, date_time, tg_id)
        await state.clear()
        await callback.answer('🟢Данные были сохранены')
    
    
@dp.callback_query(Dialog.overlap, F.data == 'changeReminder') #Пользователь решил поменять дату и время
async def accept(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Введите дату дедлайна в формате DD.MM.YYYY")
    await state.set_state(Dialog.setDate)



###
#Начало новой команды, пользователь хочет посмотреть задачи(может удалить или что-то изменить в них)
###                      
                                                    
@dp.message(F.text == '🗂Просмотреть имеющиеся задачи') #Показывает все задачи, которые есть у пользователя
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
    

### 
class del_Task(StatesGroup): #Класс, для удаления задачи  
    
    setTask = State()  
    
@dp.callback_query(F.data == 'delTask') #Пользователь выбрал удалить какую-то определённую задачу
async def start(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Удаление задачи')
    await callback.message.answer('Чтобы удалить задачу напишите её полностью')
    await state.set_state(del_Task.setTask)
    
@dp.message(del_Task.setTask) #Удаление задачи
async def del_task(message: Message, state: FSMContext):
    task = message.text
    tg_id = message.from_user.id
    if isTaskExist(task, tg_id) != True:
        await message.answer('Такого задания не существует')
        await state.clear()
    else:
        delTask(task, tg_id)
        await message.answer('Задание успешно удаленно')
        await state.clear()

 
###  
@dp.callback_query(F.data == 'delAll') #Удалить все задачи   
async def del_All(callback: CallbackQuery):
    await callback.answer('Удаление всех задач')
    tg_id = callback.from_user.id
    DeleteAll(tg_id)
    await callback.message.answer('Все задачи были удалены')

   
### 
class change_time_and_date(StatesGroup): #Класс, чтобы изменить время и дату 
    
    setTask = State()
    setDate = State()
    setTime = State()
    setConfirm = State()
    
@dp.callback_query(F.data == 'changeDateAndtime') #Пользователь решил поменять время
async def start(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Изменение времени и даты')
    await callback.message.answer('Для начала напишите задание, в котором хотите изменить время и дату')
    await state.set_state(change_time_and_date.setTask)
    
@dp.message(change_time_and_date.setTask) #Находим задачу, в которой пользователь хочет изменить время, после переходим к дате
async def task(message: Message, state: FSMContext):
    task = message.text
    tg_id = message.from_user.id
    if isTaskExist(task, tg_id) != 'Задание есть':
        await message.answer('🫥Такого задания не существует')
        await state.clear()
    else:
        await state.update_data(task=task)
        await message.answer('🧩Нашёл задание, теперь напишите дату в формате DD.MM.YYYY')
        await state.set_state(change_time_and_date.setDate)
        
        
@dp.message(change_time_and_date.setDate) #запоминаем дату и переходим ко времени
async def CreatDate(message: Message, state: FSMContext):
    list = []
    date_text = message.text
    
    for i in date_text:
        list.append(i)
        
    verification = creat_date(date_text)
    
    if verification == False:
        await message.answer("❗️Введите дату дедлайна в формате DD.MM.YYYY❗️")
        await state.set_state(change_time_and_date.setDate)
         
    else:
        await state.update_data(Date=date_text)
        await state.set_state(change_time_and_date.setTime)
        await message.answer("✅Дату запомнил, теперь введите время дедлайна в формате HH:MM")
        
@dp.message(change_time_and_date.setTime) #Запоминаем время и переходим к сохранению изменений
async def chahge_time(message: Message, state: FSMContext):
    time = message.text
    list = []

    for i in time:
        list.append(i)
        
    verification = creat_time(time)
        
    if verification == False:
        await message.answer('❗️Введите время правильно❗️')
        await state.set_state(change_time_and_date.setTime)
        
    else:
        await message.answer("✅Время запомнил, чтобы продолжить напишите что угодно")
        await state.update_data(Time=time)
        await state.set_state(change_time_and_date.setConfirm)
        
        
@dp.message(change_time_and_date.setConfirm) #Сохраняем изменения
async def startCreate(message: Message, state: FSMContext):
    data = await state.get_data()
    task = data.get('task')
    date = data.get('Date')                                                 
    time = data.get('Time')  
    tg_id = message.from_user.id 
    
    date_time, native_dt = get_time(time, date)
    
    if date_time < datetime.now(pytz.UTC):
            await message.answer(f'❌Введенна не верная дата или время \n\n ❗️Введите дату дедлайна в формате DD.MM.YYYY')
            await state.get_state(Dialog.setDate)
    
    else:
        find_job_id = returnJobId(task, tg_id)
        job = scheduler.get_job(find_job_id)
        job.reschedule(trigger='date', run_date=native_dt)
    
        changeTimeAndDate(task, date_time, tg_id)
                
        await message.answer('✳️Время и дата изменнены')
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
                                                    
                                                    
                                                    