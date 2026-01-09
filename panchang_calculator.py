import sankranti
from sankranti import Date, Place, gregorian_to_jd, jd_to_gregorian, to_dms, swe
from math import ceil
import datetime

# Import data dictionaries
from religious_data import TITHI_NAMES, PAKSHA, NAKSHATRA_NAMES, YOGA_NAMES, RASHI_NAMES, VARA_NAMES, SAMVAT_YEAR_NAMES, KARANA_NAMES

# =============================================================================
# DATA TABLES FROM calculation_formula.txt
# =============================================================================

# Varjyam start times in HOURS from nakshatra start (for a 24-hour nakshatra)
# Values from calculation_formula.txt - Table of Amrita Gadiyas and Varjyam
VARJYAM_START_HOURS = {
    1: 20.0,   # Aswini
    2: 9.6,    # Bharani
    3: 12.0,   # Krittika
    4: 16.0,   # Rohini
    5: 5.6,    # Mrigasira
    6: 8.4,    # Aridra
    7: 12.0,   # Punarvasu
    8: 8.0,    # Pushya
    9: 12.8,   # Aslesha
    10: 12.0,  # Makha
    11: 8.0,   # Pubba (Purva Phalguni)
    12: 7.2,   # Uttara (Uttara Phalguni)
    13: 8.4,   # Hasta
    14: 8.0,   # Chitta
    15: 5.6,   # Swati
    16: 5.6,   # Visakha
    17: 4.0,   # Anuradha
    18: 5.6,   # Jyeshta
    19: 8.0,   # Moola (Note: also has 22.4 in some traditions)
    20: 9.6,   # Poorvashadha
    21: 8.0,   # Uttarashadha
    22: 4.0,   # Sravana
    23: 4.0,   # Dhanishta
    24: 7.2,   # Satabhisha
    25: 6.4,   # Poorvabhadra
    26: 9.6,   # Uttarabhadra
    27: 12.0   # Revati
}

