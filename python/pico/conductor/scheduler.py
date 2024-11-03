class eventActions():
    nothing = 0
    displayTime = 1
    displayDate = 2
    displayIndoorTemp = 3
    displayIndoorHumidity = 4
    displayOutdoorTemp = 5
    displayOutdoorHumidity = 6
    updateOutdoorTempHumid = 7
    hybernate = 9

class scheduleInfo:
    """
    A class to represent a schedule information.
    Attributes:
    -----------
    hour : int
        The hour of the schedule (0-23).
    minute : int
        The minute of the schedule (0-59).
    second : int
        The second of the schedule (0-59).
    elapse : int
        The elapsed time in seconds.
    event : int
        The event type (0-5).
    Methods:
    --------
    __init__(h=0, m=0, s=0, e=0, ev=0):
        Initializes the scheduleInfo with given hour, minute, second, elapse, and event.
    """
    def __init__(self, h=0, m=0, s=0, e=0, ev=0):
        self.hour = h
        self.minute = m
        self.second = s
        self.elapse = e
        self.event = ev

    @property
    def hour(self):
        return self._hour
    
    @hour.setter
    def hour(self, value):
        print(f"hour={value}")
        if value < -1 or value >= 24:
            raise ValueError("hour must be between -1 and 23")
        self._hour = value
    
    @property
    def minute(self):
        return self._minute
    
    @minute.setter
    def minute(self, value):
        print(f"minute={value}")
        if value < -1 or value >= 60:
            raise ValueError("minute must be between -1 and 59")
        self._minute = value
    
    @property
    def second(self):
        return self._second
    
    @second.setter
    def second(self, value):
        print(f"second={value}")
        if value < 0 or value >= 60:
            raise ValueError("second must be between 0 and 59")
        self._second = value

    @property
    def elapse(self):
        return self._elapse
    
    @elapse.setter
    def elapse(self, value):
        print(f"elapse={value}")
        if value < 0:
            raise ValueError("elapse must be greater than or equal to 0")
        self._elapse = value
    
    @property
    def event(self):
        return self._event
    
    @event.setter
    def event(self, value):
        print(f"event={value}")
        if value < eventActions.nothing or value > eventActions.hybernate:
            raise ValueError("event must be between 0 and 5")
        self._event = value