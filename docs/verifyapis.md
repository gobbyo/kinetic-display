
# Verify REST API Dependencies

The Kinetic Display uses several REST APIs to obtain local time and weather information. Use your computer's web browser to verify these APIs work for your location **before** ordering materials or 3D printing parts. Some APIs are used as backups for reliability, as they may be throttled or temporarily unavailable.

## Step 1: Get Your External IP Address

- Visit [http://api.ipify.org](http://api.ipify.org) in your browser. The page will display your external IP address (e.g., `11.115.204.194`). Save this address for the next steps.

## Step 2: Get Latitude, Longitude, and Time Zone

- Replace `{0}` in `http://ip-api.com/json/{0}` with your external IP address from Step 1.
- Example: [http://ip-api.com/json/11.115.204.194](http://ip-api.com/json/11.115.204.194)
- The JSON response should include `lat`, `lon`, and `timezone` fields. Example:

```json
{
  "status": "success",
  "country": "United States",
  "countryCode": "US",
  "region": "OH",
  "regionName": "Ohio",
  "city": "Whitehall",
  "zip": "43218",
  "lat": 39.9747,
  "lon": -82.8947,
  "timezone": "America/New_York",
  "isp": "DoD Network Information Center",
  "org": "DoD Network Information Center",
  "as": "AS749 DoD Network Information Center",
  "query": "11.115.204.194"
}
```

## Step 3: Get Weather Data

- Use the `lat` and `lon` values from Step 2 in the following API:
  `https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&current_weather=true&hourly=relativehumidity_2m`
- Example: [https://api.open-meteo.com/v1/forecast?latitude=39.9747&longitude=-82.8947&current_weather=true&hourly=relativehumidity_2m](https://api.open-meteo.com/v1/forecast?latitude=39.9747&longitude=-82.8947&current_weather=true&hourly=relativehumidity_2m)
- The JSON response should include `temperature` and `relativehumidity_2m` fields. Example:

```json
{
  "latitude": 39.986526,
  "longitude": -82.90847,
  "generationtime_ms": 0.0587701797485352,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "timezone_abbreviation": "GMT",
  "elevation": 242,
  "current_weather_units": {
    "time": "iso8601",
    "interval": "seconds",
    "temperature": "°C",
    "windspeed": "km/h",
    "winddirection": "°",
    "is_day": "",
    "weathercode": "wmo code"
  },
  "current_weather": {
    "time": "2025-05-13T19:30",
    "interval": 900,
    "temperature": 21.3,
    "windspeed": 5.5,
    "winddirection": 122,
    "is_day": 1,
    "weathercode": 3
  },
  "hourly_units": {
    "time": "iso8601",
    "relativehumidity_2m": "%"
  },
  "hourly": {
    "time": [],
    "relativehumidity_2m": []
  }
}
```

## Step 4: Get World Time by IP

- Use your external IP address in the following API:
  `http://worldtimeapi.org/api/ip/{ip}`
- Example: [http://worldtimeapi.org/api/ip/11.115.204.194](http://worldtimeapi.org/api/ip/11.115.204.194)
- The JSON response should include a `datetime` field. Example:

```json
{
  "utc_offset": "-05:00",
  "timezone": "America/New_York",
  "day_of_week": 2,
  "day_of_year": 133,
  "datetime": "2025-05-13T16:42:11.694884-05:00",
  "utc_datetime": "2025-05-13T21:42:11.694884+00:00",
  "unixtime": 1747172531,
  "raw_offset": -21600,
  "week_number": 20,
  "dst": true,
  "abbreviation": "CDT",
  "dst_offset": 3600,
  "dst_from": "2025-03-09T08:00:00+00:00",
  "dst_until": "2025-11-02T07:00:00+00:00",
  "client_ip": "45.115.204.194"
}
```

## Step 5: Get Time API by IP

- Use your external IP address in the following API:
  `https://www.timeapi.io/api/Time/current/ip?ipAddress={ip}`
- Example: [https://www.timeapi.io/api/Time/current/ip?ipAddress=11.115.204.194](https://www.timeapi.io/api/Time/current/ip?ipAddress=11.115.204.194)
- The JSON response should include `year`, `month`, `hour`, `minute`, `seconds`, and `date`. Example:

```json
{
  "year": 2025,
  "month": 5,
  "day": 13,
  "hour": 15,
  "minute": 39,
  "seconds": 36,
  "milliSeconds": 804,
  "dateTime": "2025-05-13T15:39:36.8047099",
  "date": "05/13/2025",
  "time": "15:39",
  "timeZone": "America/New_York",
  "dayOfWeek": "Tuesday",
  "dstActive": true
}
```

## Step 6: Get World Time by Time Zone

- Use the `timezone` value from Step 2 in the following API:
  `http://worldtimeapi.org/api/timezone/{timezone}`
- Example: [http://worldtimeapi.org/api/timezone/America/New_York](http://worldtimeapi.org/api/timezone/America/New_York)
- The JSON response should include a `datetime` field. Example:

```json
{
  "utc_offset": "-05:00",
  "timezone": "America/New_York",
  "day_of_week": 2,
  "day_of_year": 133,
  "datetime": "2025-05-13T16:42:11.694884-05:00",
  "utc_datetime": "2025-05-13T21:42:11.694884+00:00",
  "unixtime": 1747172531,
  "raw_offset": -21600,
  "week_number": 20,
  "dst": true,
  "abbreviation": "CDT",
  "dst_offset": 3600,
  "dst_from": "2025-03-09T08:00:00+00:00",
  "dst_until": "2025-11-02T07:00:00+00:00",
  "client_ip": "45.115.204.194"
}
```

## Step 7: Get Time API by Time Zone

- Use the `timezone` value from Step 2 in the following API:
  `https://www.timeapi.io/api/Time/current/zone?timeZone={timezone}`
- Example: [https://www.timeapi.io/api/Time/current/zone?timeZone=America/New_York](https://www.timeapi.io/api/Time/current/zone?timeZone=America/New_York)
- The JSON response should include `year`, `month`, `hour`, `minute`, `seconds`, and `date`. Example:

```json
{
  "year": 2025,
  "month": 5,
  "day": 13,
  "hour": 15,
  "minute": 39,
  "seconds": 36,
  "milliSeconds": 804,
  "dateTime": "2025-05-13T15:39:36.8047099",
  "date": "05/13/2025",
  "time": "15:39",
  "timeZone": "America/New_York",
  "dayOfWeek": "Tuesday",
  "dstActive": true
}
```
