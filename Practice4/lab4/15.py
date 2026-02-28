import sys
from datetime import datetime
SECONDS_PER_DAY = 86400
def is_leap(y: int) -> bool:
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)
def parse_line(line: str):
    line = line.strip()
    if not line:
        return None
    date_part, tz_part = line.split()
    y, m, d = map(int, date_part.split('-'))
    sign = 1 if tz_part[3] == '+' else -1
    hh, mm = map(int, tz_part[4:].split(':'))
    offset_seconds = sign * (hh * 3600 + mm * 60)
    return y, m, d, offset_seconds
def birthday_date_for_year(year: int, bm: int, bd: int):
    if bm == 2 and bd == 29 and not is_leap(year):
        return 2, 28
    return bm, bd
def moment_utc(year: int, month: int, day: int, offset_seconds: int) -> datetime:
    return datetime(year, month, day, 0, 0, 0) - timedelta(seconds=offset_seconds)
from datetime import timedelta
data = [line.rstrip('\n') for line in sys.stdin if line.strip() != ""]
birth = parse_line(data[0])
curr = parse_line(data[1])

yb, bm, bd, off_b = birth
yc, cm, cd, off_c = curr

current_utc = datetime(yc, cm, cd, 0, 0, 0) - timedelta(seconds=off_c)

candidates = []
for Y in (yc, yc + 1):
    m2, d2 = birthday_date_for_year(Y, bm, bd)
    bday_utc = datetime(Y, m2, d2, 0, 0, 0) - timedelta(seconds=off_b)
    candidates.append(bday_utc)

next_bday_utc = min(dt for dt in candidates if dt >= current_utc)

diff_seconds = int((next_bday_utc - current_utc).total_seconds())
if diff_seconds <= 0:
    print(0)
else:
    print((diff_seconds + SECONDS_PER_DAY - 1) // SECONDS_PER_DAY)