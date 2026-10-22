from typing import Literal

from dotenv import load_dotenv
import os

import datetime

import psycopg
from psycopg.types.json import Jsonb

load_dotenv()
db_url = os.getenv("TABLE1")
db_url2 = os.getenv("TABLE2")
if db_url2 is None:
    raise ValueError("Переменная окружения TABLE2 не задана!")
if db_url is None:
    raise ValueError("Переменная окружения TABLE2 не задана!")
b = psycopg.connect(db_url2)
a = psycopg.connect(db_url)

class Repo:
    
    def isUserExist(self, tg_id: int) -> bool:
        with b.cursor() as cursor:
            try:
                cursor.execute("""SELECT tg_id FROM user_ WHERE tg_id = %s""", (tg_id,))
                b.commit()
                user = cursor.fetchall()
                if user[0] is None:
                    return False
                return True
            except IndexError:
                return False
                        
    def addTgIdandName(self, name: str, tg_id: int) -> Literal[True]:
        with b.cursor() as cursor:
            cursor.execute("""INSERT INTO user_ (user_name, tg_id)  VALUES(%s, %s)""", (name, tg_id))
            b.commit()
            return True
            
    def isTaskExist(self, task: str, tg_id: int) -> bool | None:
        with b.cursor() as cursor:
            try:
                cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s LIMIT 1""", (tg_id,))
                user_id_t = cursor.fetchone()
                if user_id_t:
                    with a.cursor() as cursor2:
                        cursor2.execute("""SELECT task FROM to_do_list WHERE user_id = %s AND task = %s""", (user_id_t[0], task))
                        user_task = cursor2.fetchall()
                        print(user_task)
                        if user_task[0] is not None:
                            print('есть задача')
                            return True
            except IndexError:
                return None
                
            
    def delTask(self, task: str, tg_id: int) -> bool:
        with b.cursor() as cursor:
            cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
            user_id_t = cursor.fetchone()
            if user_id_t:
                with a.cursor() as cursor2:
                    cursor2.execute("""DELETE FROM to_do_list WHERE user_id = %s AND task = %s""", (user_id_t[0], task))
                    a.commit()
                    return True
            return False
                        
    def changeTimeAndDate(self, task: str, date_and_time: datetime.datetime, tg_id: int) -> bool | None:
        with b.cursor() as cursor:
            try:
                cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
                user_id_t = cursor.fetchone()
                if user_id_t:
                    with a.cursor() as cursor2:
                        cursor2.execute("""UPDATE to_do_list SET date_and_time = %s WHERE user_id = %s AND task = %s""", (date_and_time, user_id_t[0],task))
                        a.commit()
                        return True
            except IndexError:        
                return None
            
    def addAll(self, task: str, date_and_time: datetime.datetime | None, tg_id: int, job_id: str) -> bool:
        with b.cursor() as cursor:
                cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
                user_id_t = cursor.fetchone()
                if user_id_t is not None:
                    user_id = user_id_t[0]
                    with a.cursor() as cursor2:
                        cursor2.execute("""INSERT INTO to_do_list (user_id, task, date_and_time, job_id) VALUES(%s, %s, %s, %s)""", (user_id, task, date_and_time, job_id))
                        a.commit()
                        return True
                return False
                    
    def watch(self, tg_id: int) -> list[dict[str, str]] | None:
        with b.cursor() as cursor:
            cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
            user_id = cursor.fetchone()
            
            if user_id: 
                with a.cursor() as cursor2:
                    cursor2.execute("""SELECT task, date_and_time FROM to_do_list WHERE user_id = %s""", (user_id[0],))
                    result = cursor2.fetchall()
                    task: list[dict[str, str]] = []
                    for i in result:
                        task.append({
                            'task': f"{i[0]}", 
                            'date_and_time': f"{i[1]}"
                        })
                    return task
            return None
                
                
    def returnJobId(self, task: str, tg_id: int) -> str | None:
        with b.cursor() as cursor:
            cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
            user_id = cursor.fetchone()
            
            if user_id:
                with a.cursor() as cursor2:
                    cursor2.execute("""SELECT job_id FROM to_do_list WHERE user_id = %s AND task = %s""", (user_id[0], task))
                    job_id = cursor2.fetchall()
                    if job_id[0] is None:
                        return None
                    
                    job_id_t = job_id[0]
                    return job_id_t[0]
        print('нет id')
        return None
                    


    def isTokenExist(self, tg_id: int) -> None | str:
        with b.cursor() as cursor:
            cursor.execute("""SELECT user_token FROM user_ WHERE tg_id = %s""", (tg_id,))
            token = cursor.fetchone()
            if token is None:
                return None
            return token[0]
            
            
    def addToken(self, tg_id: int, token: str):
        with b.cursor() as cursor:
            cursor.execute("""UPDATE user_ SET user_token = %s WHERE tg_id = %s""", (Jsonb(token), tg_id))
            b.commit()
            return True
            
            
    def refreshToken(self, tg_id: int, token_new: str):
        with b.cursor() as cursror:
            cursror.execute("""UPDATE user_ SET user_token = %s WHERE tg_id = %s""", (Jsonb(token_new), tg_id))
            b.commit()
            return True
            

    def isDateTimeExist(self, date_and_time: datetime.datetime | None, tg_id: int) -> list[dict[str, str]] | None:
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
                    time_task_list[0]['time'] = time_task_list[0]['time'].strftime('%Y-%m-%d %H:%M:%S%z')
                    print(time_task_list)
                    return time_task_list
                

    def DeleteAll(self, tg_id: int):
        with b.cursor() as cursor:
            cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
            user_id = cursor.fetchone()
            
            if user_id:
                with a.cursor() as cursor2:
                    cursor2.execute("""DELETE FROM to_do_list WHERE user_id = %s""", (user_id[0],))
                    a.commit()
                    return True
                    
    
    def delUser(self, tg_id: int) -> Literal[True]:
        with b.cursor() as cursor:
            cursor.execute("""DELETE FROM user_ WHERE tg_id = %s""", (tg_id,))
            b.commit()
            return True