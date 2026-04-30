from pytz import all_timezones
from datetime import datetime
import pytz

def gettime(timezone: str = "UTC") -> str:
    if timezone not in all_timezones:
        return f"Invalid timezone. Example: 'Asia/Dhaka', 'America/New_York'"
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    return f"Current time in {timezone} is {current_time}"