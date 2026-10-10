dict = {}

class SqlMock:
            
    def isUserExist(tg_id: int) -> True | False:
        if tg_id in dict:
            return True
        return False
                      
    def isTaskExist(task: str, tg_id: int) -> True | False:
        try:
            for i in dict[tg_id]['tasks']:
                if i['task'] == task:
                    return True
        except KeyError:
            return False
            
    def delTask(task: str, tg_id: int):
        try:
            for i in dict[tg_id]['tasks']:
                if i['task'] == task:
                    dict['user']['tasks'].remove(i)
        except KeyError:
            print('Произошла ошибка в delTask')  
                        
    def changeTimeAndDate(task: str, date_and_time: str, tg_id: int):
        try:
            for i in dict[tg_id]['tasks']:
                if i['task'] == task:
                    i['time'] = date_and_time
        except KeyError:
            print('Произошла ошибка в changeTimeAndDate') 
            
    def addAll(task: str, date_and_time: str, tg_id, job_id: str):
        try:
            dict[tg_id]['tasks'].append({'task': task, 'time': date_and_time, 'job_id': job_id})
        except KeyError:
            print('Произошла ошибка в addAll') 
                    
    def watch(tg_id: int) -> str:
        list = []
        try:
            for i in dict[tg_id]['tasks']:
                list.append(i)
        except KeyError:
            print('Произошла ошибка в watch')  
        return list                
                
    def returnJobId(task: str, tg_id: int) -> str | None:
        try:
            for i in dict[tg_id]['tasks']:
                if i['task'] == task:
                    return i['job_id']
        except KeyError:
            return None

    def isTokenExist(tg_id: int) -> bool:
        try:
            token = dict[tg_id]['token']
            print(token)
        except KeyError:
            return False
        return True
            
            
    def addToken(tg_id: int, token: str):
        try:
            dict[tg_id]['token'] = token
        except KeyError:
            print('Произошла ошибка в addToken') 
            
            
    def refreshToken(tg_id: int, token_new: str):
        try:
            dict[tg_id]['token'] = token_new
        except KeyError:
            print('Произошла ошибка в refreshToken')    

    def isDateTimeExist(date_and_time: str, tg_id: int) -> list | None:
        try:
            for i in dict[tg_id]['tasks']:
                if i['time'] == date_and_time:
                    return i
        except KeyError:
            return None
                

    def DeleteAll(tg_id: int):
        try:
            for i in dict[tg_id]['tasks']:
                dict[tg_id]['tasks'].remove(i)
        except KeyError:
            print('Произошла ошибка в DeleteAll') 