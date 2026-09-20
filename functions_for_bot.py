
from datetime import datetime
import pytz



def get_time(time, date) -> datetime | None:

    user_tz_str = 'Europe/Moscow'
    user_tz = pytz.timezone(user_tz_str)
    
    native_dt = datetime(int(date[6] + date[7] + date[8] + date[9]), int(date[3] + date[4]), int(date[0] + date[1]), int(time[0] + time[1]), int(time[3] + time[4]))
    aware_dt = user_tz.localize(native_dt)
    utc_dt = aware_dt.astimezone(pytz.UTC)
     
    if utc_dt < datetime.now(pytz.UTC):
        return None
    
    else:
        return utc_dt, native_dt
    
    
    
def creat_date(date) -> False | True:
    list = []
    data_text = date
    
    for i in data_text:
        list.append(i)
    
    if len(list) != 10:
        return False
            
    elif list[2] != '.' and list[5] != '.':
        return False
       
    #Проверка, если месяц февраль и в нём введён день больше 28, то будет выводится ошибка
    elif ((list[3] + list[4] != '01') or (list[3] + list[4] !='03') or (list[3] + list[4] !='05') or (list[3] + list[4] !='07') or (list[3] + list[4] !='08') or (list[3] + list[4] !='10') or (list[3] + list[4] !='12') or (list[3] + list[4] !='04') or (list[3] + list[4] !='06') or (list[3] + list[4] !='09') or (list[3] + list[4] !='11')) and (int(list[0]) >= 2 and int(list[1]) > 8):
        return False   
        
    #Проверка, если введённый день равняется или является больше 32 и при этом месяц, в котором максимум 31 день(январь, март, май и т.д.), то будет выводится ошибка  
    elif ((int(list[0]) >= 3 and int(list[1]) >= 2) and ((list[3] + list[4] != '02') or (list[3] + list[4] !='04') or (list[3] + list[4] !='06') or (list[3] + list[4] !='09') or (list[3] + list[4] !='11'))):
        return False  
        
    #Проверка, если введённый день равняется или является больше 31 и при этом месяц, в котором максимум 30 дней(апрель, июнь, сентябрь и т.д.), то будет выводится ошибка
    elif ((int(list[0]) >= 3 and int(list[1]) >= 1) and ((list[3] + list[4] != '01') or (list[3] + list[4] !='03') or (list[3] + list[4] !='05') or (list[3] + list[4] !='07') or (list[3] + list[4] !='08') or (list[3] + list[4] !='10') or (list[3] + list[4] !='12') or (list[3] + list[4] !='02'))):
        return False
        
    #Проверка, если определённые суммированный объекты выводят год меньше или равно 2025, то будет выдоваться ошибка    
    elif int(list[6] + list[7] + list[8] + list[9]) <= 2025:
        return False      
        
    else:
        return True
    
    
    
def creat_time(time) -> False | True:
    time_text = time
    list = []

    for i in time_text:
        list.append(i)
        
    if len(list) != 5:
        return False
   
    elif list[2] != ':':
        return False
    
    elif ((int(list[0]) >= 2) and (int(list[1]) >= 4)) or (int(list[3]) >= 6):
        return False
               
    else:
        return True
    
    
