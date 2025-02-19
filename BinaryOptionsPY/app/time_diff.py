from datetime import datetime, time 

def time_diff(dt2):
    now = datetime.now()
    timedelta = now - dt2
    return timedelta.days * 24 * 3600 + timedelta.seconds