from dotenv import load_dotenv
import os

import psycopg

load_dotenv()
a = psycopg.connect(os.getenv("TABLE1"))
b = psycopg.connect(os.getenv("TABLE2"))

def isUserExist(tg_id):
    with a.cursor() as cursor:
        cursor.execute("""SELECT user_id FROM user_ WHERE user_id = %s""", (tg_id,))
        a.commit()
        
def addTask(task):
    with a.cursor() as cursor:
        cursor.execute("""INSERT INTO to_do_list (task) VALUES(%s)""", (task,))
        a.commit()
        
def addTime(time, task):
    with a.cursor() as cursor:
        cursor.execute("""UPDATE to_do_list SET time_ = %s WHERE task = %s""", (time, task))
        a.commit()
        
def addDate(date, task):
    with a.cursor() as cursor:
        cursor.execute("""UPDATE to_do_list SET date_ = %s WHERE task = %s""", (date, task))
        a.commit()
        
def addUser(user):
    with b.cursor() as cursor:
        cursor.execute("""INSERT INTO user_ (user_name) VALUES(%s)""", (user,))
        b.commit()
        
def delTask(del_task):
    with a.cursor() as cursor:
        cursor.execute("""DELETE FROM to_do_list WHERE task = %s""", (del_task,))
        a.commit()
        
def changeTask(change_time):
    with a.cursor() as cursor:
        cursor.execute("""UPDATE to_do_list SET time_ = %s""", (change_time,))
        a.commit()
        
def changeDate(change_date):
    with a.cursor() as cursor:
        cursor.execute("""UPDATE to_do_list SET date_ = %s""", (change_date,))
        a.commit()