from typing import Any

from fastlife import TRegistry
from fastlife.service.job import AbstractJob


class DummyScheduler:
    def __init__(self) -> None:
        self.jobs: list[dict[str, Any]] = []

    def add_job(
        self,
        job: type[AbstractJob[TRegistry]],
        **kwargs: Any,
    ) -> None:
        self.jobs.append({"job": job, **kwargs})

    def start(self): ...

    def shutdown(self, wait: bool): ...
