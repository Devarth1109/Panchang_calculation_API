# malyalam_panchang_calculator.py

import sankranti
from sankranti import Date, Place
import datetime
from religious_data import TITHI_NAMES, NAKSHATRA_NAMES, YOGA_NAMES, RASHI_NAMES, VARA_NAMES, KARANA_NAMES, SAMVAT_YEAR_NAMES
from panchang_calculator import AMRIT_KALAM_START_HOURS

VARJYAM_START_HOURS = {
    1: [20.0],   # Aswini
    2: [9.6],    # Bharani
    3: [12.0],   # Krittika
    4: [16.0],   # Rohini
    5: [5.6],    # Mrigasira
    6: [8.4],    # Aridra
    7: [12.0],   # Punarvasu
    8: [8.0],    # Pushya
    9: [12.8],   # Aslesha
    10: [12.0],  # Makha
    11: [8.0],   # Pubba (Purva Phalguni)
    12: [7.2],   # Uttara (Uttara Phalguni)
    13: [8.4],   # Hasta
    14: [8.0],   # Chitta
    15: [5.6],   # Swati
    16: [5.6],   # Visakha
    17: [4.0],   # Anuradha
    18: [5.6],   # Jyeshta
    19: [8.0, 22.4],   # Moola - TWO Varjyam periods
    20: [9.6],   # Poorvashadha
    21: [8.0],   # Uttarashadha
    22: [4.0],   # Sravana
    23: [4.0],   # Dhanishta
    24: [7.2],   # Satabhisha
    25: [6.4],   # Poorvabhadra
    26: [9.6],   # Uttarabhadra
    27: [12.0]   # Revati
}

MALAYALAM_LUNAR_MONTH_NAMES = {
    1: "Chaitra",
    2: "Vaisakha", 
    3: "Jyeshtha",
    4: "Ashadha",
    5: "Shravana",
    6: "Bhadrapada",
    7: "Ashwina",
    8: "Karthika",
    9: "Margashirsha",
    10: "Pausha",
    11: "Magham",
    12: "Phalguna"
}

MALAYALAM_VARA = [
    "Njayar (Sunday)", "Thinkal (Monday)", "Chovva (Tuesday)", "Budhan (Wednesday)",
    "Vyazham (Thursday)", "Velli (Friday)", "Shani (Saturday)"
]

MALAYALAM_NAKSHATRA_NAMES = {
    1: "Ashwathi", 2: "Bharani", 3: "Karthika", 4: "Rohini", 5: "Makayiram",
    6: "Thiruvathira", 7: "Punartham", 8: "Pooyam", 9: "Ayilyam", 10: "Makam",
    11: "Pooram", 12: "Uthram", 13: "Atham", 14: "Chithira", 15: "Chothi",
    16: "Visakham", 17: "Anizham", 18: "Thrikketta", 19: "Moolam", 20: "Pooradam",
    21: "Uthradam", 22: "Thiruvonam", 23: "Avittam", 24: "Chathayam", 25: "Pooruruttathi",
    26: "Uthrattathi", 27: "Revathi"
}

MALAYALAM_PAKSHA = {"shukla": "Shukla Paksha", "krishna": "Krishna Paksha"}

MALAYALAM_TITHI_NAMES = {
    1: "Pradhama", 2: "Dwitiya", 3: "Tritiya", 4: "Chaturthi", 5: "Panchami",
    6: "Shashthi", 7: "Saptami", 8: "Ashtami", 9: "Navami", 10: "Dasami",
    11: "Ekadasi", 12: "Dwadasi", 13: "Trayodasi", 14: "Chaturdashi", 15: "Pournami",
    16: "Pradhama", 17: "Dwitiya", 18: "Tritiya", 19: "Chaturthi", 20: "Panchami",
    21: "Shashthi", 22: "Saptami", 23: "Ashtami", 24: "Navami", 25: "Dasami",
    26: "Ekadasi", 27: "Dwadasi", 28: "Trayodasi", 29: "Chaturdashi", 30: "Amavasya"
}

