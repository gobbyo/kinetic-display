import io
import json
from scheduler import scheduleInfo, eventActions
from machine import RTC
import time

def checkForScheduledAction(rtc,s):
    #[year, month, day, weekday, hours, minutes, seconds, subseconds]
    dt = rtc.datetime()

    if s.event == eventActions.hybernate:
        if dt[4] == s.hour and dt[5] == s.minute:
            print(f"h={s.hour}, m={s.minute}, s={s.second}, e={s.event}")
            return eventActions.hybernate

    if s.event < eventActions.hybernate:
        if (s.hour == -1 and dt[5] == (s.minute)) or (s.hour == -1 and s.minute == -1):
            if dt[6] >= s.second and dt[6] < (s.second + s.elapse):
                print(f"h={s.hour}, m={s.minute}, s={s.second}, e={s.event}")
                return s.event
                
    return 0

def main():
    schedule = []
    rtc = RTC()

    try:
        scheduleConf = io.open("schedule_2.json")
        s = json.load(scheduleConf)
        for i in s["scheduledEvent"]:
            print("--record--")
            schedule.append(scheduleInfo(i["hour"],i["minute"],i["second"],i["elapse"],i["event"]))
    except ValueError as ve:
        print("Schedule loading value error: {0}".format(ve))
    except OSError as ioe:
        print("Schedule loading IO error: {0}".format(ioe))
    finally:
        scheduleConf.close()

    print(f"schedule length={len(schedule)}")
    while(True):
        print(f"datetime={rtc.datetime()}")
        for s in schedule:
            event = checkForScheduledAction(rtc, s)
            if event != 0:
                print("event={0}".format(event))
        time.sleep(1)

if __name__ == "__main__":
    main()