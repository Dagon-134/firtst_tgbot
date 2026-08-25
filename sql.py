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
        
def isTaskExist(task, tg_id):
    with b.cursor() as cursor:
            cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s LIMIT 1""", (tg_id,))
            user_id_t = cursor.fetchone()
            user_id = user_id_t[0]
            print(user_id)
            print(task)
            if user_id_t:
                with a.cursor() as cursor2:
                    cursor2.execute("""SELECT task FROM to_do_list WHERE user_id = %s AND task = %s""", (user_id, task))
                    user_task = cursor2.fetchone()
                    print(user_task)
                    if user_task == None:
                        return None
                    else:
                        return 'Задание есть'
        
def delTask(task, tg_id):
    with b.cursor() as cursor:
        cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
        user_id_t = cursor.fetchone()
        user_id = user_id_t[0]
        if user_id_t:
            with a.cursor() as cursor2:
                cursor2.execute("""DELETE FROM to_do_list WHERE user_id = %s AND task = %s""", (user_id, task))
                a.commit()
                    
def changeTimeAndDate(task, date_and_time, tg_id):
    with b.cursor() as cursor:
        cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
        user_id_t = cursor.fetchone()
        user_id = user_id_t[0]
        print(task)
        print(user_id)
        if user_id_t:
            with a.cursor() as cursor2:
                cursor2.execute("""UPDATE to_do_list SET date_and_time = %s WHERE user_id = %s AND task = %s""", (date_and_time, user_id,task))
                a.commit()
        
def addAll(task, date_and_time, tg_id, job_id):
    with b.cursor() as cursor:
            cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
            user_id_t = cursor.fetchone()
            if user_id_t != None:
                user_id_f = user_id_t[0]
                with a.cursor() as cursor2:
                    cursor2.execute("""INSERT INTO to_do_list (user_id, task, date_and_time, job_id) VALUES(%s, %s, %s, %s)""", (user_id_f, task, date_and_time, job_id))
                    a.commit()
                
def watch(tg_id):
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
            
            
def returnJobId(task, tg_id):
    with b.cursor() as cursor:
        cursor.execute("""SELECT user_id FROM user_ WHERE tg_id = %s""", (tg_id,))
        user_id = cursor.fetchone()
        
        if user_id:
            with a.cursor() as cursor2:
                cursor2.execute("""SELECT job_id FROM to_do_list WHERE user_id = %s AND task = %s""", (user_id[0], task))
                job_id = cursor2.fetchone()
                job_id_t = job_id[0]
                print(job_id_t)
                
                if job_id == None:
                    return 'Ничего нет'
                
                else:
                    return job_id_t