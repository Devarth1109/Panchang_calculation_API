"""
Choghadiya Calculator

Choghadiya (also spelled Chogadia) is a Vedic Hindu almanac (Panchang) method
to calculate auspicious time muhurta for starting new work or journey.

The day (sunrise to sunset) and night (sunset to next sunrise) are each 
divided into 8 equal parts called Choghadiya.

Each weekday has a specific sequence of Choghadiya starting from sunrise.
"""

import datetime
import math


# Choghadiya names with their qualities
CHOGHADIYA_QUALITY = {
    "Udvega": "Bad",
    "Chara": "Neutral",
    "Labha": "Gain",
    "Amrita": "Best",
    "Kala": "Loss",
    "Shubha": "Good",
    "Roga": "Evil"
}

# Day Choghadiya sequence for each weekday (0=Sunday, 1=Monday, etc.)
# Starting from sunrise - corrected based on traditional Panchang
DAY_CHOGHADIYA_SEQUENCE = {
    0: ["Shubha", "Roga", "Udvega", "Chara", "Labha", "Amrita", "Kala", "Shubha"],      # Sunday
    1: ["Amrita", "Kala", "Shubha", "Roga", "Udvega", "Chara", "Labha", "Amrita"],      # Monday
    2: ["Roga", "Udvega", "Chara", "Labha", "Amrita", "Kala", "Shubha", "Roga"],        # Tuesday
    3: ["Labha", "Amrita", "Kala", "Shubha", "Roga", "Udvega", "Chara", "Labha"],       # Wednesday
    4: ["Shubha", "Roga", "Udvega", "Chara", "Labha", "Amrita", "Kala", "Shubha"],      # Thursday
    5: ["Chara", "Labha", "Amrita", "Kala", "Shubha", "Roga", "Udvega", "Chara"],       # Friday
    6: ["Kala", "Shubha", "Roga", "Udvega", "Chara", "Labha", "Amrita", "Kala"],        # Saturday
}

# Night Choghadiya sequence for each weekday (0=Sunday, 1=Monday, etc.)
# Starting from sunset - corrected based on traditional Panchang
NIGHT_CHOGHADIYA_SEQUENCE = {
    0: ["Roga", "Kala", "Labha", "Udvega", "Shubha", "Amrita", "Chara", "Roga"],        # Sunday night
    1: ["Chara", "Roga", "Kala", "Labha", "Udvega", "Shubha", "Amrita", "Chara"],       # Monday night
    2: ["Kala", "Labha", "Udvega", "Shubha", "Amrita", "Chara", "Roga", "Kala"],        # Tuesday night
    3: ["Udvega", "Shubha", "Amrita", "Chara", "Roga", "Kala", "Labha", "Udvega"],      # Wednesday night
    4: ["Labha", "Udvega", "Shubha", "Amrita", "Chara", "Roga", "Kala", "Labha"],       # Thursday night
    5: ["Roga", "Kala", "Labha", "Udvega", "Shubha", "Amrita", "Chara", "Roga"],        # Friday night
    6: ["Amrita", "Chara", "Roga", "Kala", "Labha", "Udvega", "Shubha", "Amrita"],      # Saturday night
}


