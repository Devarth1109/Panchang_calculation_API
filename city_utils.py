import json
import os
import datetime
try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

# Path to cities.json (assumed to be in the same directory)
CITIES_FILE = os.path.join(os.path.dirname(__file__), 'cities.json')

def load_cities():
    if not os.path.exists(CITIES_FILE):
        print(f"Error: cities.json not found at {CITIES_FILE}")
        return {}
    with open(CITIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_timezone_offset(tz_str, year, month, day, hour, minute):
    """Calculate the timezone offset in hours for a given date/time."""
    try:
        tz = zoneinfo.ZoneInfo(tz_str)
        # Create a naive datetime and localize it, or just attach tz if it's standard
        # Best practice: use local time and check offset
        dt = datetime.datetime(year, month, day, hour, minute)
        offset = tz.utcoffset(dt)
        return offset.total_seconds() / 3600.0
    except Exception as e:
        print(f"Error calculating timezone offset for {tz_str}: {e}")
        return 0.0

def find_city(cities, city_name):
    """Find a city case-insensitively."""
    city_lower = city_name.lower()
    
    # 1. Exact match
    for name in cities:
        if name.lower() == city_lower:
            return name, cities[name]
            
    # 2. Starts with match
    matches = [name for name in cities if name.lower().startswith(city_lower)]
    if len(matches) == 1:
        return matches[0], cities[matches[0]]
        
    return None, None
