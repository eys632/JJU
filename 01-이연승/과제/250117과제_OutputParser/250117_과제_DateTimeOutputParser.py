import datetime

# Define a function to parse the date and time from strings
def parse_datetime(date_string, time_string):
    try:
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        time = datetime.datetime.strptime(time_string, "%H:%M:%S").time()
        return datetime.datetime.combine(date, time)
    except ValueError as e:
        print(f"Error parsing date/time: {e}")
        return None
