
def formatHour(hour, display12hour):
    if display12hour:
        if hour > 12:
            hour -= 12
        if hour == 0:
            hour = 12
        
    return "{0:02}".format(hour)