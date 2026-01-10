from machine import RTC
import ntptime
import time

try:
    from dst_rules import get_dst_rule, get_offset
except ImportError:
    # Fallback if dst_rules not available
    def get_dst_rule(tz): return None
    def get_offset(tz, is_dst): return 0

# Default values
AUTO_TIMEZONE = "auto"

# Default time tuple values
DEFAULT_YEAR = 1970
DEFAULT_MONTH = 1
DEFAULT_DAY = 1
DEFAULT_WEEKDAY = 0
DEFAULT_HOUR = 0
DEFAULT_MINUTE = 0
DEFAULT_SECOND = 0
DEFAULT_SUBSECONDS = 0

# Config key constants
CONFIG_TIMEZONE_KEY = "timeZone"

# This class is used to sync the RTC using NTP
# and manage timezone configuration from a config file
class syncRTC:

    def __init__(self, config=None): # Initialize the Config object, not the file name
        self.config = config
        self.timeZone = None
        if self.config:
            try:
                self.timeZone = self.config.read(CONFIG_TIMEZONE_KEY)
            except:
                self.timeZone = None
    
    def syncclock(self, rtc, max_retries=3, ntp_host="pool.ntp.org"):
        print("Sync clock using NTP")
        returnval = False

        try:
            # Set a default date/time
            rtc.datetime((DEFAULT_YEAR, DEFAULT_MONTH, DEFAULT_DAY, 
                         DEFAULT_WEEKDAY, DEFAULT_HOUR, DEFAULT_MINUTE, 
                         DEFAULT_SECOND, DEFAULT_SUBSECONDS))
            print("RTC set to default date/time")
            
            # Use NTP for time sync with retry logic
            print(f"Using NTP server: {ntp_host}")
            ntptime.host = ntp_host
            
            for attempt in range(1, max_retries + 1):
                try:
                    print(f"NTP sync attempt {attempt} of {max_retries}")
                    ntptime.settime()  # Sets RTC to UTC
                    print("NTP sync successful (UTC)")
                    
                    # Convert UTC to local time with timezone and DST
                    if self.timeZone:
                        print(f"Applying timezone: {self.timeZone}")
                        utc_time = rtc.datetime()
                        year, month, day, weekday, hour, minute, second, subsecond = utc_time
                        
                        # Determine if DST is active
                        is_dst = self._is_dst_active(year, month, day, hour, weekday)
                        dst_status = "DST active" if is_dst else "Standard time"
                        print(f"DST check: {dst_status}")
                        
                        # Get timezone offset
                        offset_hours = get_offset(self.timeZone, is_dst)
                        if offset_hours is not None:
                            print(f"UTC offset: {offset_hours:+.1f} hours")
                            
                            # Calculate local time
                            utc_seconds = time.mktime((year, month, day, hour, minute, second, 0, 0))
                            local_seconds = utc_seconds + int(offset_hours * 3600)
                            local_tuple = time.localtime(local_seconds)
                            
                            # Set RTC to local time
                            # Convert to RTC format: (year, month, day, weekday, hour, minute, second, subsecond)
                            local_rtc_time = (local_tuple[0], local_tuple[1], local_tuple[2], 
                                            local_tuple[6], local_tuple[3], local_tuple[4], 
                                            local_tuple[5], subsecond)
                            rtc.datetime(local_rtc_time)
                            print(f"RTC set to local time: {local_tuple[0]}-{local_tuple[1]:02d}-{local_tuple[2]:02d} {local_tuple[3]:02d}:{local_tuple[4]:02d}:{local_tuple[5]:02d}")
                        else:
                            print(f"Warning: Unknown timezone '{self.timeZone}', RTC remains in UTC")
                    else:
                        print("No timezone configured, RTC set to UTC")
                    
                    returnval = True
                    break
                    
                except Exception as retry_exc:
                    print(f"Attempt {attempt} failed: {retry_exc}")
                    if attempt < max_retries:
                        time.sleep(2)
                    else:
                        raise
            
        except Exception as e:
            print(f"NTP sync exception: {e}")
            returnval = False

        return returnval

    def refresh_timezone(self):
        """Reload the timeZone from the config file."""
        if self.config:
            try:
                self.timeZone = self.config.read(CONFIG_TIMEZONE_KEY)
            except:
                self.timeZone = None
    
    def _is_dst_active(self, year, month, day, hour, weekday):
        """Determine if DST is active for the configured timezone on a given date."""
        if not self.timeZone:
            return False
        
        dst_rule = get_dst_rule(self.timeZone)
        if not dst_rule or not dst_rule.get("observes_dst"):
            return False
        
        start_month = dst_rule["start_month"]
        end_month = dst_rule["end_month"]
        
        # Northern hemisphere (DST in spring/summer)
        if start_month < end_month:
            if month < start_month or month > end_month:
                return False
            if month > start_month and month < end_month:
                return True
            # Check specific transition dates
            if month == start_month:
                transition_day = self._get_transition_day(year, start_month, 
                    dst_rule["start_week"], dst_rule["start_day"])
                if day < transition_day:
                    return False
                if day == transition_day and hour < dst_rule["start_hour"]:
                    return False
                return True
            if month == end_month:
                transition_day = self._get_transition_day(year, end_month, 
                    dst_rule["end_week"], dst_rule["end_day"])
                if day > transition_day:
                    return False
                if day == transition_day and hour >= dst_rule["end_hour"]:
                    return False
                return True
        
        # Southern hemisphere (DST in winter: Oct-Apr)
        else:
            if month > end_month and month < start_month:
                return False
            if month < end_month or month > start_month:
                return True
            # Check specific transition dates
            if month == start_month:
                transition_day = self._get_transition_day(year, start_month, 
                    dst_rule["start_week"], dst_rule["start_day"])
                if day < transition_day:
                    return False
                if day == transition_day and hour < dst_rule["start_hour"]:
                    return False
                return True
            if month == end_month:
                transition_day = self._get_transition_day(year, end_month, 
                    dst_rule["end_week"], dst_rule["end_day"])
                if day > transition_day:
                    return False
                if day == transition_day and hour >= dst_rule["end_hour"]:
                    return False
                return True
        
        return False
    
    def _get_transition_day(self, year, month, week, target_weekday):
        """Calculate the day of month for DST transition.
        
        Args:
            year: Year
            month: Month (1-12)
            week: Week of month (1-5, or -1 for last)
            target_weekday: Target day of week (0=Monday, 6=Sunday)
        
        Returns:
            Day of month for the transition
        """
        # Find first day of month's weekday
        # Using a simple algorithm since MicroPython may not have full datetime
        import time
        
        # Get the first day of the month
        first_day = time.localtime(time.mktime((year, month, 1, 0, 0, 0, 0, 0)))
        first_weekday = (first_day[6] + 1) % 7  # Convert Monday=0 to Sunday=0
        
        if week == -1:  # Last occurrence
            # Find days in month
            if month == 12:
                next_month = (year + 1, 1, 1, 0, 0, 0, 0, 0)
            else:
                next_month = (year, month + 1, 1, 0, 0, 0, 0, 0)
            
            days_in_month = time.localtime(
                time.mktime(next_month) - 86400
            )[2]
            
            # Start from last day and work backwards
            for day in range(days_in_month, 0, -1):
                day_tuple = time.localtime(time.mktime((year, month, day, 0, 0, 0, 0, 0)))
                if (day_tuple[6] + 1) % 7 == target_weekday:
                    return day
        else:
            # Find the nth occurrence
            # Calculate offset from first day
            if target_weekday >= first_weekday:
                offset = target_weekday - first_weekday
            else:
                offset = 7 - first_weekday + target_weekday
            
            # Add weeks
            return 1 + offset + (week - 1) * 7
        
        return 1  # Fallback
    
    def get_local_time(self, rtc):
        """Get local time with timezone and DST adjustment.
        
        Args:
            rtc: RTC object with UTC time
        
        Returns:
            Tuple: (year, month, day, weekday, hour, minute, second, subsecond)
        """
        # Get current UTC time from RTC
        utc_time = rtc.datetime()
        year, month, day, weekday, hour, minute, second, subsecond = utc_time
        
        if not self.timeZone:
            print("No timezone configured, returning UTC")
            return utc_time
        
        # Check if DST is active
        is_dst = self._is_dst_active(year, month, day, hour, weekday)
        
        # Get timezone offset
        offset_hours = get_offset(self.timeZone, is_dst)
        if offset_hours is None:
            print(f"Unknown timezone: {self.timeZone}, returning UTC")
            return utc_time
        
        # Apply offset
        import time
        utc_seconds = time.mktime((year, month, day, hour, minute, second, 0, 0))
        local_seconds = utc_seconds + (offset_hours * 3600)
        local_tuple = time.localtime(local_seconds)
        
        # Convert back to RTC format: (year, month, day, weekday, hour, minute, second, subsecond)
        return (local_tuple[0], local_tuple[1], local_tuple[2], 
                local_tuple[6], local_tuple[3], local_tuple[4], 
                local_tuple[5], subsecond)
    
    def get_local_time_str(self, rtc):
        """Get local time as formatted string.
        
        Args:
            rtc: RTC object with UTC time
        
        Returns:
            String: Formatted local time
        """
        local = self.get_local_time(rtc)
        year, month, day, weekday, hour, minute, second, _ = local
        
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        tz_str = self.timeZone if self.timeZone else "UTC"
        
        return f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d} {weekdays[weekday]} [{tz_str}]"