ANANDADI_YOGA_NAMES = [
    "Aananda", "Kaladanda", "Thumra", "Prajapathi", "Soumya", "Thulanksha", 
    "Dhwaja", "Shreevatsa", "Vajra", "Mudgara", "Chatra", "Mithra", 
    "Maanas", "Padmam", "Lumba", "Uthpatha", "Mruthyu", "Kaana", 
    "Siddhi", "Shubham", "Amrutha", "Musala", "Kada", "Mathanga", 
    "Rakshasa", "Chara", "Sthira"
]

# Fixed Offsets: Verified against DrikPanchang reference data
ANANDADI_WEEKDAY_OFFSET = {
    0: 0,    # Sunday
    1: 24,   # Monday
    2: 20,   # Tuesday
    3: 15,   # Wednesday
    4: 12,   # Thursday
    5: 8,    # Friday
    6: 4     # Saturday
}

TAMIL_YOGA_TABLE = {
    # Sunday (0)
    0: ["Siddha", "Prabalarishta", "Marana", "Siddha", "Siddha", "Marana",
        "Siddha", "Siddha", "Siddha", "Marana", "Siddha", "Amrita",
        "Amrita", "Siddha", "Siddha", "Marana", "Siddha", "Marana",
        "Amrita", "Amrita", "Amrita", "Siddha", "Marana", "Marana",
        "Siddha", "Amrita", "Amrita"],
    # Monday (1) - Uthrattathi(index 25)=Marana
    1: ["Marana", "Siddha", "Siddha", "Amrita", "Amrita", "Marana",
        "Siddha", "Amrita", "Siddha", "Siddha", "Siddha", "Siddha",
        "Amrita", "Marana", "Siddha", "Siddha", "Siddha", "Marana",
        "Siddha", "Siddha", "Marana", "Amrita", "Siddha", "Siddha",
        "Siddha", "Marana", "Amrita"],
    # Tuesday (2)
    2: ["Amrita", "Siddha", "Marana", "Marana", "Marana", "Siddha",
        "Marana", "Siddha", "Marana", "Siddha", "Marana", "Siddha",
        "Siddha", "Marana", "Siddha", "Siddha", "Siddha", "Siddha",
        "Siddha", "Siddha", "Siddha", "Siddha", "Marana", "Marana",
        "Marana", "Siddha", "Siddha"],
    # Wednesday (3) - Ayilyam(index 8)=Marana, Chithira(index 13)=Marana
    3: ["Siddha", "Siddha", "Siddha", "Siddha", "Siddha", "Siddha",
        "Siddha", "Siddha", "Marana", "Siddha", "Siddha", "Siddha",
        "Siddha", "Marana", "Siddha", "Siddha", "Amrita", "Amrita",
        "Siddha", "Siddha", "Siddha", "Amrita", "Siddha", "Siddha",
        "Siddha", "Siddha", "Siddha"],
    # Thursday (4)
    4: ["Siddha", "Siddha", "Marana", "Siddha", "Marana", "Marana",
        "Siddha", "Amrita", "Siddha", "Siddha", "Siddha", "Marana",
        "Siddha", "Siddha", "Amrita", "Siddha", "Siddha", "Marana",
        "Marana", "Siddha", "Siddha", "Siddha", "Siddha", "Marana",
        "Marana", "Siddha", "Siddha"],
    # Friday (5) - Rohini(index 3)=Amrita, Makayiram(index 4)=Amrita, Pooruruttathi(index 24)=Marana
    5: ["Siddha", "Siddha", "Siddha", "Amrita", "Amrita", "Siddha",
        "Siddha", "Siddha", "Marana", "Marana", "Siddha", "Siddha",
        "Siddha", "Marana", "Siddha", "Siddha", "Siddha", "Marana",
        "Siddha", "Siddha", "Amrita", "Marana", "Siddha", "Siddha",
        "Marana", "Siddha", "Amrita"],
    # Saturday (6) - Moolam(index 18)=Marana, Pooradam(index 19)=Amrita, Chothi(index 14)=Amrita
    6: ["Siddha", "Marana", "Siddha", "Siddha", "Siddha", "Siddha",
        "Siddha", "Siddha", "Marana", "Siddha", "Siddha", "Marana",
        "Siddha", "Marana", "Amrita", "Siddha", "Amrita", "Siddha",
        "Marana", "Amrita", "Siddha", "Siddha", "Siddha", "Siddha",
        "Marana", "Siddha", "Siddha"]
}

