import sankranti
from sankranti import Date, Place, gregorian_to_jd, jd_to_gregorian, to_dms, swe
from math import ceil, floor
import datetime

# Import data dictionaries
from religious_data import TITHI_NAMES, NAKSHATRA_NAMES, YOGA_NAMES, RASHI_NAMES, VARA_NAMES, KARANA_NAMES

# Import Varjyam and Amrit Kalam tables from main panchang calculator
from panchang_calculator import VARJYAM_START_HOURS, AMRIT_KALAM_START_HOURS

# Marathi-specific month names (Amanta system - New Moon to New Moon)
MARATHI_MONTH_NAMES = [
    "Chaitra", "Vaishakh", "Jyeshtha", "Ashadh", 
    "Shravan", "Bhadrapad", "Ashwin", "Kartik", 
    "Margashirsh", "Paush", "Magh", "Phalgun"
]

# Marathi Paksha names
MARATHI_PAKSHA = {
    "shukla": "Shukla Paksha",
    "krishna": "Krishna Paksha"
}

# Marathi weekday names
MARATHI_VARA = [
    "Ravivaar", "Somvaar", "Mangalvaar", "Budhvaar",
    "Guruvaar", "Shukravaar", "Shanivaar"
]

# Shaka Samvat year names (60-year cycle)
SHAKA_SAMVAT_NAMES = [
    "Prabhava", "Vibhava", "Shukla", "Pramoda", "Prajapati",
    "Angirasa", "Shrimukha", "Bhava", "Yuva", "Dhatri",
    "Ishvara", "Bahudhanya", "Pramathi", "Vikrama", "Vrisha",
    "Chitrabhanu", "Subhanu", "Tarana", "Parthiva", "Vyaya",
    "Sarvajit", "Sarvadharin", "Virodhin", "Vikrita", "Khara",
    "Nandana", "Vijaya", "Jaya", "Manmatha", "Durmukha",
    "Hemalamba", "Vilamba", "Vikarin", "Sharvari", "Plava",
    "Shubhakrit", "Shobhana", "Krodhin", "Vishvavasu", "Parabhava",
    "Plavanga", "Kilaka", "Saumya", "Sadharana", "Virodhikrit",
    "Paridhavi", "Pramadin", "Ananda", "Rakshasa", "Anala",
    "Pingala", "Kalayukta", "Siddharthi", "Raudra", "Durmati",
    "Dundubhi", "Rudhirodgarin", "Raktaksha", "Krodhana", "Kshaya"
]

