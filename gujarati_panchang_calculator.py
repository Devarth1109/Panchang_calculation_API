import sankranti
from sankranti import Date, Place, gregorian_to_jd, jd_to_gregorian, to_dms, swe
from math import ceil
import datetime
from religious_data import TITHI_NAMES, NAKSHATRA_NAMES, YOGA_NAMES, RASHI_NAMES, VARA_NAMES, KARANA_NAMES, SAMVAT_YEAR_NAMES
from panchang_calculator import VARJYAM_START_HOURS, AMRIT_KALAM_START_HOURS, get_pravishte

# Gujarati Month Names
GUJARATI_MONTHS = {
    1: "Kartak",
    2: "Magshar", 
    3: "Posh",
    4: "Maha",
    5: "Fagan",
    6: "Chaitra",
    7: "Vaishakh",
    8: "Jeth",
    9: "Ashadh",
    10: "Shravan",
    11: "Bhadarvo",
    12: "Aaso"
}

# Gujarati Tithi Names
GUJARATI_TITHIS = {
    1: "Padvo",
    2: "Beej",
    3: "Trij",
    4: "Choth",
    5: "Pancham",
    6: "Chhath",
    7: "Satam",
    8: "Atham",
    9: "Nom",
    10: "Dasham",
    11: "Agiyaras",
    12: "Baras",
    13: "Teras",
    14: "Chaudas",
    15: "Punam",  # Full Moon
    30: "Amas"    # New Moon
}

# Gujarati Weekdays
GUJARATI_WEEKDAYS = {
    0: "Ravivar",
    1: "Somvar",
    2: "Mangalvar",
    3: "Budhvar",
    4: "Guruvar",
    5: "Shukravar",
    6: "Shanivar"
}

def format_time_12hr(dms_list, include_date=False, ref_date=None, check_next_day=False):
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
        m_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        next_date = ref_date + datetime.timedelta(days=day_offset)
        time_str += f", {m_names[next_date.month-1]} {next_date.day:02d}"
    
    return time_str

def format_time_range_12hr(start_dms, end_dms, ref_date=None):
    start_h, start_m, start_s = start_dms
    end_h, end_m, end_s = end_dms
    
    m_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

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
        start_str += f", {m_names[start_date.month-1]} {start_date.day:02d}"
    
    end_period = "AM" if end_h < 12 else "PM"
    end_h_12 = end_h if end_h <= 12 else end_h - 12
    if end_h_12 == 0:
        end_h_12 = 12
    end_str = f"{int(end_h_12):02d}:{int(end_m):02d} {end_period}"
    
    if end_day_offset > 0 and ref_date:
        end_date = ref_date + datetime.timedelta(days=end_day_offset)
        end_str += f", {m_names[end_date.month-1]} {end_date.day:02d}"
    
    return f"{start_str} to {end_str}"

def jd_to_time_12hr(jd_ut, tz, ref_date):
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
        m_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        time_str += f", {m_names[current_date.month-1]} {current_date.day:02d}"
    
    return time_str

