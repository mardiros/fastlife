import logging

from fastlife.config.jobs import sheduled_job_config
from tests.fastlife_app.config import MyRegistry

log = logging.getLogger(__name__)


@sheduled_job_config(trigger="interval", seconds=5, max_instances=1)
def ping_me(registry: MyRegistry):
    log.info("ping")


@sheduled_job_config(trigger="interval", seconds=5, max_instances=1)
async def pong_me(registry: MyRegistry):
    log.info("pong")
