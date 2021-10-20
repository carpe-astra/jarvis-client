"""API endpoints for tasks"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from app import workers
from app.core._logging import logger
from app.models.tasks import Action, ScheduleAt, ScheduleIn, SchedulePeriodic, Task
from app.modules_util import (
    MODULES_PATH,
    InvalidFunctionError,
    InvalidModuleError,
    get_function_callable,
)

router = APIRouter()


# Helper Functions
# ================================================================
def get_job_by_id(task_id: str):
    job = workers.get_job(task_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        )
    return job


def get_func_from_action(action: Action):
    try:
        func = get_function_callable(action.module, action.function)

    except InvalidModuleError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Module not found."
        )

    except InvalidFunctionError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Function not found."
        )

    return func


def get_task_from_job(job: workers.Job):
    scheduled_jobs = workers.scheduler.get_jobs(with_times=True)

    if job in workers.scheduler:
        for _job, _time in scheduled_jobs:
            if _job == job:
                scheduled_time = _time
                break

        if job.meta.get("interval", None):
            schedule = SchedulePeriodic(
                scheduled_time=scheduled_time,
                interval=job.meta.get("interval"),
                repeat=job.meta.get("repeat"),
            )

        else:
            schedule = ScheduleAt(scheduled_time=scheduled_time)
    else:
        schedule = ScheduleAt(scheduled_time=job.enqueued_at)

    return Task(
        id=job.id,
        action=Action(
            function=job.func_name.removeprefix(f"{MODULES_PATH}."),
            args=job.args,
            kwargs=job.kwargs,
        ),
        schedule=schedule,
    )


# Endpoints
# ================================================================
@router.get("/", response_model=List[Task])
async def get_tasks():
    return [get_task_from_job(job) for job in workers.get_jobs()]


@router.get("/id/{task_id}", response_model=Task)
async def get_task_by_id(task_id: str):
    job = get_job_by_id(task_id)
    return get_task_from_job(job)


@router.post("/enqueue", response_model=Task)
async def enqueue_task(
    action: Action = Depends(),
):
    func = get_func_from_action(action)
    now = datetime.now()
    job = workers.enqueue_at(now, func, *action.args, **action.kwargs)
    return get_task_from_job(job)


@router.post("/enqueue/at", response_model=Task)
async def enqueue_task_at(action: Action = Depends(), schedule: ScheduleAt = Depends()):
    func = get_func_from_action(action)
    job = workers.enqueue_at(
        schedule.scheduled_time, func, *action.args, **action.kwargs
    )
    return get_task_from_job(job)


@router.post("/enqueue/in", response_model=Task)
async def enqueue_task_in(action: Action = Depends(), schedule: ScheduleIn = Depends()):
    func = get_func_from_action(action)
    job = workers.enqueue_in(schedule.time_delta, func, *action.args, **action.kwargs)
    return get_task_from_job(job)


@router.post("/enqueue/periodic", response_model=Task)
async def enqueue_task_periodic(
    action: Action = Depends(), schedule: SchedulePeriodic = Depends()
):
    func = get_func_from_action(action)
    job = workers.enqueue_periodic(
        schedule.scheduled_time,
        schedule.interval,
        schedule.repeat,
        func,
        *action.args,
        **action.kwargs,
    )
    return get_task_from_job(job)


# @router.patch("/update/id/{task_id}", response_model=Task)
# async def update_task(task_id: str):
#     return Task()


@router.delete("/dequeue/id/{task_id}")
async def dequeue_task(task_id: str):
    workers.dequeue(task_id)
    return
