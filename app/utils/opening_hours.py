import datetime

import pytz
from aiogram.types import BusinessOpeningHours


def check_opening_hours(opening_hours : BusinessOpeningHours):
    tz = pytz.timezone(opening_hours.time_zone_name)
    now = datetime.datetime.now(tz)
    monday_start = now - datetime.timedelta(
        days=now.weekday(),
        hours=now.hour,
        minutes=now.minute,
        seconds=now.second,
        microseconds=now.microsecond
    )

    minutes_since_monday = (now - monday_start).total_seconds() / 60
    for day in opening_hours.opening_hours:
        if day.opening_minute <= minutes_since_monday <= day.closing_minute:
            return False

    return True
