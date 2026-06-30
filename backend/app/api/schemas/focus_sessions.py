#Verify the validity of the given data for creating a focus session
from datetime import datetime
from pydantic import BaseModel, model_validator, ConfigDict

#Input model for creating a focus session
class FocusSessionCreate(BaseModel):

    title: str | None = None

    start_time: datetime
    work_time: int
    break_time: int

    task_id: int | None = None
    goal_id: int | None = None

    @model_validator(mode='after')
    def check_task_goal_or_title(cls, values):
        if values.task_id is None and values.title is None:
            raise ValueError("A focus session without task must have a title.")
        return values

# Output model for a focus session
class FocusSessionOut(BaseModel):
    id: int
    title: str | None = None

    start_time: datetime
    end_time: datetime
    work_time: int
    break_time: int

    task_id:int | None = None
    goal_id: int | None = None
    user_id: int