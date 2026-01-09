from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import datetime
from city_utils import load_cities, find_city, get_timezone_offset
from panchang_calculator import PanchangCalculator

app = FastAPI(title="Panchang Calculator API", description="API to calculate 25 Hindu Panchang variables", version="1.0")

# Load cities once on startup
CITIES_DB = load_cities()
CALC = PanchangCalculator()

class PanchangRequest(BaseModel):
    city: Optional[str] = None
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
    return {"message": "Welcome to Panchang APIs. Use /panchang endpoint."}

@app.get("/panchang")
def get_panchang(
    city: Optional[str] = Query(None, description="City name"),
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

    # City Lookup
    if city:
        found_name, city_data = find_city(CITIES_DB, city)
        if city_data:
            location_name = found_name
            if final_lat is None: final_lat = city_data.get('latitude')
            if final_lon is None: final_lon = city_data.get('longitude')
            
            if final_tz is None:
                tz_str = city_data.get('timezone')
                if tz_str:
                    final_tz = get_timezone_offset(tz_str, year, month, day, hour, minute)
                else:
                    final_tz = 5.5 # Default fallback
        else:
            if final_lat is None or final_lon is None:
                 raise HTTPException(status_code=404, detail=f"City '{city}' not found and no coordinates provided.")
    
    # Fallback default (New Delhi)
    if final_lat is None: final_lat = 28.6139
    if final_lon is None: final_lon = 77.2090
    if final_tz is None: final_tz = 5.5
    
    try:
        results = CALC.calculate(year, month, day, hour, minute, second, final_lat, final_lon, final_tz)
        
        # Add metadata to response
        response = {
            "meta": {
                "location": location_name,
                "latitude": final_lat,
                "longitude": final_lon,
                "timezone_offset": final_tz,
                "timestamp": f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
            },
            "data": results
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
