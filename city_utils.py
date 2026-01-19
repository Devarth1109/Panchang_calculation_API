import json
import os
import datetime
import requests
import threading
try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

# Path to cities.json (assumed to be in the same directory)
CITIES_FILE = os.path.join(os.path.dirname(__file__), 'cities.json')

# GeoNames API configuration
GEONAMES_USERNAME = "divyesh"
GEONAMES_SEARCH_URL = "http://api.geonames.org/searchJSON"
GEONAMES_GET_URL = "http://api.geonames.org/getJSON"

# Lock for thread-safe file operations
_cities_file_lock = threading.Lock()

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


def save_city_to_file(city_data):
    """
    Save a new city entry to cities.json in a thread-safe manner.
    
    Args:
        city_data: Dictionary containing city information
    """
    with _cities_file_lock:
        try:
            # Load existing data
            cities_list = []
            if os.path.exists(CITIES_FILE):
                with open(CITIES_FILE, 'r', encoding='utf-8') as f:
                    cities_list = json.load(f)
                    if not isinstance(cities_list, list):
                        cities_list = []
            
            # Check if city already exists (by geonameId)
            geoname_id = city_data.get('geonameId')
            if geoname_id:
                for existing_city in cities_list:
                    if existing_city.get('geonameId') == geoname_id:
                        return  # City already exists, no need to add
            
            # Append new city
            cities_list.append(city_data)
            
            # Save back to file
            with open(CITIES_FILE, 'w', encoding='utf-8') as f:
                json.dump(cities_list, f, indent=2, ensure_ascii=False)
            
            print(f"City '{city_data.get('city')}' saved to cities.json")
        except Exception as e:
            print(f"Error saving city to file: {e}")

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


def fetch_city_from_geonames(city_name, state_name=None, country_name=None):
    """
    Fetch city details from GeoNames API.
    
    Args:
        city_name: Name of the city (required)
        state_name: Name of the state/province (optional)
        country_name: Name of the country or country code (optional)
    
    Returns:
        dict: City data in the same format as cities.json entries, or None if not found
    """
    try:
        # Build search query
        search_query = city_name
        if state_name:
            search_query += f" {state_name}"
        
        params = {
            'q': search_query,
            'maxRows': 10,
            'username': GEONAMES_USERNAME,
            'style': 'FULL',
            'featureClass': 'P',  # Populated places only
        }
        
        # Add country filter if provided (try to detect if it's a code or name)
        if country_name:
            # Common country code check (2-letter codes)
            if len(country_name) == 2 and country_name.isalpha():
                params['country'] = country_name.upper()
            else:
                # Search by name - add to query
                search_query += f" {country_name}"
                params['q'] = search_query
        
        response = requests.get(GEONAMES_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = data.get('geonames', [])
        if not results:
            return None
        
        # Filter results based on provided criteria
        city_lower = normalize_string(city_name)
        state_lower = normalize_string(state_name) if state_name else None
        country_lower = normalize_string(country_name) if country_name else None
        
        best_match = None
        best_score = -1
        
        for result in results:
            score = 0
            result_city = normalize_string(result.get('name', ''))
            result_ascii = normalize_string(result.get('asciiName', ''))
            result_state = normalize_string(result.get('adminName1', ''))
            result_country = normalize_string(result.get('countryName', ''))
            result_country_code = normalize_string(result.get('countryCode', ''))
            
            # City name match
            if result_city == city_lower or result_ascii == city_lower:
                score += 100  # Exact match
            elif city_lower in result_city or city_lower in result_ascii:
                score += 50  # Partial match
            else:
                continue  # Skip if city doesn't match at all
            
            # State match bonus
            if state_lower:
                if result_state == state_lower:
                    score += 50
                elif state_lower in result_state or result_state in state_lower:
                    score += 25
                else:
                    score -= 10  # Penalty for state mismatch when state is specified
            
            # Country match bonus
            if country_lower:
                if result_country == country_lower or result_country_code == country_lower:
                    score += 50
                elif country_lower in result_country:
                    score += 25
                else:
                    score -= 20  # Penalty for country mismatch when country is specified
            
            # Population bonus (prefer larger cities)
            population = result.get('population', 0)
            if population > 0:
                score += min(population / 100000, 20)  # Max 20 points for population
            
            if score > best_score:
                best_score = score
                best_match = result
        
        if not best_match:
            return None
        
        # Convert to our city format
        city_data = {
            'geonameId': best_match.get('geonameId'),
            'city': best_match.get('name'),
            'asciiName': best_match.get('asciiName'),
            'countryCode': best_match.get('countryCode'),
            'countryName': best_match.get('countryName'),
            'stateName': best_match.get('adminName1'),
            'latitude': float(best_match.get('lat')) if best_match.get('lat') else None,
            'longitude': float(best_match.get('lng')) if best_match.get('lng') else None,
            'timezone': best_match.get('timezone', {}).get('timeZoneId') if isinstance(best_match.get('timezone'), dict) else None,
            'population': best_match.get('population', 0)
        }
        
        return city_data
        
    except requests.exceptions.Timeout:
        print(f"GeoNames API timeout for city: {city_name}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"GeoNames API request error: {e}")
        return None
    except Exception as e:
        print(f"Error fetching city from GeoNames: {e}")
        return None

def find_city(cities, city_name, state_name=None, country_name=None, use_geonames_fallback=True):
    """
    Find a city with optional state and country filtering.
    Falls back to GeoNames API if city not found locally.
    
    Args:
        cities: List of city dictionaries
        city_name: Name of the city (required)
        state_name: Name of the state/province (optional)
        country_name: Name of the country or country code (optional)
        use_geonames_fallback: Whether to use GeoNames API if city not found locally (default: True)
    
    Returns:
        tuple: (found_city_name, city_data) or (None, None) if not found
    """
    if not city_name:
        return None, None
    
    # First, try to find in local database
    found_name, city_data = _find_city_local(cities, city_name, state_name, country_name)
    
    if city_data:
        return found_name, city_data
    
    # If not found locally and fallback is enabled, try GeoNames API
    if use_geonames_fallback:
        print(f"City '{city_name}' not found locally, fetching from GeoNames API...")
        city_data = fetch_city_from_geonames(city_name, state_name, country_name)
        
        if city_data:
            # Save to cities.json for future use
            save_city_to_file(city_data)
            
            # Add to in-memory list (if cities is mutable)
            if isinstance(cities, list):
                cities.append(city_data)
            
            return city_data.get('city'), city_data
    
    return None, None


def _find_city_local(cities, city_name, state_name=None, country_name=None):
    """
    Find a city in the local database with optional state and country filtering.
    
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