class ChoghadiyaCalculator:
    """Calculate Choghadiya muhurta for a given date and location."""
    
    def __init__(self):
        pass
    
    def calculate_sunrise_sunset(self, year, month, day, lat, lon, tz_offset):
        """
        Calculate sunrise and sunset times for a given date and location.
        Uses the standard astronomical algorithm.
        
        Returns:
            tuple: (sunrise_hour, sunrise_min, sunset_hour, sunset_min)
        """
        import math
        
        # Day of year
        n1 = math.floor(275 * month / 9)
        n2 = math.floor((month + 9) / 12)
        n3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
        day_of_year = n1 - (n2 * n3) + day - 30
        
        # Convert longitude to hour value
        lng_hour = lon / 15.0
        
        # Sunrise calculation
        t_rise = day_of_year + ((6 - lng_hour) / 24)
        
        # Sun's mean anomaly
        m_rise = (0.9856 * t_rise) - 3.289
        
        # Sun's true longitude
        l_rise = m_rise + (1.916 * math.sin(math.radians(m_rise))) + \
                 (0.020 * math.sin(math.radians(2 * m_rise))) + 282.634
        l_rise = l_rise % 360
        
        # Sun's right ascension
        ra_rise = math.degrees(math.atan(0.91764 * math.tan(math.radians(l_rise))))
        ra_rise = ra_rise % 360
        
        # Right ascension adjustment
        l_quad = (math.floor(l_rise / 90)) * 90
        ra_quad = (math.floor(ra_rise / 90)) * 90
        ra_rise = ra_rise + (l_quad - ra_quad)
        ra_rise = ra_rise / 15
        
        # Sun's declination
        sin_dec = 0.39782 * math.sin(math.radians(l_rise))
        cos_dec = math.cos(math.asin(sin_dec))
        
        # Sun's local hour angle for sunrise
        zenith = 90.833  # Official zenith for sunrise/sunset
        cos_h = (math.cos(math.radians(zenith)) - (sin_dec * math.sin(math.radians(lat)))) / \
                (cos_dec * math.cos(math.radians(lat)))
        
        # Clamp cos_h to valid range
        cos_h = max(-1, min(1, cos_h))
        
        # Sunrise hour angle
        h_rise = 360 - math.degrees(math.acos(cos_h))
        h_rise = h_rise / 15
        
        # Local mean time of sunrise
        t_rise_local = h_rise + ra_rise - (0.06571 * t_rise) - 6.622
        
        # UTC time of sunrise
        ut_rise = t_rise_local - lng_hour
        ut_rise = ut_rise % 24
        
        # Local time of sunrise
        local_rise = ut_rise + tz_offset
        local_rise = local_rise % 24
        
        sunrise_hour = int(local_rise)
        sunrise_min = int((local_rise - sunrise_hour) * 60)
        
        # Sunset calculation
        t_set = day_of_year + ((18 - lng_hour) / 24)
        m_set = (0.9856 * t_set) - 3.289
        l_set = m_set + (1.916 * math.sin(math.radians(m_set))) + \
                (0.020 * math.sin(math.radians(2 * m_set))) + 282.634
        l_set = l_set % 360
        
        ra_set = math.degrees(math.atan(0.91764 * math.tan(math.radians(l_set))))
        ra_set = ra_set % 360
        l_quad = (math.floor(l_set / 90)) * 90
        ra_quad = (math.floor(ra_set / 90)) * 90
        ra_set = ra_set + (l_quad - ra_quad)
        ra_set = ra_set / 15
        
        sin_dec = 0.39782 * math.sin(math.radians(l_set))
        cos_dec = math.cos(math.asin(sin_dec))
        
        cos_h = (math.cos(math.radians(zenith)) - (sin_dec * math.sin(math.radians(lat)))) / \
                (cos_dec * math.cos(math.radians(lat)))
        cos_h = max(-1, min(1, cos_h))
        
        h_set = math.degrees(math.acos(cos_h))
        h_set = h_set / 15
        
        t_set_local = h_set + ra_set - (0.06571 * t_set) - 6.622
        ut_set = t_set_local - lng_hour
        ut_set = ut_set % 24
        
        local_set = ut_set + tz_offset
        local_set = local_set % 24
        
        sunset_hour = int(local_set)
        sunset_min = int((local_set - sunset_hour) * 60)
        
        return (sunrise_hour, sunrise_min, sunset_hour, sunset_min)
    
    def _time_to_minutes(self, hour, minute):
        """Convert time to total minutes from midnight."""
        return hour * 60 + minute
    
    def _minutes_to_time(self, total_minutes):
        """Convert total minutes to hour and minute."""
        total_minutes = total_minutes % (24 * 60)
        hour = int(total_minutes // 60)
        minute = int(total_minutes % 60)
        return hour, minute
    
    def _format_time_12h(self, hour, minute):
        """Format time in 12-hour format with AM/PM."""
        period = "AM" if hour < 12 else "PM"
        display_hour = hour % 12
        if display_hour == 0:
            display_hour = 12
        return f"{display_hour:02d}:{minute:02d} {period}"
    
    def calculate(self, year, month, day, lat, lon, tz_offset, tz_name=None):
        """
        Calculate Choghadiya for a given date and location.
        
        Args:
            year: Year
            month: Month (1-12)
            day: Day (1-31)
            lat: Latitude
            lon: Longitude
            tz_offset: Timezone offset in hours (e.g., 5.5 for IST)
            tz_name: Timezone name (e.g., "Asia/Kolkata") - optional
        
        Returns:
            dict: Complete Choghadiya information
        """
        # Get weekday (0=Monday in Python, we need 0=Sunday)
        date = datetime.date(year, month, day)
        weekday = (date.weekday() + 1) % 7  # Convert to 0=Sunday
        
        # Calculate sunrise and sunset
        sunrise_h, sunrise_m, sunset_h, sunset_m = self.calculate_sunrise_sunset(
            year, month, day, lat, lon, tz_offset
        )
        
        # Calculate next day sunrise for night choghadiya
        next_date = date + datetime.timedelta(days=1)
        next_sunrise_h, next_sunrise_m, _, _ = self.calculate_sunrise_sunset(
            next_date.year, next_date.month, next_date.day, lat, lon, tz_offset
        )
        
        # Day duration in minutes
        sunrise_minutes = self._time_to_minutes(sunrise_h, sunrise_m)
        sunset_minutes = self._time_to_minutes(sunset_h, sunset_m)
        day_duration = sunset_minutes - sunrise_minutes
        
        # Night duration in minutes (sunset to next sunrise)
        # Next sunrise is on the next day, so add 24*60 minutes
        next_sunrise_minutes = self._time_to_minutes(next_sunrise_h, next_sunrise_m) + (24 * 60)
        night_duration = next_sunrise_minutes - sunset_minutes
        
        # Each choghadiya duration
        day_choghadiya_duration = day_duration / 8
        night_choghadiya_duration = night_duration / 8
        
        # Get choghadiya sequences for the day
        day_sequence = DAY_CHOGHADIYA_SEQUENCE[weekday]
        night_sequence = NIGHT_CHOGHADIYA_SEQUENCE[weekday]
        
        # Calculate day choghadiya periods
        day_choghadiya = []
        for i in range(8):
            start_minutes = sunrise_minutes + (i * day_choghadiya_duration)
            end_minutes = start_minutes + day_choghadiya_duration
            
            start_h, start_m = self._minutes_to_time(start_minutes)
            end_h, end_m = self._minutes_to_time(end_minutes)
            
            name = day_sequence[i]
            
            day_choghadiya.append({
                "name": name,
                "quality": CHOGHADIYA_QUALITY[name],
                "start_time": self._format_time_12h(start_h, start_m),
                "end_time": self._format_time_12h(end_h, end_m)
            })
        
        # Calculate night choghadiya periods
        night_choghadiya = []
        for i in range(8):
            start_minutes = sunset_minutes + (i * night_choghadiya_duration)
            end_minutes = start_minutes + night_choghadiya_duration
            
            # Handle day overflow
            start_h, start_m = self._minutes_to_time(start_minutes)
            end_h, end_m = self._minutes_to_time(end_minutes)
            
            # Check if end time is on next day
            is_next_day = end_minutes >= 24 * 60
            
            name = night_sequence[i]
            
            # Format end time with next day indicator
            end_time_12h = self._format_time_12h(end_h, end_m)
            if is_next_day:
                end_time_12h += f", {next_date.strftime('%b %d')}"
            
            night_choghadiya.append({
                "name": name,
                "quality": CHOGHADIYA_QUALITY[name],
                "start_time": self._format_time_12h(start_h, start_m),
                "end_time": end_time_12h
            })
        
        return {
            "sunrise": self._format_time_12h(sunrise_h, sunrise_m),
            "sunset": self._format_time_12h(sunset_h, sunset_m),
            "day_choghadiya": day_choghadiya,
            "night_choghadiya": night_choghadiya
        }
