import requests
import json
import time
from typing import List, Dict
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GeoNamesCityScraper:
    def __init__(self, username: str):
        self.username = username
        self.base_url = "http://api.geonames.org"
        self.all_cities = []
        
    def get_all_countries(self) -> List[Dict]:
        """Fetch all countries from GeoNames"""
        url = f"{self.base_url}/countryInfoJSON"
        params = {'username': self.username}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('geonames', [])
        except Exception as e:
            logger.error(f"Error fetching countries: {e}")
            return []
    
    def get_cities_by_country(self, country_code: str, max_rows: int = 1000) -> List[Dict]:
        """Fetch cities for a specific country"""
        url = f"{self.base_url}/searchJSON"
        
        # Feature codes for cities and populated places
        # PPL = populated place, PPLA = seat of first-order administrative division
        # PPLC = capital, PPLA2, PPLA3, PPLA4 = various administrative seats
        feature_codes = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC']
        
        cities = []
        
        for feature_code in feature_codes:
            start_row = 0
            while True:
                params = {
                    'country': country_code,
                    'featureCode': feature_code,
                    'maxRows': max_rows,
                    'startRow': start_row,
                    'username': self.username,
                    'style': 'FULL'
                }
                
                try:
                    response = requests.get(url, params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    results = data.get('geonames', [])
                    if not results:
                        break
                    
                    cities.extend(results)
                    logger.info(f"Fetched {len(results)} cities with feature code {feature_code} from {country_code} (total: {len(cities)})")
                    
                    # If we got less than max_rows, we've reached the end
                    if len(results) < max_rows:
                        break
                    
                    start_row += max_rows
                    time.sleep(0.2)  # Rate limiting to avoid API throttling
                    
                except Exception as e:
                    logger.error(f"Error fetching cities for {country_code} with feature {feature_code}: {e}")
                    break
        
        return cities
    
    def process_city_data(self, city: Dict) -> Dict:
        """Extract and format required city information"""
        # Convert latitude and longitude to float
        lat = city.get('lat')
        lon = city.get('lng')
        
        try:
            lat = float(lat) if lat else None
            lon = float(lon) if lon else None
        except (ValueError, TypeError):
            lat = None
            lon = None
        
        return {
            'geonameId': city.get('geonameId'),
            'city': city.get('name'),
            'asciiName': city.get('asciiName'),
            'countryCode': city.get('countryCode'),
            'countryName': city.get('countryName'),
            'stateName': city.get('adminName1'),  # State/Province name
            'latitude': lat,
            'longitude': lon,
            'timezone': city.get('timezone', {}).get('timeZoneId') if isinstance(city.get('timezone'), dict) else None,
            'population': city.get('population', 0)
        }
    
    def fetch_all_cities(self, output_file: str = 'cities.json', min_population: int = 0):
        """Main method to fetch all cities from all countries"""
        logger.info("Starting to fetch all cities from GeoNames...")
        
        # Get all countries
        countries = self.get_all_countries()
        logger.info(f"Found {len(countries)} countries")
        
        all_cities_data = []
        
        # Fetch cities for each country
        for idx, country in enumerate(countries, 1):
            country_code = country.get('countryCode')
            country_name = country.get('countryName')
            
            logger.info(f"Processing country {idx}/{len(countries)}: {country_name} ({country_code})")
            
            cities = self.get_cities_by_country(country_code)
            
            # Process and filter cities
            for city in cities:
                processed_city = self.process_city_data(city)
                
                # Filter by minimum population if specified
                if processed_city['population'] >= min_population:
                    all_cities_data.append(processed_city)
            
            logger.info(f"Total cities collected so far: {len(all_cities_data)}")
            time.sleep(0.5)  # Rate limiting between countries
        
        # Remove duplicates based on geonameId
        unique_cities = {city['geonameId']: city for city in all_cities_data}
        final_cities = list(unique_cities.values())
        
        # Sort by country and then by city name
        final_cities.sort(key=lambda x: (x['countryCode'], x['city']))
        
        # Save to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_cities, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Successfully saved {len(final_cities)} unique cities to {output_file}")
        
        # Print summary statistics
        self.print_summary(final_cities)
    
    def print_summary(self, cities: List[Dict]):
        """Print summary statistics"""
        countries = set(city['countryCode'] for city in cities)
        logger.info(f"\n--- Summary ---")
        logger.info(f"Total unique cities: {len(cities)}")
        logger.info(f"Total countries covered: {len(countries)}")
        logger.info(f"Average cities per country: {len(cities) / len(countries):.2f}")


if __name__ == "__main__":
    # IMPORTANT: Replace 'divyesh' with your actual GeoNames username
    # Register for free at: http://www.geonames.org/login
    USERNAME = "divyesh"
    
    scraper = GeoNamesCityScraper(username=USERNAME)
    
    # Fetch all cities (you can set min_population to filter smaller places)
    # For example: min_population=1000 will only include cities with 1000+ people
    scraper.fetch_all_cities(
        output_file='cities.json',
        min_population=0  # Set to 0 to get ALL populated places
    )
    
    print("\nDone! Check cities.json for the results.")