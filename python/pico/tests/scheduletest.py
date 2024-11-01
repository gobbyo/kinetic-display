import io
import json
import scheduler
from machine import RTC
import time

def checkForScheduledAction(rtc,s):
    #print("checkForScheduledAction for event={0}".format(s.event))
    #[year, month, day, weekday, hours, minutes, seconds, subseconds]
    
    dt = rtc.datetime()

    if s.event == scheduler.eventActions.hybernate:
        if dt[4] == s.hour and dt[5] == s.minute:
            print(f"h={s.hour}, m={s.minute}, s={s.second}, e={s.event}")
            return scheduler.eventActions.hybernate
    
    if s.event >= scheduler.eventActions.displayTime or s.event <= scheduler.eventActions.updateOutdoorTempHumid:
        if s.hour == -1 and dt[5] == (s.minute):
            if dt[6] == s.second:
                print(f"h={s.hour}, m={s.minute}, s={s.second}, e={s.event}")
                return s.event
    
    return 0

def main():
    schedule = []
    rtc = RTC()

    try:
        scheduleConf = io.open("schedule_0.json")
        s = json.load(scheduleConf)
        for i in s["scheduledEvent"]:
            print("--record--")
            schedule.append(scheduler.scheduleInfo(i["hour"],i["minute"],i["second"],i["elapse"],i["event"]))
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