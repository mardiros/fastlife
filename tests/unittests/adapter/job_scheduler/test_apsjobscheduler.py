from typing import Any, cast

from fastlife.adapters.apscheduler.job_scheduler import JobScheduler
from fastlife.config.configurator import (
    Configurator,
)
from fastlife.service.job import JobHandler
from fastlife.service.registry import DefaultRegistry


class DuckScheduler:
    def __init__(self) -> None:
        self.jobs: list[dict[str, Any]] = []
        self.started = None
        self.wait_shutdown = None

    def add_job(
        self,
        job: JobHandler[Any],
        **kwargs: Any,
    ) -> None:
        self.jobs.append({"job": job, **kwargs})

    def start(self):
        self.started = True

    def shutdown(self, wait: bool):
        self.started = False
        self.wait_shutdown = wait


class MyDummyJobScheduler(JobScheduler[Any]):
    def __init__(self, registry: Any) -> None:
        super().__init__(registry)
        self.scheduler = DuckScheduler()  # type: ignore


def test_register_interval_job(conf: Configurator):
    async def dummy_task(registry: DefaultRegistry) -> None: ...

    conf.set_job_scheduler(MyDummyJobScheduler)
    conf.register_job(dummy_task, trigger="interval", seconds=42)

    scheduler = cast(
        DuckScheduler,
        conf.registry.job_scheduler.scheduler,  # type: ignore
    )
    assert len(scheduler.jobs) == 1
    assert scheduler.jobs[0]["job"] is dummy_task
    assert scheduler.jobs[0]["kwargs"] == {"registry": conf.registry}
    assert scheduler.jobs[0]["trigger"] == "interval"
    assert scheduler.jobs[0]["seconds"] == 42


def test_start(conf: Configurator):
    sched = MyDummyJobScheduler(None)
    sched.start()
    assert sched.scheduler.started is True  # type: ignore


def test_shutdown(conf: Configurator):
    sched = MyDummyJobScheduler(None)
    sched.shutdown(wait=True)
    assert sched.scheduler.started is False  # type: ignore
    assert sched.scheduler.wait_shutdown is True  # type: ignore
