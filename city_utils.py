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
    """Load cities from JSON file into a list format for better filtering"""
    if not os.path.exists(CITIES_FILE):
        print(f"Error: cities.json not found at {CITIES_FILE}")
        return []
    
    with open(CITIES_FILE, 'r', encoding='utf-8') as f:
        cities_data = json.load(f)
    
    # If it's a list, return as-is
    if isinstance(cities_data, list):
        return cities_data
    
    # If it's a dict (old format), convert to list
    cities_list = []
    for city_name, city_info in cities_data.items():
        if isinstance(city_info, dict):
            city_info['city'] = city_name
            cities_list.append(city_info)
    
    return cities_list

def get_timezone_offset(tz_str, year, month, day, hour, minute):
    """Calculate the timezone offset in hours for a given date/time."""
    try:
        tz = zoneinfo.ZoneInfo(tz_str)
        dt = datetime.datetime(year, month, day, hour, minute)
        offset = tz.utcoffset(dt)
        return offset.total_seconds() / 3600.0
    except Exception as e:
        print(f"Error calculating timezone offset for {tz_str}: {e}")
        return 0.0

def normalize_string(s):
    """Normalize string for comparison (lowercase, strip whitespace)"""
    if not s:
        return ""
    return s.lower().strip()

def find_city(cities, city_name, state_name=None, country_name=None):
    """
    Find a city with optional state and country filtering.
    
    Args:
        cities: List of city dictionaries
        city_name: Name of the city (required)
        state_name: Name of the state/province (optional)
        country_name: Name of the country or country code (optional)
    
    Returns:
        tuple: (found_city_name, city_data) or (None, None) if not found
    """
    if not cities or not city_name:
        return None, None
    
    city_lower = normalize_string(city_name)
    state_lower = normalize_string(state_name) if state_name else None
    country_lower = normalize_string(country_name) if country_name else None
    
    # Collect all matches
    exact_matches = []
    partial_matches = []
    
    for city in cities:
        city_name_norm = normalize_string(city.get('city', ''))
        ascii_name_norm = normalize_string(city.get('asciiName', ''))
        state_norm = normalize_string(city.get('stateName', ''))
        country_norm = normalize_string(city.get('countryName', ''))
        country_code_norm = normalize_string(city.get('countryCode', ''))
        
        # Check if city name matches (exact or ASCII name)
        city_match = (city_name_norm == city_lower or ascii_name_norm == city_lower)
        city_partial = (city_lower in city_name_norm or city_lower in ascii_name_norm)
        
        # Check state match if provided
        state_match = True
        if state_lower:
            state_match = (state_lower == state_norm or state_lower in state_norm)
        
        # Check country match if provided
        country_match = True
        if country_lower:
            country_match = (
                country_lower == country_norm or 
                country_lower == country_code_norm or
                country_lower in country_norm
            )
        
        # Exact city name match with filters
        if city_match and state_match and country_match:
            exact_matches.append(city)
        # Partial city name match with filters
        elif city_partial and state_match and country_match:
            partial_matches.append(city)
    
    # Return results based on matches found
    if len(exact_matches) == 1:
        city = exact_matches[0]
        return city.get('city'), city
    elif len(exact_matches) > 1:
        # Multiple exact matches - prioritize by population
        sorted_matches = sorted(exact_matches, key=lambda x: x.get('population', 0), reverse=True)
        city = sorted_matches[0]
        return city.get('city'), city
    elif len(partial_matches) == 1:
        city = partial_matches[0]
        return city.get('city'), city
    elif len(partial_matches) > 1:
        # Multiple partial matches - prioritize by population
        sorted_matches = sorted(partial_matches, key=lambda x: x.get('population', 0), reverse=True)
        city = sorted_matches[0]
        return city.get('city'), city
    
    return None, None

def search_cities(cities, city_name, state_name=None, country_name=None, limit=10):
    """
    Search for cities and return multiple matches (useful for autocomplete/suggestions).
    
    Args:
        cities: List of city dictionaries
        city_name: Name of the city (required)
        state_name: Name of the state/province (optional)
        country_name: Name of the country or country code (optional)
        limit: Maximum number of results to return
    
    Returns:
        list: List of matching city dictionaries
    """
    if not cities or not city_name:
        return []
    
    city_lower = normalize_string(city_name)
    state_lower = normalize_string(state_name) if state_name else None
    country_lower = normalize_string(country_name) if country_name else None
    
    matches = []
    
    for city in cities:
        city_name_norm = normalize_string(city.get('city', ''))
        ascii_name_norm = normalize_string(city.get('asciiName', ''))
        state_norm = normalize_string(city.get('stateName', ''))
        country_norm = normalize_string(city.get('countryName', ''))
        country_code_norm = normalize_string(city.get('countryCode', ''))
        
        # Check if city name matches
        city_match = (
            city_lower in city_name_norm or 
            city_lower in ascii_name_norm or
            city_name_norm.startswith(city_lower)
        )
        
        if not city_match:
            continue
        
        # Check state match if provided
        state_match = True
        if state_lower:
            state_match = (state_lower == state_norm or state_lower in state_norm)
        
        # Check country match if provided
        country_match = True
        if country_lower:
            country_match = (
                country_lower == country_norm or 
                country_lower == country_code_norm or
                country_lower in country_norm
            )
        
        if city_match and state_match and country_match:
            matches.append(city)
    
    # Sort by population (descending) and return top results
    matches_sorted = sorted(matches, key=lambda x: x.get('population', 0), reverse=True)
    return matches_sorted[:limit]