from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

from sql import Repo

from calendare import addAllInCalendare

from datetime import datetime
import pytz

from keyboards import getChange, getMenu, confirm, RightorNot
from application.create_time import createTime
from application.get_list_of_tasks import what_we_have
from application.scheduelr_stuff import scheduler_job

from AI_agent import generate_response

rt_handler = Router()

from dotenv import load_dotenv
import os

load_dotenv()

bot_url = os.getenv("BOT_TOKEN")
if bot_url is None:
    raise ValueError("Переменная окружения BOT_TOKEN не задана!")
bot = Bot(token=bot_url)

class Dialog(StatesGroup):

    setTask = State()
    setDate = State()
    setTime = State()
    confirm = State()
    overlap = State()
    choose = State()
    

###
#Начальная команда, первое знакомство с ботом
###    

@rt_handler.message(CommandStart())
async def start_bot(message: Message):
    if message.from_user is not None:
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
async def start_create_task(message: Message, state: FSMContext, repo: Repo):
    await message.answer('♿️Для того чтобы начать напишите задачу')
    if message.from_user is not None:
        name = message.from_user.first_name
        tg_id = message.from_user.id
        if tg_id is not None:
            return
        if repo.isUserExist(tg_id) == True:
            await state.update_data(userId=tg_id)
            await state.set_state(Dialog.setTask)
            
        else:
            repo.addTgIdandName(name, tg_id)
            await state.update_data(taskId=tg_id)
            await state.set_state(Dialog.setTask)

    
@rt_handler.message(Dialog.setTask) #Запомним название и перейдём к дате
async def time_and_date(message: Message, state: FSMContext):
    task_text = message.text
    await message.answer("✅Задачу запомнил, теперь введите дату дедлайна в формате DD.MM.YYYY")
    await state.update_data(taskName=task_text)
    await state.set_state(Dialog.setDate)
       
@rt_handler.message(Dialog.setDate) #Запомним дату и перейдём ко времени
async def CreateDate(message: Message, state: FSMContext, main_functions: createTime):
    data_text = message.text
    verification = main_functions.validate_date(data_text)
        
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
async def CreateTime(message: Message, state: FSMContext, main_functions: createTime):
    time_text = message.text
    verification = main_functions.validate_time(time_text)
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
async def final(message: Message, state: FSMContext, main_functions: createTime, all_tasks: what_we_have, scheduler: scheduler_job, repo: Repo):
    print('Дошёл до функции')
    data = await state.get_data()
    task = data.get('taskName', 'Без названия')
    date = data.get('taskDate', '')
    time = data.get('taskTime', '')
    tg_id = data.get('userId', 0)  
    date_time = None 
    
    try:

        result = main_functions.get_time(time, date)
        
        if result is not False and result is not True:
            date_time, native_dt = result
        
    except TypeError:
        await message.answer(f'❌Введенна не верная дата или время \n\n❗️Введите дату дедлайна в формате DD.MM.YYYY')
        await state.set_state(Dialog.setDate)

        
    check_time = repo.isDateTimeExist(date_time, tg_id)
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
        
        repo.addAll(task, date_time, tg_id, job)
        addAllInCalendare(task, date_time, tg_id)
        await state.clear()                
        await message.answer("🟢Задача поставлена!")   
          
          
                  
@rt_handler.message(Dialog.choose, F.text == '✅Всё правильно')
async def all_right(message: Message, state: FSMContext):
    await message.answer('Чтобы подтвердить напишите что угодно кнопку')
    await state.set_state(Dialog.confirm)
    
@rt_handler.message(Dialog.choose, F.text == '⏰Хочу поменять время')
async def try_another_time(message: Message, state: FSMContext):
    await message.answer('Введите новое время')
    await state.set_state(Dialog.setTime)
    
@rt_handler.message(Dialog.choose, F.text == '📅Хочу поменять дату')
async def try_another_date(message: Message, state: FSMContext):
    await message.answer('Введите новую дату')
    await state.set_state(Dialog.setDate)
    
    

