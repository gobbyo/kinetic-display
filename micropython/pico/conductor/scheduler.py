import gc

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

# Make scheduleInfo more memory efficient using slots
class scheduleInfo:
    __slots__ = ('hour', 'minute', 'second', 'elapse', 'event')
    
    def __init__(self, hour, minute, second, elapse, event):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.elapse = elapse
        self.event = event

class ScheduleLoader:
    @staticmethod
    def load_schedule_simple(filename):
        """Simple, reliable method for loading schedules"""
        import ujson
        import uio
        
        schedule_items = []
        try:
            with uio.open(filename, 'r') as f:
                data = ujson.load(f)
                
                if "scheduledEvent" in data:
                    for event in data["scheduledEvent"]:
                        schedule_items.append(
                            scheduleInfo(
                                event.get("hour", -1),
                                event.get("minute", -1),
                                event.get("second", 0),
                                event.get("elapse", 1),
                                event.get("event", 0)
                            )
                        )
                        # Force garbage collection after each item
                        gc.collect()
            
            print(f"Simple loader: loaded {len(schedule_items)} events")
        except Exception as e:
            print(f"Error in load_schedule_simple: {e}")
            
        return schedule_items
    
    @staticmethod
    def load_schedule_stream(filename):
        """Stream-based JSON parser that processes one object at a time"""
        import uio
        
        schedule_items = []
        try:
            # We'll manually parse the JSON file character by character
            # This avoids loading the entire file into memory at once
            with uio.open(filename, 'r') as f:
                content = ""
                in_scheduled_events = False
                current_object = ""
                brace_count = 0
                
                # Read char by char
                while True:
                    char = f.read(1)
                    if not char:  # End of file
                        break
                    
                    content += char
                    
                    # Look for the scheduledEvent array start
                    if not in_scheduled_events and '"scheduledEvent":' in content:
                        in_scheduled_events = True
                        content = ""  # Clear buffer
                        # Skip to opening bracket of array
                        while True:
                            char = f.read(1)
                            if not char:
                                break
                            if char == '[':
                                break
                        continue
                    
                    # Once we're in the scheduled events array
                    if in_scheduled_events:
                        if char == '{':
                            brace_count += 1
                            if brace_count == 1:
                                current_object = "{"  # Start new object
                            else:
                                current_object += char
                        elif char == '}':
                            brace_count -= 1
                            current_object += char
                            
                            # If we've closed the object, process it
                            if brace_count == 0:
                                try:
                                    # Parse the object's properties
                                    hour = -1
                                    minute = -1
                                    second = 0
                                    elapse = 1
                                    event = 0
                                    
                                    # Simple property extraction with basic parsing
                                    if '"hour":' in current_object:
                                        hour_pos = current_object.find('"hour":') + 7
                                        hour_end = current_object.find(',', hour_pos)
                                        if hour_end == -1:
                                            hour_end = current_object.find('}', hour_pos)
                                        hour = int(current_object[hour_pos:hour_end].strip())
                                    
                                    if '"minute":' in current_object:
                                        minute_pos = current_object.find('"minute":') + 9
                                        minute_end = current_object.find(',', minute_pos)
                                        if minute_end == -1:
                                            minute_end = current_object.find('}', minute_pos)
                                        minute = int(current_object[minute_pos:minute_end].strip())
                                    
                                    if '"second":' in current_object:
                                        second_pos = current_object.find('"second":') + 9
                                        second_end = current_object.find(',', second_pos)
                                        if second_end == -1:
                                            second_end = current_object.find('}', second_pos)
                                        second = int(current_object[second_pos:second_end].strip())
                                    
                                    if '"elapse":' in current_object:
                                        elapse_pos = current_object.find('"elapse":') + 9
                                        elapse_end = current_object.find(',', elapse_pos)
                                        if elapse_end == -1:
                                            elapse_end = current_object.find('}', elapse_pos)
                                        elapse = int(current_object[elapse_pos:elapse_end].strip())
                                    
                                    if '"event":' in current_object:
                                        event_pos = current_object.find('"event":') + 8
                                        event_end = current_object.find(',', event_pos)
                                        if event_end == -1:
                                            event_end = current_object.find('}', event_pos)
                                        event = int(current_object[event_pos:event_end].strip())
                                    
                                    schedule_items.append(
                                        scheduleInfo(hour, minute, second, elapse, event)
                                    )
                                    
                                except Exception as e:
                                    print(f"Error parsing event: {e}")
                                
                                current_object = ""
                                gc.collect()  # Force garbage collection
                        else:
                            # Add to current object if we're inside one
                            if brace_count > 0:
                                current_object += char
                        
                        # Check if we've reached the end of the array
                        if char == ']' and brace_count == 0:
                            break
                
                print(f"Stream loader: loaded {len(schedule_items)} events")
        except Exception as e:
            print(f"Error in load_schedule_stream: {e}")
        
        return schedule_items
    
    @staticmethod
    def load_schedule_optimized(filename):
        """Optimized schedule loader that tries to minimize memory usage"""
        import uio
        
        schedule_items = []
        try:
            # We'll create a chunked reader to avoid loading the whole file
            CHUNK_SIZE = 256  # Small enough for memory constraints
            
            with uio.open(filename, 'r') as f:
                # Find the start of the scheduledEvent array without loading whole file
                while True:
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        break
                        
                    if '"scheduledEvent":' in chunk:
                        # Found the array, now reset and skip to it
                        f.seek(0)
                        break
                
                # Find and skip to the array
                array_start_found = False
                while not array_start_found:
                    line = f.readline()
                    if not line:
                        break
                        
                    if '"scheduledEvent":' in line:
                        # Skip to the opening bracket
                        while True:
                            char = f.read(1)
                            if not char:
                                break
                            if char == '[':
                                array_start_found = True
                                break
                        break
                
                # Now read objects one by one
                if array_start_found:
                    inside_object = False
                    brace_level = 0
                    current_event = {}
                    current_key = None
                    current_value = ""
                    in_quotes = False
                    in_key = False
                    
                    while True:
                        char = f.read(1)
                        if not char:
                            break
                            
                        # Handle quotes (for keys and string values)
                        if char == '"' and f.read(-1) != '\\':  # Not escaped quotes
                            in_quotes = not in_quotes
                            if inside_object:
                                if not in_key and not in_quotes:
                                    # End of key
                                    in_key = False
                                    current_key = current_value.strip('"')
                                    current_value = ""
                                continue
                        
                        # Handle object boundaries
                        if char == '{' and not in_quotes:
                            inside_object = True
                            brace_level += 1
                            current_event = {"hour": -1, "minute": -1, "second": 0, "elapse": 1, "event": 0}
                            continue
                            
                        if char == '}' and not in_quotes:
                            brace_level -= 1
                            if brace_level == 0:
                                # End of object, create the schedule item
                                try:
                                    schedule_items.append(
                                        scheduleInfo(
                                            current_event["hour"],
                                            current_event["minute"],
                                            current_event["second"],
                                            current_event["elapse"],
                                            current_event["event"]
                                        )
                                    )
                                except Exception as e:
                                    print(f"Error creating schedule item: {e}")
                                    
                                inside_object = False
                                current_event = {}
                                gc.collect()
                            continue
                        
                        # Handle property key-value pairs
                        if inside_object:
                            if char == ':' and not in_quotes:
                                in_key = False
                                in_value = True
                                continue
                            
                            if char == ',' and not in_quotes:
                                # End of value, process it
                                try:
                                    if current_key in ["hour", "minute", "second", "elapse", "event"]:
                                        current_event[current_key] = int(current_value.strip())
                                except:
                                    pass
                                    
                                current_key = None
                                current_value = ""
                                in_value = False
                                continue
                            
                            # Collecting key or value characters
                            if in_quotes or (char not in [' ', '\n', '\r', '\t']):
                                current_value += char
                        
                        # End of array
                        if char == ']' and not in_quotes and not inside_object:
                            break
            
            print(f"Optimized loader: loaded {len(schedule_items)} events")
        except Exception as e:
            print(f"Error in load_schedule_optimized: {e}")
            
        return schedule_items