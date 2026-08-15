from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, CommandObject
from sql import isUserExist, addTask, addTime, addDate, delTask, addUser, changeTask, changeDate

from dotenv import load_dotenv
import os

import asyncio



class Dialog(StatesGroup):
    
    setTask = State()
    setDate = State()
    setTime = State()
    confirm = State()


load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(text=f'Привет, {message.from_user.first_name}, я бот напоминалка. Моя задача принимать твои задачи и время, в которое ты хочешь их выполнить. Для того чтобы начать нажми на /ready')
    name = message.from_user.first_name
    if isUserExist(name) is True:
        pass
    else:
        addUser(name) 
    
@dp.message(Command('ready'))
async def what_should_i_make(message: Message, state: FSMContext):
    await message.answer('Теперь можете ввести то, что вы хотите сделать в будущем')
    await state.set_state(Dialog.setTask)
    
@dp.message(Dialog.setTask)
async def time_and_date(message: Message, state: FSMContext):
    task_text = message.text
    if task_text == ' ':
        await message.answer("Задача пуста, ведите её заново, нажав на /ready")
    else:
        await message.answer("Название запомнил, теперь введите дату дедлайна в формате DD.MM.YYYY")
        await state.update_data(taskName=task_text)
        await state.set_state(Dialog.setDate)
        addTask(task_text)
    
        
@dp.message(Dialog.setDate)
async def startCreate(message: Message, state: FSMContext):
    list = []
    data_text = message.text
    data = await state.get_data()
    task_text = data.get('taskName')
    
    for i in data_text:
        list.append(i)
    
    if len(list) >= 11:
            await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /ready")
            delTask(task_text)
            
    elif list[2] != '.' and list[5] != '.':
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /ready")
        delTask(task_text)
    
        
    #Проверка, если месяц февраль и в нём введён день больше 28, то будет выводится ошибка
    elif ((list[3] + list[4] != '01') or (list[3] + list[4] !='03') or (list[3] + list[4] !='05') or (list[3] + list[4] !='07') or (list[3] + list[4] !='08') or (list[3] + list[4] !='10') or (list[3] + list[4] !='12') or (list[3] + list[4] !='04') or (list[3] + list[4] !='06') or (list[3] + list[4] !='09') or (list[3] + list[4] !='11')) and (int(list[0]) >= 2 and int(list[1]) > 8):
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /ready")
        delTask(task_text)
    
    #Проверка, если введённый день равняется или является больше 32 и при этом месяц, в котором максимум 31 день(январь, март, май и т.д.), то будет выводится ошибка  
    elif ((int(list[0]) >= 3 and int(list[1]) >= 2) and ((list[3] + list[4] != '02') or (list[3] + list[4] !='04') or (list[3] + list[4] !='06') or (list[3] + list[4] !='09') or (list[3] + list[4] !='11'))):
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /ready")
        delTask(task_text)
    
    #Проверка, если введённый день равняется или является больше 31 и при этом месяц, в котором максимум 30 дней(апрель, июнь, сентябрь и т.д.), то будет выводится ошибка
    elif ((int(list[0]) >= 3 and int(list[1]) >= 1) and ((list[3] + list[4] != '01') or (list[3] + list[4] !='03') or (list[3] + list[4] !='05') or (list[3] + list[4] !='07') or (list[3] + list[4] !='08') or (list[3] + list[4] !='10') or (list[3] + list[4] !='12') or (list[3] + list[4] !='02'))):
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /ready")
        delTask(task_text)

    
    #Проверка, если определённые суммированный объекты выводят год меньше или равно 2025, то будет выдоваться ошибка    
    elif int(list[6] + list[7] + list[8] + list[9]) <= 2025:
        await message.answer("Дата введена не правильно, чтобы продолжить начните заново, нажав на /ready")
        delTask(task_text)


       
    else:
        await state.update_data(taskDate=data_text)
        await state.set_state(Dialog.setTime)
        addDate(data_text, task_text)
        await message.answer("Дату запомнил, теперь введите время дедлайна в формате HH:MM")




@dp.message(Dialog.setTime)
async def startCreate(message: Message, state: FSMContext):
    time_text = message.text
    list = []
    data = await state.get_data()
    task_text = data.get('taskName')

    
    for i in time_text:
        list.append(i)
        
    if len(list) != 5:
        await message.answer('введите время правильно, начав заново и нажав на /ready')
        delTask(task_text)
   
    elif list[2] != ':':
        await message.answer('введите время правильно, начав заново и нажав на /ready')
        delTask(task_text)
        
    elif ((int(list[0]) >= 2) and (int(list[1]) >= 4)) or (int(list[3]) >= 6):
        await message.answer('введите время правильно, начав заново и нажав на /ready')
        delTask(task_text)
        
    else:
        await message.answer("Время запомнил")
        
        time_text = message.text
        await state.update_data(taskTime=time_text)
        addTime(time_text, task_text)

        await message.answer(f"Итого задача:\n {data["taskName"]} которую нужно сделать до {data["taskDate"]} {time_text}")
        await message.answer("Напишите любое сообщение, чтобы подтвердить задачу")
        
        await state.set_state(Dialog.confirm)
    


@dp.message(Dialog.confirm)
async def startCreate(message: Message, state: FSMContext):
    await message.answer("Задача поставлена!")
    # Сохранение всего в бд

        
        
async def main():
    await dp.start_polling(bot)

asyncio.run(main())


