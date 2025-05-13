# Web Service and Settings

## Connect your Mobile device or Computer to the **kinetic-display** Wifi Access Point (AP)

![Connect-display-wifi-service](../img/user-guide-wifi/connectWifi.webp)

## Connect your Mobile device or Computer to the Web Service Settings Page

![Connect-to-display-webservice](../img/user-guide-wifi/getURL.webp)

## Settings

1. **Schedule**.
    1. Dropdown selection
    2. Add Schedule button
    3. Delete Schedule button
1. **Wifi SSID and Wifi PWD**.
    Your home wifi network name and password. SSID = ssid-name, PWD = wifi-password When the settings page is opened for the first time, the default Wifi SSID and Wifi PWD are set to ```SSID``` and ```Password```. You'll need to change the ```SSID``` and ```Password``` to your home network wifi name and password.
2. **Time**.
    Dropdown selection of **12** or **24** hour display of time. The default is set to **12** hour.
3. **TempCF**.
    Dropdown selection to display the temperature in **Celcius** or **Fahrenheit**. The default is set to **Fahrenheit**.
4. **TimeZone**.
    Dropdown selection of time zones for the local time display. When the settings page is opened for the first time, **By IP Address** is selected, the display will obtain its external-facing IP address, then use the IP address to obtain your local time. The when a named time zone is selected, the display uses the time zone name to obtain your local time.
5. **Display Motor Wait Time**.
    A value between **15** and **30** milliseconds.  The default is **16** milliseconds. It is the length of time in milliseconds the motor is on when a segment extends or retracts.
6. **Display Motor Speed**.
    A value between **50** and **99** percent. The default is **85** percent. It is the amount of power the motor is provided when extending or retracting. Reducing the motor speed slows the extension and retraction of the display segments. Conversely, increasing the motor speed quickens the extension and retraction of the segments.
7. **Test on startup**.
    A dropdown selection of **Test** or **No Test**.
       - **Test** this setting causes each digit from 3 through 0 to extend each segment in order of A-G, then retract each segment A-G. The scheduled actions for display begin when all digits and colons fully retracted. For example, suppose the display is showing **10:30** and the power unexpectedly goes out, then the power is restored 11 minutes later. The display will immediately light up showing its last knowns state of **10:30**, then each digit will extend and retract its segments until the entire display is cleared before showing the time of **10:41**.
       - **No Test** this setting causes the display to resume from its last known state.  For example, suppose the display is showing **10:30** and the power unexpectedly goes out, then the power is restored 11 minutes later. The display will immediately light up showing its last knowns state of **10:30**, when the time is retrieved from the internet, the **10** and **:** will remain and only the **30** changes to the number **41**.
8. **Digit Style or Type**.
    Dropdown selection of **Human** or **Alien**.

    | Human | Alien |
    | :---: | :--- |
    | ![h-0](../img/digits/digit-0.webp) | ![a-0](../img/digits/digit-alien-0.webp) |
    | ![h-1](../img/digits/digit-1.webp) | ![a-1](../img/digits/digit-alien-1.webp) |
    | ![h-2](../img/digits/digit-2.webp) | ![a-2](../img/digits/digit-alien-2.webp) |