"""
Base class for scheduled job.

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
    "JobHook",
    "JobScheduler",
    "JobSchedulerTrigger",
    "Undefined",
    "undefined",
]

JobSchedulerTriggerLiteral = Literal["interval", "cron", "date"]
JobSchedulerTrigger: TypeAlias = JobSchedulerTriggerLiteral | BaseTrigger


JobHook = Callable[[TRegistry], None] | Callable[[TRegistry], Awaitable[None]]


class JobScheduler(Generic[TRegistry]):
    """
    Build the registry of job using venusian.
    """

    def __init__(self, registry: TRegistry) -> None:
        self.registry = registry
        self.scheduler: BaseScheduler = resolve(registry.settings.scheduler_class)()

    def register_job(
        self,
        job: JobHook[TRegistry],
        /,
        *,
        trigger: JobSchedulerTrigger,
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
        self.scheduler.start()

    def shutdown(self, *, wait: bool) -> None:
        self.scheduler.shutdown(wait=wait)
