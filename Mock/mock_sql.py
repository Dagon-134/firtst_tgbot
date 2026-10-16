from typing import TypedDict, List

class Tasks(TypedDict):
    task: str
    time: str
    job_id: str

class User(TypedDict):
    token: str
    tasks: List[Tasks]
    
class SqlMock:
    def __init__(self):
        self.dict: dict[str, User] = {}
            
    def isUserExist(self, tg_id: int) -> bool | None:
        try: 
            if str(tg_id) in self.dict:
                return True
        except KeyError:
            return None
                      
    def isTaskExist(self, task: str, tg_id: int) -> bool | None:
        try:
            for i in self.dict[str(tg_id)]['tasks']:
                if i['task'] == task:
                    return True
        except KeyError:
            return None
            
    def delTask(self, task: str, tg_id: int) -> bool | None: 
        try:
            for i in self.dict[str(tg_id)]['tasks']:
                if i['task'] == task:
                    self.dict[str(tg_id)]['tasks']
                    return True
        except KeyError:
            print('Произошла ошибка в delTask')  
            return None
                        
    def changeTimeAndDate(self, task: str, date_and_time: str, tg_id: int) -> bool | None:
        try:
            for i in self.dict[str(tg_id)]['tasks']:
                if i['task'] == task:
                    i['time'] = date_and_time
                    return True
        except KeyError:
            print('Произошла ошибка в changeTimeAndDate') 
            return None
            
    def addAll(self, task: str, date_and_time: str, tg_id: int, job_id: str) -> bool:
        try:
            if str(tg_id) not in self.dict:
                self.dict[str(tg_id)] = {'token': '', 'tasks': []}
            self.dict[str(tg_id)]['tasks'].append({'task': task, 'time': date_and_time, 'job_id': job_id})
            return True
        except KeyError:
            print('Произошла ошибка в addAll') 
            return False
                    
    def watch(self, tg_id: int) -> bool | None:
        list_of_tasks: list[dict[str, str]] = []
        try:
            for i in self.dict[str(tg_id)]['tasks']:
                list_of_tasks.append({
                    'task': f"{i['task']}", 
                    'time': f"{i['time']}"
                    })
        except KeyError:
            print('Произошла ошибка в watch')  
            return None
        return True                
                
    def returnJobId(self, task: str, tg_id: int) -> bool| None:
        try:
            for i in self.dict[str(tg_id)]['tasks']:
                if i['task'] == task:
                    return True
        except KeyError:
            return None

    def isTokenExist(self, tg_id: int) -> bool:
        try:
            if 'token' not in self.dict[str(tg_id)]:
                print('Токена нет')
                return False
            else:
                self.dict[str(tg_id)]['token']
        except KeyError:
            return False
        return True
            
            
    def addToken(self, tg_id: int, token: str) -> bool | None:
        try:
            if token not in self.dict[str(tg_id)]['token']:
                self.dict[str(tg_id)]['token'] = token
                return True
        except KeyError:
            print('Произошла ошибка в addToken') 
            return None
            
    def refreshToken(self, tg_id: int, token_new: str) -> bool | None:
        try:
            self.dict[str(tg_id)]['token'] = token_new
            return True
        except KeyError:
            print('Произошла ошибка в refreshToken')
            return None    

    def isDateTimeExist(self, date_and_time: str, tg_id: int) -> bool | None:
        list_of_tasks: list[dict[str, str]] = []
        try:
            for i in self.dict[str(tg_id)]['tasks']:
                if i['time'] == date_and_time:
                    list_of_tasks.append({
                        'task': f"{i['task']}", 
                        'date_and_time': f"{i['time']}"
                    })
        except KeyError:
            return None
        if list_of_tasks == []:
            return True
                

    def DeleteAll(self, tg_id: int) -> bool:
        try:
            self.dict[str(tg_id)]['tasks'].clear()
            return True
        except KeyError:
            print('Произошла ошибка в DeleteAll') 
            return False
        
        
    def addId(self, tg_id: int):
        try:
            if str(tg_id) not in self.dict:
                self.dict[str(tg_id)] = {'token': '', 'tasks': []}
        except KeyError:
            print('Не получилось добавить пользователя')
            