#!/usr/bin/env python3
import datetime
from importlib.metadata import version

header = (
    f"## {version('fastlifeweb')}  - "
    f"Released on {datetime.datetime.now().date().isoformat()}"
)

with open("CHANGELOG.md.new", "w") as changelog:
    changelog.write(header)
    changelog.write("\n")
    changelog.write("* please write here")
    changelog.write("\n\n")
