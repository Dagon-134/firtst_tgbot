from dotenv import load_dotenv
import os

import psycopg

load_dotenv()
a = psycopg.connect(os.getenv("TABLE1"))
b = psycopg.connect(os.getenv("TABLE2"))

def isUserExist(tg_id):
    with b.cursor() as cursor:
        cursor.execute("""SELECT tg_id FROM user_ WHERE tg_id = %s""", (tg_id,))
        b.commit()
        user = cursor.fetchone
        if user == None:
            pass
        else:
            return "Пользователь есть"
                      
def addTgIdandName(name, tg_id):
    with b.cursor() as cursor:
        cursor.execute("""INSERT INTO user_ (user_name, tg_id)  VALUES(%s, %s)""", (name, tg_id))
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
        
def addAll(task, date_and_time, tg_id):
    with b.cursor() as cursor:
            cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
            user_id_t = cursor.fetchone()
            if user_id_t != None:
                user_id_f = user_id_t[0]
                with a.cursor() as cursor2:
                    cursor2.execute("""INSERT INTO to_do_list (user_id, task, date_and_time) VALUES(%s, %s, %s)""", (user_id_f, task, date_and_time))
                    a.commit()
                
def watch(tg_id):
    with b.cursor() as cursor:
        cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
        user_id = cursor.fetchone()
        
        if user_id: 
            with a.cursor() as cursor2:
                cursor2.execute("""SELECT task, time_, date_ FROM to_do_list WHERE user_id = %s""", (user_id,))
                result = cursor2.fetchall()
                task = []
                for i in result:
                    task.append({
                        'task': f"{i[0]}", 
                        'time': f"{i[1]}", 
                        'date': f"{i[2]}"
                    })
                return task