# Amrit Kalam start times in HOURS from nakshatra start (for a 24-hour nakshatra)
# Values from calculation_formula.txt - Table of Amrita Gadiyas and Varjyam
AMRIT_KALAM_START_HOURS = {
    1: 16.8,   # Aswini
    2: 19.2,   # Bharani
    3: 21.6,   # Krittika
    4: 20.8,   # Rohini
    5: 15.2,   # Mrigasira
    6: 14.0,   # Aridra
    7: 21.6,   # Punarvasu
    8: 17.6,   # Pushya
    9: 22.4,   # Aslesha
    10: 21.6,  # Makha
    11: 17.6,  # Pubba (Purva Phalguni)
    12: 16.8,  # Uttara (Uttara Phalguni)
    13: 18.0,  # Hasta
    14: 17.6,  # Chitta
    15: 15.2,  # Swati
    16: 15.2,  # Visakha
    17: 13.6,  # Anuradha
    18: 15.2,  # Jyeshta
    19: 17.6,  # Moola
    20: 19.2,  # Poorvashadha
    21: 17.6,  # Uttarashadha
    22: 13.6,  # Sravana
    23: 13.6,  # Dhanishta
    24: 16.8,  # Satabhisha
    25: 16.0,  # Poorvabhadra
    26: 19.2,  # Uttarabhadra
    27: 21.6   # Revati
}
# NOTE: Values from calculation_formula.txt - Table of Amrita Gadiyas

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def format_time_12hr(dms_list, include_date=False, ref_date=None):
    """Converts [H, M, S] list to 12-hour format with AM/PM."""
    h, m, s = dms_list
    day_offset = 0
    if h >= 24:
        day_offset = int(h // 24)
        h = h % 24
    
    # Convert to 12-hour format
    period = "AM" if h < 12 else "PM"
    h_12 = h if h <= 12 else h - 12
    if h_12 == 0:
        h_12 = 12
    
    time_str = f"{int(h_12):02d}:{int(m):02d} {period}"
    
    if include_date and day_offset > 0 and ref_date:
        # Add date information
        next_date = ref_date + datetime.timedelta(days=day_offset)
        time_str += f", {MONTH_NAMES[next_date.month-1]} {next_date.day:02d}"
    
    return time_str

def format_time_range_12hr(start_dms, end_dms, ref_date=None):
    """Formats a time range in 12-hour format."""
    start_h, start_m, start_s = start_dms
    end_h, end_m, end_s = end_dms
    
    # Check if start time is next day (hours >= 24)
    start_day_offset = 0
    if start_h >= 24:
        start_day_offset = int(start_h // 24)
        start_h = start_h % 24
    
    # Check if end time is next day
    end_day_offset = 0
    if end_h >= 24:
        end_day_offset = int(end_h // 24)
        end_h = end_h % 24
    
    # Format start time
    start_period = "AM" if start_h < 12 else "PM"
    start_h_12 = start_h if start_h <= 12 else start_h - 12
    if start_h_12 == 0:
        start_h_12 = 12
    start_str = f"{int(start_h_12):02d}:{int(start_m):02d} {start_period}"
    
    # Add date to start time if it's on a different day
    if start_day_offset > 0 and ref_date:
        start_date = ref_date + datetime.timedelta(days=start_day_offset)
        start_str += f", {MONTH_NAMES[start_date.month-1]} {start_date.day:02d}"
    
    # Format end time
    end_period = "AM" if end_h < 12 else "PM"
    end_h_12 = end_h if end_h <= 12 else end_h - 12
    if end_h_12 == 0:
        end_h_12 = 12
    end_str = f"{int(end_h_12):02d}:{int(end_m):02d} {end_period}"
    
    # Add date to end time if it's on a different day
    if end_day_offset > 0 and ref_date:
        end_date = ref_date + datetime.timedelta(days=end_day_offset)
        end_str += f", {MONTH_NAMES[end_date.month-1]} {end_date.day:02d}"
    
    return f"{start_str} to {end_str}"

def format_dms_time(dms_list):
    """Converts [H, M, S] list to HH:MM:SS string."""
    h, m, s = dms_list
    day_offset = 0
    if h >= 24:
        day_offset = int(h // 24)
        h = h % 24
    
    time_str = f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
    if day_offset > 0:
        time_str += f" (+{day_offset})"
    return time_str

def jd_to_time_str(jd_ut, tz):
    """Converts JD (UT) to Local Time String HH:MM:SS."""
    local_jd = jd_ut + (tz / 24.0)
    g = sankranti.jd_to_gregorian(local_jd) # (y,m,d,h,min,s)
    h_flt = g[3] + g[4]/60.0 + g[5]/3600.0
    h = int(h_flt)
    m = int((h_flt - h) * 60)
    s = int(((h_flt - h) * 60 - m) * 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def jd_to_time_12hr(jd_ut, tz, ref_date):
    """Converts JD (UT) to 12-hour format with AM/PM and date if needed."""
    local_jd = jd_ut + (tz / 24.0)
    g = sankranti.jd_to_gregorian(local_jd)
    h_flt = g[3] + g[4]/60.0 + g[5]/3600.0
    h = int(h_flt)
    m = int((h_flt - h) * 60)
    
    # Calculate date difference correctly
    current_date = datetime.date(g[0], g[1], g[2])
    day_offset = (current_date - ref_date).days
    
    # Convert to 12-hour format
    period = "AM" if h < 12 else "PM"
    h_12 = h if h <= 12 else h - 12
    if h_12 == 0:
        h_12 = 12
    
    time_str = f"{int(h_12):02d}:{int(m):02d} {period}"
    
    if day_offset > 0:
        time_str += f", {MONTH_NAMES[current_date.month-1]} {current_date.day:02d}"
    
    return time_str

def get_pravishte(jd, place):
    """
    Calculate Pravishte/Gate: days since Sun entered current rashi (1-indexed)
    
    Per calculation_formula.txt:
    - Rashi (sign) is determined by Sun's Nirayana longitude
    - Each rashi is 30 degrees
    - Pravishte = number of days since Sun entered current rashi
    """
    # Get timezone from place
    tz = place[2] if isinstance(place, tuple) else place.timezone
    
    # Get sun's current sidereal longitude
    sun_long = sankranti.solar_longitude(jd)
    current_rasi_index = int(sun_long / 30)  # 0-11
    
    # Find when sun entered current rashi (the degree at which this rashi starts)
    target_long = current_rasi_index * 30  # e.g., Aries=0, Taurus=30, etc.
    
    # Search backwards to find the exact ingress time
    def func(t):
        s = sankranti.solar_longitude(t)
        # Handle wrap-around for Aries (0 degrees)
        if current_rasi_index == 0:
            # For Aries, sun crosses from ~360 to 0
            if s > 180:
                return s - 360
            return s
        return sankranti.norm180(s - target_long)
    
    # Search backwards up to 32 days
    try:
        ingress_jd = sankranti.bisection_search(func, jd - 32, jd)
    except:
        # If search fails, estimate based on average sun motion (~1 degree/day)
        degrees_into_sign = sun_long - target_long
        ingress_jd = jd - degrees_into_sign
    
    # Calculate days since ingress
    ingress_date = sankranti.jd_to_gregorian(ingress_jd + tz/24.0)
    current_date = sankranti.jd_to_gregorian(jd + tz/24.0)
    d1 = datetime.date(ingress_date[0], ingress_date[1], ingress_date[2])
    d2 = datetime.date(current_date[0], current_date[1], current_date[2])
    
    # Return days since sun entered current rashi (1-indexed)
    return (d2 - d1).days + 1

def find_end_time(jd, func_current, current_val, steps_per_circle):
    """
    Finds when the function changes value (integer part + 1).
    func_current: returns floating point 'index' or 'phase'.
    current_val: int (current index).
    """
    target = current_val # e.g. Tithi 1 -> End is when value becomes 2 (or wrap)
    # Tithi: 1..30. Phase 0..360.
    # Tithi = ceil(phase/12). 
    # Logic: Finding when phase crosses (current_val * step).
    pass

class PanchangCalculator:
    def __init__(self):
        # Ensure Lahiri Ayanamsa (Chitrapaksha) is used, matching DrikPanchang
        sankranti.set_ayanamsa_mode()
        pass
        
    def calculate(self, year, month, day, hour, minute, second, lat, lon, info_timezone):
        # Use IST timezone for all calculations and display
        # Note: Traditional Hindu astronomy uses LMT (longitude/15) for calculations,
        # but modern panchangs typically show IST for consistency
        place = Place(lat, lon, info_timezone)
        
        # 1. JD for Start of Day (UTC Midnight)
        jd_midnight = sankranti.gregorian_to_jd(Date(year, month, day))
        
        # 2. JD for Current Moment
        jd_now = sankranti.local_time_to_jdut1(year, month, day, hour, minute, second, info_timezone)
        
        result = {}
        ref_date = datetime.date(year, month, day)
        
        # Rise/Set times
        sr_info = sankranti.sunrise(jd_midnight, place)
        ss_info = sankranti.sunset(jd_midnight, place)
        mr_val = sankranti.moonrise(jd_midnight, place)
        ms_val = sankranti.moonset(jd_midnight, place)
        
        result['Sunrise'] = format_time_12hr(sr_info[1])
        result['Sunset'] = format_time_12hr(ss_info[1])
        
        # Calculate sunrise hours for comparison
        sunrise_hours = sr_info[1][0] + sr_info[1][1]/60 + sr_info[1][2]/3600
        sunset_hours = ss_info[1][0] + ss_info[1][1]/60 + ss_info[1][2]/3600
        
        # Handle moonrise - check if it's too close to sunrise (within 2 minutes)
        # When moonrise is essentially at sunrise, it's not a distinct visible event
        # Also handle cases where moonrise is out of valid range
        if mr_val[0] < 0 or mr_val[0] >= 48:
            result['Moonrise'] = "No Moonrise"
        else:
            moonrise_hours = mr_val[0] + mr_val[1]/60 + mr_val[2]/3600
            # Check if moonrise is within 2 minutes of sunrise
            diff_minutes = abs(moonrise_hours - sunrise_hours) * 60
            if diff_minutes < 2:
                result['Moonrise'] = "No Moonrise"
            else:
                result['Moonrise'] = format_time_12hr(mr_val, include_date=True, ref_date=ref_date)
        
        # Handle moonset - check if it falls within the current Hindu day
        # Hindu day runs from sunrise to next sunrise
        # If moonset is on the next calendar day, check if it's before next day's sunrise
        if ms_val[0] < 0 or ms_val[0] >= 36:
            result['Moonset'] = "No Moonset"
        else:
            moonset_hours = ms_val[0] + ms_val[1]/60 + ms_val[2]/3600
            
            # If moonset is after 24 hours (next calendar day)
            if moonset_hours >= 24:
                # Get next day's sunrise
                next_day = datetime.date(year, month, day) + datetime.timedelta(days=1)
                jd_next = sankranti.gregorian_to_jd(next_day)
                sr_next = sankranti.sunrise(jd_next, place)
                sunrise_next_hours = sr_next[1][0] + sr_next[1][1]/60 + sr_next[1][2]/3600
                
                # Convert moonset to next day's time (subtract 24)
                moonset_next_day_hours = moonset_hours - 24
                
                # If moonset is after next day's sunrise, it doesn't belong to current Hindu day
                if moonset_next_day_hours >= sunrise_next_hours:
                    result['Moonset'] = "No Moonset"
                else:
                    result['Moonset'] = format_time_12hr(ms_val, include_date=True, ref_date=ref_date)
            else:
                result['Moonset'] = format_time_12hr(ms_val, include_date=True, ref_date=ref_date)
        
        # Samvats/Months need Tithi info based on Sunrise
        masa_info = sankranti.masa(jd_midnight, place, amanta=True)
        masa_num, is_leap = masa_info[0], masa_info[1]
        kali, saka = sankranti.elapsed_year(jd_midnight, masa_num)
        vikram = saka + 135
        
        # Gujarati
        tithi_at_rise = sankranti.tithi(jd_midnight, place)[0]
        gujarati = vikram - 1
        if masa_num > 8: gujarati = vikram
        elif masa_num == 8 and tithi_at_rise <= 15: gujarati = vikram
        
        # The 60-year cycle name changes at Chaitra Shukla Pratipada (Hindu New Year)
        # For months before Chaitra (Magha=11, Phalguna=12), use previous year's cycle position
        # Chaitra is month 1, so months 11 and 12 are before the new year
        
        # Shaka Samvat - the library's elapsed_year already returns the correct year
        # accounting for months before Chaitra, so we just use a constant offset of 11
        saka_cycle_idx = (saka + 11) % 60
        
        # Vikram Samvat - Use constant offset of 9 for 60-year cycle name
        # The year number (vikram) already accounts for Hindu New Year transition
        # 2080 -> Anala (49), 2081 -> Pingala (50), etc.
        vikram_cycle_idx = (vikram + 9) % 60
        
        # Gujarati Samvat
        gujarati_cycle_idx = (gujarati + 8) % 60
        
        result['Shaka Samvat'] = f"{saka} {SAMVAT_YEAR_NAMES[saka_cycle_idx]}"
        result['Vikram Samvat'] = f"{vikram} {SAMVAT_YEAR_NAMES[vikram_cycle_idx]}"
        result['Gujarati Samvat'] = f"{gujarati} {SAMVAT_YEAR_NAMES[gujarati_cycle_idx]}"
        
        months_list = ["Chaitra", "Vaisakha", "Jyeshtha", "Ashadha", "Shravana", "Bhadrapada", "Ashwina", "Kartika", "Margashirsha", "Pausha", "Magha", "Phalguni"]
        def get_mname(num, leap): return f"{months_list[num-1]} (Adhik)" if leap else months_list[num-1]
        
        result['Amanta Month'] = get_mname(masa_num, is_leap)
        
        # Purnimanta month calculation:
        # In Purnimanta system, month ends on Purnima (full moon), so:
        # - Krishna Paksha comes FIRST in the month
        # - Shukla Paksha comes SECOND in the month
        # 
        # Relationship to Amanta:
        # - During Shukla Paksha (tithi 1-15): Purnimanta = Amanta (same month)
        # - During Krishna Paksha (tithi 16-30): Purnimanta = Amanta + 1 (next month)
        #
        # In adhik masa, both systems show the same adhik month
        if is_leap:
            result['Purnimanta Month'] = get_mname(masa_num, is_leap)
        else:
            # Check if we're in Shukla or Krishna Paksha
            is_shukla_paksha = tithi_at_rise <= 15
            
            if is_shukla_paksha:
                # Shukla Paksha: Purnimanta = Amanta (same month)
                purnimanta_month = masa_num
                purnimanta_leap = is_leap
            else:
                # Krishna Paksha: Purnimanta = Amanta + 1 (next month)
                purnimanta_month = (masa_num % 12) + 1
                purnimanta_leap = False  # Next month is not adhik
            
            result['Purnimanta Month'] = get_mname(purnimanta_month, purnimanta_leap)
        
        result['Weekday'] = VARA_NAMES[sankranti.vaara(jd_midnight)]['sanskrit']
        
        # Use sankranti functions for Tithi, Nakshatra, Yoga, Karana
        # These calculate at sunrise and return end times
        # They can return 2 or 4 elements if there's a skipped/overlapping value
        tithi_data = sankranti.tithi(jd_midnight, place)
        nakshatra_data = sankranti.nakshatra(jd_midnight, place)
        yoga_data = sankranti.yoga(jd_midnight, place)
        karana_data = sankranti.karana(jd_midnight, place)
        
        # Format Tithi (can have 2 tithis if one ends during the day)
        tithi_num = tithi_data[0]
        tithi_end_time = tithi_data[1]
        result['Paksha'] = "Shukla Paksha" if tithi_num <= 15 else "Krishna Paksha"
        t_name = TITHI_NAMES[tithi_num]['english']
        
        # Convert end time to hours for comparison
        end_hours = tithi_end_time[0] + tithi_end_time[1]/60.0
        sunrise_hours = sr_info[1][0] + sr_info[1][1]/60.0
        sunset_hours = ss_info[1][0] + ss_info[1][1]/60.0
        
        # Show end time if it's during the panchang day (sunrise to next sunrise, i.e., within ~24 hours)
        if end_hours < 24 + sunrise_hours:  # Ends before next sunrise
            result['Tithi'] = f"{t_name} upto {format_time_12hr(tithi_end_time, include_date=True, ref_date=ref_date)}"
            # Add the next tithi if end time is before midnight or early next day
            if end_hours < 24:
                next_tithi_num = (tithi_num % 30) + 1
                next_t_name = TITHI_NAMES[next_tithi_num]['english']
                result['Tithi'] += f"; {next_t_name}"
        else:
            # Tithi prevails the whole day
            result['Tithi'] = t_name
        
        # Format Nakshatra
        nak_num = nakshatra_data[0]
        nak_end_time = nakshatra_data[1]
        nak_name = NAKSHATRA_NAMES[nak_num-1]['english']
        
        # Convert end time to hours for comparison
        nak_end_hours = nak_end_time[0] + nak_end_time[1]/60.0
        
        # Check if nakshatra changes during the day (between sunrise and early next morning up to 30 hours)
        if sunrise_hours <= nak_end_hours < 30 or nak_end_hours < sunrise_hours:
            result['Nakshatra'] = f"{nak_name} upto {format_time_12hr(nak_end_time, include_date=True, ref_date=ref_date)}"
            # Add the next nakshatra
            next_nak_num = (nak_num % 27) + 1
            next_nak_name = NAKSHATRA_NAMES[next_nak_num-1]['english']
            result['Nakshatra'] += f"; {next_nak_name}"
        else:
            # Nakshatra prevails the whole day
            result['Nakshatra'] = nak_name
        
        # Format Yoga
        yoga_num = yoga_data[0]
        yoga_end_time = yoga_data[1]
        y_name = YOGA_NAMES[yoga_num-1]['english']
        
        # Convert end time to hours for comparison
        yoga_end_hours = yoga_end_time[0] + yoga_end_time[1]/60.0
        
        # Show end time if yoga ends within the panchang day (sunrise to next sunrise ~30 hours)
        if yoga_end_hours < 30:
            result['Yoga'] = f"{y_name} upto {format_time_12hr(yoga_end_time, include_date=True, ref_date=ref_date)}"
            # Add the next yoga if it starts before next sunrise
            if yoga_end_hours < 24 + sunrise_hours:
                next_yoga_num = (yoga_num % 27) + 1
                next_y_name = YOGA_NAMES[next_yoga_num-1]['english']
                result['Yoga'] += f"; {next_y_name}"
        else:
            result['Yoga'] = y_name
        
        # Format Karana
        def get_karana_name(num):
            if num == 1: return "Kimstughna"
            elif num >= 58:
                if num == 58: return "Shakuni"
                elif num == 59: return "Chatushpada"
                elif num == 60: return "Naga"
            else:
                idx = (num - 2) % 7
                name = KARANA_NAMES[idx]
                # Fix spelling: Gara -> Garaja
                if name == "Gara":
                    name = "Garaja"
                return name
        
        # Sunrise time in fractional hours (for comparison)
        sunrise_hours = sr_info[1][0] + sr_info[1][1]/60.0 + sr_info[1][2]/3600.0
        
        # Filter karanas - only include those that end at or after sunrise, and remove duplicates
        karana_list = []
        seen_karanas = set()
        for i in range(0, len(karana_data), 2):
            if i+1 < len(karana_data):
                k_num = karana_data[i]
                k_end = karana_data[i+1]
                k_end_hours = k_end[0] + k_end[1]/60.0 + k_end[2]/3600.0
                
                # Include karana if it ends at or after sunrise and not already seen
                if k_end_hours >= sunrise_hours and k_num not in seen_karanas:
                    karana_list.append((k_num, k_end, k_end_hours))
                    seen_karanas.add(k_num)
        
        # Sort karanas by end time
        karana_list.sort(key=lambda x: x[2])
        
        # Format the karanas
        if karana_list:
            # First karana
            karana_num, karana_end_time, _ = karana_list[0]
            kn = get_karana_name(karana_num)
            result['Karana'] = f"{kn} upto {format_time_12hr(karana_end_time, include_date=True, ref_date=ref_date)}"
            
            # Add second karana if present and within the day
            if len(karana_list) >= 2:
                karana_num2, karana_end_time2, k2_hours = karana_list[1]
                kn2 = get_karana_name(karana_num2)
                # Only show if ends within reasonable timeframe (before midnight or early next morning)
                if k2_hours < 24:  # Ends same day
                    result['Karana'] += f"; {kn2} upto {format_time_12hr(karana_end_time2, include_date=True, ref_date=ref_date)}"
                elif k2_hours < 30:  # Ends early next morning (before 6 AM next day assuming ~6 AM sunrise)
                    result['Karana'] += f"; {kn2} upto {format_time_12hr(karana_end_time2, include_date=True, ref_date=ref_date)}"
                else:
                    result['Karana'] += f"; {kn2}"
            else:
                # Add the next karana that follows
                next_karana_num = (karana_num % 60) + 1
                next_kn = get_karana_name(next_karana_num)
                result['Karana'] += f"; {next_kn}"
        else:
            result['Karana'] = "No karana data"
        
        # Pravishte - should use sunrise JD for consistency with panchang tradition
        sunrise_jd = sr_info[0]  # Use sunrise JD (local)
        result['Pravishte/Gate'] = get_pravishte(sunrise_jd, place)
        
        # Signs - use sunrise positions (panchang tradition)
        # Note: Must use UT sunrise like nakshatra() does for consistency
        sunrise_ut = sunrise_jd - info_timezone / 24.0
        result['Sunsign'] = RASHI_NAMES[int(sankranti.solar_longitude(sunrise_ut)/30)]['english']
        result['Moonsign'] = RASHI_NAMES[int(sankranti.lunar_longitude(sunrise_ut)/30)]['english']
        
        # Kalams
        rk = sankranti.rahu_kalam(jd_midnight, place)
        gk = sankranti.gulika_kalam(jd_midnight, place)
        yg = sankranti.yamaganda_kalam(jd_midnight, place)
        
        result['Rahu Kalam'] = format_time_range_12hr(rk[0], rk[1], ref_date)
        result['Gulikai Kalam'] = format_time_range_12hr(gk[0], gk[1], ref_date)
        result['Yamaganda'] = format_time_range_12hr(yg[0], yg[1], ref_date)
        
        # Abhijit Muhurta is not applicable on Wednesdays
        if sankranti.vaara(jd_midnight) == 3:
             result['Abhijit'] = "None"
        else:
            ab = sankranti.abhijit_muhurta(jd_midnight, place)
            ab_start = sankranti.to_dms(ab[0])
            ab_end = sankranti.to_dms(ab[1])
            result['Abhijit'] = format_time_range_12hr(ab_start, ab_end, ref_date)
        
        # Dur Muhurtam - Custom calculation to fix sankranti library bug
        # The sankranti library incorrectly uses day muhurta duration for night periods
        # We need to use night muhurta duration for night Dur Muhurtam
        
        # Get sunrise/sunset times in decimal hours
        sunrise_h = sr_info[1][0] + sr_info[1][1]/60.0 + sr_info[1][2]/3600.0
        sunset_h = ss_info[1][0] + ss_info[1][1]/60.0 + ss_info[1][2]/3600.0
        
        # Get next day's sunrise for night duration
        next_sr_info = sankranti.sunrise(jd_midnight + 1, place)
        next_sunrise_h = 24 + next_sr_info[1][0] + next_sr_info[1][1]/60.0 + next_sr_info[1][2]/3600.0
        
        # Calculate muhurta durations
        day_duration = sunset_h - sunrise_h
        night_duration = next_sunrise_h - sunset_h
        day_muhurta = day_duration / 15.0
        night_muhurta = night_duration / 15.0
        
        # Dur Muhurtam indices vary by weekday (0=Sunday, 1=Monday, etc.)
        # Day Dur Muhurtam (from sunrise): [muhurta_index]
        # Night Dur Muhurtam (from sunset): [muhurta_index]
        weekday = sankranti.vaara(jd_midnight)
        
        # Standard Dur Muhurtam positions (0-indexed):
        # Sunday: Day 8th (7), Night 7th (6) - but some use different
        # Monday: Day 7th (6), Night 6th (5)
        # Tuesday: Day 4th (3), Night 7th (6)
        # Wednesday: Day 5th (4), Night 5th (4)
        # Thursday: Day 6th (5), Night 6th (5)
        # Friday: Day 3rd (2), Night 3rd (2)
        # Saturday: Day 2nd (1), Night 2nd (1)
        
        # Using sankranti's muhurta indices but with correct duration
        dm_raw = sankranti.durmuhurtam(jd_midnight, place)
        
        # First Dur Muhurtam (day period) - sankranti calculates this correctly
        dm_start1 = sankranti.to_dms(dm_raw[0][0])
        dm_end1 = sankranti.to_dms(dm_raw[1][0])
        dm_str = format_time_range_12hr(dm_start1, dm_end1, ref_date)
        
        # Second Dur Muhurtam - check if it's day or night period
        if dm_raw[0][1] != 0:
            dm2_start_raw = dm_raw[0][1]
            dm2_end_raw = dm_raw[1][1]
            
            # Check if this is a nighttime period (after sunset)
            if dm2_start_raw >= sunset_h:
                # Nighttime period - recalculate with night muhurta duration
                # Sankranti uses wrong muhurta duration for night periods
                night_muhurta_index = round((dm2_start_raw - sunset_h) / night_muhurta)
                
                dm2_start_correct = sunset_h + (night_muhurta_index * night_muhurta)
                dm2_end_correct = sunset_h + ((night_muhurta_index + 1) * night_muhurta)
                
                dm_start2 = sankranti.to_dms(dm2_start_correct)
                dm_end2 = sankranti.to_dms(dm2_end_correct)
            else:
                # Daytime period - use sankranti's values as-is
                dm_start2 = sankranti.to_dms(dm2_start_raw)
                dm_end2 = sankranti.to_dms(dm2_end_raw)
            
            dm_str += f"; {format_time_range_12hr(dm_start2, dm_end2, ref_date)}"
        
        result['Dur Muhurtam'] = dm_str
        
        # Varjyam/Amrit - Calculate ONLY for nakshatra at SUNRISE (DrikPanchang convention)
        # DrikPanchang shows Varjyam/Amrit based on the sunrise nakshatra only
        sunrise_jd_ut = sr_info[0] - place.timezone/24.0
        
        # Get nakshatra at sunrise
        nak_num = nakshatra_data[0]
        
        # Find start time of current nakshatra (in UT)
        def nak_start_dist(t):
            m = sankranti.lunar_longitude(t)
            target = (nak_num - 1) * (360/27.0)
            return sankranti.norm180(m - target)
        
        # Search for nakshatra start (could be before sunrise)
        n_start_jd = sankranti.bisection_search(nak_start_dist, sunrise_jd_ut - 1.5, sunrise_jd_ut + 0.2)
        
        # Find nakshatra end time - need special handling for Revati (nakshatra 27)
        # because it ends at 360°/0° which causes wrap-around issues
        if nak_num == 27:  # Revati - ends at 360°/0°
            def nak_end_dist(t):
                m = sankranti.lunar_longitude(t)
                # For Revati ending at 360°, track when moon crosses 0°
                if m > 180:
                    return m - 360  # Negative value approaching 0
                else:
                    return m  # Positive value after crossing 0
            # Search from after sunrise forward
            n_end_jd = sankranti.bisection_search(nak_end_dist, sunrise_jd_ut + 0.1, sunrise_jd_ut + 2.0)
        else:
            def nak_end_dist(t):
                m = sankranti.lunar_longitude(t)
                target = nak_num * (360/27.0)
                return sankranti.norm180(m - target)
            # Search for nakshatra end (could be after next sunrise)
            n_end_jd = sankranti.bisection_search(nak_end_dist, sunrise_jd_ut, sunrise_jd_ut + 2.0)
        
        # Calculate for sunrise nakshatra AND the next one if it starts within the day
        nakshatras_to_calculate = [{
            'num': nak_num,
            'start_jd': n_start_jd,
            'end_jd': n_end_jd
        }]
        
        # Check if next nakshatra starts before next sunrise overlap (roughly)
        # We check if Current Nakshatra ends before next sunrise + buffer
        if n_end_jd < sunrise_jd_ut + 1.2: 
             next_nak_num = (nak_num % 27) + 1
             
             def next_nak_end_dist(t):
                m = sankranti.lunar_longitude(t)
                target = next_nak_num * (360/27.0)
                return sankranti.norm180(m - target)
                
             # Prev nak end is Next nak start
             next_n_start_jd = n_end_jd
             next_n_end_jd = sankranti.bisection_search(next_nak_end_dist, next_n_start_jd, next_n_start_jd + 1.5)
             
             nakshatras_to_calculate.append({
                 'num': next_nak_num,
                 'start_jd': next_n_start_jd,
                 'end_jd': next_n_end_jd
             })
        
        # Calculate Varjyam and Amrit Kalam for all relevant nakshatras
        varjyam_periods = []
        amrit_periods = []
        
        for nak_info in nakshatras_to_calculate:
            nak_num_calc = nak_info['num']
            n_start = nak_info['start_jd']
            n_end = nak_info['end_jd']
            
            # Get table values (both are in HOURS for a 24-hour nakshatra)
            v_start_hours = VARJYAM_START_HOURS.get(nak_num_calc, 0)
            a_start_hours = AMRIT_KALAM_START_HOURS.get(nak_num_calc, 0)
            
            duration_days = n_end - n_start
            
            # Varjyam: Formula from calculation_formula.txt
            # Starting time = Nakshatra start + (duration * X/24) where X is in hours
            # Duration = duration * 1.6/24 (1/15th of nakshatra = 1.6 hours for 24-hour nakshatra)
            v_s_ut = n_start + (duration_days * v_start_hours / 24.0)
            v_duration_days = duration_days * 1.6 / 24.0
            v_e_ut = v_s_ut + v_duration_days
            
            # Amrit Kalam: Same formula
            a_s_ut = n_start + (duration_days * a_start_hours / 24.0)
            a_duration_days = duration_days * 1.6 / 24.0
            a_e_ut = a_s_ut + a_duration_days
            
            # Only include if it occurs on the panchang day
            # Panchang day = current sunrise to next sunrise
            next_sunrise_approx = sunrise_jd_ut + 1.0
            
            # Include Varjyam only if it starts after current sunrise and before next sunrise
            if v_s_ut >= sunrise_jd_ut and v_s_ut < next_sunrise_approx:
                v_start_time = jd_to_time_12hr(v_s_ut, info_timezone, ref_date)
                v_end_time = jd_to_time_12hr(v_e_ut, info_timezone, ref_date)
                varjyam_periods.append(f"{v_start_time} to {v_end_time}")
            
            # Include Amrit Kalam only if it starts after current sunrise and before next sunrise
            if a_s_ut >= sunrise_jd_ut and a_s_ut < next_sunrise_approx:
                a_start_time = jd_to_time_12hr(a_s_ut, info_timezone, ref_date)
                a_end_time = jd_to_time_12hr(a_e_ut, info_timezone, ref_date)
                amrit_periods.append(f"{a_start_time} to {a_end_time}")
        
        # Join multiple periods with semicolon
        result['Varjyam'] = "; ".join(varjyam_periods) if varjyam_periods else "None"
        result['Amrit Kalam'] = "; ".join(amrit_periods) if amrit_periods else "None"
        
        return result

if __name__ == "__main__":
    c = PanchangCalculator()
    
    print("=" * 60)
    print("Delhi - January 8, 2026")
    print("=" * 60)
    res = c.calculate(2026, 1, 8, 6, 0, 0, 28.6139, 77.2090, 5.5)
    for k, v in res.items():
        print(f"{k}: {v}")
