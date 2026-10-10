from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from sql import isUserExist, delTask, addAll, addTgIdandName, isTaskExist, changeTimeAndDate, isDateTimeExist, DeleteAll

from calendare import addAllInCalendare

from datetime import datetime
import pytz

from keyboards import getChange, getMenu, confirm, RightorNot

from application.create_task import createTask
from application.get_list_of_tasks import what_we_have
from application.scheduelr_stuff import scheduler_job

rt_handler = Router()

from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))

class Dialog(StatesGroup):

    setTask = State()
    setDate = State()
    setTime = State()
    confirm = State()
    overlap = State()
    choose = State()


async def send_alert(user_id, text):
    await bot.send_message(
        chat_id=user_id,
        text=f"НАПОМИНАНИЕ: {text}"
    )
    delTask(text, user_id)
    

###
#Начальная команда, первое знакомство с ботом
###    

@rt_handler.message(CommandStart())
async def start(message: Message):
    await message.answer(text=f'👋Привет, {message.from_user.first_name}, я бот напоминалка. Моя задача принимать твои задачи и время, в которое ты хочешь их выполнить, а потом напомнить тебе о них в нужное время.',
                         reply_markup=getMenu())



###
#Команда выводит инструкцию
###

@rt_handler.message(Command('instructions'))
async def instructions(message: Message):
    await message.answer(f'🤖Я бот напоминалка, а эта команда вызывают инструкцию, если вдруг ты запутаешся в использование бота. \n\nНачнём с основы, если ты хочешь создать новое задание, то нажми на команду /start, после чего нажми на кнопку "Создать задачу".\n\nПо той же команде ты сможешь просмотреть всеш888888888888888888888 свои имеющиеся на данный момент задачи. \nЕсли у тебя есть просроченные или потеренные во времени задачи, то ты просто можешь их удалить. \n\n Потеренные задачи - это те задачи, которые потерялись из-за того, что ты отключил бота или заблокировал, а потом вернулся. \n\n❗️Если ты хочешь, чтобы твои задачи не терялись, то просто не нужно удалять бота❗️')



###
#Создадим здачу
###

@rt_handler.message(F.text == '📖Создать задачу')
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

    
@rt_handler.message(Dialog.setTask) #Запомним название и перейдём к дате
async def time_and_date(message: Message, state: FSMContext):
    task_text = message.text
    await message.answer("✅Задачу запомнил, теперь введите дату дедлайна в формате DD.MM.YYYY")
    await state.update_data(taskName=task_text)
    await state.set_state(Dialog.setDate)
       
@rt_handler.message(Dialog.setDate) #Запомним дату и перейдём ко времени
async def CreateDate(message: Message, state: FSMContext, main_functions: createTask):
    data_text = message.text
    verification = main_functions.creat_date(data_text)
        
    if verification == False:
        await message.answer("❗️Введите дату дедлайна в формате DD.MM.YYYY❗️")
        await state.set_state(Dialog.setDate)  
      
    else:
        data = await state.get_data()
        date = data.get('taskDate')
        if date is None:
            print('date пустой')
            await state.update_data(taskDate=data_text)
            await state.set_state(Dialog.setTime)
            await message.answer("✅Дату запомнил, теперь введите время дедлайна в формате HH:MM")
        else:
            await state.update_data(taskDate=data_text)
            await state.set_state(Dialog.confirm)
            await message.answer('Напишите что угодно, для подтверждения')

@rt_handler.message(Dialog.setTime) #Запомним время и перейдём к подтверждению задачи
async def CreateTime(message: Message, state: FSMContext, main_functions: createTask):
    time_text = message.text
    verification = main_functions.creat_time(time_text)
    data = await state.get_data()
   
    if verification == False:
        await message.answer('❗️Введите время правильно❗️')
        await state.set_state(Dialog.setTime)
                
    else:
        data = await state.get_data()
        time = data.get('taskTime')
        if time is None:
            await state.update_data(taskTime=time_text)

            await message.answer(f"Итого задача:\n\n{data["taskName"]} которую нужно сделать {data["taskDate"]} в {time_text}")
            await message.answer("👀Всё ли правильно?",
                                reply_markup=RightorNot())
            await state.set_state(Dialog.choose)
        else:
            await state.update_data(taskTime=time_text)
            await state.set_state(Dialog.confirm)
            await message.answer('Напишите что угодно, для подтверждения')

