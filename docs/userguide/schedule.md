# User Guide - Schedule Creation and Management

The Kinetic Display includes a powerful scheduling system that controls what information is shown on your display and when it appears. This guide will help you understand how to create, customize, and manage your display schedules.

!!! tip "Key Points"
    - Scheduling is managed by the Conductor (Raspberry Pi Pico W 2040)
    - Custom schedules are created as JSON files
    - Add or remove schedules through the display's [web service settings](websettings.md)
    - Multiple schedules allow for different display behaviors for various situations

## How Scheduling Works

The scheduling system operates on three key concepts:

| Concept | Description |
|---------|-------------|
| **Schedules** | Collections of timed events that determine the display behavior |
| **Event actions** | Specific display functions (showing time, date, temperature, etc.) |
| **Time triggers** | When each event should activate (using precise times or wildcards) |

By combining these elements, you can create dynamic display routines tailored to your needs.

## Core Components

### 1. Schedule Files

Each display can store multiple schedule configurations:

- **`schedule_0.json`**, **`schedule_1.json`**, **`schedule_2.json`**, etc.
- Each schedule file is a JSON document containing a list of `scheduledEvent` objects
- Multiple schedules allow you to save different display configurations for various situations

#### Schedule File Structure

A complete schedule JSON file has the following structure:

```json
{
  "title": "Schedule Name",              // Name shown in settings dropdown
  "scheduleDescription": "Description",  // Brief explanation of this schedule
  "scheduledEvent": [
    // Array of scheduled events (detailed below)
  ]
}
```

#### Event Structure

Each event defines **when** to trigger and **what** action to perform:

```json
{
  "hour": -1,    // Every hour (wildcard)
  "minute": 0,   // When minute is 0 (top of each hour)
  "second": 20,  // When second is 20
  "elapse": 9,   // Run for 9 seconds
  "event": 2     // Show the date (action #2)
}
```

#### Event Fields Explained

| Field | Purpose | Example Values |
|-------|---------|----------------|
| `hour` | Hour to trigger (0-23, or -1 for every hour) | `8`, `13`, `-1` |
| `minute` | Minute to trigger (0-59, or -1 for every minute) | `30`, `45`, `-1` |
| `second` | Second to trigger (0-59) | `0`, `15` |
| `elapse` | Duration in seconds | `5`, `10`, `30` |
| `event` | Action ID (see Event Actions table) | `1`, `2`, `9` |

### 2. The Scheduler System

The scheduling system uses these components to control your display:

- The `ScheduleLoader` class (`scheduler.py`) loads schedule files and creates a list of `scheduleInfo` objects
- The main loop (`uart_command.py`) continuously checks if the current time matches any scheduled events
- When a match occurs, the corresponding action is triggered for the specified duration

### 3. Time Matching Patterns

Using `-1` as a wildcard in time fields creates flexible scheduling patterns:

#### Every Hour

Set `hour: -1` to run at the same minute/second each hour

```json
{ "hour": -1, "minute": 30, "second": 0, ... }  // Runs at 30 minutes past every hour
```

#### Every Minute

Set `minute: -1` to run at the same second each minute

```json
{ "hour": -1, "minute": -1, "second": 0, ... }  // Runs at the start of every minute
```

#### Specific Time

Set exact values to run at a specific time each day

```json
{ "hour": 8, "minute": 0, "second": 0, ... }  // Runs at 8:00:00 AM
```

---

## Event Actions Reference

The `eventActions` class in `scheduler.py` defines all possible actions the display can perform:

| Value | Name | Description |
|-------|------|-------------|
| 0 | nothing | Do nothing |
| 1 | displayTime | Show the current time |
| 2 | displayDate | Show the current date |
| 3 | displayIndoorTemp | Show indoor temperature |
| 4 | displayIndoorHumidity | Show indoor humidity |
| 5 | displayOutdoorTemp | Show outdoor temperature |
| 6 | displayOutdoorHumidity | Show outdoor humidity |
| 7 | updateOutdoorTempHumid | Update external temp/humidity sensor |
| 9 | hybernate | Enter hibernation mode |

You use the `event` field in each scheduled event to specify which action to perform.

---

## Building Your Schedule

### Step 1: Plan Your Display Routine

!!! question "Consider These Questions"
    - What information is most important at different times of day?
    - How long should each piece of information display?
    - Are there times when the display should turn off (hibernate)?
    - What pattern will make the information most useful to viewers?

### Step 2: Create Your Schedule File

Each schedule file contains an array of events. Start with this basic structure:

```json
{
  "title": "My Custom Schedule",
  "scheduleDescription": "Brief description of what this schedule does",
  "scheduledEvent": [
    { /* event 1 */ },
    { /* event 2 */ },
    // more events...
  ]
}
```

### Step 3: Add Specific Events

For each action you want to schedule, add an event object to the `scheduledEvent` array:

#### Example: Show Time Every Minute

This event displays the current time for 10 seconds at the start of every minute:

```json
{
  "hour": -1,     // Every hour
  "minute": -1,   // Every minute
  "second": 0,    // When second is 0
  "elapse": 10,   // Run for 10 seconds
  "event": 1      // Display time (action #1)
}
```

