import logging

from fastlife.config.jobs import scheduled_job
from tests.fastlife_app.config import MyRegistry

log = logging.getLogger(__name__)


@scheduled_job(trigger="interval", seconds=5, max_instances=1)
def ping_me(registry: MyRegistry):
    log.info("ping")


@scheduled_job(trigger="interval", seconds=5, max_instances=1)
async def pong_me(registry: MyRegistry):
    log.info("pong")