@rt_handler.message(Dialog.confirm) #Всё было правильно - сохраняем в бд(Проверки: 1.Если пользователь ввёл уже существующую дату и время, предложим перенести на другое число или время; 2.Если была введена прошедшая дата, то выберем другую дату)
async def startCreate(message: Message, state: FSMContext, main_functions: createTask, all_tasks: what_we_have, scheduler: scheduler_job):
    print('Дошёл до функции')
    data = await state.get_data()
    task = data.get('taskName')
    date = data.get('taskDate')                                                 
    time = data.get('taskTime')  
    tg_id = data.get('userId')   
    
    try:
        date_time, native_dt = main_functions.get_time(time, date)
        
    except TypeError:
        await message.answer(f'❌Введенна не верная дата или время \n\n❗️Введите дату дедлайна в формате DD.MM.YYYY')
        await state.set_state(Dialog.setDate)
        
    check_time = isDateTimeExist(date_time, tg_id)
    if check_time is not None:
        fix_result = all_tasks.get_tasks2(check_time)
        await message.answer(f'❕Время и дата соответсвует с уже существующими:\n{fix_result}',
                            reply_markup=confirm())
        await state.set_state(Dialog.overlap)
        
    if date_time == False:
        await message.answer(f'❌Введенна не верная дата или время \n\n❗️Введите дату дедлайна в формате DD.MM.YYYY')
        await state.set_state(Dialog.setDate)
    
    else:
        job = await scheduler.create_job(tg_id, date_time, task)
        
        addAll(task, date_time, tg_id, job)
        addAllInCalendare(task, date_time, tg_id)
        await state.clear()                
        await message.answer("🟢Задача поставлена!")   
          
          
                  
@rt_handler.message(Dialog.choose, F.text == '✅Всё правильно')
async def all_right(message: Message, state: FSMContext):
    await message.answer('Чтобы подтвердить напишите что угодно кнопку')
    await state.set_state(Dialog.confirm)
    
@rt_handler.message(Dialog.choose, F.text == '⏰Хочу поменять время')
async def try_another_date(message: Message, state: FSMContext):
    await message.answer('Введите новое время')
    await state.set_state(Dialog.setTime)
    
@rt_handler.message(Dialog.choose, F.text == '📅Хочу поменять дату')
async def try_another_date(message: Message, state: FSMContext):
    await message.answer('Введите новую дату')
    await state.set_state(Dialog.setDate)
    
    

@rt_handler.callback_query(Dialog.overlap, F.data == 'nothingGhange') #Пользователь решил не менять дату и время, всё сохраняется в бд
async def cancel(callback: CallbackQuery, state: FSMContext, main_functions: createTask, scheduler: scheduler_job):
    data = await state.get_data()
    task = data.get('taskName')
    date = data.get('taskDate')                                                 
    time = data.get('taskTime')  
    tg_id = data.get('userId')   
    
    
    try:
        date_time, native_dt = main_functions.get_time(time, date)
        
    except TypeError:
        await callback.answer(f'❌Введенна не верная дата или время \n\n ❗️Введите дату дедлайна в формате DD.MM.YYYY')
        await state.set_state(Dialog.setDate)
        
    else:
    
        if date_time == False:
            await callback.answer(f'❌Введенна не верная дата или время \n\n ❗️Введите дату дедлайна в формате DD.MM.YYYY')
            await state.set_state(Dialog.setDate)
        
        else:
            job = await scheduler.create_job(tg_id, date_time, task)
                    
            addAll(task, date_time, tg_id, job)
            addAllInCalendare(task, date_time, tg_id)
            await state.clear()
            await callback.answer('🟢Данные были сохранены')
    
    
