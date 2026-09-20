from dotenv import load_dotenv
import os

import datetime

import psycopg
from psycopg.types.json import Jsonb

load_dotenv()
a = psycopg.connect(os.getenv("TABLE1"))
b = psycopg.connect(os.getenv("TABLE2"))

def isUserExist(tg_id: int) -> True | False:
    with b.cursor() as cursor:
        cursor.execute("""SELECT tg_id FROM user_ WHERE tg_id = %s""", (tg_id,))
        b.commit()
        user = cursor.fetchone
        if user is None:
            return False
    return True
                      
def addTgIdandName(name: str, tg_id: int):
    with b.cursor() as cursor:
        cursor.execute("""INSERT INTO user_ (user_name, tg_id)  VALUES(%s, %s)""", (name, tg_id))
        b.commit()
        
def isTaskExist(task: str, tg_id: int) -> True | False:
    with b.cursor() as cursor:
            cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s LIMIT 1""", (tg_id,))
            user_id_t = cursor.fetchone()
            user_id = user_id_t[0]
            if user_id_t:
                with a.cursor() as cursor2:
                    cursor2.execute("""SELECT task FROM to_do_list WHERE user_id = %s AND task = %s""", (user_id, task))
                    user_task = cursor2.fetchone()
                    print(user_task)
                    if user_task is not None:
                        return True
    return False
        
def delTask(task: str, tg_id: int):
    with b.cursor() as cursor:
        cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
        user_id_t = cursor.fetchone()
        user_id = user_id_t[0]
        if user_id_t:
            with a.cursor() as cursor2:
                cursor2.execute("""DELETE FROM to_do_list WHERE user_id = %s AND task = %s""", (user_id, task))
                a.commit()
                    
def changeTimeAndDate(task: str, date_and_time: datetime, tg_id: int):
    with b.cursor() as cursor:
        cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
        user_id_t = cursor.fetchone()
        user_id = user_id_t[0]
        if user_id_t:
            with a.cursor() as cursor2:
                cursor2.execute("""UPDATE to_do_list SET date_and_time = %s WHERE user_id = %s AND task = %s""", (date_and_time, user_id,task))
                a.commit()
        
def addAll(task: str, date_and_time: datetime, tg_id, job_id: str):
    with b.cursor() as cursor:
            cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
            user_id_t = cursor.fetchone()
            if user_id_t != None:
                user_id_f = user_id_t[0]
                with a.cursor() as cursor2:
                    cursor2.execute("""INSERT INTO to_do_list (user_id, task, date_and_time, job_id) VALUES(%s, %s, %s, %s)""", (user_id_f, task, date_and_time, job_id))
                    a.commit()
                
def watch(tg_id: int) -> str:
    with b.cursor() as cursor:
        cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
        user_id = cursor.fetchone()
        
        if user_id: 
            with a.cursor() as cursor2:
                cursor2.execute("""SELECT task, date_and_time FROM to_do_list WHERE user_id = %s""", (user_id[0],))
                result = cursor2.fetchall()
                task = []
                for i in result:
                    task.append({
                        'task': f"{i[0]}", 
                        'date_and_time': f"{i[1]}"
                    })
                return task
            
            
def returnJobId(task: str, tg_id: int) -> str | None:
    with b.cursor() as cursor:
        cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
        user_id = cursor.fetchone()
        
        if user_id:
            with a.cursor() as cursor2:
                cursor2.execute("""SELECT job_id FROM to_do_list WHERE user_id = %s AND task = %s""", (user_id[0], task))
                job_id = cursor2.fetchone()
                job_id_t = job_id[0]
                print(job_id_t)
                
                if job_id is not None:
                    return job_id_t
    return None
                


def isTokenExist(tg_id: int) -> bool:
    with b.cursor() as cursor:
        cursor.execute("""SELECT user_token FROM user_ WHERE tg_id = %s""", (tg_id,))
        token = cursor.fetchone()
        if token is None:
            return None
        return token[0]
        
        
def addToken(tg_id: int, token: str):
    with b.cursor() as cursor:
        cursor.execute("""UPDATE user_ SET user_token = %s WHERE tg_id = %s""", (Jsonb(token), tg_id))
        b.commit()
        
        
def refreshToken(tg_id: int, token_new: str):
    with b.cursor() as cursror:
        cursror.execute("""UPDATE user_ SET user_token = %s WHERE tg_id = %s""", (Jsonb(token_new), tg_id))
        b.commit()
        

def isDateTimeExist(date_and_time: datetime, tg_id: int) -> dict | None:
    with b.cursor() as cursor:
        cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
        user_id = cursor.fetchone()
        print(date_and_time)
        
        if user_id:
            with a.cursor() as cursor2:
                cursor2.execute("""SELECT date_and_time, task FROM to_do_list WHERE date_and_time = %s AND user_id = %s""", (date_and_time, user_id[0]))
                time_and_task = cursor2.fetchall()
                time_task_list = []
                if len(time_and_task) == 0:
                    return None 
                for i in time_and_task:
                        time_task_list.append({
                            'time': i[0],
                            'task': i[1]
                        })
                return time_task_list
            

def DeleteAll(tg_id: int):
    with b.cursor() as cursor:
        cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
        user_id = cursor.fetchone()
        
        if user_id:
            with a.cursor() as cursor2:
                cursor2.execute("""DELETE FROM to_do_list WHERE user_id = %s""", (user_id[0],))
                a.commit()