import datetime
import time

def get_current_datetime():
    return datetime.datetime.now()

def get_current_string_time():
    return get_current_datetime().strftime("%H:%M %m/%d/%y")

def get_current_epoch():
    return time.time()

def get_average_time(list_of_time_taken):
    if len(list_of_time_taken) > 0:
        return sum(list_of_time_taken) / len(list_of_time_taken)
    return -1
