"""
Service for scheduled jobs.

By default, scheduled jobs are disabled,
to start scheduled job based on {term}`APScheduler`
the scheduler must be installed using the configurator
method {meth}`fastlife.config.configurator.GenericConfigurator.set_job_scheduler`
during the bootstrap and before scanning installed jobs using the decorator
{function}`fastlife.config.jobs.scheduled_job`.
"""

import abc
from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Any, Generic, Literal, TypeAlias

from apscheduler.triggers.base import BaseTrigger
from apscheduler.util import _Undefined as Undefined  # type: ignore
from apscheduler.util import undefined

from fastlife.service.registry import TRegistry

__all__ = [
    "JobHandler",
    "JobSchedulerTrigger",
    "Undefined",
    "undefined",
]

JobSchedulerTriggerLiteral = Literal["interval", "cron", "date"]
JobSchedulerTrigger: TypeAlias = JobSchedulerTriggerLiteral | BaseTrigger


JobHandler = Callable[[TRegistry], None] | Callable[[TRegistry], Awaitable[None]]


class AbstractJobScheduler(abc.ABC, Generic[TRegistry]):
    """
    Devine the job scheduler interface.

    fastlife rely on {term}`APScheduler` and {term}`Starlette`'s lifespan
    to start the scheduler.
    By default, it is disabled, the job scheduler based on APScheduler
    as to be installed to get it working.

    This avoids to run APScheduler for the application that don't requires it.
    At the moment. the signature of the registration job relies on APScheduler
    definition so the library needs to be always installed event if the scheduler
    does not run.
    """

    def __init__(self, registry: TRegistry) -> None:
        self.registry = registry

    @abc.abstractmethod
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

    @abc.abstractmethod
    def start(self) -> None:
        """
        Start the scheduler.

        This will have no effect until the settings enable_scheduler is enabled.
        """

    @abc.abstractmethod
    def shutdown(self, *, wait: bool) -> None:
        """
        Shutdown the scheduler.

        This will have no effect until the settings enable_scheduler is enabled.
        """


class SinkholeJobScheduler(AbstractJobScheduler[TRegistry]):
    """The default job scheduler that never scheduled jobs."""

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
        """Do nothing."""

    def start(self) -> None:
        """Do nothing."""

    def shutdown(self, *, wait: bool) -> None:
        """Do nothing."""
