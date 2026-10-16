from Mock.mock_sql import SqlMock

class Test_Repo:
    
    def test_addAll(self):
        
        #Arrange
        db = SqlMock()
        test_tg_id: int = 1092334
        test_task: str = 'Помыть руки'
        test_time: str = '20:30'
        test_job_id: str = '11123_sdhfbsjdhf_121212' 
        
        
        #Act
        result = db.addAll(test_task, test_time, test_tg_id, test_job_id)
        
        #Assert
        assert result is True
    
    def test_isUserExist(self):
        
        # Arrange
        db = SqlMock()
        test_tg_id1: int = 1092334
        db.addId(test_tg_id1)
        test_tg_id2: int = 1231231
        
        #Act
        result_1 = db.isUserExist(test_tg_id1)
        result_2 = db.isUserExist(test_tg_id2)
        
        # Assert
        assert result_1 is True
        assert result_2 is None
        
    def test_isTaskExist(self):
        
        #Arrange
        db = SqlMock()
        test_tg_id: int = 1092334
        test_task: str = 'Помыть руки'
        test_time: str = '20:30'
        test_job_id: str = '11123_sdhfbsjdhf_121212'
        db.addAll(test_task, test_time, test_tg_id, test_job_id)
        test_task2: str = 'Чем то заняться'
        
        #Act
        result = db.delTask(test_task, test_tg_id)
        result2 = db.delTask(test_task2, test_tg_id)
        
        #Assert
        assert result is True
        assert result2 is None
        
    def test_changeTimeAndDate(self):
        
        #Arrange
        db = SqlMock()
        test_tg_id: int = 1092334
        test_task: str = 'Помыть руки'
        test_time: str = '20:30'
        test_job_id: str = '11123_sdhfbsjdhf_121212'
        db.addAll(test_task, test_time, test_tg_id, test_job_id)
        test_task2: str = 'Чем то заняться'
        
        #Act
        result = db.changeTimeAndDate(test_task, test_time, test_tg_id)
        result2 = db.changeTimeAndDate(test_task2, test_time, test_tg_id)
        
        #Assert
        assert result is True
        assert result2 is None
        
    def test_watch(self):
        
        #Arrange
        db = SqlMock()
        test_tg_id: int = 1092334
        test_task: str = 'Помыть руки'
        test_time: str = '20:30'
        test_job_id: str = '11123_sdhfbsjdhf_121212'
        db.addAll(test_task, test_time, test_tg_id, test_job_id)
        test_tg_id2: int = 1231231312
                
        #Act
        result = db.watch(test_tg_id)
        result2 = db.watch(test_tg_id2)
        
        #Assert
        assert result is True
        assert result2 is None
        
    def test_returnJObId(self):
        
        #Arrange
        db = SqlMock()
        test_tg_id: int = 1092334
        test_task: str = 'Помыть руки'
        test_time: str = '20:30'
        test_job_id: str = '11123_sdhfbsjdhf_121212'
        db.addAll(test_task, test_time, test_tg_id, test_job_id)
        test_task2: str = 'Чем-то заняться'

        #Act
        result = db.returnJobId(test_task, test_tg_id)
        result2 = db.returnJobId(test_task2, test_tg_id)
        
        #Assert
        assert result is True
        assert result2 is None
        
    def test_isTokenExist(self):
        #Arrange
        db = SqlMock()
        test_tg_id: int = 1092334
        db.addId(test_tg_id)
        test_token: str = 'ajsdjfndbch1291982klasdascujnhqyg78312yysdfghjkwertyu'
        db.addToken(test_tg_id, test_token)
        test_tg_id2: int = 1231231312
        
        #Act
        result = db.isTokenExist(test_tg_id)
        result2 = db.isTokenExist(test_tg_id2)
        
        #Assert
        assert result is True
        assert result2 is False
        
    def test_addToken(self):
        #Arrange
        db = SqlMock()
        test_tg_id: int = 1092334
        db.addId(test_tg_id)
        test_token: str = 'ajsdjfndbch1291982klasdascujnhqyg78312yysdfghjkwertyu'
        db.addToken(test_tg_id, test_token)
        
        test_tg_id2: int = 123
        db.addId(test_tg_id2)
        test_token2: str = '42'
        
        #Act
        result = db.addToken(test_tg_id, test_token)
        result2 = db.addToken(test_tg_id2, test_token2)
        
        #Assert
        assert result is None
        assert result2 is True
        
    def test_refreshToken(self):
        
        #Arrange
        db = SqlMock()
        test_tg_id: int = 1092334
        db.addId(test_tg_id)
        test_token: str = 'ajsdjfndbch1291982klasdascujnhqyg78312yysdfghjkwertyu'
        db.addToken(test_tg_id, test_token)
        test_tg_id2: int = 123
        
        #Act
        result = db.refreshToken(test_tg_id, test_token)
        result2 = db.refreshToken(test_tg_id2, test_token)
        
        #Assert
        assert result is True
        assert result2 is None
        
    def test_isDateTimeExist(self):
        
        #Arrange
        db = SqlMock()
        test_tg_id: int = 1092334
        test_task: str = 'Помыть руки'
        time: str = '20:30'
        test_job_id: str = '11123_sdhfbsjdhf_121212'
        db.addAll(test_task, time, test_tg_id, test_job_id)
        test_time1: str = '20:30'
        test_time2: str = '09:09'
        
        #Act
        result = db.isDateTimeExist(test_time1, test_tg_id)
        result2 = db.isDateTimeExist(test_time2, test_tg_id)
        
        #Assert
        assert result is None
        assert result2 is True
        
    def test_DeletAll(self):
        #Arrange
        db = SqlMock()
        test_tg_id: int = 1092334
        test_task: str = 'Помыть руки'
        time: str = '20:30'
        test_job_id: str = '11123_sdhfbsjdhf_121212'
        db.addAll(test_task, time, test_tg_id, test_job_id)
        test_tg_id2: int = 123
        
        #Act
        result = db.DeleteAll(test_tg_id)
        result2 = db.DeleteAll(test_tg_id2)
        
        #Assert
        assert result is True
        assert result2 is False
        