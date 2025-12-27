"""
Configure views using a decorator.

A simple usage:

```python
from typing import Annotated

from fastapi import Response
from fastlife import Template, template, view_config


@view_config("hello_world", "/", methods=["GET"])
async def hello_world(
    template: Annotated[Template, template("HelloWorld.jinja")],
) -> Response:
    return template()
```
"""

from collections.abc import Callable
from datetime import datetime
from typing import Any

import venusian
from apscheduler.util import undefined

from fastlife.service.job import AbstractJob, JobSchedulerTrigger, Undefined
from fastlife.service.registry import TRegistry

from .configurator import VENUSIAN_CATEGORY, GenericConfigurator


def sheduled_job_config(
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
) -> Callable[..., type[AbstractJob[TRegistry]]]:
    """
    A decorator function to register a job in the
    {class}`Configurator <fastlife.config.configurator.GenericConfigurator>`
    while scaning a module using {func}`include
    <fastlife.config.configurator.GenericConfigurator.include>`.

    :return: the configuration callback.
    """
    job_name = name

    def configure(
        wrapped: type[AbstractJob[TRegistry]],
    ) -> type[AbstractJob[TRegistry]]:
        def callback(
            scanner: venusian.Scanner, name: str, ob: type[AbstractJob[TRegistry]]
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
