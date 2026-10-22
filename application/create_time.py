from datetime import datetime
import pytz

class createTime:
        
    def validate_date(self, date) -> bool:
        try:
            dt = datetime.strptime(date, "%d.%m.%Y")
            
        except ValueError:
            return False

        return True
    
        
    def validate_time(self, time) -> bool:
        try:
            dt = datetime.strptime(time, "%H:%M")
            
        except ValueError:
            return False
        
        return True
    
    
    def get_time(self, time, date) -> tuple[datetime, datetime] | bool:
        try:
            user_tz_str = 'Europe/Moscow'
            user_tz = pytz.timezone(user_tz_str)
            
            native_dt = datetime(int(date[6] + date[7] + date[8] + date[9]), int(date[3] + date[4]), int(date[0] + date[1]), int(time[0] + time[1]), int(time[3] + time[4]))
            aware_dt = user_tz.localize(native_dt)
            utc_dt = aware_dt.astimezone(pytz.UTC)
            
            if utc_dt < datetime.now(pytz.UTC):
                return False
            
            else:
                return (utc_dt, native_dt)
        except IndexError:
            return False