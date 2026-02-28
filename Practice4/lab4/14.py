from datetime import datetime, timedelta, timezone
import re

def parse_datetime(line):
    date_str, tz_str = line.split()
    year, month, day = map(int, date_str.split('-'))
    match = re.match(r'UTC([+-])(\d+):(\d+)', tz_str)
    sign, hours, minutes = match.groups()
    offset_minutes = int(hours) * 60 + int(minutes)
    if sign == '-':
        offset_minutes = -offset_minutes
    tz = timezone(timedelta(minutes=offset_minutes))
    return datetime(year, month, day, 0, 0, 0, tzinfo=tz)

dt1 = parse_datetime(input())
dt2 = parse_datetime(input())
dt1_utc = dt1.astimezone(timezone.utc)
dt2_utc = dt2.astimezone(timezone.utc)

delta_seconds = abs((dt1_utc - dt2_utc).total_seconds())
full_days = int(delta_seconds // 86400)

print(full_days)