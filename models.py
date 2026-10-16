from pydantic import BaseModel, field_validator
from datetime import datetime

class Task(BaseModel):
    UserId: int
    TaskName: str
    Time: datetime
    JobId: str
    
    @field_validator("JobId")
    @classmethod
    def validate_jobid(cls, value: str):
        if len(value.split("_")) != 3:
            raise ValueError('JobId не соответсвует формату')
        return value