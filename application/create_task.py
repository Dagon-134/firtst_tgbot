from datetime import datetime
import pytz

class createTask:
        
    def creat_date(self, date) -> False | True:
        try:
            dt = datetime.strptime(date, "%d.%m.%Y")
            
        except ValueError:
            return False

        return True
    
        
    def creat_time(self, time) -> False | True:
        try:
            dt = datetime.strptime(time, "%H:%M")
            
        except ValueError:
            return False
        
        return True
    
    
    def get_time(self, time, date) -> datetime | None:
        user_tz_str = 'Europe/Moscow'
        user_tz = pytz.timezone(user_tz_str)
        
        native_dt = datetime(int(date[6] + date[7] + date[8] + date[9]), int(date[3] + date[4]), int(date[0] + date[1]), int(time[0] + time[1]), int(time[3] + time[4]))
        aware_dt = user_tz.localize(native_dt)
        utc_dt = aware_dt.astimezone(pytz.UTC)
        
        if utc_dt < datetime.now(pytz.UTC):
            return None
        
        else:
            return utc_dt, native_dt