@rt_handler.callback_query(Dialog.overlap, F.data == 'nothingGhange') #Пользователь решил не менять дату и время, всё сохраняется в бд
async def cancel(callback: CallbackQuery, state: FSMContext, main_functions: createTime, scheduler: scheduler_job, repo: Repo):
    data = await state.get_data()
    task = data.get('taskName')
    date = data.get('taskDate')                                                 
    time = data.get('taskTime')  
    tg_id = data.get('userId')   
    date_time = None
    
    
    try:
        result = main_functions.get_time(time, date)
        
        if result is not False and result is not True:
            date_time, natve_dt = result
        
    except TypeError:
        await callback.answer(f'❌Введенна не верная дата или время \n\n ❗️Введите дату дедлайна в формате DD.MM.YYYY')
        await state.set_state(Dialog.setDate)
        
    else:
    
        if date_time == False:
            await callback.answer(f'❌Введенна не верная дата или время \n\n ❗️Введите дату дедлайна в формате DD.MM.YYYY')
            await state.set_state(Dialog.setDate)
        
        else:
            if tg_id is not None and task is not None:
                job = await scheduler.create_job(tg_id, date_time, task)
                        
                repo.addAll(task, date_time, tg_id, job)
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
    if message.from_user is None:
        return
    tg_id = message.from_user.id
    tasks = all_tasks.get_tasks1(tg_id)

    await message.answer(f'Ваши задачи: {tasks}',
                             reply_markup=getChange()) 
    

### 
class del_Task(StatesGroup): #Класс, для удаления задачи  
    
    setTask = State()  
    
@rt_handler.callback_query(F.data == 'delTask') #Пользователь выбрал удалить какую-то определённую задачу
async def start_dell(callback: CallbackQuery, state: FSMContext):
    if callback.message is None:
        return
    await callback.answer('Удаление задачи')
    await callback.message.answer('Чтобы удалить задачу напишите её полностью')
    await state.set_state(del_Task.setTask)
    
@rt_handler.message(del_Task.setTask) #Удаление задачи
async def del_task(message: Message, state: FSMContext, repo: Repo):
    if message.from_user is None:
        return
    task = message.text
    tg_id = message.from_user.id
    if task is not None:
        if repo.isTaskExist(task, tg_id) == None:
            await message.answer('Такого задания не существует')
            await state.clear()
        else:
            repo.delTask(task, tg_id)
            await message.answer('Задание успешно удаленно')
            await state.clear()

 
###  
@rt_handler.callback_query(F.data == 'delAll') #Удалить все задачи   
async def del_All(callback: CallbackQuery, repo: Repo):
    if callback.message is None:
        return
    await callback.answer('Удаление всех задач')
    tg_id = callback.from_user.id
    repo.DeleteAll(tg_id)
    await callback.message.answer('Все задачи были удалены')

   
### 
class change_time_and_date(StatesGroup): #Класс, чтобы изменить время и дату 
    
    setTask = State()
    setDate = State()
    setTime = State()
    setConfirm = State()
    
@rt_handler.callback_query(F.data == 'changeDateAndtime') #Пользователь решил поменять время
async def start(callback: CallbackQuery, state: FSMContext):
    if callback.message is None:
        return
    await callback.answer('Изменение времени и даты')
    await callback.message.answer('Для начала напишите задание, в котором хотите изменить время и дату')
    await state.set_state(change_time_and_date.setTask)
    
@rt_handler.message(change_time_and_date.setTask) #Находим задачу, в которой пользователь хочет изменить время, после переходим к дате
async def task(message: Message, state: FSMContext, repo: Repo):
    if message.from_user is None:
        return
    task = message.text
    tg_id = message.from_user.id
    if task is not None:
        if repo.isTaskExist(task, tg_id) != True:
            await message.answer('🫥Такого задания не существует')
            await state.clear()
        else:
            await state.update_data(task=task)
            await message.answer('🧩Нашёл задание, теперь напишите дату в формате DD.MM.YYYY')
            await state.set_state(change_time_and_date.setDate)
        
        