@rt_handler.callback_query(Dialog.overlap, F.data == 'changeReminder') #Пользователь решил поменять дату и время
async def accept(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Введите дату дедлайна в формате DD.MM.YYYY")
    await state.set_state(Dialog.setDate)



###
#Начало новой команды, пользователь хочет посмотреть задачи(может удалить или что-то изменить в них)
###                      
                                                    
@rt_handler.message(F.text == '🗂Просмотреть имеющиеся задачи') #Показывает все задачи, которые есть у пользователя
async def watchTask(message: Message, all_tasks: what_we_have):
    tg_id = message.from_user.id
    tasks = all_tasks.get_tasks1(tg_id)

    await message.answer(f'Ваши задачи: {tasks}',
                             reply_markup=getChange()) 
    

### 
class del_Task(StatesGroup): #Класс, для удаления задачи  
    
    setTask = State()  
    
@rt_handler.callback_query(F.data == 'delTask') #Пользователь выбрал удалить какую-то определённую задачу
async def start(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Удаление задачи')
    await callback.message.answer('Чтобы удалить задачу напишите её полностью')
    await state.set_state(del_Task.setTask)
    
@rt_handler.message(del_Task.setTask) #Удаление задачи
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
@rt_handler.callback_query(F.data == 'delAll') #Удалить все задачи   
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
    
@rt_handler.callback_query(F.data == 'changeDateAndtime') #Пользователь решил поменять время
async def start(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Изменение времени и даты')
    await callback.message.answer('Для начала напишите задание, в котором хотите изменить время и дату')
    await state.set_state(change_time_and_date.setTask)
    
@rt_handler.message(change_time_and_date.setTask) #Находим задачу, в которой пользователь хочет изменить время, после переходим к дате
async def task(message: Message, state: FSMContext):
    task = message.text
    tg_id = message.from_user.id
    if isTaskExist(task, tg_id) != True:
        await message.answer('🫥Такого задания не существует')
        await state.clear()
    else:
        await state.update_data(task=task)
        await message.answer('🧩Нашёл задание, теперь напишите дату в формате DD.MM.YYYY')
        await state.set_state(change_time_and_date.setDate)
        
        
@rt_handler.message(change_time_and_date.setDate) #запоминаем дату и переходим ко времени
async def CreatDate(message: Message, state: FSMContext, main_functions: createTask):
    list = []
    date_text = message.text
    
    for i in date_text:
        list.append(i)
        
    verification = main_functions.creat_date(date_text)
    
    if verification == False:
        await message.answer("❗️Введите дату дедлайна в формате DD.MM.YYYY❗️")
        await state.set_state(change_time_and_date.setDate)
         
    else:
        await state.update_data(Date=date_text)
        await state.set_state(change_time_and_date.setTime)
        await message.answer("✅Дату запомнил, теперь введите время дедлайна в формате HH:MM")
        
@rt_handler.message(change_time_and_date.setTime) #Запоминаем время и переходим к сохранению изменений
async def chahge_time(message: Message, state: FSMContext, main_functions: createTask):
    time = message.text
    list = []

    for i in time:
        list.append(i)
        
    verification = main_functions.creat_time(time)
        
    if verification == False:
        await message.answer('❗️Введите время правильно❗️')
        await state.set_state(change_time_and_date.setTime)
        
    else:
        await message.answer("✅Время запомнил, чтобы продолжить напишите что угодно")
        await state.update_data(Time=time)
        await state.set_state(change_time_and_date.setConfirm)
        
        
@rt_handler.message(change_time_and_date.setConfirm) #Сохраняем изменения
async def startCreate(message: Message, state: FSMContext, main_functions: createTask, scheduler: scheduler_job):
    data = await state.get_data()
    task = data.get('task')
    date = data.get('Date')                                                 
    time = data.get('Time')  
    tg_id = message.from_user.id 
    
    try:
        date_time, native_dt = main_functions.get_time(time, date)
    
    except TypeError:
        await message.answer(f'❌Введенна не верная дата или время \n\n ❗️Введите дату дедлайна в формате DD.MM.YYYY')
        await state.set_state(change_time_and_date.setDate)

    if date_time < datetime.now(pytz.UTC):
            await message.answer(f'❌Введенна не верная дата или время \n\n❗️Введите дату дедлайна в формате DD.MM.YYYY')
            await state.get_state(change_time_and_date.setDate)
    
    else:
        job = await scheduler.change_job(task, tg_id, native_dt)
        
        if job == False:
            await message.answer(f'👣Задача была уже выполнена. \n\n❕Удаляйте задачи, если они они были заданы в прошлом(или вы перезапустили бота), иначе они будут копится у вас в хранилище❕')
            await state.clear()
            
        else:
            changeTimeAndDate(task, date_time, tg_id)
                    
            await message.answer('✳️Время и дата изменнены')
            await state.clear()     