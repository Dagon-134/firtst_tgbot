from application.create_time import createTime

class Test_time:
    
    def test_validate_date(self):
        #Arrange
        Create = createTime()
        test_date1 = '20.10.2027'
        test_date2 = '20:1:2025'
        
        #Act
        result1 = Create.validate_date(test_date1)
        result2 = Create.validate_date(test_date2)
        
        #Asser
        assert result1 is True
        assert result2 is False
        
    def test_validate_time(self):
        #Arrange
        Create = createTime()
        test_time1 = '20:09'
        test_time2 = '20.1'
        
        #Act
        result1 = Create.validate_time(test_time1)
        result2 = Create.validate_time(test_time2)
        
        #Assert
        assert result1 is True
        assert result2 is False
        
    def test_get_time(self):
        #Arrange
        Create = createTime()
        test_time1 = '20:09'
        test_date1 = '20.10.2027'
        test_result = ('2027-10-20 17:09:00+0000', '2027-10-20 20:09:00')
        
        test_time2 = '20.1'
        test_date2 = '20:1:2025'      
        
        #Act
        result1 = Create.get_time(test_time1, test_date1)
        result2 = Create.get_time(test_time2, test_date2)
        
        if result1 is not True and result1 is not False:
                   
            date_time, native_dt = result1
            
            date_time = date_time.strftime('%Y-%m-%d %H:%M:%S%z')
            native_dt = native_dt.strftime('%Y-%m-%d %H:%M:%S%z')
            result = (date_time, native_dt)
            
            #Assert
            assert result == ('2027-10-20 17:09:00+0000', '2027-10-20 20:09:00')
            assert result2 is False