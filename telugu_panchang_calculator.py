import sankranti
from sankranti import Date, Place, gregorian_to_jd, jd_to_gregorian, to_dms, swe
import datetime
from religious_data import TITHI_NAMES, NAKSHATRA_NAMES, YOGA_NAMES, RASHI_NAMES, VARA_NAMES, KARANA_NAMES, SAMVAT_YEAR_NAMES
from panchang_calculator import VARJYAM_START_HOURS, AMRIT_KALAM_START_HOURS

# Telugu Month Names (Amanta System)
# Matches images: Maghamu, Bhadhrapadamu, Margasiramu
TELUGU_MONTHS = {
    1: "Chaitramu",
    2: "Vaisakhamu", 
    3: "Jyeshthamu",
    4: "Ashadhamu",
    5: "Sravanamu",
    6: "Bhadrapadamu",
    7: "Asviyujamu",
    8: "Kartikamu",
    9: "Margasiramu",
    10: "Pushyamu",
    11: "Maghamu",
    12: "Phalgunamu"
}

# Telugu Tithi Names
# Padyami, Vidiya, Tadiya, Chavithi, Panchami, Shashthi, Sapthami, Ashtami, Navami, Dasami, Ekadasi, Dwadasi, Trayodasi, Chaturdasi, Pournami, Amavasya
TELUGU_TITHIS = {
    1: "Padyami",
    2: "Vidiya",
    3: "Tadiya",
    4: "Chavithi",
    5: "Panchami",
    6: "Shashthi",
    7: "Sapthami",
    8: "Ashtami",
    9: "Navami",
    10: "Dasami",
    11: "Ekadasi",
    12: "Dwadasi",
    13: "Trayodasi",
    14: "Chaturdasi",
    15: "Pournami",
    30: "Amavasya"
}