MONTH_NAMES_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def format_time_12hr(dms_list, include_date=False, ref_date=None):
    h, m, s = dms_list
    day_offset = 0
    if h >= 24:
        day_offset = int(h // 24)
        h = h % 24
    period = "AM" if h < 12 else "PM"
    h_12 = h if h <= 12 else h - 12
    if h_12 == 0: h_12 = 12
    time_str = f"{int(h_12):02d}:{int(m):02d} {period}"
    if include_date and day_offset > 0 and ref_date:
        next_date = ref_date + datetime.timedelta(days=day_offset)
        time_str += f", {MONTH_NAMES_SHORT[next_date.month-1]} {next_date.day:02d}"
    return time_str

def format_time_range_12hr(start_dms, end_dms, ref_date=None):
    start_h, start_m, _ = start_dms
    end_h, end_m, _ = end_dms
    def fmt(h, m, ref):
        off = int(h // 24)
        h %= 24
        p = "AM" if h < 12 else "PM"
        h12 = h if 0 < h <= 12 else abs(h-12)
        if h12 == 0: h12 = 12
        s = f"{int(h12):02d}:{int(m):02d} {p}"
        if off > 0 and ref:
            d = ref + datetime.timedelta(days=off)
            s += f", {MONTH_NAMES_SHORT[d.month-1]} {d.day:02d}"
        return s
    return f"{fmt(start_h, start_m, ref_date)} to {fmt(end_h, end_m, ref_date)}"

def jd_to_time_12hr(jd_ut, tz, ref_date):
    local_jd = jd_ut + tz / 24.0
    frac = local_jd - int(local_jd) + 0.5
    if frac >= 1.0: frac -= 1.0
    total_hours = frac * 24
    hours, minutes = int(total_hours), int((total_hours - int(total_hours)) * 60)
    greg = sankranti.jd_to_gregorian(local_jd)
    time_date = datetime.date(greg[0], greg[1], greg[2])
    day_offset = (time_date - ref_date).days
    period = "AM" if hours < 12 else "PM"
    h_12 = hours if 0 < hours <= 12 else abs(hours - 12)
    if h_12 == 0: h_12 = 12
    time_str = f"{int(h_12):02d}:{int(minutes):02d} {period}"
    if day_offset > 0:
        time_str += f", {MONTH_NAMES_SHORT[time_date.month-1]} {time_date.day:02d}"
    return time_str

def get_anandadi_yoga(weekday, nakshatra_num):
    offset = ANANDADI_WEEKDAY_OFFSET.get(weekday, 0)
    yoga_index = (nakshatra_num - 1 + offset) % 27
    return ANANDADI_YOGA_NAMES[yoga_index]

def get_tamil_yoga(weekday, nakshatra_num):
    if weekday in TAMIL_YOGA_TABLE and 1 <= nakshatra_num <= 27:
        return TAMIL_YOGA_TABLE[weekday][nakshatra_num - 1]
    return "Unknown"

def get_shaka_samvat(year, month, day, lunar_month=None):
    if lunar_month is not None:
        if lunar_month >= 1 and lunar_month <= 9:
            # Chaitra to Margashirsha - new Shaka year
            shaka_year = year - 78
        elif lunar_month >= 10:
            # Pausha, Magha, Phalguna - check Gregorian month
            if month >= 1 and month <= 3:
                shaka_year = year - 79  # Still in old Shaka year
            else:
                shaka_year = year - 78
        else:
            shaka_year = year - 78
    else:
        # Fallback to original logic if lunar month not provided
        shaka_year = (year - 79) if (month < 4 or (month == 4 and day < 15)) else (year - 78)
    
    samvat_index = (shaka_year + 11) % 60
    return shaka_year, SAMVAT_YEAR_NAMES[samvat_index]

class MalayalamPanchangCalculator:
    def __init__(self):
        sankranti.set_ayanamsa_mode()
        
    def calculate(self, year, month, day, hour, minute, second, lat, lon, info_timezone):
        place = Place(lat, lon, info_timezone)
        jd_midnight = sankranti.gregorian_to_jd(Date(year, month, day))
        result = {}
        ref_date = datetime.date(year, month, day)
        
        sr_info, ss_info = sankranti.sunrise(jd_midnight, place), sankranti.sunset(jd_midnight, place)
        mr_val, ms_val = sankranti.moonrise(jd_midnight, place), sankranti.moonset(jd_midnight, place)
        result['Sunrise'], result['Sunset'] = format_time_12hr(sr_info[1]), format_time_12hr(ss_info[1])
        
        # Moon processing
        sunrise_hours = sr_info[1][0] + sr_info[1][1]/60 + sr_info[1][2]/3600
        if mr_val[0] < 0 or mr_val[0] >= 48 or abs((mr_val[0] + mr_val[1]/60) - sunrise_hours)*60 < 2:
            result['Moonrise'] = "No Moonrise"
        else:
            result['Moonrise'] = format_time_12hr(mr_val, True, ref_date)
            
        if ms_val[0] < 0 or ms_val[0] >= 36:
            result['Moonset'] = "No Moonset"
        else:
            ms_h = ms_val[0] + ms_val[1]/60
            if ms_h >= 24:
                sr_next = sankranti.sunrise(jd_midnight + 1, place)
                if (ms_h - 24) >= (sr_next[1][0] + sr_next[1][1]/60): result['Moonset'] = "No Moonset"
                else: result['Moonset'] = format_time_12hr(ms_val, True, ref_date)
            else: result['Moonset'] = format_time_12hr(ms_val, True, ref_date)

        # Calculate lunar month first (needed for Shaka Samvat)
        masa_info = sankranti.masa(jd_midnight, place, amanta=True)
        l_month = MALAYALAM_LUNAR_MONTH_NAMES.get(masa_info[0], "Unknown")
        result['Lunar Month'] = f"{l_month} (Adhik)" if masa_info[1] else l_month
        
        # Now calculate Shaka Samvat using lunar month
        shaka_year, samvat_name = get_shaka_samvat(year, month, day, lunar_month=masa_info[0])
        result['Shaka Samvat'] = f"{shaka_year} {samvat_name}"
        weekday_idx = sankranti.vaara(jd_midnight)
        result['Weekday'] = MALAYALAM_VARA[weekday_idx]
        
        t_data = sankranti.tithi(jd_midnight, place)
        result['Paksha'] = MALAYALAM_PAKSHA['shukla'] if t_data[0] <= 15 else MALAYALAM_PAKSHA['krishna']
        t_name = MALAYALAM_TITHI_NAMES.get(t_data[0], TITHI_NAMES[t_data[0]]['english'])
        t_end_h = t_data[1][0] + t_data[1][1]/60.0
        if t_end_h < 24 + sunrise_hours:
            result['Tithi'] = f"{t_name} upto {format_time_12hr(t_data[1], True, ref_date)}"
            if t_end_h < 24:
                nt = (t_data[0] % 30) + 1
                result['Tithi'] += f"; {MALAYALAM_TITHI_NAMES.get(nt, TITHI_NAMES[nt]['english'])}"
        else: result['Tithi'] = t_name

        n_data = sankranti.nakshatra(jd_midnight, place)
        n_name = MALAYALAM_NAKSHATRA_NAMES.get(n_data[0], NAKSHATRA_NAMES[n_data[0]-1]['english'])
        n_end_h = n_data[1][0] + n_data[1][1]/60.0
        if sunrise_hours <= n_end_h < 30 or n_end_h < sunrise_hours:
            result['Nakshathram'] = f"{n_name} upto {format_time_12hr(n_data[1], True, ref_date)}"
            nn = (n_data[0] % 27) + 1
            result['Nakshathram'] += f"; {MALAYALAM_NAKSHATRA_NAMES.get(nn, NAKSHATRA_NAMES[nn-1]['english'])}"
        else: result['Nakshathram'] = n_name

        y_data = sankranti.yoga(jd_midnight, place)
        y_name, y_end_h = YOGA_NAMES[y_data[0]-1]['english'], y_data[1][0] + y_data[1][1]/60.0
        nsr = sankranti.sunrise(jd_midnight + 1, place)
        nsr_h = 24 + nsr[1][0] + nsr[1][1]/60.0
        if y_end_h >= nsr_h: result['Yoga'] = f"{y_name} upto Full Night"
        elif y_end_h < 30:
            result['Yoga'] = f"{y_name} upto {format_time_12hr(y_data[1], True, ref_date)}"
            if y_end_h < 24 + sunrise_hours:
                ny = (y_data[0] % 27) + 1
                result['Yoga'] += f"; {YOGA_NAMES[ny-1]['english']}"
        else: result['Yoga'] = y_name

        k_data = sankranti.karana(jd_midnight, place)
        def kname(n):
            if n == 1: return "Kimthugnam"
            if n == 58: return "Pullu"
            if n == 59: return "Chathushpadam"
            if n == 60: return "Nagavu"
            return ["Simham", "Puli", "Panni", "Kazhatha", "Aana", "Surabhi", "Vishti"][(n-2)%7]
        
        k_list = []
        seen = set()
        for i in range(0, len(k_data), 2):
            kh = k_data[i+1][0] + k_data[i+1][1]/60.0
            if kh >= sunrise_hours and k_data[i] not in seen:
                k_list.append((k_data[i], k_data[i+1], kh))
                seen.add(k_data[i])
        k_list.sort(key=lambda x: x[2])
        if k_list:
            result['Karana'] = f"{kname(k_list[0][0])} upto {format_time_12hr(k_list[0][1], True, ref_date)}"
            if len(k_list) >= 2:
                nk_h = k_list[1][2]
                suff = "upto Full Night" if nk_h >= nsr_h else f"upto {format_time_12hr(k_list[1][1], True, ref_date)}"
                result['Karana'] += f"; {kname(k_list[1][0])} {suff}"
            else:
                result['Karana'] += f"; {kname((k_list[0][0]%60)+1)} upto Full Night"

        s_jd_ut = sr_info[0] - info_timezone / 24.0
        result['Sunsign'] = RASHI_NAMES[int(sankranti.solar_longitude(s_jd_ut)/30)]['english']
        result['Moonsign'] = RASHI_NAMES[int(sankranti.lunar_longitude(s_jd_ut)/30)]['english']
        
        rk, gk, yg = sankranti.rahu_kalam(jd_midnight, place), sankranti.gulika_kalam(jd_midnight, place), sankranti.yamaganda_kalam(jd_midnight, place)
        result['Rahu Kalam'], result['Gulikai Kalam'], result['Yamaganda'] = format_time_range_12hr(rk[0], rk[1], ref_date), format_time_range_12hr(gk[0], gk[1], ref_date), format_time_range_12hr(yg[0], yg[1], ref_date)
        
        if weekday_idx == 3: result['Abhijit'] = "None"
        else:
            ab = sankranti.abhijit_muhurta(jd_midnight, place)
            result['Abhijit'] = format_time_range_12hr(sankranti.to_dms(ab[0]), sankranti.to_dms(ab[1]), ref_date)

        dm = sankranti.durmuhurtam(jd_midnight, place)
        dm_s = format_time_range_12hr(sankranti.to_dms(dm[0][0]), sankranti.to_dms(dm[1][0]), ref_date)
        if dm[0][1] != 0:
            d2s, d2e = dm[0][1], dm[1][1]
            if d2s >= (ss_info[1][0] + ss_info[1][1]/60):
                dur_n = (nsr_h - (ss_info[1][0] + ss_info[1][1]/60)) / 15.0
                idx_n = round((d2s - (ss_info[1][0] + ss_info[1][1]/60)) / dur_n)
                d2s = (ss_info[1][0] + ss_info[1][1]/60) + (idx_n * dur_n)
                d2e = d2s + dur_n
            dm_s += f"; {format_time_range_12hr(sankranti.to_dms(d2s), sankranti.to_dms(d2e), ref_date)}"
        result['Dur Muhurtam'] = dm_s

        # Varjyam/Amrit
        def get_n_jd(num, start_jd):
            def dist(t):
                m = sankranti.lunar_longitude(t)
                target = num * (360/27.0)
                if num == 27 and m > 180: return m - 360
                return sankranti.norm180(m - target)
            return sankranti.bisection_search(dist, start_jd, start_jd + 1.5)

        def get_n_start(num, ref_jd):
            def dist(t):
                m = sankranti.lunar_longitude(t)
                target = (num - 1) * (360/27.0)
                return sankranti.norm180(m - target)
            return sankranti.bisection_search(dist, ref_jd - 1.5, ref_jd + 0.2)

        cur_n = n_data[0]
        n_start_jd = get_n_start(cur_n, s_jd_ut)
        n_end_jd = get_n_jd(cur_n, s_jd_ut)
        n_tasks = [{'num': cur_n, 's': n_start_jd, 'e': n_end_jd}]
        if n_end_jd < s_jd_ut + 1.2:
            nxt_n = (cur_n % 27) + 1
            n_tasks.append({'num': nxt_n, 's': n_end_jd, 'e': get_n_jd(nxt_n, n_end_jd)})

        # Calculate next sunrise JD for validation
        nsr_jd_ut = nsr[0] - info_timezone / 24.0
        
        v_list, a_list = [], []
        for nt in n_tasks:
            dur = nt['e'] - nt['s']
            for vh in VARJYAM_START_HOURS.get(nt['num'], [0]):
                vs = nt['s'] + (dur * vh / 24.0)
                ve = vs + (dur * 1.6 / 24.0)
                # Varjyam must: start >= sunrise, end <= nakshatra end, end <= next sunrise
                # Also validate that Varjyam end doesn't exceed the nakshatra end
                if (s_jd_ut <= vs < nsr_jd_ut and 
                    ve <= nt['e'] and 
                    ve <= nsr_jd_ut and 
                    (ve - vs) > 0.003):
                    v_list.append((vs, f"{jd_to_time_12hr(vs, info_timezone, ref_date)} to {jd_to_time_12hr(ve, info_timezone, ref_date)}"))
            ah = AMRIT_KALAM_START_HOURS.get(nt['num'], 0)
            as_ut = nt['s'] + (dur * ah / 24.0)
            ae_ut = as_ut + (dur * 1.6 / 24.0)
            # Amrit Kalam must: start >= sunrise, start < next sunrise
            if s_jd_ut <= as_ut < nsr_jd_ut and (ae_ut - as_ut) > 0.003:
                a_list.append(f"{jd_to_time_12hr(as_ut, info_timezone, ref_date)} to {jd_to_time_12hr(ae_ut, info_timezone, ref_date)}")
        
        v_list.sort(key=lambda x: x[0])
        result['Amrit Kalam'] = "; ".join(a_list) if a_list else "None"
        result['Varjyam'] = "; ".join([x[1] for x in v_list]) if v_list else "None"

        # Yoga Transitions
        ay_cur, ty_cur = get_anandadi_yoga(weekday_idx, cur_n), get_tamil_yoga(weekday_idx, cur_n)
        if sunrise_hours <= n_end_h < nsr_h:
            nxt_n = (cur_n % 27) + 1
            ay_nxt, ty_nxt = get_anandadi_yoga(weekday_idx, nxt_n), get_tamil_yoga(weekday_idx, nxt_n)
            n_end_str = format_time_12hr(n_data[1], True, ref_date)
            
            # Check for 3rd Nakshatra within same day
            n2_end_jd = get_n_jd(nxt_n, n_end_jd)
            n2_end_loc = n2_end_jd + info_timezone / 24.0
            n2_h = ((n2_end_loc - int(n2_end_loc) + 0.5) % 1.0) * 24
            n2_days = (datetime.date(*sankranti.jd_to_gregorian(n2_end_loc)[:3]) - ref_date).days
            if (n2_days * 24 + n2_h) < nsr_h:
                n3_n = (nxt_n % 27) + 1
                ay3, ty3 = get_anandadi_yoga(weekday_idx, n3_n), get_tamil_yoga(weekday_idx, n3_n)
                n2_str = format_time_12hr([int(n2_h), int((n2_h-int(n2_h))*60), 0], True, ref_date)
                result['Anandadi Yoga'] = f"{ay_cur} upto {n_end_str}; {ay_nxt} upto {n2_str}; {ay3}"
                result['Tamil Yoga'] = f"{ty_cur} upto {n_end_str}; {ty_nxt} upto {n2_str}; {ty3}"
            else:
                result['Anandadi Yoga'] = f"{ay_cur} upto {n_end_str}; {ay_nxt}"
                result['Tamil Yoga'] = f"{ty_cur} upto {n_end_str}; {ty_nxt}"
        else:
            result['Anandadi Yoga'], result['Tamil Yoga'] = ay_cur, ty_cur

        return result