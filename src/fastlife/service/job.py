"""
Service for scheduled jobs.
"""

from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Any, Generic, Literal, TypeAlias

from apscheduler.schedulers.base import BaseScheduler
from apscheduler.triggers.base import BaseTrigger
from apscheduler.util import _Undefined as Undefined  # type: ignore
from apscheduler.util import undefined

from fastlife.service.registry import TRegistry
from fastlife.shared_utils.resolver import resolve

__all__ = [
    "JobHandler",
    "JobScheduler",
    "JobSchedulerTrigger",
    "Undefined",
    "undefined",
]

JobSchedulerTriggerLiteral = Literal["interval", "cron", "date"]
JobSchedulerTrigger: TypeAlias = JobSchedulerTriggerLiteral | BaseTrigger


JobHandler = Callable[[TRegistry], None] | Callable[[TRegistry], Awaitable[None]]


class JobScheduler(Generic[TRegistry]):
    """
    Job scheduler and registry.
    """

    def __init__(self, registry: TRegistry) -> None:
        self.registry = registry
        self.scheduler: BaseScheduler = resolve(registry.settings.scheduler_class)()

    def register_job(
        self,
        job: JobHandler[TRegistry],
        /,
        *,
        trigger: JobSchedulerTrigger | None = None,
        id: str | None = None,
        name: str | None = None,
        misfire_grace_time: int | Undefined = undefined,
        coalesce: Undefined = undefined,
        max_instances: int | Undefined = undefined,
        next_run_time: datetime | Undefined = undefined,
        jobstore: str = "default",
        executor: str = "default",
        replace_existing: bool = False,
        **trigger_args: Any,
    ) -> None:
        """
        Register a scheduled job.

        :param job: the job handler to run.
        :param trigger: the way the job is triggered.
        :param id: optional identifier for the job.
        :param name: optional name for the job.
        :param misfire_grace_time: seconds after the designated runtime that the job is still
            allowed to be run (or `None` to allow the job to run no matter how late it is)
        :param coalesce: run once instead of many times if the scheduler determines that the
            job should be run more than once in succession
        :param max_instances: maximum number of concurrently running instances allowed for this
            job
        :param next_run_time: when to first run the job, regardless of the trigger (pass
            `None` to add the job as paused)
        :param jobstore: alias of the job store to store the job in
        :param executor: alias of the executor to run the job with
        :param replace_existing: `True` to replace an existing job with the same `id`
            (but retain the number of runs from the existing one)
        """
        self.scheduler.add_job(  # type: ignore
            job,
            kwargs={"registry": self.registry},
            trigger=trigger,
            id=id,
            name=name,
            misfire_grace_time=misfire_grace_time,
            coalesce=coalesce,
            max_instances=max_instances,
            next_run_time=next_run_time,
            jobstore=jobstore,
            executor=executor,
            replace_existing=replace_existing,
            **trigger_args,
        )

    def start(self) -> None:
        """Start the scheduler."""
        self.scheduler.start()

    def shutdown(self, *, wait: bool) -> None:
        """Shutdown the scheduler."""
        self.scheduler.shutdown(wait=wait)