# Telugu Weekdays (Based on images: Mangalawara, Somawara, etc.)
# "wara" suffix seems used in the reference format
TELUGU_WEEKDAYS = {
    0: "Ravivara",
    1: "Somavara",
    2: "Mangalavara",
    3: "Budhavara",
    4: "Guruvara",
    5: "Sukravara",
    6: "Shanivara"
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

class TeluguPanchangCalculator:
    def __init__(self):
        sankranti.set_ayanamsa_mode()
        
    def calculate(self, year, month, day, hour, minute, second, lat, lon, info_timezone):
        place = Place(lat, lon, info_timezone)
        jd_midnight = sankranti.gregorian_to_jd(Date(year, month, day))
        ref_date = datetime.date(year, month, day)
        
        result_meta = {
            "location": "",
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
            "calendar_system": "Telugu Panchang"
        }
        
        result_data = {}
        
        # Sun/Moon Rise/Set
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

        # Shaka Samvat
        masa_info = sankranti.masa(jd_midnight, place, amanta=True)
        masa_num, is_leap = masa_info[0], masa_info[1]
        
        # Standard Shaka calculation
        # Shaka starts Chaitra Shukla Pratipada.
        saka = year - 78
        if month < 4: # Jan, Feb, Mar
             if masa_num >= 10: # Pushya, Magha, Phalguna -> Previous Shaka Year
                  saka -= 1
        
        # Samvatsara Name
        # Shaka 1947 + 11 = 1958 % 60 = 38 (Visvavasu)
        saka_offset = 11
        samvatsara_idx = (saka + saka_offset) % 60
        samvatsara_name = SAMVAT_YEAR_NAMES[samvatsara_idx]
        
        result_data['Shaka Samvat'] = f"{saka} {samvatsara_name}"
        
        # Lunar Month matches image (Maghamu for Magha)
        month_name = TELUGU_MONTHS[masa_num]
        if is_leap:
            month_name += " (Adhik)"
        result_data['Lunar Month'] = month_name
        
        # Weekday
        wd = sankranti.vaara(jd_midnight)
        result_data['Weekday'] = TELUGU_WEEKDAYS[wd]
        
        # Pakshamulu
        tithi_data = sankranti.tithi(jd_midnight, place)
        t_num = tithi_data[0]
        t_end = tithi_data[1]
        
        result_data['Pakshamulu'] = "Sukla Pakshamulu" if t_num <= 15 else "Krishna Pakshamulu"
        
        # Tithulu
        disp_t_num = t_num if t_num <= 15 else t_num - 15
        t_name = TELUGU_TITHIS.get(disp_t_num, str(disp_t_num))
        if t_num == 30: t_name = "Amavasya"
        if t_num == 15: t_name = "Pournami"
        
        t_end_h = t_end[0] + t_end[1]/60
        if t_end_h < 24 + sunrise_hours:
            result_data['Tithulu'] = f"{t_name} upto {format_time_12hr(t_end, include_date=True, ref_date=ref_date)}"
        else:
            result_data['Tithulu'] = t_name
            
        # Nakshatramulu
        nak_data = sankranti.nakshatra(jd_midnight, place)
        n_num = nak_data[0]
        n_end = nak_data[1]
        n_name = NAKSHATRA_NAMES[n_num-1]['english']
        
        n_end_h = n_end[0] + n_end[1]/60
        if n_end_h < 32:
            result_data['Nakshatramulu'] = f"{n_name} upto {format_time_12hr(n_end, include_date=True, ref_date=ref_date)}"
        else:
            result_data['Nakshatramulu'] = n_name
            
        # Yogalu
        yoga_data = sankranti.yoga(jd_midnight, place)
        y_num = yoga_data[0]
        y_end = yoga_data[1]
        y_name = YOGA_NAMES[y_num-1]['english']
        
        y_end_h = y_end[0] + y_end[1]/60
        if y_end_h < 32:
            yoga_str = f"{y_name} upto {format_time_12hr(y_end, include_date=True, ref_date=ref_date)}"
            # Next yoga logic similar to gujarati
            if y_end_h < 24 + sunrise_hours:
                next_y_num = (y_num % 27) + 1
                next_y_name = YOGA_NAMES[next_y_num-1]['english']
                
                y_end_jd_local = jd_midnight + (y_end[0] + y_end[1]/60 + y_end[2]/3600)/24.0
                if y_end[0] >= 24: y_end_jd_local = jd_midnight + 1 + (y_end[0]-24 + y_end[1]/60)/24.0
                
                y_end_jd_ut = y_end_jd_local - info_timezone/24.0
                
                def next_y_dist(t):
                    return sankranti.norm180((sankranti.solar_longitude(t)+sankranti.lunar_longitude(t)) - (next_y_num * 360/27.0))
                
                try:
                    next_end_jd = sankranti.bisection_search(next_y_dist, y_end_jd_ut + 0.5, y_end_jd_ut + 1.2)
                    yoga_str += f"; {next_y_name} upto {jd_to_time_12hr(next_end_jd, info_timezone, ref_date)}"
                except: pass
            
            result_data['Yogalu'] = yoga_str
        else:
            result_data['Yogalu'] = y_name
            
        # Karanamulu
        karana_data = sankranti.karana(jd_midnight, place)
        karana_list = []
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
                    karana_list.append(f"{k_name} upto {format_time_12hr(k_end, include_date=True, ref_date=ref_date, check_next_day=True)}")
        
        result_data['Karanamulu'] = "; ".join(karana_list) if karana_list else "No data"
        
        # Sun/Moon Sign
        sunrise_jd_ut = sr_info[0] - info_timezone/24.0
        result_data['Sunsign'] = RASHI_NAMES[int(sankranti.solar_longitude(sunrise_jd_ut)/30)]['english']
        result_data['Moonsign'] = RASHI_NAMES[int(sankranti.lunar_longitude(sunrise_jd_ut)/30)]['english']
        
        # Timings
        rk = sankranti.rahu_kalam(jd_midnight, place)
        gk = sankranti.gulika_kalam(jd_midnight, place)
        yg = sankranti.yamaganda_kalam(jd_midnight, place)
        
        result_data['Rahu Kalam'] = format_time_range_12hr(rk[0], rk[1], ref_date)
        result_data['Gulikai Kalam'] = format_time_range_12hr(gk[0], gk[1], ref_date)
        result_data['Yamaganda'] = format_time_range_12hr(yg[0], yg[1], ref_date)
        
        if sankranti.vaara(jd_midnight) == 3:
            result_data['Abhijit'] = "None"
        else:
            ab = sankranti.abhijit_muhurta(jd_midnight, place)
            result_data['Abhijit'] = format_time_range_12hr(to_dms(ab[0]), to_dms(ab[1]), ref_date)
            
        # Dur Muhurtam
        sunrise_h = sr_info[1][0] + sr_info[1][1]/60.0 + sr_info[1][2]/3600.0
        sunset_h = ss_info[1][0] + ss_info[1][1]/60.0 + ss_info[1][2]/3600.0
        next_sr = sankranti.sunrise(jd_midnight+1, place)
        next_sr_h = 24 + next_sr[1][0] + next_sr[1][1]/60 + next_sr[1][2]/3600
        
        night_len = next_sr_h - sunset_h
        night_muh = night_len / 15.0
        
        dm_raw = sankranti.durmuhurtam(jd_midnight, place)
        dm_str = format_time_range_12hr(to_dms(dm_raw[0][0]), to_dms(dm_raw[1][0]), ref_date)
        
        if dm_raw[0][1] != 0:
            dm2_s = dm_raw[0][1]
            if dm2_s >= sunset_h:
                n_idx = round((dm2_s - sunset_h)/night_muh)
                dm2_s = sunset_h + n_idx*night_muh
                dm2_e = sunset_h + (n_idx+1)*night_muh
            else:
                dm2_e = dm_raw[1][1]
            dm_str += f"; {format_time_range_12hr(to_dms(dm2_s), to_dms(dm2_e), ref_date)}"
            
        result_data['Dur Muhurtamulu'] = dm_str
        
        # =====================================================================
        # Varjyam and Amrit Kalam Calculation
        # =====================================================================
        # Calculate based on nakshatra at sunrise (DrikPanchang convention)
        nak_data = sankranti.nakshatra(jd_midnight, place)
        nak_num = nak_data[0]
        
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
            try:
                next_n_end_jd = sankranti.bisection_search(next_nak_end_dist, next_n_start_jd, next_n_start_jd + 1.5)
                
                nakshatras_to_calculate.append({
                    'num': next_nak_num,
                    'start_jd': next_n_start_jd,
                    'end_jd': next_n_end_jd
                })
            except:
                pass
        
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
        
        return {
            "meta": result_meta,
            "data": result_data
        }

    def calculate_full(self, year, month, day, hour, minute, second, lat, lon, info_timezone):
        return self.calculate(year, month, day, hour, minute, second, lat, lon, info_timezone)

if __name__ == "__main__":
    c = TeluguPanchangCalculator()
    # Test case: Jan 27 2026, Phuket (Image 1)
    # Phuket: 7.8804° N, 98.3923° E. Timezone 7.0
    print("Test: Jan 27 2026, Phuket")
    res = c.calculate(2026, 1, 27, 6, 0, 0, 7.8804, 98.3923, 7.0)
    import json
    print(json.dumps(res, indent=4))
