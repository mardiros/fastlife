import logging
from typing import ClassVar

from fastlife.config.jobs import sheduled_job_config
from fastlife.service.job import AbstractJob
from tests.fastlife_app.config import MyRegistry

log = logging.getLogger(__name__)


@sheduled_job_config(
    trigger="interval",
    max_instances=1,
    seconds=15,
)
class PingMe(AbstractJob[MyRegistry]):
    called: ClassVar[int] = 0

    async def run(self) -> None:
        PingMe.called += 1  # type: ignore
        log.info(
            "I have been called %d times",
            PingMe.called,  # type: ignore
        )
