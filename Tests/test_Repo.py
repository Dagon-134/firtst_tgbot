from application.create_time import createTime

import time

from sql import Repo

class Test_Repo:
    
    def test_addAll(self):
        
        #Arrange
        db = Repo()
        main_functions = createTime()
        test_tg_id: int = 1092334
        name: str = 'Dagon'
        test_task: str = 'Помыть руки'
        test_time: str = '23:09'
        test_date: str = '09.12.2026'
        test_job_id: str = '11123_sdhfbsjdhf_121212' 
        
        db.addTgIdandName(name, test_tg_id)
        
        take_datetime = main_functions.get_time(test_time, test_date)
                
        if take_datetime is False or take_datetime is True:
            assert False
            
        date_time, native_dt = take_datetime
        
        #Act
        result = db.addAll(test_task, date_time, test_tg_id, test_job_id)
        
        #Assert
        db.delTask(test_task, test_tg_id)
        db.delUser(test_tg_id)
        assert result is True
        
    def test_isUserExist(self):
        
        # Arrange
        db = Repo()
        main_functions = createTime()
        test_tg_id1: int = 1092334
        name: str = 'Dagon'
        test_tg_id2: int = 12
        test_task: str = 'Помыть руки'
        test_time: str = '23:09'
        test_date: str = '09.12.2026'
        test_job_id: str = '11123_sdhfbsjdhf_121212' 
        
        db.addTgIdandName(name, test_tg_id1)
        
        take_datetime = main_functions.get_time(test_time, test_date)
                
        if take_datetime is False or take_datetime is True:
            assert False

        date_time, native_dt = take_datetime
        
        db.addAll(test_task, date_time, test_tg_id1, test_job_id)
        
        #Act
        result_1 = db.isUserExist(test_tg_id1)
        result_2 = db.isUserExist(test_tg_id2)
        
        # Assert
        db.delTask(test_task, test_tg_id1)
        db.delUser(test_tg_id1)
        assert result_1 is True
        assert result_2 is False
        
    def test_addTgIdandName(self):
        #Arrange
        db = Repo()
        test_tg_id: int = 1092334
        name: str = 'Dagon'
        
        #Act
        result = db.addTgIdandName(name, test_tg_id)    
        
        #Assert
        assert result is True   
        
    def test_isTaskExist(self):
        
        #Arrange
        db = Repo()
        main_functions = createTime()
        test_tg_id: int = 1092334
        name: str = 'Dagon'
        test_task: str = 'Помыть руки'
        test_time: str = '23:09'
        test_date: str = '09.12.2026'
        test_job_id: str = '11123_sdhfbsjdhf_121212'
        test_task2: str = 'Чем то заняться'
        
        db.addTgIdandName(name, test_tg_id)
        time.sleep(1)
        
        result = main_functions.get_time(test_time, test_date)
                
        if result is False or result is True:
            assert False

        date_time, native_dt = result
        
        db.addAll(test_task, date_time, test_tg_id, test_job_id)
        
        #Act
        result = db.isTaskExist(test_task, test_tg_id)
        result2 = db.isTaskExist(test_task2, test_tg_id)
        
        #Assert
        db.delTask(test_task, test_tg_id)
        db.delUser(test_tg_id)
        assert result is True
        assert result2 is None
        
    def test_changeTimeAndDate(self,):
        
        #Arrange
        db = Repo()
        main_functions = createTime()
        test_tg_id: int = 1092334
        test_tg_id2: int = 123123123
        name: str = 'Dagon'
        test_task: str = 'Помыть руки'
        test_time: str = '20:30'
        test_date: str = '09.12.2026'
        test_job_id: str = '11123_sdhfbsjdhf_121212'
        test_task2: str = 'Чем то заняться'
        
        db.addTgIdandName(name, test_tg_id)
        
        result = main_functions.get_time(test_time, test_date)
                
        if result is False or result is True:
            assert False

        date_time, native_dt = result
        
        db.addAll(test_task, date_time, test_tg_id, test_job_id)
        
        #Act
        result = db.changeTimeAndDate(test_task, date_time, test_tg_id)
        result2 = db.changeTimeAndDate(test_task2, date_time, test_tg_id2)
        
        #Assert
        db.delTask(test_task, test_tg_id)
        db.delUser(test_tg_id)
        assert result is True
        assert result2 is None
        
    def test_watch(self):
        
        #Arrange
        db = Repo()
        main_functions = createTime()
        test_tg_id: int = 1092334
        name: str = 'Dagon'
        test_task: str = 'Помыть руки'
        test_time: str = '20:30'
        test_date: str = '09.12.2026'
        test_job_id: str = '11123_sdhfbsjdhf_121212'
        test_tg_id2: int = 1231231312
        test_result: list[dict[str, str]] = [{'task': 'Помыть руки', 'date_and_time': '2026-12-09 20:30:00+03:00'}]
        
        db.addTgIdandName(name, test_tg_id)
        
        result = main_functions.get_time(test_time, test_date)
                
        if result is False or result is True:
            assert False

        date_time, native_dt = result
        
        db.addAll(test_task, date_time, test_tg_id, test_job_id)
                
        #Act
        result = db.watch(test_tg_id)
        result2 = db.watch(test_tg_id2)
        
        #Assert
        db.delTask(test_task, test_tg_id)
        db.delUser(test_tg_id)
        assert result == test_result
        assert result2 is None
        
    def test_returnJObId(self,):
        
        #Arrange
        db = Repo()
        main_functions = createTime()
        test_tg_id: int = 1092334
        name: str = 'Dagon'
        test_task: str = 'Помыть руки'
        test_time: str = '20:30'
        test_date: str = '09.12.2026'
        test_job_id: str = '11123_sdhfbsjdhf_121212'
        test_tg_id2: int = 123123123
        
        db.addTgIdandName(name, test_tg_id)
        
        result = main_functions.get_time(test_time, test_date)
                
        if result is False or result is True:
            assert False

        date_time, native_dt = result
        
        db.addAll(test_task, date_time, test_tg_id, test_job_id)

        #Act
        result = db.returnJobId(test_task, test_tg_id)
        result2 = db.returnJobId(test_task, test_tg_id2)
        
        #Assert
        db.delTask(test_task, test_tg_id)
        db.delUser(test_tg_id)
        assert result == test_job_id
        assert result2 is None
        
    def test_isTokenExist(self):
        #Arrange
        db = Repo()
        test_tg_id: int = 1092334
        name: str = 'Dagon'
        test_token: str = 'ajsdjfndbch1291982klasdascujnhqyg78312yysdfghjkwertyu'
        db.addToken(test_tg_id, test_token)
        test_tg_id2: int = 1231231312
        
        db.addTgIdandName(name, test_tg_id)
        db.addTgIdandName(name, test_tg_id2)
        
        db.addToken(test_tg_id, test_token)
        
        #Act
        result = db.isTokenExist(test_tg_id)
        result2 = db.isTokenExist(test_tg_id2)
        
        #Assert
        db.delUser(test_tg_id)
        db.delUser(test_tg_id2)
        assert result == test_token
        assert result2 is None
        
    def test_addToken(self):
        #Arrange
        db = Repo()
        test_tg_id: int = 1092334
        name: str = 'Dagon'
        test_token: str = 'ajsdjfndbch1291982klasdascujnhqyg78312yysdfghjkwertyu'
        
        db.addTgIdandName(name, test_tg_id)
        
        #Act
        result = db.addToken(test_tg_id, test_token)
        
        #Assert
        db.delUser(test_tg_id)
        assert result is True
        
    def test_refreshToken(self):
        
        #Arrange
        db = Repo()
        test_tg_id: int = 1092334
        name: str = 'Dagon'
        test_token: str = 'ajsdjfndbch1291982klasdascujnhqyg78312yysdfghjkwertyu'
        
        db.addTgIdandName(name, test_tg_id)
        db.addToken(test_tg_id, test_token)
        
        #Act
        result = db.refreshToken(test_tg_id, test_token)
        
        #Assert
        db.delUser(test_tg_id)
        assert result is True
        
    def test_isDateTimeExist(self):
        
        #Arrange
        db = Repo()
        main_functions = createTime()
        test_tg_id: int = 1092334
        name: str = 'Dagon'
        test_task: str = 'Помыть руки'
        test_time: str = '20:30'
        test_date: str = '09.12.2026'
        test_job_id: str = '11123_sdhfbsjdhf_121212'
        test_time2: str = '09:09'
        test_result =  [{'time': '2026-12-09 20:30:00+0300', 'task': 'Помыть руки'}]
        
        take_datetime = main_functions.get_time(test_time, test_date)
        take_datetime2 = main_functions.get_time(test_time2, test_date)
        
        db.addTgIdandName(name, test_tg_id)
        
        if take_datetime is False or take_datetime is True:
            assert False
            
        if take_datetime2 is False or take_datetime2 is True:
            assert False
        
        date_time, native_dt = take_datetime
        date_time2, native_dt2 = take_datetime2
        
        db.addAll(test_task, date_time, test_tg_id, test_job_id)
        
        #Act
        result = db.isDateTimeExist(date_time, test_tg_id)
        result2 = db.isDateTimeExist(date_time2, test_tg_id)
        
        
        #Assert
        db.delTask(test_task, test_tg_id)
        db.delUser(test_tg_id)
        assert result == test_result
        assert result2 is None
        
    def test_DeletAll(self):
        #Arrange
        db = Repo()
        main_functions = createTime()
        test_tg_id: int = 1092334
        name: str = 'Dagon'
        test_task: str = 'Помыть руки'
        test_time: str = '20:30'
        test_date: str = '20.12.2026'
        test_job_id: str = '11123_sdhfbsjdhf_121212'
        
        db.addTgIdandName(name, test_tg_id)
        
        take_datetime = main_functions.get_time(test_time, test_date)
        
        if take_datetime is False or take_datetime is True:
            assert False
            
        date_time, native_dt = take_datetime
                
        db.addAll(test_task, date_time, test_tg_id, test_job_id)
        
        #Act
        result = db.DeleteAll(test_tg_id)
        
        #Assert
        db.delTask(test_task, test_tg_id)
        db.delUser(test_tg_id)
        assert result is True
        
    def test_delUser(self):
        #Arrange
        db = Repo()
        test_tg_id: int = 1092334
        name: str = 'Dagon'
        
        db.addTgIdandName(name, test_tg_id)
        
        #Act
        result = db.delUser(test_tg_id)
        
        #Assert
        db.delUser(test_tg_id)
        assert result is True
        
    def test_delTask(self):
        #Arrange
        db = Repo()
        main_functions = createTime()
        test_tg_id: int = 1092334
        name: str = 'Dagon'
        test_task: str = 'Помыть руки'
        test_time: str = '20:30'
        test_date: str = '20.12.2026'
        test_job_id: str = '11123_sdhfbsjdhf_121212'
        
        test_tg_id2: int = 123
        
        db.addTgIdandName(name, test_tg_id)
        
        take_datetime = main_functions.get_time(test_time, test_date)
        
        if take_datetime is False or take_datetime is True:
            assert False
            
        date_time, native_dt = take_datetime
                
        db.addAll(test_task, date_time, test_tg_id, test_job_id)
        
        #Act
        result = db.delTask(test_task, test_tg_id)
        result2 = db.delTask(test_task, test_tg_id2)
        
        #Assert
        assert result is True
        assert result2 is False