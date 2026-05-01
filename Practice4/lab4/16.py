from datetime import datetime, timedelta, timezone
import re

def parse_datetime(line):
    dt_str, tz_str = line.rsplit(' ', 1)
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    match = re.match(r'UTC([+-])(\d+):(\d+)', tz_str)
    sign, hours, minutes = match.groups()
    offset_minutes = int(hours) * 60 + int(minutes)
    if sign == '-':
        offset_minutes = -offset_minutes
    tz = timezone(timedelta(minutes=offset_minutes))
    return dt.replace(tzinfo=tz)

start = parse_datetime(input())
end = parse_datetime(input())

duration_seconds = int((end.astimezone(timezone.utc) - start.astimezone(timezone.utc)).total_seconds())
print(duration_seconds)