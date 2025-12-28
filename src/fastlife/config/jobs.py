"""
Configure scheduled job using a decorator.

Scheduled jobs are useful for handling application lifecycle tasks,
such as database cleanup, cache population, and other asynchronous
operations that aren't tied to user requests.

Exemple of usage:

```python
from typing import Annotated

from fastapi import Response
from fastlife import sheduled_job


@sheduled_job(trigger="interval", seconds=60)
async def cleanup():
    with self.registry.uow_factory() as t:
        await t.uow.tokens.remove_expired_sessions()
        await t.commit()
```

Note that if the trigger parameter is comming from a settings,
the usage of a {func}`fastlife.config.configurator.configure` decorator
is more appropriate in order to inject it using the underlying method
{func}`fastlife.config.configurator.register_job` consumed by the
sheduled_job decorator.
"""

from collections.abc import Callable
from datetime import datetime
from typing import Any

import venusian
from apscheduler.util import undefined

from fastlife.service.job import JobHook, JobSchedulerTrigger, Undefined
from fastlife.service.registry import TRegistry

from .configurator import VENUSIAN_CATEGORY, GenericConfigurator


def sheduled_job(
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
) -> Callable[..., JobHook[TRegistry]]:
    """
    A decorator function to register a job in the
    {class}`Configurator <fastlife.config.configurator.GenericConfigurator>`
    while scaning a module using {func}`include
    <fastlife.config.configurator.GenericConfigurator.include>`.

    :return: the configuration callback.
    """
    job_name = name

    def configure(
        wrapped: JobHook[TRegistry],
    ) -> JobHook[TRegistry]:
        def callback(
            scanner: venusian.Scanner, name: str, ob: JobHook[TRegistry]
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