class GujaratiPanchangCalculator:
    def __init__(self):
        sankranti.set_ayanamsa_mode()
        
    def calculate(self, year, month, day, hour, minute, second, lat, lon, info_timezone):
        place = Place(lat, lon, info_timezone)
        
        # JDs
        jd_midnight = sankranti.gregorian_to_jd(Date(year, month, day))
        jd_now = sankranti.local_time_to_jdut1(year, month, day, hour, minute, second, info_timezone)
        ref_date = datetime.date(year, month, day)
        
        result_meta = {
            "location": "", # To be filled by API wrapper or caller
            "city": "",
            "state": "",
            "country": "",
            "countryCode": "",
            "latitude": lat,
            "longitude": lon,
            "timezone_offset": info_timezone,
            "date": ref_date.strftime("%d/%m/%Y"),
            "time": f"{hour:02d}:{minute:02d}:{second:02d}",
            "timestamp": int(datetime.datetime(year, month, day, hour, minute, second).timestamp()),
            "calendar_system": "Gujarati Panchang"
        }
        
        result_data = {}
        
        sr_info = sankranti.sunrise(jd_midnight, place)
        ss_info = sankranti.sunset(jd_midnight, place)
        mr_val = sankranti.moonrise(jd_midnight, place)
        ms_val = sankranti.moonset(jd_midnight, place)
        
        result_data['Sunrise'] = format_time_12hr(sr_info[1])
        result_data['Sunset'] = format_time_12hr(ss_info[1])
        
        sunrise_hours = sr_info[1][0] + sr_info[1][1]/60 + sr_info[1][2]/3600
        
        if mr_val[0] < 0 or mr_val[0] >= 48:
             result_data['Moonrise'] = "No Moonrise"
        else:
            moonrise_hours = mr_val[0] + mr_val[1]/60 + mr_val[2]/3600
            diff_minutes = abs(moonrise_hours - sunrise_hours) * 60
            if diff_minutes < 2:
                result_data['Moonrise'] = "No Moonrise"
            else:
                result_data['Moonrise'] = format_time_12hr(mr_val, include_date=True, ref_date=ref_date)
        
        if ms_val[0] < 0 or ms_val[0] >= 36:
            result_data['Moonset'] = "No Moonset"
        else:
            moonset_hours = ms_val[0] + ms_val[1]/60 + ms_val[2]/3600
            
            if moonset_hours >= 24:
                next_day = datetime.date(year, month, day) + datetime.timedelta(days=1)
                jd_next = sankranti.gregorian_to_jd(next_day)
                sr_next = sankranti.sunrise(jd_next, place)
                sunrise_next_hours = sr_next[1][0] + sr_next[1][1]/60 + sr_next[1][2]/3600
                
                moonset_next_day_hours = moonset_hours - 24
                
                if moonset_next_day_hours >= sunrise_next_hours:
                    result_data['Moonset'] = "No Moonset"
                else:
                    result_data['Moonset'] = format_time_12hr(ms_val, include_date=True, ref_date=ref_date)
            else:
                result_data['Moonset'] = format_time_12hr(ms_val, include_date=True, ref_date=ref_date)


        masa_info = sankranti.masa(jd_midnight, place, amanta=True)
        masa_num, is_leap = masa_info[0], masa_info[1]
        
        saka = year - 78
        if month < 4:
             if masa_num >= 10: 
                  saka -= 1
        
        vikram = saka + 135
        
        gujarati_year = vikram - 1 
        if masa_num >= 8: 
            gujarati_year = vikram
            
        gujarati_offset = 8
        samvatsara_idx = (gujarati_year + gujarati_offset) % 60
        samvatsara_name = SAMVAT_YEAR_NAMES[samvatsara_idx]
        
        result_data['Gujarati Samvat'] = f"{gujarati_year} {samvatsara_name}"
        
        if masa_num >= 8:
            guj_month_num = masa_num - 7
        else:
            guj_month_num = masa_num + 5
            
        final_month_name = GUJARATI_MONTHS[guj_month_num]
        
        if is_leap:
             final_month_name = f"{final_month_name} (Adhik)"
             
        result_data['Lunar Month'] = final_month_name
        
        weekday_idx = sankranti.vaara(jd_midnight)
        result_data['Weekday'] = GUJARATI_WEEKDAYS[weekday_idx]
        
        tithi_data = sankranti.tithi(jd_midnight, place)
        tithi_num_start = tithi_data[0]
        tithi_end_jd = tithi_data[1][0] + tithi_data[1][1]/60.0 + tithi_data[1][2]/3600.0
        
        is_shukla = tithi_num_start <= 15
        paksha_name = "Sud" if is_shukla else "Vad"
        result_data['Paksha'] = paksha_name
        
        display_tithi_num = tithi_num_start if tithi_num_start <= 15 else tithi_num_start - 15
        
        t_name = GUJARATI_TITHIS.get(display_tithi_num, f"{display_tithi_num}")
        if tithi_num_start == 30: t_name = "Amas"
        if tithi_num_start == 15: t_name = "Punam"
        
        tithi_end_time = tithi_data[1]
        t_end_h = tithi_end_time[0] + tithi_end_time[1]/60
        sr_h = sr_info[1][0] + sr_info[1][1]/60
        
        if t_end_h < 24 + sr_h:
            result_data['Tithi'] = f"{t_name} upto {format_time_12hr(tithi_end_time, include_date=True, ref_date=ref_date)}"
        else:
             result_data['Tithi'] = t_name
             
        nak_data = sankranti.nakshatra(jd_midnight, place)
        nak_num = nak_data[0]
        nak_end = nak_data[1]
        nak_name = NAKSHATRA_NAMES[nak_num-1]['english']
        
        nak_end_h = nak_end[0] + nak_end[1]/60
        if nak_end_h < 32: # Extended window to catch early next morning
             result_data['Nakshathram'] = f"{nak_name} upto {format_time_12hr(nak_end, include_date=True, ref_date=ref_date)}"
        else:
             result_data['Nakshathram'] = nak_name
             
        yoga_data = sankranti.yoga(jd_midnight, place)
        yoga_num = yoga_data[0]
        yoga_end = yoga_data[1]
        yoga_name = YOGA_NAMES[yoga_num-1]['english']
        
        yoga_end_h = yoga_end[0] + yoga_end[1]/60
        if yoga_end_h < 32: # Extended window
            result_data['Yoga'] = f"{yoga_name} upto {format_time_12hr(yoga_end, include_date=True, ref_date=ref_date)}"
        else:
            result_data['Yoga'] = yoga_name

        sunrise_jd_ut = sr_info[0] - info_timezone/24.0
        result_data['Sunsign'] = RASHI_NAMES[int(sankranti.solar_longitude(sunrise_jd_ut)/30)]['english']
        result_data['Moonsign'] = RASHI_NAMES[int(sankranti.lunar_longitude(sunrise_jd_ut)/30)]['english']
        
        # Karana calculation
        def get_karana_name(num):
            if num == 1: return "Kimstughna"
            elif num >= 58:
                if num == 58: return "Shakuni"
                elif num == 59: return "Chatushpada"
                elif num == 60: return "Naga"
            else:
                idx = (num - 2) % 7
                name = KARANA_NAMES[idx]
                if name == "Gara": name = "Garaja"
                return name
        
        karana_data = sankranti.karana(jd_midnight, place)
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
            result_data['Karana'] = f"{kn} upto {format_time_12hr(karana_end_time, include_date=True, ref_date=ref_date)}"
            
            if len(karana_list) >= 2:
                karana_num2, karana_end_time2, k2_hours = karana_list[1]
                kn2 = get_karana_name(karana_num2)
                if k2_hours < 30:
                    result_data['Karana'] += f"; {kn2} upto {format_time_12hr(karana_end_time2, include_date=True, ref_date=ref_date)}"
                else:
                    result_data['Karana'] += f"; {kn2}"
            else:
                next_karana_num = (karana_num % 60) + 1
                next_kn = get_karana_name(next_karana_num)
                result_data['Karana'] += f"; {next_kn}"
        else:
            result_data['Karana'] = "No karana data"
        
        # Kalams
        rk = sankranti.rahu_kalam(jd_midnight, place)
        gk = sankranti.gulika_kalam(jd_midnight, place)
        yg = sankranti.yamaganda_kalam(jd_midnight, place)
        
        result_data['Rahu Kalam'] = format_time_range_12hr(rk[0], rk[1], ref_date)
        result_data['Gulikai Kalam'] = format_time_range_12hr(gk[0], gk[1], ref_date)
        result_data['Yamaganda'] = format_time_range_12hr(yg[0], yg[1], ref_date)
        
        # Abhijit Muhurta
        if sankranti.vaara(jd_midnight) == 3:
            result_data['Abhijit'] = "None"
        else:
            ab = sankranti.abhijit_muhurta(jd_midnight, place)
            ab_start = sankranti.to_dms(ab[0])
            ab_end = sankranti.to_dms(ab[1])
            result_data['Abhijit'] = format_time_range_12hr(ab_start, ab_end, ref_date)
        
        # Dur Muhurtam
        sunrise_h = sr_info[1][0] + sr_info[1][1]/60.0 + sr_info[1][2]/3600.0
        sunset_h = ss_info[1][0] + ss_info[1][1]/60.0 + ss_info[1][2]/3600.0
        
        next_sr_info = sankranti.sunrise(jd_midnight + 1, place)
        next_sunrise_h = 24 + next_sr_info[1][0] + next_sr_info[1][1]/60.0 + next_sr_info[1][2]/3600.0
        
        night_duration = next_sunrise_h - sunset_h
        night_muhurta = night_duration / 15.0
        
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
        
        result_data['Dur Muhurtam'] = dm_str
        
        # =====================================================================
        # Varjyam and Amrit Kalam Calculation
        # =====================================================================
        # Calculate based on nakshatra at sunrise (DrikPanchang convention)
        
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
                v_start_time = jd_to_time_12hr(v_s_ut, info_timezone, ref_date)
                v_end_time = jd_to_time_12hr(v_e_ut, info_timezone, ref_date)
                varjyam_periods.append(f"{v_start_time} to {v_end_time}")
            
            # Include Amrit Kalam only if it starts after current sunrise and before next sunrise
            if a_s_ut >= sunrise_jd_ut and a_s_ut < next_sunrise_approx and a_duration_days >= MIN_DURATION:
                a_start_time = jd_to_time_12hr(a_s_ut, info_timezone, ref_date)
                a_end_time = jd_to_time_12hr(a_e_ut, info_timezone, ref_date)
                amrit_periods.append(f"{a_start_time} to {a_end_time}")
        
        # Join multiple periods with semicolon
        result_data['Varjyam'] = "; ".join(varjyam_periods) if varjyam_periods else "None"
        result_data['Amrit Kalam'] = "; ".join(amrit_periods) if amrit_periods else "None"
    
        full_result = {
            "meta": result_meta,
            "data": result_data
        }
        
        return full_result
        
    def _calculate_extended_details(self, result_data, jd_midnight, place, ref_date, sr_info, ss_info, info_timezone):
        """Helper to fill complex calculations like Yoga/Karana multiple entries & Kalams"""
        
        sunrise_hours = sr_info[1][0] + sr_info[1][1]/60.0
        
        # --- Yoga ---
        yoga_data = sankranti.yoga(jd_midnight, place)
        y_num = yoga_data[0]
        y_end = yoga_data[1]
        y_name = YOGA_NAMES[y_num-1]['english']
        
        y_end_h = y_end[0] + y_end[1]/60.0
        
        yoga_str = f"{y_name} upto {format_time_12hr(y_end, include_date=True, ref_date=ref_date)}"
        
        if y_end_h < 24 + sunrise_hours:
             next_y_num = (y_num % 27) + 1
             next_y_name = YOGA_NAMES[next_y_num-1]['english']
             
             y_end_local_h = y_end[0] + y_end[1]/60.0 + y_end[2]/3600.0
             if y_end_local_h >= 24:
                 extra_days = int(y_end_local_h // 24)
                 remain_h = y_end_local_h % 24
                 y_end_jd_local = jd_midnight + extra_days + remain_h/24.0
             else:
                 y_end_jd_local = jd_midnight + y_end_local_h/24.0
             
             y_end_jd_ut = y_end_jd_local - info_timezone/24.0
             
             def next_yoga_end_dist(t):
                 s = sankranti.solar_longitude(t)
                 m = sankranti.lunar_longitude(t)
                 total = s + m
                 target = next_y_num * (360/27.0)
                 return sankranti.norm180(total - target)
            
             try:
                 next_y_end_jd_ut = sankranti.bisection_search(next_yoga_end_dist, y_end_jd_ut + 0.5, y_end_jd_ut + 1.2)
                 next_y_end = jd_to_time_12hr(next_y_end_jd_ut, info_timezone, ref_date)
                 
                 yoga_str = f"{yoga_str}; {next_y_name} upto {next_y_end}"
             except:
                 pass
        else:
             yoga_str = y_name
             
        result_data['Yoga'] = yoga_str

        karana_data = sankranti.karana(jd_midnight, place)
        karana_str_list = []
        for i in range(0, len(karana_data), 2):
            if i+1 < len(karana_data):
                k_num = karana_data[i]
                k_end = karana_data[i+1]
                
                k_end_h = k_end[0] + k_end[1]/60
                
                k_name = ""
                if k_num == 1: k_name = "Kimstughna"
                elif k_num >= 58:
                    if k_num == 58: k_name = "Shakuni"
                    elif k_num == 59: k_name = "Chatushpada"
                    elif k_num == 60: k_name = "Naga"
                else:
                    idx = (k_num - 2) % 7
                    k_name = KARANA_NAMES[idx]
                    if k_name == "Gara": k_name = "Garaja"
                
                if k_end_h >= sunrise_hours:
                    karana_str_list.append(f"{k_name} upto {format_time_12hr(k_end, include_date=True, ref_date=ref_date, check_next_day=True)}")
                    
        result_data['Karana'] = "; ".join(karana_str_list) if karana_str_list else "No data"
       
        rk = sankranti.rahu_kalam(jd_midnight, place)
        gk = sankranti.gulika_kalam(jd_midnight, place)
        yg = sankranti.yamaganda_kalam(jd_midnight, place)
        
        result_data['Rahu Kalam'] = format_time_range_12hr(rk[0], rk[1], ref_date)
        result_data['Gulikai Kalam'] = format_time_range_12hr(gk[0], gk[1], ref_date)
        result_data['Yamaganda'] = format_time_range_12hr(yg[0], yg[1], ref_date)
        
        # Abhijit
        if sankranti.vaara(jd_midnight) == 3: # Wednesday
             result_data['Abhijit'] = "None"
        else:
            ab = sankranti.abhijit_muhurta(jd_midnight, place)
            result_data['Abhijit'] = format_time_range_12hr(to_dms(ab[0]), to_dms(ab[1]), ref_date)
      
        sunrise_h = sr_info[1][0] + sr_info[1][1]/60.0 + sr_info[1][2]/3600.0
        sunset_h = ss_info[1][0] + ss_info[1][1]/60.0 + ss_info[1][2]/3600.0
        
        next_sr_info = sankranti.sunrise(jd_midnight + 1, place)
        next_sunrise_h = 24 + next_sr_info[1][0] + next_sr_info[1][1]/60.0 + next_sr_info[1][2]/3600.0
        
        night_duration = next_sunrise_h - sunset_h
        night_muhurta = night_duration / 15.0
        
        dm_raw = sankranti.durmuhurtam(jd_midnight, place)
        dm_str = format_time_range_12hr(to_dms(dm_raw[0][0]), to_dms(dm_raw[1][0]), ref_date)
        
        if dm_raw[0][1] != 0: # Second dur muhurtam
             dm2_start = dm_raw[0][1]
             # Fix if night time
             if dm2_start >= sunset_h:
                  # Recalc
                  night_idx = round((dm2_start - sunset_h) / night_muhurta)
                  dm2_start = sunset_h + (night_idx * night_muhurta)
                  dm2_end = sunset_h + ((night_idx+1) * night_muhurta)
             else:
                  dm2_end = dm_raw[1][1]
             
             dm_str += f"; {format_time_range_12hr(to_dms(dm2_start), to_dms(dm2_end), ref_date)}"
             
        result_data['Dur Muhurtam'] = dm_str
        
        # NOTE: Varjyam and Amrit Kalam are now calculated in calculate() method
        # No need to recalculate here - the values are already correctly set
        
        return result_data

    def calculate_full(self, year, month, day, hour, minute, second, lat, lon, info_timezone):
        basic_res = self.calculate(year, month, day, hour, minute, second, lat, lon, info_timezone)
        
        jd_midnight = sankranti.gregorian_to_jd(Date(year, month, day))
        place = Place(lat, lon, info_timezone)
        ref_date = datetime.date(year, month, day)
        sr_info = sankranti.sunrise(jd_midnight, place)
        ss_info = sankranti.sunset(jd_midnight, place)
        
        extended_data = self._calculate_extended_details(basic_res['data'], jd_midnight, place, ref_date, sr_info, ss_info, info_timezone)
        
        return basic_res

if __name__ == "__main__":
    # Test Code
    c = GujaratiPanchangCalculator()
    print("Test: Jan 27 2026, Tokyo")
    res = c.calculate_full(2026, 1, 27, 6, 0, 0, 35.6895, 139.6917, 9.0)
    import json
    print(json.dumps(res, indent=4))
