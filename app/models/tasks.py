from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

from pydantic import UUID4, BaseModel


class Action(BaseModel):
    function: str = ""
    args: List[Any] = []
    kwargs: Dict[str, Any] = {}


class Schedule(BaseModel):
    pass


class ScheduleAt(Schedule):
    scheduled_time: datetime = datetime.now()


class ScheduleIn(Schedule):
    time_delta: timedelta = timedelta()


class SchedulePeriodic(Schedule):
    scheduled_time: datetime = datetime.now()
    interval: int
    repeat: int = None


class Task(BaseModel):
    id: UUID4
    action: Action
    schedule: Union[ScheduleAt, ScheduleIn, SchedulePeriodic]
