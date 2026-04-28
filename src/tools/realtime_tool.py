import pytz
from src.timezon import all_timezones

def display_realtime_info():
    for tz in all_timezones:
        print(f"Time zone: {tz}")
        print(f"Current time: {pytz.timezone(tz).localize(pytz.datetime.now())}")
        print("-------------------------------")


display_realtime_info()