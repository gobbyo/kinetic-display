# User Guide – On/Off Switch

The Kinetic Display features a physical SPDT (Single Pole Double Throw) switch on the back of the unit. This switch lets you easily change between configuration mode and normal operation, and also helps save power.

![Switch Position Diagram](../img/user-guide-settings/settings-3.webp)

---

## What Does the Switch Do?

The On/Off switch has two main functions:

1. **Operating Mode Selection**
2. **Power Management**

### 1. Operating Mode Selection

The switch determines how your display behaves depending on its position and when you plug in the power:

| Power State                | Switch Position | Mode            | What Happens                                                        |
|---------------------------|-----------------|-----------------|---------------------------------------------------------------------|
| Plug in with switch **ON** | ON              | Normal          | Display runs your schedule, shows time, date, temp, etc.            |
| Plug in with switch **OFF**| OFF             | Configuration   | Display creates a WiFi hotspot for settings changes                 |
| Already plugged in, set to OFF | OFF         | Low Power       | Digits turn off, controller stays on (saves power)                  |

### 2. Power Management

The switch controls a relay that turn off the digits when they're not needed, reducing energy use and wear.

---

## How Each Switch Position Works

### OFF Position

**When you set the switch to OFF and plug in the display:**

- The display creates a WiFi access point named `kinetic-display` (password: `12oclock`)
- You can connect to this network and visit [http://192.168.4.1](http://192.168.4.1) to change settings, WiFi, or schedules

**When you set the switch to OFF while the display is already running:**

- The display enters a low-power state
- All digit segments retract and turn off
- The controller stays on, but non-essential components are powered down

### ON Position

**When you set the switch to ON after saving settings:**

- The display connects to your home WiFi
- Time is synchronized automatically
- The display follows your selected schedule, showing time, date, temperature, and more
- All sensors and features are active (indoor/outdoor temp, humidity, light sensor, etc.)

---

## Scheduled Hibernation (Automatic Power Saving)

You can also schedule the display to hibernate automatically, even if the switch is ON. Just add an event with `event: 9` to your schedule. When this event triggers, the display will enter low-power mode for the specified time.

**Example schedule entry:**

```json
{
  "hour": 22,    // At 10:00 PM
  "minute": 0,
  "second": 0,
  "elapse": 480, // Hibernate for 8 minutes
  "event": 9     // Hibernate mode
}
```

---

## Why Use the On/Off Switch?

- **Save Energy:** Reduce power use when the display isn’t needed
- **Extend Component Life:** Less wear on moving parts
- **Easy Setup:** Quickly switch to configuration mode for WiFi or schedule changes
- **Flexible:** Use both manual (switch) and automatic (scheduled) hibernation

!!! tip "Power Saving"
    For best energy savings, use the OFF position when you don’t need the display for a while, or set up scheduled hibernation for overnight hours.