MONTH_NAMES_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def format_time_12hr(dms_list, include_date=False, ref_date=None):
    """Converts [H, M, S] list to 12-hour format with AM/PM."""
    h, m, s = dms_list
    day_offset = 0
    if h >= 24:
        day_offset = int(h // 24)
        h = h % 24
    
    period = "AM" if h < 12 else "PM"
    h_12 = h if h <= 12 else h - 12
    if h_12 == 0:
        h_12 = 12
    
    time_str = f"{int(h_12):02d}:{int(m):02d} {period}"
    
    if include_date and day_offset > 0 and ref_date:
        next_date = ref_date + datetime.timedelta(days=day_offset)
        time_str += f", {MONTH_NAMES_SHORT[next_date.month-1]} {next_date.day:02d}"
    
    return time_str

def format_time_range_12hr(start_dms, end_dms, ref_date=None):
    """Formats a time range in 12-hour format."""
    start_h, start_m, start_s = start_dms
    end_h, end_m, end_s = end_dms
    
    start_day_offset = 0
    if start_h >= 24:
        start_day_offset = int(start_h // 24)
        start_h = start_h % 24
    
    end_day_offset = 0
    if end_h >= 24:
        end_day_offset = int(end_h // 24)
        end_h = end_h % 24
    
    start_period = "AM" if start_h < 12 else "PM"
    start_h_12 = start_h if start_h <= 12 else start_h - 12
    if start_h_12 == 0:
        start_h_12 = 12
    start_str = f"{int(start_h_12):02d}:{int(start_m):02d} {start_period}"
    
    if start_day_offset > 0 and ref_date:
        start_date = ref_date + datetime.timedelta(days=start_day_offset)
        start_str += f", {MONTH_NAMES_SHORT[start_date.month-1]} {start_date.day:02d}"
    
    end_period = "AM" if end_h < 12 else "PM"
    end_h_12 = end_h if end_h <= 12 else end_h - 12
    if end_h_12 == 0:
        end_h_12 = 12
    end_str = f"{int(end_h_12):02d}:{int(end_m):02d} {end_period}"
    
    if end_day_offset > 0 and ref_date:
        end_date = ref_date + datetime.timedelta(days=end_day_offset)
        end_str += f", {MONTH_NAMES_SHORT[end_date.month-1]} {end_date.day:02d}"
    
    return f"{start_str} to {end_str}"

def jd_to_time_12hr(jd_ut, tz, ref_date):
    """Converts JD (UT) to 12-hour format with AM/PM and date if needed."""
    local_jd = jd_ut + tz / 24.0
    g = sankranti.jd_to_gregorian(local_jd)
    h_flt = g[3] + g[4]/60.0 + g[5]/3600.0
    h = int(h_flt)
    m = int((h_flt - h) * 60)
    
    current_date = datetime.date(g[0], g[1], g[2])
    day_offset = (current_date - ref_date).days
    
    period = "AM" if h < 12 else "PM"
    h_12 = h if h <= 12 else h - 12
    if h_12 == 0:
        h_12 = 12
    
    time_str = f"{int(h_12):02d}:{int(m):02d} {period}"
    
    if day_offset > 0:
        time_str += f", {MONTH_NAMES_SHORT[current_date.month-1]} {current_date.day:02d}"
    
    return time_str


def jd_to_time_12hr_varjyam(jd_ut, tz, ref_date):
    """Converts JD (UT) to 12-hour format for Varjyam/Amrit Kalam display."""
    local_jd = jd_ut + tz / 24.0
    g = sankranti.jd_to_gregorian(local_jd)
    h_flt = g[3] + g[4]/60.0 + g[5]/3600.0
    h = int(h_flt)
    m = int((h_flt - h) * 60)
    
    current_date = datetime.date(g[0], g[1], g[2])
    day_offset = (current_date - ref_date).days
    
    period = "AM" if h < 12 else "PM"
    h_12 = h if h <= 12 else h - 12
    if h_12 == 0:
        h_12 = 12
    
    time_str = f"{int(h_12):02d}:{int(m):02d} {period}"
    
    if day_offset > 0:
        time_str += f", {MONTH_NAMES_SHORT[current_date.month-1]} {current_date.day:02d}"
    
    return time_str


class MarathiPanchangCalculator:
    def __init__(self):
        sankranti.set_ayanamsa_mode()
        
    def calculate(self, year, month, day, hour, minute, second, lat, lon, info_timezone):
        place = Place(lat, lon, info_timezone)
        
        jd_midnight = sankranti.gregorian_to_jd(Date(year, month, day))
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
        
        sunrise_hours = sr_info[1][0] + sr_info[1][1]/60 + sr_info[1][2]/3600
        sunset_hours = ss_info[1][0] + ss_info[1][1]/60 + ss_info[1][2]/3600
        
        # Moonrise handling
        if mr_val[0] < 0 or mr_val[0] >= 48:
            result['Moonrise'] = "No Moonrise"
        else:
            moonrise_hours = mr_val[0] + mr_val[1]/60 + mr_val[2]/3600
            diff_minutes = abs(moonrise_hours - sunrise_hours) * 60
            if diff_minutes < 2:
                result['Moonrise'] = "No Moonrise"
            else:
                result['Moonrise'] = format_time_12hr(mr_val, include_date=True, ref_date=ref_date)
        
        # Moonset handling
        if ms_val[0] < 0 or ms_val[0] >= 36:
            result['Moonset'] = "No Moonset"
        else:
            moonset_hours = ms_val[0] + ms_val[1]/60 + ms_val[2]/3600
            
            if moonset_hours >= 24:
                next_day = datetime.date(year, month, day) + datetime.timedelta(days=1)
                jd_next = sankranti.gregorian_to_jd(next_day)
                sr_next = sankranti.sunrise(jd_next, place)
                sunrise_next_hours = sr_next[1][0] + sr_next[1][1]/60 + sr_next[1][2]/3600
                
                moonset_next_day_hours = moonset_hours - 24
                
                if moonset_next_day_hours >= sunrise_next_hours:
                    result['Moonset'] = "No Moonset"
                else:
                    result['Moonset'] = format_time_12hr(ms_val, include_date=True, ref_date=ref_date)
            else:
                result['Moonset'] = format_time_12hr(ms_val, include_date=True, ref_date=ref_date)
        
        # Marathi Calendar System - Uses Amanta (New Moon to New Moon)
        masa_info = sankranti.masa(jd_midnight, place, amanta=True)
        masa_num, is_leap = masa_info[0], masa_info[1]
        kali, saka = sankranti.elapsed_year(jd_midnight, masa_num)
        
        # Shaka Samvat calculation with 60-year cycle
        saka_cycle_idx = (saka + 11) % 60
        
        # Get month name
        month_name = MARATHI_MONTH_NAMES[masa_num - 1]
        if is_leap:
            month_name = f"{month_name} (Adhik)"
        
        result['Shaka Samvat'] = f"{saka} {SHAKA_SAMVAT_NAMES[saka_cycle_idx]}"
        result['Lunar Month'] = month_name
        
        # Weekday
        weekday_idx = sankranti.vaara(jd_midnight)
        result['Weekday'] = MARATHI_VARA[weekday_idx]
        
        # Paksha and Tithi
        tithi_data = sankranti.tithi(jd_midnight, place)
        tithi_num = tithi_data[0]
        tithi_end_time = tithi_data[1]
        
        # Determine Paksha
        if tithi_num <= 15:
            result['Paksha'] = MARATHI_PAKSHA['shukla']
        else:
            result['Paksha'] = MARATHI_PAKSHA['krishna']
        
        t_name = TITHI_NAMES[tithi_num]['english']
        
        end_hours = tithi_end_time[0] + tithi_end_time[1]/60.0
        sunrise_hours = sr_info[1][0] + sr_info[1][1]/60.0
        
        if end_hours < 24 + sunrise_hours:
            result['Tithi'] = f"{t_name} upto {format_time_12hr(tithi_end_time, include_date=True, ref_date=ref_date)}"
            if end_hours < 24:
                next_tithi_num = (tithi_num % 30) + 1
                next_t_name = TITHI_NAMES[next_tithi_num]['english']
                result['Tithi'] += f"; {next_t_name}"
        else:
            result['Tithi'] = t_name
        
        # Nakshatra
        nakshatra_data = sankranti.nakshatra(jd_midnight, place)
        nak_num = nakshatra_data[0]
        nak_end_time = nakshatra_data[1]
        nak_name = NAKSHATRA_NAMES[nak_num-1]['english']
        
        nak_end_hours = nak_end_time[0] + nak_end_time[1]/60.0
        
        if sunrise_hours <= nak_end_hours < 30 or nak_end_hours < sunrise_hours:
            result['Nakshatra'] = f"{nak_name} upto {format_time_12hr(nak_end_time, include_date=True, ref_date=ref_date)}"
            next_nak_num = (nak_num % 27) + 1
            next_nak_name = NAKSHATRA_NAMES[next_nak_num-1]['english']
            result['Nakshatra'] += f"; {next_nak_name}"
        else:
            result['Nakshatra'] = nak_name
        
        # Yoga
        yoga_data = sankranti.yoga(jd_midnight, place)
        yoga_num = yoga_data[0]
        yoga_end_time = yoga_data[1]
        y_name = YOGA_NAMES[yoga_num-1]['english']
        
        yoga_end_hours = yoga_end_time[0] + yoga_end_time[1]/60.0
        
        if yoga_end_hours < 30:
            result['Yoga'] = f"{y_name} upto {format_time_12hr(yoga_end_time, include_date=True, ref_date=ref_date)}"
            if yoga_end_hours < 24 + sunrise_hours:
                next_yoga_num = (yoga_num % 27) + 1
                next_y_name = YOGA_NAMES[next_yoga_num-1]['english']
                result['Yoga'] += f"; {next_y_name}"
        else:
            result['Yoga'] = y_name
        
        # Karana
        def get_karana_name(num):
            if num == 1: return "Kimstughna"
            elif num >= 58:
                if num == 58: return "Shakuni"
                elif num == 59: return "Chatushpada"
                elif num == 60: return "Naga"
            else:
                idx = (num - 2) % 7
                name = KARANA_NAMES[idx]
                if name == "Gara":
                    name = "Garaja"
                return name
        
        karana_data = sankranti.karana(jd_midnight, place)
        sunrise_hours = sr_info[1][0] + sr_info[1][1]/60.0 + sr_info[1][2]/3600.0
        
        karana_list = []
        seen_karanas = set()
        for i in range(0, len(karana_data), 2):
            if i+1 < len(karana_data):
                k_num = karana_data[i]
                k_end = karana_data[i+1]
                k_end_hours = k_end[0] + k_end[1]/60.0 + k_end[2]/3600.0
                
                if k_end_hours >= sunrise_hours and k_num not in seen_karanas:
                    karana_list.append((k_num, k_end, k_end_hours))
                    seen_karanas.add(k_num)
        
        karana_list.sort(key=lambda x: x[2])
        
        if karana_list:
            karana_num, karana_end_time, _ = karana_list[0]
            kn = get_karana_name(karana_num)
            result['Karana'] = f"{kn} upto {format_time_12hr(karana_end_time, include_date=True, ref_date=ref_date)}"
            
            if len(karana_list) >= 2:
                karana_num2, karana_end_time2, k2_hours = karana_list[1]
                kn2 = get_karana_name(karana_num2)
                if k2_hours < 24:
                    result['Karana'] += f"; {kn2} upto {format_time_12hr(karana_end_time2, include_date=True, ref_date=ref_date)}"
                elif k2_hours < 30:
                    result['Karana'] += f"; {kn2} upto {format_time_12hr(karana_end_time2, include_date=True, ref_date=ref_date)}"
                else:
                    result['Karana'] += f"; {kn2}"
            else:
                next_karana_num = (karana_num % 60) + 1
                next_kn = get_karana_name(next_karana_num)
                result['Karana'] += f"; {next_kn}"
        else:
            result['Karana'] = "No karana data"
        
        # Sun and Moon signs
        sunrise_jd_local = sr_info[0]
        sunrise_jd_ut = sunrise_jd_local - info_timezone / 24.0
        
        result['Sunsign'] = RASHI_NAMES[int(sankranti.solar_longitude(sunrise_jd_ut)/30)]['english']
        result['Moonsign'] = RASHI_NAMES[int(sankranti.lunar_longitude(sunrise_jd_ut)/30)]['english']
        
        # Kalams
        rk = sankranti.rahu_kalam(jd_midnight, place)
        gk = sankranti.gulika_kalam(jd_midnight, place)
        yg = sankranti.yamaganda_kalam(jd_midnight, place)
        
        result['Rahu Kalam'] = format_time_range_12hr(rk[0], rk[1], ref_date)
        result['Gulikai Kalam'] = format_time_range_12hr(gk[0], gk[1], ref_date)
        result['Yamaganda'] = format_time_range_12hr(yg[0], yg[1], ref_date)
        
        # Abhijit Muhurta
        if sankranti.vaara(jd_midnight) == 3:
            result['Abhijit'] = "None"
        else:
            ab = sankranti.abhijit_muhurta(jd_midnight, place)
            ab_start = sankranti.to_dms(ab[0])
            ab_end = sankranti.to_dms(ab[1])
            result['Abhijit'] = format_time_range_12hr(ab_start, ab_end, ref_date)
        
        # Dur Muhurtam
        sunrise_h = sr_info[1][0] + sr_info[1][1]/60.0 + sr_info[1][2]/3600.0
        sunset_h = ss_info[1][0] + ss_info[1][1]/60.0 + ss_info[1][2]/3600.0
        
        next_sr_info = sankranti.sunrise(jd_midnight + 1, place)
        next_sunrise_h = 24 + next_sr_info[1][0] + next_sr_info[1][1]/60.0 + next_sr_info[1][2]/3600.0
        
        day_duration = sunset_h - sunrise_h
        night_duration = next_sunrise_h - sunset_h
        day_muhurta = day_duration / 15.0
        night_muhurta = night_duration / 15.0
        
        weekday = sankranti.vaara(jd_midnight)
        
        dm_raw = sankranti.durmuhurtam(jd_midnight, place)
        
        dm_start1 = sankranti.to_dms(dm_raw[0][0])
        dm_end1 = sankranti.to_dms(dm_raw[1][0])
        dm_str = format_time_range_12hr(dm_start1, dm_end1, ref_date)
        
        if dm_raw[0][1] != 0:
            dm2_start_raw = dm_raw[0][1]
            dm2_end_raw = dm_raw[1][1]
            
            if dm2_start_raw >= sunset_h:
                night_muhurta_index = round((dm2_start_raw - sunset_h) / night_muhurta)
                
                dm2_start_correct = sunset_h + (night_muhurta_index * night_muhurta)
                dm2_end_correct = sunset_h + ((night_muhurta_index + 1) * night_muhurta)
                
                dm_start2 = sankranti.to_dms(dm2_start_correct)
                dm_end2 = sankranti.to_dms(dm2_end_correct)
            else:
                dm_start2 = sankranti.to_dms(dm2_start_raw)
                dm_end2 = sankranti.to_dms(dm2_end_raw)
            
            dm_str += f"; {format_time_range_12hr(dm_start2, dm_end2, ref_date)}"
        
        result['Dur Muhurtam'] = dm_str
        
        # =====================================================================
        # Varjyam and Amrit Kalam Calculation
        # =====================================================================
        # Calculate based on nakshatra at sunrise (DrikPanchang convention)
        sunrise_jd_ut = sr_info[0] - info_timezone / 24.0
        
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
        if nak_num == 27:  # Revati - ends at 360°/0°
            def nak_end_dist(t):
                m = sankranti.lunar_longitude(t)
                if m > 180:
                    return m - 360
                else:
                    return m
            n_end_jd = sankranti.bisection_search(nak_end_dist, sunrise_jd_ut + 0.1, sunrise_jd_ut + 2.0)
        else:
            def nak_end_dist(t):
                m = sankranti.lunar_longitude(t)
                target = nak_num * (360/27.0)
                return sankranti.norm180(m - target)
            n_end_jd = sankranti.bisection_search(nak_end_dist, sunrise_jd_ut, sunrise_jd_ut + 1.2)
        
        # Calculate for sunrise nakshatra AND the next one if it starts within the day
        nakshatras_to_calculate = [{
            'num': nak_num,
            'start_jd': n_start_jd,
            'end_jd': n_end_jd
        }]
        
        # Check if next nakshatra starts before next sunrise
        if n_end_jd < sunrise_jd_ut + 1.2:
            next_nak_num = (nak_num % 27) + 1
            
            def next_nak_end_dist(t):
                m = sankranti.lunar_longitude(t)
                target = next_nak_num * (360/27.0)
                return sankranti.norm180(m - target)
            
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
            
            # Varjyam: Starting time = Nakshatra start + (duration * X/24)
            # Duration = 1/15th of nakshatra = 1.6 hours for 24-hour nakshatra
            v_s_ut = n_start + (duration_days * v_start_hours / 24.0)
            v_duration_days = duration_days * 1.6 / 24.0
            v_e_ut = v_s_ut + v_duration_days
            
            # Amrit Kalam: Same formula
            a_s_ut = n_start + (duration_days * a_start_hours / 24.0)
            a_duration_days = duration_days * 1.6 / 24.0
            a_e_ut = a_s_ut + a_duration_days
            
            # Only include if it occurs on the panchang day (sunrise to next sunrise)
            next_sunrise_approx = sunrise_jd_ut + 1.0
            
            # Minimum duration threshold (5 minutes in days)
            MIN_DURATION = 5.0 / (24 * 60)
            
            # Include Varjyam only if it starts after current sunrise and before next sunrise
            if v_s_ut >= sunrise_jd_ut and v_s_ut < next_sunrise_approx and v_duration_days >= MIN_DURATION:
                v_start_time = jd_to_time_12hr_varjyam(v_s_ut, info_timezone, ref_date)
                v_end_time = jd_to_time_12hr_varjyam(v_e_ut, info_timezone, ref_date)
                varjyam_periods.append(f"{v_start_time} to {v_end_time}")
            
            # Include Amrit Kalam only if it starts after current sunrise and before next sunrise
            if a_s_ut >= sunrise_jd_ut and a_s_ut < next_sunrise_approx and a_duration_days >= MIN_DURATION:
                a_start_time = jd_to_time_12hr_varjyam(a_s_ut, info_timezone, ref_date)
                a_end_time = jd_to_time_12hr_varjyam(a_e_ut, info_timezone, ref_date)
                amrit_periods.append(f"{a_start_time} to {a_end_time}")
        
        # Join multiple periods with semicolon
        result['Varjyam'] = "; ".join(varjyam_periods) if varjyam_periods else "None"
        result['Amrit Kalam'] = "; ".join(amrit_periods) if amrit_periods else "None"
        
        return result

if __name__ == "__main__":
    c = MarathiPanchangCalculator()
    
    print("=" * 60)
    print("Mumbai - January 19, 2026")
    print("=" * 60)
    res = c.calculate(2026, 1, 19, 6, 0, 0, 19.0760, 72.8777, 5.5)
    for k, v in res.items():
        print(f"{k}: {v}")