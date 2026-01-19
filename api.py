from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
import datetime
from city_utils import load_cities, find_city, get_timezone_offset
from panchang_calculator import PanchangCalculator
from choghadiya_calculator import ChoghadiyaCalculator

app = FastAPI(
    title="Panchang & Choghadiya API", 
    description="API to calculate Hindu Panchang variables and Choghadiya muhurta", 
    version="1.2"
)

# Load cities once on startup
CITIES_DB = load_cities()
CALC = PanchangCalculator()
CHOG_CALC = ChoghadiyaCalculator()

class PanchangRequest(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz: Optional[float] = None
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None
    second: Optional[int] = 0

@app.get("/")
def read_root():
    return {"message": "Welcome to Panchang APIs. Use /panchang or /choghadiya endpoints."}

@app.get("/panchang")
def get_panchang(
    city: Optional[str] = Query(None, description="City name"),
    state: Optional[str] = Query(None, description="State/Province name"),
    country: Optional[str] = Query(None, description="Country name or country code"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude"),
    tz: Optional[float] = Query(None, description="Timezone Offset"),
    year: Optional[int] = Query(None, description="Year"),
    month: Optional[int] = Query(None, description="Month"),
    day: Optional[int] = Query(None, description="Day"),
    hour: Optional[int] = Query(None, description="Hour"),
    minute: Optional[int] = Query(None, description="Minute"),
    second: Optional[int] = Query(0, description="Second")
):
    # Default to current time if date/time not provided
    now = datetime.datetime.now()
    if year is None: year = now.year
    if month is None: month = now.month
    if day is None: day = now.day
    if hour is None: hour = now.hour
    if minute is None: minute = now.minute
    
    final_lat = lat
    final_lon = lon
    final_tz = tz
    location_name = city or "Custom Coordinates"
    location_details = {}

    # City Lookup with state and country filtering (with GeoNames API fallback)
    if city:
        found_name, city_data = find_city(CITIES_DB, city, state, country)
        if city_data:
            location_name = found_name
            
            # Store location details
            location_details = {
                'city': city_data.get('city'),
                'state': city_data.get('stateName'),
                'country': city_data.get('countryName'),
                'countryCode': city_data.get('countryCode')
            }
            
            if final_lat is None: 
                final_lat = city_data.get('latitude')
            if final_lon is None: 
                final_lon = city_data.get('longitude')
            
            if final_tz is None:
                tz_str = city_data.get('timezone')
                if tz_str:
                    final_tz = get_timezone_offset(tz_str, year, month, day, hour, minute)
                else:
                    final_tz = 5.5 # Default fallback
        else:
            # City not found in local database AND GeoNames API
            if final_lat is None or final_lon is None:
                error_msg = f"City '{city}' not found"
                if state:
                    error_msg += f" in state '{state}'"
                if country:
                    error_msg += f" in country '{country}'"
                error_msg += ". Could not find in local database or GeoNames API. Please provide coordinates."
                raise HTTPException(status_code=404, detail=error_msg)
    
    # Fallback default (New Delhi)
    if final_lat is None: final_lat = 28.6139
    if final_lon is None: final_lon = 77.2090
    if final_tz is None: final_tz = 5.5
    
    try:
        results = CALC.calculate(year, month, day, hour, minute, second, final_lat, final_lon, final_tz)
        
        # Build comprehensive location info
        location_info = location_name
        if location_details:
            parts = [location_details.get('city')]
            if location_details.get('state'):
                parts.append(location_details.get('state'))
            if location_details.get('country'):
                parts.append(location_details.get('country'))
            location_info = ", ".join(filter(None, parts))
        
        # Add metadata to response
        response = {
            "meta": {
                "location": location_info,
                "city": location_details.get('city') if location_details else city,
                "state": location_details.get('state') if location_details else state,
                "country": location_details.get('country') if location_details else country,
                "countryCode": location_details.get('countryCode') if location_details else None,
                "latitude": final_lat,
                "longitude": final_lon,
                "timezone_offset": final_tz,
                "date": f"{year}-{month:02d}-{day:02d}",
                "time": f"{hour:02d}:{minute:02d}:{second:02d}",
                "timestamp": f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
            },
            "data": results
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/choghadiya")
def get_choghadiya(
    city: Optional[str] = Query(None, description="City name"),
    state: Optional[str] = Query(None, description="State/Province name"),
    country: Optional[str] = Query(None, description="Country name or country code"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude"),
    tz: Optional[float] = Query(None, description="Timezone Offset"),
    year: Optional[int] = Query(None, description="Year"),
    month: Optional[int] = Query(None, description="Month"),
    day: Optional[int] = Query(None, description="Day")
):
    # Default to current date if not provided
    now = datetime.datetime.now()
    if year is None: year = now.year
    if month is None: month = now.month
    if day is None: day = now.day
    
    final_lat = lat
    final_lon = lon
    final_tz = tz
    location_name = city or "Custom Coordinates"
    location_details = {}
    tz_name = None

    # City Lookup with state and country filtering (with GeoNames API fallback)
    if city:
        found_name, city_data = find_city(CITIES_DB, city, state, country)
        if city_data:
            location_name = found_name
            
            # Store location details
            location_details = {
                'city': city_data.get('city'),
                'state': city_data.get('stateName'),
                'country': city_data.get('countryName'),
                'countryCode': city_data.get('countryCode')
            }
            
            if final_lat is None: 
                final_lat = city_data.get('latitude')
            if final_lon is None: 
                final_lon = city_data.get('longitude')
            
            if final_tz is None:
                tz_name = city_data.get('timezone')
                if tz_name:
                    final_tz = get_timezone_offset(tz_name, year, month, day, 12, 0)
                else:
                    final_tz = 5.5  # Default fallback
        else:
            # City not found in local database AND GeoNames API
            if final_lat is None or final_lon is None:
                error_msg = f"City '{city}' not found"
                if state:
                    error_msg += f" in state '{state}'"
                if country:
                    error_msg += f" in country '{country}'"
                error_msg += ". Could not find in local database or GeoNames API. Please provide coordinates."
                raise HTTPException(status_code=404, detail=error_msg)
    
    # Fallback default (New Delhi)
    if final_lat is None: final_lat = 28.6139
    if final_lon is None: final_lon = 77.2090
    if final_tz is None: final_tz = 5.5
    
    try:
        # Calculate choghadiya
        results = CHOG_CALC.calculate(year, month, day, final_lat, final_lon, final_tz, tz_name)
        
        # Build comprehensive location info
        location_info = location_name
        if location_details:
            parts = [location_details.get('city')]
            if location_details.get('state'):
                parts.append(location_details.get('state'))
            if location_details.get('country'):
                parts.append(location_details.get('country'))
            location_info = ", ".join(filter(None, parts))
        
        # Build day choghadiya times list (8 periods)
        day_choghadiya_times = []
        for chog in results["day_choghadiya"]:
            day_choghadiya_times.append({
                f"{chog['name']}-{chog['quality']}": f"{chog['start_time']} to {chog['end_time']}"
            })
        
        # Build night choghadiya times list (8 periods)
        night_choghadiya_times = []
        for chog in results["night_choghadiya"]:
            night_choghadiya_times.append({
                f"{chog['name']}-{chog['quality']}": f"{chog['start_time']} to {chog['end_time']}"
            })
        
        # Build response in desired format
        response = {
            "meta": {
                "location": location_info,
                "city": location_details.get('city') if location_details else city,
                "state": location_details.get('state') if location_details else state,
                "country": location_details.get('country') if location_details else country,
                "countryCode": location_details.get('countryCode') if location_details else None,
                "latitude": final_lat,
                "longitude": final_lon,
                "timezone_offset": final_tz,
                "date": f"{year}-{month:02d}-{day:02d}",
                "timestamp": f"{year}-{month:02d}-{day:02d}"
            },
            "choghadiya": {
                "day_choghadiya_start": results["sunrise"],
                "day_choghadiya_times": day_choghadiya_times,
                "night_choghadiya_start": results["sunset"],
                "night_choghadiya_times": night_choghadiya_times
            },
            "Note": f"All timings are represented in 12-hour notation in local time of {location_info} with DST adjustment (if applicable). Hours which are past midnight are suffixed with next day date. In Panchang day starts and ends with sunrise."
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)