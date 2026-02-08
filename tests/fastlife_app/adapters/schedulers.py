from datetime import datetime
from typing import Any

from fastlife import TRegistry
from fastlife.service.job import (
    AbstractJobScheduler,
    JobHandler,
    JobSchedulerTrigger,
    Undefined,
    undefined,
)


class DummyScheduler(AbstractJobScheduler[Any]):
    def __init__(self, registry: Any) -> None:
        super().__init__(registry)
        self.jobs: list[dict[str, Any]] = []

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
        self.jobs.append(
            {
                "job": job,
                "trigger": trigger,
                "id": id,
                "name": name,
                "misfire_grace_time": misfire_grace_time,
                "coalesce": coalesce,
                "max_instances": max_instances,
                "next_run_time": next_run_time,
                "jobstore": jobstore,
                "executor": executor,
                "replace_existing": replace_existing,
                **trigger_args,
            }
        )

    def start(self): ...

    def shutdown(self, *, wait: bool): ...
