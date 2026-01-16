import enum

from pydantic import BaseModel, Field


class Weekday(enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class Form(BaseModel):
    days: set[Weekday] = Field(
        title="Weekay",
        default={
            Weekday.MONDAY,
            Weekday.TUESDAY,
            Weekday.WEDNESDAY,
            Weekday.THURSDAY,
            Weekday.FRIDAY,
        },
    )
