# Web Service and Settings

## Connect your Mobile device or Computer to the **kinetic-display** Wifi Access Point (AP)

![Connect-display-wifi-service](../img/user-guide-wifi/connectWifi.webp)

## Connect your Mobile device or Computer to the Web Service Settings Page

![Connect-to-display-webservice](../img/user-guide-wifi/getURL.webp)

## Settings

1. Schedule
    1. Dropdown selection
    2. Add Schedule button
    3. Delete Schedule button
1. WiFi SSID and PWD
    Your home wifi network name and password. SSID = ssid-name, PWD = wifi-password
1. Time
    Dropdown selection of 12 or 24 hour display of time.
1. TempCF
    Dropdown selection to display the temperature in Celcius or Fehrenheit.
1. TimeZone
    Dropdown selection of time zones for the local time display. When the first itme, **By IP Address** is selected, the display will obtain its external-facing IP address, then use the IP address to obtain your local time. The when a named time zone is selected, the display uses the time zone name to obtain your local time.
1. Display Motor Wait Time
    A value between 15 and 30 milliseconds.  The default is 16 milliseconds. It is the length of time in milliseconds the motor is on when a segment extends or retracts.
1. Display Motor Speed
    A value between 50 and 99 percent. The default is 85 percent. It is the amount of power the motor is provided when extending or retracting.
1. Test on startup
    Each segement is extended and retracted in order from A-G, starting with Digit 3 and ending with Digit 0.
       - **Enabling** this setting causes the display to clear itself before it shows its scheduled display items. For example, suppose the display is showing 10:30 and the power unexpectedly goes out. The power is restored 11 minutes later, the display will immediately light up showing its last knowns state of 10:30, then each digit will extend and retract its segements until the entire display is cleared (no segments are exteded). 
       - **Disabling** this setting causes the display to resume from its last known state.  For example, suppose the display is showing 10:30 and the power unexpectedly goes out. The power is restored 11 minutes later, the display will immediately light up showing its last knowns state of 10:30, then when the time is retrieved from the internet, the 10 and : will remain and only the 30 changes to the number 41.
1. Digit Style or Type
    Dropdown selection of **Human** or **Alien**.

    | Human | Alien |
    | :---: | :--- |
    | ![h-0](../img/digits/digit-0.webp) | ![a-0](../img/digits/digit-alien-0.webp) |
    | ![h-1](../img/digits/digit-1.webp) | ![a-1](../img/digits/digit-alien-1.webp) |
    | ![h-2](../img/digits/digit-2.webp) | ![a-2](../img/digits/digit-alien-2.webp) |