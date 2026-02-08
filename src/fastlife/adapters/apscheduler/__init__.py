"""
Use {term}`apscheduler` to run scheduled jobs.

Usage:

```
from fastlife import Configurator, configure
from fastlife.adapters.apscheduler import JobScheduler


@configure
def includeme(conf: Configurator) -> None:
    conf.set_job_scheduler(JobScheduler)
```

"""

from .job_scheduler import JobScheduler

__all__ = ["JobScheduler"]
