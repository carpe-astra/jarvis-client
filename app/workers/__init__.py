"""Module for enqueueing tasks to be scheduled and performed in the background"""

from datetime import datetime, timedelta
from typing import Callable

from rq import Queue
from rq.exceptions import NoSuchJobError
from rq.job import Job, JobStatus
from rq_scheduler import Scheduler

from app.config import settings
from app.core._logging import logger
from redis import Redis

# Globals
# ================================================================
_redis_conn = Redis(host=settings.redis_host, port=settings.redis_port)
queue = Queue(connection=_redis_conn)
scheduler = Scheduler(queue=queue, connection=_redis_conn)


# Public Functions
# ================================================================
def get_job(job_id: str):
    try:
        job = Job.fetch(job_id, connection=_redis_conn)
    except NoSuchJobError:
        job = None
    return job


def get_jobs():
    jobs = queue.jobs
    jobs.extend(scheduler.get_jobs())
    return jobs


def enqueue_at(scheduled_time: datetime, func, *args, **kwargs):
    job = scheduler.enqueue_at(scheduled_time, func, *args, **kwargs)

    logger.info(
        "Enqueing task at",
        job_id=job.id,
        scheduled_time=scheduled_time,
        queue_name=scheduler.queue_name,
        func=func.__name__,
        args=args,
        kwargs=kwargs,
    )

    return job


def enqueue_in(time_delta: timedelta, func, *args, **kwargs):
    job = scheduler.enqueue_in(time_delta, func, *args, **kwargs)

    logger.info(
        "Enqueing task in",
        job_id=job.id,
        time_delta=time_delta,
        queue_name=scheduler.queue_name,
        func=func.__name__,
        args=args,
        kwargs=kwargs,
    )

    return job


def enqueue_periodic(
    scheduled_time: datetime,
    interval: int,
    repeat: int,
    func: Callable,
    *args,
    **kwargs
):
    job = scheduler.schedule(
        scheduled_time=scheduled_time,
        func=func,
        args=args,
        kwargs=kwargs,
        interval=interval,
        repeat=repeat,
    )

    logger.info(
        "Enqueing periodic task",
        job_id=job.id,
        scheduled_time=scheduled_time,
        queue_name=scheduler.queue_name,
        func=func.__name__,
        args=args,
        kwargs=kwargs,
    )

    return job


def enqueue(func, *args, **kwargs):
    job = scheduler.enqueue_at(datetime.now(), func, *args, **kwargs)
    return job


def dequeue(job_id: str):
    if job_id in scheduler:
        scheduler.cancel(job_id)
    elif job_id in queue:
        queue.remove(job_id)
