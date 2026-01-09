import argparse
import datetime

from panchang_calculator import PanchangCalculator
from city_utils import load_cities, find_city, get_timezone_offset

def main():
    parser = argparse.ArgumentParser(description="Calculate Hindu Panchang Variables")
    parser.add_argument("--city", type=str, help="City Name to lookup lat/lon/tz")
    parser.add_argument("--lat", type=float, help="Latitude (override)")
    parser.add_argument("--lon", type=float, help="Longitude (override)")
    parser.add_argument("--tz", type=float, help="Timezone offset (override)")
    
    now = datetime.datetime.now()
    parser.add_argument("--year", type=int, default=now.year, help="Year")
    parser.add_argument("--month", type=int, default=now.month, help="Month")
    parser.add_argument("--day", type=int, default=now.day, help="Day")
    parser.add_argument("--hour", type=int, default=now.hour, help="Hour")
    parser.add_argument("--minute", type=int, default=now.minute, help="Minute")
    parser.add_argument("--second", type=int, default=now.second, help="Second")
    
    args = parser.parse_args()
    
    lat = args.lat
    lon = args.lon
    tz = args.tz
    city_name = args.city or "New Delhi"
    
    # If City is provided (or defaulting to New Delhi if no lat/lon), try lookup
    if args.city or (lat is None and lon is None):
        cities = load_cities()
        if cities:
            found_name, city_data = find_city(cities, city_name)
            if city_data:
                print(f"Found City: {found_name}")
                if lat is None:
                    lat = city_data.get('latitude')
                if lon is None:
                    lon = city_data.get('longitude')
                
                # Calculate TZ if not provided
                if tz is None:
                    tz_str = city_data.get('timezone')
                    if tz_str:
                        tz = get_timezone_offset(tz_str, args.year, args.month, args.day, args.hour, args.minute)
                        print(f"Timezone: {tz_str} (Offset: {tz})")
                    else:
                        print("Warning: No timezone found for city, defaulting to 5.5")
                        tz = 5.5
            else:
                print(f"City '{city_name}' not found in database.")
                if lat is None or lon is None:
                    print("Please provide --lat and --lon.")
                    return
    
    # Defaults if still missing
    if lat is None: lat = 28.6139
    if lon is None: lon = 77.2090
    if tz is None: tz = 5.5

    print(f"Calculating Panchang for {city_name} (Lat: {lat}, Lon: {lon})")
    print(f"Date: {args.year}-{args.month:02d}-{args.day:02d} Time: {args.hour:02d}:{args.minute:02d}:{args.second:02d} (TZ: {tz})")
    print("-" * 40)
    
    calc = PanchangCalculator()
    try:
        results = calc.calculate(args.year, args.month, args.day, args.hour, args.minute, args.second, lat, lon, tz)
        
        # Determine strict order
        keys_order = [
            "Sunrise", "Sunset", "Moonrise", "Moonset", 
            "Shaka Samvat", "Vikram Samvat", "Gujarati Samvat",
            "Amanta Month", "Purnimanta Month",
            "Weekday", "Paksha", "Tithi", "Nakshatra", "Yoga", "Karana",
            "Pravishte/Gate", "Sunsign", "Moonsign",
            "Rahu Kalam", "Gulikai Kalam", "Yamaganda",
            "Abhijit", "Dur Muhurtam", "Amrit Kalam", "Varjyam"
        ]
        
        i = 1
        for key in keys_order:
            val = results.get(key, "N/A")
            print(f"{i}. {key}: {val}")
            i += 1
            
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
