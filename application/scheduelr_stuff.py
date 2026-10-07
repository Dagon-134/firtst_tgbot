from scheduler import scheduler

from application.reminder import Reminder

from datetime import datetime

from sql import returnJobId

class scheduler_job:
    
    def __init__(self, bot):
        self.reminder = Reminder(bot)
    
    async def create_job(self, tg_id: int, time: datetime, task: str) -> str:
        job_id = f"alert_{tg_id}_{int(time.timestamp())}"
                
        scheduler.add_job(
            func=self.reminder.send_alert, 
            trigger='date',
            run_date=time,         
            id=job_id,
            args=[tg_id, task],
            replace_existing=True
        )
        return job_id

    async def change_job(task, tg_id, native_dt):
        find_job_id = returnJobId(task, tg_id)
        job = scheduler.get_job(find_job_id)
        job.reschedule(trigger='date', run_date=native_dt)