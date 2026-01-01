"""
Configure scheduled job using a decorator.

Scheduled jobs are useful for handling application lifecycle tasks,
such as database cleanup, cache population, and other asynchronous
operations that aren't tied to user requests.

Exemple of usage:

```python
from typing import Annotated

from fastapi import Response
from fastlife import scheduled_job


@scheduled_job(trigger="interval", seconds=60)
async def cleanup():
    with self.registry.uow_factory() as t:
        await t.uow.tokens.remove_expired_sessions()
        await t.commit()
```

Note that if the trigger parameter is comming from a settings,
the usage of a {func}`fastlife.config.configurator.configure` decorator
is more appropriate in order to inject it using the underlying method
{func}`fastlife.config.configurator.register_job` consumed by the
scheduled_job decorator.
"""

from collections.abc import Callable
from datetime import datetime
from typing import Any

import venusian
from apscheduler.util import undefined

from fastlife.service.job import JobHandler, JobSchedulerTrigger, Undefined
from fastlife.service.registry import TRegistry

from .configurator import VENUSIAN_CATEGORY, GenericConfigurator


def scheduled_job(
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
) -> Callable[..., JobHandler[TRegistry]]:
    """
    A decorator function to register a job in the
    {func}`Configurator <fastlife.config.configurator.GenericConfigurator.register_job>`
    while scaning a module using {func}`include
    <fastlife.config.configurator.GenericConfigurator.include>`.

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
    :return: the configuration callback.
    """
    job_name = name

    def configure(
        wrapped: JobHandler[TRegistry],
    ) -> JobHandler[TRegistry]:
        def callback(
            scanner: venusian.Scanner, name: str, ob: JobHandler[TRegistry]
        ) -> None:
            if not hasattr(scanner, VENUSIAN_CATEGORY):
                return  # coverage: ignore
            config: GenericConfigurator[TRegistry] = getattr(scanner, VENUSIAN_CATEGORY)
            config.register_job(
                wrapped,
                trigger=trigger,
                id=id,
                name=job_name or name,
                misfire_grace_time=misfire_grace_time,
                coalesce=coalesce,
                max_instances=max_instances,
                next_run_time=next_run_time,
                jobstore=jobstore,
                executor=executor,
                replace_existing=replace_existing,
                **trigger_args,
            )

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
        return wrapped

    return configure
