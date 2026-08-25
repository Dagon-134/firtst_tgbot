from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def getMenu():
    
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Создать задачу')],
            [KeyboardButton(text='Просмотреть имеющиеся задачи')]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )
    
    return menu


def getChange():
    
    change = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Удалить задачу', callback_data='delTask')],
            [InlineKeyboardButton(text='Изменить время и дату', callback_data='changeDateAndtime')]
        ],
        one_time_keyboard=True
    )
    
    return change

def getSome(chislo):
    
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text='что') for i in range(chislo)])
    # rkb.adjust(*[3 for i in range(chislo//3 + 1)])
    rkb.adjust(3, repeat=True)
    return rkb.as_markup(resize_keyboard=True, one_time_keyboard=True) 