#### Example: Show Date at Regular Intervals

These events display the date for 25 seconds every 5 minutes:

```json
{
  "hour": -1,     // Every hour
  "minute": 0,    // When minute is 0
  "second": 15,   // When second is 15
  "elapse": 25,   // Run for 25 seconds
  "event": 2      // Display date (action #2)
},
{
  "hour": -1,     // Every hour
  "minute": 5,    // When minute is 5
  "second": 15,   // When second is 15
  "elapse": 25,   // Run for 25 seconds
  "event": 2      // Display date (action #2)
}
```

#### Example: Enter Hibernation at Night

This event puts the display into hibernation mode at 10:00 PM for 8 minutes:

```json
{
  "hour": 22,     // At 10:00 PM
  "minute": 0,    // At minute 0
  "second": 0,    // At second 0
  "elapse": 480,  // Run for 480 minutes (8 hours)
  "event": 9      // Enter hibernation (action #9)
}
```

## Real-World Example: schedule_0.json

The `schedule_0.json` file is an "All Features" schedule that demonstrates how to use all display capabilities:

!!! example "schedule_0.json Structure"
    ```json
    {
      "title": "All Features",
      "scheduleDescription": "Time, date, month, internal and external temp and humid",
      "scheduledEvent": [
        {
          "hour": -1, "minute": -1, "second": 0, "elapse": 10, "event": 1
        },
        {
          "hour": -1, "minute": -1, "second": 45, "elapse": 10, "event": 1
        },
        {
          "hour": -1, "minute": 0, "second": 20, "elapse": 9, "event": 2
        },
        {
          "hour": -1, "minute": 10, "second": 20, "elapse": 9, "event": 2
        },
        {
          "hour": -1, "minute": 2, "second": 20, "elapse": 9, "event": 3
        },
        {
          "hour": -1, "minute": 24, "second": 20, "elapse": 9, "event": 3
        },
        {
          "hour": -1, "minute": 2, "second": 30, "elapse": 9, "event": 4
        },
        {
          "hour": -1, "minute": 24, "second": 30, "elapse": 9, "event": 4
        },
        {
          "hour": -1, "minute": 5, "second": 20, "elapse": 9, "event": 5
        },
        {
          "hour": -1, "minute": 25, "second": 20, "elapse": 9, "event": 5
        },
        {
          "hour": -1, "minute": 5, "second": 30, "elapse": 9, "event": 6
        },
        {
          "hour": -1, "minute": 25, "second": 30, "elapse": 9, "event": 6
        },
        {
          "hour": 22, "minute": 0, "second": 0, "elapse": 480, "event": 9
        }
      ]
    }
    ```

### Understanding the Schedule Pattern

This schedule creates a predictable pattern with:

1. **Time Displays**
   - At second 0 of every minute: Show time for 10 seconds
   - At second 45 of every minute: Show time for 10 seconds

2. **Date Displays**
   - At second 20 of minutes 0, 10, 20, 30, 40, and 50: Show date for 9 seconds

3. **Indoor Conditions**
   - At minute 2 and 24 of each hour, second 20: Show indoor temperature for 9 seconds
   - At minute 2 and 24 of each hour, second 30: Show indoor humidity for 9 seconds

4. **Outdoor Conditions**
   - At minute 5 and 25 of each hour, second 20: Show outdoor temperature for 9 seconds
   - At minute 5 and 25 of each hour, second 30: Show outdoor humidity for 9 seconds

5. **Hibernation**
   - At 10:00 PM (hour 22): Enter hibernation mode for 8 hours (480 minutes)

### Tips for Effective Schedules

- **Avoid overlapping events**: If multiple events match the same time, only one will run
- **Mind the timing**: Ensure your `elapse` times don't create unwanted overlaps. Gaps are OK and will only cause a pause in the display when powering up.
- **Use hibernation**: To save power, schedule hibernation during overnight hours
- **Balance information**: Rotate between different types of information for the best user experience
- **Consider patterns**: Create predictable patterns so users can anticipate when specific information will be displayed

---

## Managing Schedules Through the Web Interface

Once you've created a custom schedule JSON file, you can add it to your Kinetic Display using the web interface.

### Adding a New Schedule

1. Connect to your Kinetic Display's web interface as described in the [Web Settings](websettings.md) guide
2. On the settings page, click the **Add Schedule** button
3. In the dialog that appears:
   - Upload your JSON file using the file selector
   - The system will add it to the available schedules

   ![settings-1](../img/user-guide-settings/settings-1.webp)

### Selecting a Schedule

1. From the Schedule dropdown menu, select your preferred schedule
2. Click **Save** to apply the changes
3. Follow the prompted steps to restart the display

### Deleting a Schedule

If you no longer need a particular schedule:

1. Select the schedule from the dropdown menu
2. Click the **Delete Schedule** button
3. Confirm the deletion when prompted
4. Click **Save** to apply the changes

!!! note
    The system includes several pre-installed schedules that provide good starting points and fallback options.

### Tips for Schedule Management

- **Create multiple schedules** for different situations
- **Back up your custom schedules** before making significant changes
- **Test new schedules** thoroughly to ensure they work as expected
- **Start with a copy** of an existing schedule as a template for your custom schedules