@rt_handler.message(change_time_and_date.setDate) #запоминаем дату и переходим ко времени
async def CreatDate(message: Message, state: FSMContext, main_functions: createTime):
    list = []
    date_text = message.text
        
    verification = main_functions.validate_date(date_text)
    
    if verification == False:
        await message.answer("❗️Введите дату дедлайна в формате DD.MM.YYYY❗️")
        await state.set_state(change_time_and_date.setDate)
         
    else:
        await state.update_data(Date=date_text)
        await state.set_state(change_time_and_date.setTime)
        await message.answer("✅Дату запомнил, теперь введите время дедлайна в формате HH:MM")
        
@rt_handler.message(change_time_and_date.setTime) #Запоминаем время и переходим к сохранению изменений
async def chahge_time(message: Message, state: FSMContext, main_functions: createTime):
    time = message.text
        
    verification = main_functions.validate_time(time)
        
    if verification == False:
        await message.answer('❗️Введите время правильно❗️')
        await state.set_state(change_time_and_date.setTime)
        
    else:
        await message.answer("✅Время запомнил, чтобы продолжить напишите что угодно")
        await state.update_data(Time=time)
        await state.set_state(change_time_and_date.setConfirm)
        
        
@rt_handler.message(change_time_and_date.setConfirm) #Сохраняем изменения
async def startCreate(message: Message, state: FSMContext, main_functions: createTime, scheduler: scheduler_job, repo: Repo):
    if message.from_user is None:
        return
    data = await state.get_data()
    if data is None:
        return 
    task = data.get('task')
    date = data.get('Date')                                                 
    time = data.get('Time')  
    tg_id = message.from_user.id 
    date_time = None
    native_dt = None
    
    try:
        result = main_functions.get_time(time, date)
        
        if result is not False and result is not True:
            date_time, native_dt = result
    
    except TypeError:
        await message.answer(f'❌Введенна не верная дата или время \n\n ❗️Введите дату дедлайна в формате DD.MM.YYYY')
        await state.set_state(change_time_and_date.setDate)
        
    if date_time is None:
        return
    if date_time < datetime.now(pytz.UTC):
            await message.answer(f'❌Введенна не верная дата или время \n\n❗️Введите дату дедлайна в формате DD.MM.YYYY')
            await state.set_state(change_time_and_date.setDate)
    
    else:
        job = await scheduler.change_job(task, tg_id, native_dt)
        
        if job == False:
            await message.answer(f'👣Задача была уже выполнена. \n\n❕Удаляйте задачи, если они они были заданы в прошлом(или вы перезапустили бота), иначе они будут копится у вас в хранилище❕')
            await state.clear()
            
        else:
            if task is not None:
                repo.changeTimeAndDate(task, date_time, tg_id)
                        
                await message.answer('✳️Время и дата изменнены')
                await state.clear()    
            
            
            
            
###
#ИИ для создания темы
###

class Settings_AI(StatesGroup):
    
    choose_topic = State()

@rt_handler.message(Command('ai'))
async def start_ai_function(message: Message, state: FSMContext):
    await message.answer(f'Привет, я AI агента!\n\nЯ здесь, чтобы помочь найти тебе занятие.\nСначала давай определимся с темой.\nНапиши мне чем ты хотел бы заняться, но желательно по подробней.\n\nНапример:\nЯ хочу изчуть какую-то новую тему в сфере космологии, я очень мало чего знаю об этой теме, но она мне интересна, так давай начнём с озов')
    await state.set_state(Settings_AI.choose_topic)
    
@rt_handler.message(Settings_AI.choose_topic)
async def science(message: Message):
    user_message = message.text
    msg = await message.answer('Генерирую тему...')
    response = await generate_response(user_message)
    msg.delete()
    await message.answer(f'{response}')
    