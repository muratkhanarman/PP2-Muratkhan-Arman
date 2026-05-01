from datetime import datetime, date, timedelta
now = datetime.now()
print("Current datetime:", now)
my_date = date(2025, 6, 1)
print("Specific date:", my_date)
today = date.today()
difference = my_date - today
print("Days until 2025-06-01:", difference.days)
formatted = now.strftime("%Y-%m-%d %H:%M")
print("Formatted:", formatted)
parsed = datetime.strptime("2025-12-31", "%Y-%m-%d")
print("Parsed date:", parsed)