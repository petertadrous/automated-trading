import datetime
from typing import Optional, Union


from config.defaults import DATE_FORMAT, DAY_DELTA


DateType = Union[str, datetime.date]


def strfdate(d: datetime.date) -> str:
    return datetime.date.strftime(d, DATE_FORMAT)

def strpdate(d: str) -> datetime.date:
    return datetime.datetime.strptime(d, DATE_FORMAT)

def add_days(
        d: DateType,
        delta: int = DAY_DELTA,
) -> datetime.date:
    """Adds `delta` days to `d` object and returns string representation.
    Handles converting `d` from string to `datetime.date` type."""
    if isinstance(d, str):
        d = strpdate(d)
    start_date = d + datetime.timedelta(days=delta)
    return start_date


def get_default_end_date(
        start: Optional[DateType] = None,
        delta: Optional[int] = DAY_DELTA,
) -> str:
    if start is None or delta is None:
        return strfdate(datetime.date.today())
    if isinstance(start, str):
        start = strpdate(start)
    return strfdate(add_days(start, delta))


def get_default_start_date(
    end: DateType,
    delta: int = DAY_DELTA,
) -> str:
    if isinstance(end, str):
        end = strpdate(end)
    return strfdate(add_days(end, -delta))
