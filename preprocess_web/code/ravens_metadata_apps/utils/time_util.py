"""basic functions for time"""
try:
    from django.utils import timezone as dt
except:
    from datetime import datetime as dt

def get_current_timestring():
    """Return a time string to use as part of a file name"""
    return dt.now().strftime('%Y-%m-%d_%H-%M-%S')
