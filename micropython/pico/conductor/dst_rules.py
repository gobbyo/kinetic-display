# Daylight Saving Time (DST) Rules Dictionary
# Contains DST transition information for major timezones

# DST rules format:
# {
#     "timezone": {
#         "observes_dst": True/False,
#         "std_offset": offset in hours from UTC (standard time),
#         "dst_offset": offset in hours from UTC (daylight time),
#         "start_rule": "rule description",
#         "end_rule": "rule description",
#         "start_month": month number,
#         "start_week": week of month (1-5, -1 for last),
#         "start_day": day of week (0=Monday, 6=Sunday),
#         "start_hour": hour of transition (local time),
#         "end_month": month number,
#         "end_week": week of month,
#         "end_day": day of week,
#         "end_hour": hour of transition (local time)
#     }
# }

DST_RULES = {
    # North America
    "America/New_York": {
        "observes_dst": True,
        "std_offset": -5,  # EST
        "dst_offset": -4,  # EDT
        "start_rule": "Second Sunday in March at 2:00 AM",
        "end_rule": "First Sunday in November at 2:00 AM",
        "start_month": 3,
        "start_week": 2,
        "start_day": 6,  # Sunday
        "start_hour": 2,
        "end_month": 11,
        "end_week": 1,
        "end_day": 6,
        "end_hour": 2
    },
    "America/Chicago": {
        "observes_dst": True,
        "std_offset": -6,  # CST
        "dst_offset": -5,  # CDT
        "start_rule": "Second Sunday in March at 2:00 AM",
        "end_rule": "First Sunday in November at 2:00 AM",
        "start_month": 3,
        "start_week": 2,
        "start_day": 6,
        "start_hour": 2,
        "end_month": 11,
        "end_week": 1,
        "end_day": 6,
        "end_hour": 2
    },
    "America/Denver": {
        "observes_dst": True,
        "std_offset": -7,  # MST
        "dst_offset": -6,  # MDT
        "start_rule": "Second Sunday in March at 2:00 AM",
        "end_rule": "First Sunday in November at 2:00 AM",
        "start_month": 3,
        "start_week": 2,
        "start_day": 6,
        "start_hour": 2,
        "end_month": 11,
        "end_week": 1,
        "end_day": 6,
        "end_hour": 2
    },
    "America/Los_Angeles": {
        "observes_dst": True,
        "std_offset": -8,  # PST
        "dst_offset": -7,  # PDT
        "start_rule": "Second Sunday in March at 2:00 AM",
        "end_rule": "First Sunday in November at 2:00 AM",
        "start_month": 3,
        "start_week": 2,
        "start_day": 6,
        "start_hour": 2,
        "end_month": 11,
        "end_week": 1,
        "end_day": 6,
        "end_hour": 2
    },
    "America/Phoenix": {
        "observes_dst": False,
        "std_offset": -7,  # MST (no DST)
        "dst_offset": -7,
        "start_rule": None,
        "end_rule": None
    },
    
    # Europe
    "Europe/London": {
        "observes_dst": True,
        "std_offset": 0,  # GMT
        "dst_offset": 1,  # BST
        "start_rule": "Last Sunday in March at 1:00 AM UTC",
        "end_rule": "Last Sunday in October at 1:00 AM UTC",
        "start_month": 3,
        "start_week": -1,  # Last week
        "start_day": 6,
        "start_hour": 1,
        "end_month": 10,
        "end_week": -1,
        "end_day": 6,
        "end_hour": 1
    },
    "Europe/Paris": {
        "observes_dst": True,
        "std_offset": 1,  # CET
        "dst_offset": 2,  # CEST
        "start_rule": "Last Sunday in March at 2:00 AM local",
        "end_rule": "Last Sunday in October at 3:00 AM local",
        "start_month": 3,
        "start_week": -1,
        "start_day": 6,
        "start_hour": 2,
        "end_month": 10,
        "end_week": -1,
        "end_day": 6,
        "end_hour": 3
    },
    "Europe/Berlin": {
        "observes_dst": True,
        "std_offset": 1,  # CET
        "dst_offset": 2,  # CEST
        "start_rule": "Last Sunday in March at 2:00 AM local",
        "end_rule": "Last Sunday in October at 3:00 AM local",
        "start_month": 3,
        "start_week": -1,
        "start_day": 6,
        "start_hour": 2,
        "end_month": 10,
        "end_week": -1,
        "end_day": 6,
        "end_hour": 3
    },
    
    # Australia
    "Australia/Sydney": {
        "observes_dst": True,
        "std_offset": 10,  # AEST
        "dst_offset": 11,  # AEDT
        "start_rule": "First Sunday in October at 2:00 AM local",
        "end_rule": "First Sunday in April at 3:00 AM local",
        "start_month": 10,
        "start_week": 1,
        "start_day": 6,
        "start_hour": 2,
        "end_month": 4,
        "end_week": 1,
        "end_day": 6,
        "end_hour": 3
    },
    "Australia/Melbourne": {
        "observes_dst": True,
        "std_offset": 10,  # AEST
        "dst_offset": 11,  # AEDT
        "start_rule": "First Sunday in October at 2:00 AM local",
        "end_rule": "First Sunday in April at 3:00 AM local",
        "start_month": 10,
        "start_week": 1,
        "start_day": 6,
        "start_hour": 2,
        "end_month": 4,
        "end_week": 1,
        "end_day": 6,
        "end_hour": 3
    },
    "Australia/Brisbane": {
        "observes_dst": False,
        "std_offset": 10,  # AEST (no DST)
        "dst_offset": 10,
        "start_rule": None,
        "end_rule": None
    },
    
    # Asia
    "Asia/Tokyo": {
        "observes_dst": False,
        "std_offset": 9,  # JST (no DST)
        "dst_offset": 9,
        "start_rule": None,
        "end_rule": None
    },
    "Asia/Shanghai": {
        "observes_dst": False,
        "std_offset": 8,  # CST (no DST)
        "dst_offset": 8,
        "start_rule": None,
        "end_rule": None
    },
    "Asia/Dubai": {
        "observes_dst": False,
        "std_offset": 4,  # GST (no DST)
        "dst_offset": 4,
        "start_rule": None,
        "end_rule": None
    },
    
    # New Zealand
    "Pacific/Auckland": {
        "observes_dst": True,
        "std_offset": 12,  # NZST
        "dst_offset": 13,  # NZDT
        "start_rule": "Last Sunday in September at 2:00 AM local",
        "end_rule": "First Sunday in April at 3:00 AM local",
        "start_month": 9,
        "start_week": -1,
        "start_day": 6,
        "start_hour": 2,
        "end_month": 4,
        "end_week": 1,
        "end_day": 6,
        "end_hour": 3
    },
    
    # South America
    "America/Sao_Paulo": {
        "observes_dst": False,  # Brazil discontinued DST in 2019
        "std_offset": -3,
        "dst_offset": -3,
        "start_rule": None,
        "end_rule": None
    },
    
    # Middle East
    "Asia/Jerusalem": {
        "observes_dst": True,
        "std_offset": 2,  # IST
        "dst_offset": 3,  # IDT
        "start_rule": "Friday before last Sunday in March at 2:00 AM",
        "end_rule": "Last Sunday in October at 2:00 AM",
        "start_month": 3,
        "start_week": -1,
        "start_day": 4,  # Friday (two days before last Sunday)
        "start_hour": 2,
        "end_month": 10,
        "end_week": -1,
        "end_day": 6,
        "end_hour": 2
    }
}


def get_dst_rule(timezone):
    """
    Get DST rules for a specific timezone.
    
    Args:
        timezone: String timezone identifier (e.g., "America/New_York")
        
    Returns:
        Dictionary with DST rules or None if timezone not found
    """
    return DST_RULES.get(timezone)


def observes_dst(timezone):
    """
    Check if a timezone observes daylight saving time.
    
    Args:
        timezone: String timezone identifier
        
    Returns:
        Boolean indicating if DST is observed
    """
    rules = get_dst_rule(timezone)
    return rules.get("observes_dst", False) if rules else False


def get_offset(timezone, is_dst=False):
    """
    Get the UTC offset for a timezone.
    
    Args:
        timezone: String timezone identifier
        is_dst: Boolean indicating if DST is currently active
        
    Returns:
        Integer offset in hours from UTC, or None if timezone not found
    """
    rules = get_dst_rule(timezone)
    if not rules:
        return None
    
    if is_dst and rules["observes_dst"]:
        return rules["dst_offset"]
    else:
        return rules["std_offset"]


def list_timezones():
    """
    Get a list of all available timezones.
    
    Returns:
        List of timezone identifiers
    """
    return sorted(DST_RULES.keys())
