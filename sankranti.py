from __future__ import division
from math import ceil, floor
from collections import namedtuple as struct
import swisseph as swe

Date = struct('Date', ['year', 'month', 'day'])
Place = struct('Place', ['latitude', 'longitude', 'timezone'])

sidereal_year = 365.256360417   # From WolframAlpha

# Hindu sunrise/sunset: DrikPanchang uses Visual Sunrise (Upper Limb + Refraction)
# Removing BIT_DISC_CENTER and BIT_NO_REFRACTION to match.
_rise_flags = 0

# namah suryaya chandraya mangalaya ... rahuve ketuve namah
swe.RAHU = swe.MEAN_NODE # Rahu = either MEAN_NODE or swe.TRUE_NODE
swe.KETU = swe.PLUTO  # I've mapped Pluto to Ketu
planet_list = [swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER,
               swe.VENUS, swe.SATURN, swe.MEAN_NODE, # Rahu = MEAN_NODE
               swe.KETU, swe.URANUS, swe.NEPTUNE ]

revati_359_50 = lambda: swe.set_sid_mode(swe.SIDM_USER, 1926892.343164331, 0)
galc_cent_mid_mula = lambda: swe.set_sid_mode(swe.SIDM_USER, 1922011.128853056, 0)

# Possible ayanamas
# swe.SIDM_ALDEBARAN_15TAU     swe.SIDM_BABYL_HUBER         swe.SIDM_DJWHAL_KHUL         swe.SIDM_J2000               swe.SIDM_SASSANIAN             swe.SIDM_TRUE_CITRA
# swe.SIDM_ARYABHATA           swe.SIDM_BABYL_KUGLER1       swe.SIDM_FAGAN_BRADLEY       swe.SIDM_JN_BHASIN           swe.SIDM_SS_CITRA              swe.SIDM_TRUE_REVATI
# swe.SIDM_ARYABHATA_MSUN      swe.SIDM_BABYL_KUGLER2       swe.SIDM_GALCENT_0SAG        swe.SIDM_KRISHNAMURTI        swe.SIDM_SS_REVATI             swe.SIDM_USER
# swe.SIDM_B1950               swe.SIDM_BABYL_KUGLER3       swe.SIDM_HIPPARCHOS          swe.SIDM_LAHIRI              swe.SIDM_SURYASIDDHANTA        swe.SIDM_USHASHASHI
# swe.SIDM_BABYL_ETPSC         swe.SIDM_DELUCE              swe.SIDM_J1900               swe.SIDM_RAMAN               swe.SIDM_SURYASIDDHANTA_MSUN   swe.SIDM_YUKTESHWAR
set_ayanamsa_mode = lambda: swe.set_sid_mode(swe.SIDM_LAHIRI)
reset_ayanamsa_mode = lambda: swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY)

# Temporary function
def get_planet_name(planet):
  names = { swe.SUN: 'Surya', swe.MOON: 'Candra', swe.KUJA: 'Mangala',
            swe.MERCURY: 'Budha', swe.JUPITER: 'Guru', swe.VENUS: 'Sukra',
            swe.SATURN: 'Sani', swe.RAHU: 'Rahu', swe.KETU: 'Ketu', swe.PLUTO: 'Ketu'}
  return names[planet]

# Convert 23d 30' 30" to 23.508333 degrees
from_dms = lambda degs, mins, secs = 0: degs + mins/60 + secs/3600

# the inverse
def to_dms_prec(deg):
  d = int(deg)
  mins = (deg - d) * 60
  m = int(mins)
  s = round((mins - m) * 60, 6)
  return [d, m, s]

def to_dms(deg):
  d, m, s = to_dms_prec(deg)
  return [d, m, int(s)]

def unwrap_angles(angles):
  """Add 360 to those elements in the input list so that
     all elements are sorted in ascending order."""
  result = angles
  for i in range(1, len(angles)):
    if result[i] < result[i-1]: result[i] += 360

  assert(result == sorted(result))
  return result

# Make angle lie between [-180, 180) instead of [0, 360)
norm180 = lambda angle: (angle - 360) if angle >= 180 else angle;

# Make angle lie between [0, 360)
norm360 = lambda angle: angle % 360

# Ketu is always 180° after Rahu, so same coordinates but different constellations
# i.e if Rahu is in Pisces, Ketu is in Virgo etc
ketu = lambda rahu: (rahu + 180) % 360

# Set env variable SE_EPHE_PATH to /usr/share/libswe/ephe
swe.set_ephe_path('/usr/share/libswe/ephe')
init_swisseph = lambda: None

def function(point):
    swe.set_sid_mode(swe.SIDM_USER, point, 0.0)
    #swe.set_sid_mode(swe.SIDM_LAHIRI)
    # Place Revati at 359°50'
    #fval = norm180(swe.fixstar_ut("Revati", point, flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) - ((359 + 49/60 + 59/3600) - 360)
    # Place Revati at 0°0'0"
    #fval = norm180(swe.fixstar_ut("Revati", point, flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0])
    # Place Aldebaran in middle of Rohini (Rohini paksha ayanamsha)
    #fval = norm180(swe.fixstar_ut("Aldebaran", jd,  swe.FLG_SIDEREAL)[0][0] - (46+40/60))
    # Place Citra at 180°
    fval = swe.fixstar_ut("Citra", point, flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0] - (180)
    # Place Pushya (delta Cancri) at 106°
    # fval = swe.fixstar_ut(",deCnc", point, flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0] - (106)
    return fval

def bisection_search(func, start, stop):
  left = start
  right = stop
  epsilon = 5E-10   # Anything better than this puts the loop below infinite

  while True:
    middle = (left + right) / 2
    midval =  func(middle)
    rtval = func(right)
    if midval * rtval >= 0:
      right = middle
    else:
      left = middle

    if (right - left) <= epsilon: break

  return (right + left) / 2

def inverse_lagrange(x, y, ya):
  """Given two lists x and y, find the value of x = xa when y = ya, i.e., f(xa) = ya"""
  assert(len(x) == len(y))
  total = 0
  for i in range(len(x)):
    numer = 1
    denom = 1
    for j in range(len(x)):
      if j != i:
        numer *= (ya - y[j])
        denom *= (y[i] - y[j])

    total += numer * x[i] / denom

  return total

# Julian Day number as on (year, month, day) at 00:00 UTC
gregorian_to_jd = lambda date, hours = 0.0: swe.julday(date.year, date.month, date.day, hours)
def jd_to_gregorian(jd):
    try:
        result = swe.revjul(jd, swe.GREG_CAL)
        if isinstance(result, (tuple, list)) and len(result) >= 6:
            return result[:6]
        else:
            raise ValueError("Invalid result from swe.revjul")
    except Exception as e:
        # Fallback using datetime for JD conversion
        from datetime import datetime, timedelta
        # JD 2440587.5 corresponds to 1970-01-01 00:00:00 UTC
        base_jd = 2440587.5
        seconds_since_epoch = (jd - base_jd) * 86400
        dt = datetime(1970, 1, 1) + timedelta(seconds=seconds_since_epoch)
        return (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

def local_time_to_jdut1(year, month, day, hour = 0, minutes = 0, seconds = 0, timezone = 0.0):
  """Converts local time to JD(UT1)"""
  y, m, d, h, mnt, s = swe.utc_time_zone(year, month, day, hour, minutes, seconds, timezone)
  # BUG in pyswisseph: replace 0 by s
  jd_et, jd_ut1 = swe.utc_to_jd(y, m, d, h, mnt, 0, cal = swe.GREG_CAL)
  return jd_ut1

def nakshatra_pada(longitude):
  """Gives nakshatra (1..27) and paada (1..4) in which given longitude lies"""
  # 27 nakshatras span 360°
  one_star = (360 / 27)  # = 13°20'
  # Each nakshatra has 4 padas, so 27 x 4 = 108 padas in 360°
  one_pada = (360 / 108) # = 3°20'
  quotient = int(longitude / one_star)
  reminder = (longitude - quotient * one_star)
  pada = int(reminder / one_pada)
  # convert 0..26 to 1..27 and 0..3 to 1..4
  return [1 + quotient, 1 + pada]

def sidereal_longitude(jd, planet, tropical = False):
  """Computes nirayana (sidereal) longitude of given planet on jd"""
  set_ayanamsa_mode()
  is_tropical = swe.FLG_TROPICAL if tropical else swe.FLG_SIDEREAL
  longi = swe.calc_ut(jd, planet, flags = swe.FLG_SWIEPH | is_tropical)
  reset_ayanamsa_mode()
  return norm360(longi[0][0]) # degrees

solar_longitude = lambda jd, tropical = False: sidereal_longitude(jd, swe.SUN, tropical)
lunar_longitude = lambda jd, tropical = False: sidereal_longitude(jd, swe.MOON, tropical)

def sunrise(jd, place):
  """Sunrise when centre of disc is at horizon for given date and place"""
  lat, lon, tz = place
  result = swe.rise_trans(jd - tz/24, swe.SUN, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_RISE)
  rise = result[1][0]  # julian-day number
  # Convert to local time
  return [rise + tz/24., to_dms((rise - jd) * 24 + tz)]

def sunset(jd, place):
  """Sunset when centre of disc is at horizon for given date and place"""
  lat, lon, tz = place
  result = swe.rise_trans(jd - tz/24, swe.SUN, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_SET)
  setting = result[1][0]  # julian-day number
  # Convert to local time
  return [setting + tz/24., to_dms((setting - jd) * 24 + tz)]

def moonrise(jd, place):
  """Moonrise when centre of disc is at horizon for given date and place"""
  lat, lon, tz = place
  # Search from sunrise to find the next moonrise (not previous one)
  rise = sunrise(jd, place)[0]
  result = swe.rise_trans(rise - tz/24, swe.MOON, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_RISE)
  moonrise_jd = result[1][0]  # julian-day number
  # Convert to local time
  return to_dms((moonrise_jd - jd) * 24 + tz)

def moonset(jd, place):
  """Moonset when centre of disc is at horizon for given date and place"""
  lat, lon, tz = place
  # Search from sunrise to find the next moonset (not previous one)
  rise = sunrise(jd, place)[0]
  result = swe.rise_trans(rise - tz/24, swe.MOON, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_SET)
  setting = result[1][0]  # julian-day number
  # Convert to local time
  return to_dms((setting - jd) * 24 + tz)

# Tithi doesn't depend on Ayanamsa
def tithi(jd, place):
  """Tithi at sunrise for given date and place. Also returns tithi's end time."""
  tz = place[2] if isinstance(place, tuple) else place.timezone
  # 1. Find time of sunrise
  rise = sunrise(jd, place)[0] - tz / 24

  # 2. Find tithi at this JDN
  moon_phase = lunar_phase(rise)
  today = ceil(moon_phase / 12)
  degrees_left = today * 12 - moon_phase

  # 3. Compute longitudinal differences at intervals of 0.25 days from sunrise
  offsets = [0.25, 0.5, 0.75, 1.0]
  lunar_long_diff = [ (lunar_longitude(rise + t) - lunar_longitude(rise)) % 360 for t in offsets ]
  solar_long_diff = [ (solar_longitude(rise + t) - solar_longitude(rise)) % 360 for t in offsets ]
  relative_motion = [ moon - sun for (moon, sun) in zip(lunar_long_diff, solar_long_diff) ]

  # 4. Find end time by 4-point inverse Lagrange interpolation
  y = relative_motion
  x = offsets
  # compute fraction of day (after sunrise) needed to traverse 'degrees_left'
  approx_end = inverse_lagrange(x, y, degrees_left)
  ends = (rise + approx_end - jd) * 24 + tz
  answer = [int(today), to_dms(ends)]

  # 5. Check for skipped tithi
  moon_phase_tmrw = lunar_phase(rise + 1)
  tomorrow = ceil(moon_phase_tmrw / 12)
  isSkipped = (tomorrow - today) % 30 > 1
  if isSkipped:
    # interpolate again with same (x,y)
    leap_tithi = today + 1
    degrees_left = leap_tithi * 12 - moon_phase
    approx_end = inverse_lagrange(x, y, degrees_left)
    ends = (rise + approx_end -jd) * 24 + tz
    leap_tithi = 1 if today == 30 else leap_tithi
    answer += [int(leap_tithi), to_dms(ends)]

  return answer


def nakshatra(jd, place):
  """Current nakshatra as of julian day (jd)
     1 = Asvini, 2 = Bharani, ..., 27 = Revati
  """
  # 1. Find time of sunrise
  lat, lon, tz = place
  rise = sunrise(jd, place)[0] - tz / 24.  # Sunrise at UT 00:00

  offsets = [0.0, 0.25, 0.5, 0.75, 1.0]
  longitudes = [ lunar_longitude(rise + t) for t in offsets]

  # 2. Today's nakshatra is when offset = 0
  # There are 27 Nakshatras spanning 360 degrees
  nak = int(floor(longitudes[0] * 27 / 360) + 1)

  # 3. Find end time by 5-point inverse Lagrange interpolation
  y = unwrap_angles(longitudes)
  x = offsets
  approx_end = inverse_lagrange(x, y, nak * 360 / 27)
  ends = (rise - jd + approx_end) * 24 + tz
  answer = [int(nak), to_dms(ends)]

  # 4. Check for skipped nakshatra
  nak_tmrw = int(floor(longitudes[-1] * 27 / 360) + 1)
  isSkipped = (nak_tmrw - nak) % 27 > 1
  if isSkipped:
    leap_nak = nak + 1
    approx_end = inverse_lagrange(offsets, longitudes, leap_nak * 360 / 27)
    ends = (rise - jd + approx_end) * 24 + tz
    leap_nak = 1 if nak == 27 else leap_nak
    answer += [int(leap_nak), to_dms(ends)]

  return answer


def yoga(jd, place):
  """Yoga at given jd and place.
     1 = Vishkambha, 2 = Priti, ..., 27 = Vaidhrti
  """
  # 1. Find time of sunrise
  lat, lon, tz = place
  rise = sunrise(jd, place)[0] - tz / 24.  # Sunrise at UT 00:00

  # 2. Find the Nirayana longitudes and add them
  lunar_long = lunar_longitude(rise)
  solar_long = solar_longitude(rise)
  total = (lunar_long + solar_long) % 360
  # There are 27 Yogas spanning 360 degrees
  yog = int(floor(total * 27 / 360) + 1)

  # 3. Find how many longitudes is there left to be swept
  degrees_left = yog * (360 / 27) - total

  # 3. Compute longitudinal sums at intervals of 0.25 days from sunrise
  offsets = [0.25, 0.5, 0.75, 1.0]
  lunar_long_diff = [ (lunar_longitude(rise + t) - lunar_longitude(rise)) % 360 for t in offsets ]
  solar_long_diff = [ (solar_longitude(rise + t) - solar_longitude(rise)) % 360 for t in offsets ]
  total_motion = [ moon + sun for (moon, sun) in zip(lunar_long_diff, solar_long_diff) ]

  # 4. Find end time by 4-point inverse Lagrange interpolation
  y = total_motion
  x = offsets
  # compute fraction of day (after sunrise) needed to traverse 'degrees_left'
  approx_end = inverse_lagrange(x, y, degrees_left)
  ends = (rise + approx_end - jd) * 24 + tz
  answer = [int(yog), to_dms(ends)]

  # 5. Check for skipped yoga
  lunar_long_tmrw = lunar_longitude(rise + 1)
  solar_long_tmrw = solar_longitude(rise + 1)
  total_tmrw = (lunar_long_tmrw + solar_long_tmrw) % 360
  tomorrow = int(floor(total_tmrw * 27 / 360) + 1)
  isSkipped = (tomorrow - yog) % 27 > 1
  if isSkipped:
    # interpolate again with same (x,y)
    leap_yog = yog + 1
    degrees_left = leap_yog * (360 / 27) - total
    approx_end = inverse_lagrange(x, y, degrees_left)
    ends = (rise + approx_end - jd) * 24 + tz
    leap_yog = 1 if yog == 27 else leap_yog
    answer += [int(leap_yog), to_dms(ends)]

  return answer


def karana(jd, place):
  """Returns the karana and their ending times. (from 1 to 60)"""
  tz = place[2] if isinstance(place, tuple) else place.timezone
  # 1. Find time of sunrise
  rise = sunrise(jd, place)[0] - tz / 24.  # Convert to UT for consistency with nakshatra/yoga

  # 2. Check karana at midnight (start of civil day)
  moon_phase_midnight = lunar_phase(jd)
  karana_at_midnight = ceil(moon_phase_midnight / 6)
  
  # 3. Find karana at sunrise (UT)
  moon_phase = lunar_phase(rise)
  today = ceil(moon_phase / 6)
    
  # 4. Compute longitudinal differences at intervals of 0.25 days from sunrise
  offsets = [0.25, 0.5, 0.75, 1.0]
  lunar_long_diff = [ (lunar_longitude(rise + t) - lunar_longitude(rise)) % 360 for t in offsets ]
  solar_long_diff = [ (solar_longitude(rise + t) - solar_longitude(rise)) % 360 for t in offsets ]
  relative_motion = [ norm180(moon - sun) for (moon, sun) in zip(lunar_long_diff, solar_long_diff) ]

  answer = []
  
  # 5. If karana at midnight is different from karana at sunrise, include it first
  if karana_at_midnight != today:
    degrees_left = norm180(karana_at_midnight * 6 - moon_phase_midnight)
    # Use midnight as reference point for this karana
    midnight_offsets = [0.25, 0.5, 0.75, 1.0]
    midnight_lunar_diff = [ (lunar_longitude(jd + t) - lunar_longitude(jd)) % 360 for t in midnight_offsets ]
    midnight_solar_diff = [ (solar_longitude(jd + t) - solar_longitude(jd)) % 360 for t in midnight_offsets ]
    midnight_relative = [ norm180(moon - sun) for (moon, sun) in zip(midnight_lunar_diff, midnight_solar_diff) ]
    approx_end = inverse_lagrange(midnight_offsets, midnight_relative, degrees_left)
    ends = (jd + approx_end - jd) * 24 + tz
    answer = [int(karana_at_midnight), to_dms(ends)]
  
  # 6. Add karana at sunrise
  degrees_left = norm180(today * 6 - moon_phase)
  y = relative_motion
  x = offsets
  approx_end = inverse_lagrange(x, y, degrees_left)
  ends = (rise + approx_end - jd) * 24 + tz
  answer += [int(today), to_dms(ends)]
  
  # 7. Check for additional karanas during the day
  moon_phase_tmrw = lunar_phase(rise + 1)
  tomorrow = ceil(moon_phase_tmrw / 6)
  karanas_diff = (tomorrow - today) % 60
  
  if karanas_diff > 1:
    # There's a skipped karana, add it
    leap_karana = (today % 60) + 1
    if leap_karana > 60:
      leap_karana = 1
    degrees_left = norm180(leap_karana * 6 - moon_phase)
    approx_end = inverse_lagrange(x, y, degrees_left)
    ends = (rise + approx_end - jd) * 24 + tz
    answer += [int(leap_karana), to_dms(ends)]
    
    # Check if there's yet another karana (3rd one)
    if karanas_diff >= 2:
      leap_karana2 = (leap_karana % 60) + 1
      if leap_karana2 > 60:
        leap_karana2 = 1
      degrees_left = leap_karana2 * 6 - moon_phase
      approx_end = inverse_lagrange(x, y, degrees_left)
      ends = (rise + approx_end - jd) * 24 + tz
      answer += [int(leap_karana2), to_dms(ends)]
  
  return answer

def vaara(jd):
  """Weekday for given Julian day. 0 = Sunday, 1 = Monday,..., 6 = Saturday"""
  return int(ceil(jd + 1) % 7)

def masa(jd, place, amanta = True):
  """Returns lunar month and if it is adhika or not.
     Set amanta = False for Purnimanta month.
     1 = Chaitra, 2 = Vaisakha, ..., 12 = Phalguna"""
  ti = tithi(jd, place)[0]
  critical = sunrise(jd, place)[0]  # - tz/24 ?
  last_moon = new_moon(critical, ti, -1) if amanta else full_moon(critical, ti, -1)
  next_moon = new_moon(critical, ti, +1) if amanta else full_moon(critical, ti, +1)
  this_solar_month = raasi(last_moon)
  next_solar_month = raasi(next_moon)
  is_leap_month = (this_solar_month == next_solar_month)
  if amanta:
    maasa = this_solar_month + 1
  else:
    maasa = this_solar_month + 2
  if maasa > 12: maasa = (maasa % 12)
  return [int(maasa), is_leap_month]

# epoch-midnight to given midnight
# Days elapsed since beginning of Kali Yuga
ahargana = lambda jd: jd - 588465.5

def elapsed_year(jd, maasa_num):
  ahar = ahargana(jd)  # or (jd + sunrise(jd, place)[0])
  kali = int((ahar + (4 - maasa_num) * 30) / sidereal_year)
  saka = kali - 3179
  vikrama = saka + 135
  return kali, saka

# New moon day: sun and moon have same longitude (0 degrees = 360 degrees difference)
def new_moon(jd, tithi_, opt = -1):
  """Returns JDN, where
     opt = -1:  JDN < jd such that lunar_phase(JDN) = 360 degrees
     opt = +1:  JDN >= jd such that lunar_phase(JDN) = 360 degrees
  """
  if opt == -1:  start = jd - tithi_         # previous new moon
  if opt == +1:  start = jd + (30 - tithi_)  # next new moon
  # Search within a span of (start +- 2) days
  x = [ -2 + offset/4 for offset in range(17) ]
  y = [lunar_phase(start + i) for i in x]
  y = unwrap_angles(y)
  y0 = inverse_lagrange(x, y, 360)
  return start + y0

# assumes "tithi" 1..30 are from new moon to new moon
# so tithi = 15 is full moon day
# Full moon day: sun and moon are 180 deg apart
def full_moon(jd, tithi_, opt = -1):
  """Returns JDN, where
     opt = -1:  JDN < jd such that lunar_phase(JDN) = 180 degrees
     opt = +1:  JDN >= jd such that lunar_phase(JDN) = 180 degrees
  """
  if opt == -1:    # previous full moon
    start = jd - (tithi_ - 15) if tithi_ > 15 else jd - (tithi_ + 15)
  if opt == +1:   # next full moon
    start = jd + (15 - tithi_) if tithi_ < 15 else jd - tithi_ + 45
  # Search within a span of (start +- 2) days
  x = [ -2 + offset/4 for offset in range(17) ]
  y = [lunar_phase(start + i) for i in x]
  y = unwrap_angles(y)
  y0 = inverse_lagrange(x, y, 180)
  return start + y0

def raasi(jd):
  """Zodiac of given jd. 1 = Mesha, ... 12 = Meena"""
  s = solar_longitude(jd)
  solar_nirayana = solar_longitude(jd)
  # 12 rasis occupy 360 degrees, so each one is 30 degrees
  return ceil(solar_nirayana / 30.)

def lunar_phase(jd):
  solar_long = solar_longitude(jd)
  lunar_long = lunar_longitude(jd)
  moon_phase = (lunar_long - solar_long) % 360
  return moon_phase

def samvatsara(jd, maasa_num):
  kali = elapsed_year(jd, maasa_num)[0]
  # Change 14 to 0 for North Indian tradition
  # See the function "get_Jovian_Year_name_south" in pancanga.pl
  if kali >= 4009:    kali = (kali - 14) % 60
  samvat = (kali + 27 + int((kali * 211 - 108) / 18000)) % 60
  return samvat

def ritu(masa_num):
  """0 = Vasanta,...,5 = Shishira"""
  return (masa_num - 1) // 2

def day_duration(jd, place):
  srise = sunrise(jd, place)[0]  # julian day num
  sset = sunset(jd, place)[0]    # julian day num
  diff = (sset - srise) * 24     # In hours
  return [diff, to_dms(diff)]

# The day duration is divided into 8 parts
# Similarly night duration
def gauri_chogadiya(jd, place):
  lat, lon, tz = place
  # tz already extracted from tuple above
  srise = swe.rise_trans(jd - tz/24, swe.SUN, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_RISE)[1][0]
  sset = swe.rise_trans(jd - tz/24, swe.SUN, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_SET)[1][0]
  day_dur = (sset - srise)

  end_times = []
  for i in range(1, 9):
    end_times.append(to_dms((srise + (i * day_dur) / 8 - jd) * 24 + tz))

  # Night duration = time from today's sunset to tomorrow's sunrise
  srise = swe.rise_trans((jd + 1) - tz/24, swe.SUN, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_RISE)[1][0]
  night_dur = (srise - sset)
  for i in range(1, 9):
    end_times.append(to_dms((sset + (i * night_dur) / 8 - jd) * 24 + tz))

  return end_times

def trikalam(jd, place, option='rahu'):
  lat, lon, tz = place
  # tz already extracted from tuple above
  srise = swe.rise_trans(jd - tz/24, swe.SUN, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_RISE)[1][0]
  sset = swe.rise_trans(jd - tz/24, swe.SUN, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_SET)[1][0]
  day_dur = (sset - srise)
  weekday = vaara(jd)

  # value in each array is for given weekday (0 = sunday, etc.)
  offsets = { 'rahu': [0.875, 0.125, 0.75, 0.5, 0.625, 0.375, 0.25],
              'gulika': [0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.0],
              'yamaganda': [0.5, 0.375, 0.25, 0.125, 0.0, 0.75, 0.625] }

  start_time = srise + day_dur * offsets[option][weekday]
  end_time = start_time + 0.125 * day_dur

  # to local timezone
  start_time = (start_time - jd) * 24 + tz
  end_time = (end_time - jd) * 24 + tz
  return [to_dms(start_time), to_dms(end_time)] # decimal hours to H:M:S

rahu_kalam = lambda jd, place: trikalam(jd, place, 'rahu')
yamaganda_kalam = lambda jd, place: trikalam(jd, place, 'yamaganda')
gulika_kalam = lambda jd, place: trikalam(jd, place, 'gulika')

def durmuhurtam(jd, place):
  lat, lon, tz = place
  # tz already extracted from tuple above

  # Night = today's sunset to tomorrow's sunrise
  sset = swe.rise_trans(jd - tz/24, swe.SUN, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_SET)[1][0]
  srise = swe.rise_trans((jd + 1) - tz/24, swe.SUN, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_RISE)[1][0]
  night_dur = (srise - sset)

  # Day = today's sunrise to today's sunset
  srise = swe.rise_trans(jd - tz/24, swe.SUN, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_RISE)[1][0]
  day_dur = (sset - srise)

  weekday = vaara(jd)

  # There is one durmuhurtam on Sun, Wed; the rest have two
  # Use None to indicate no period at that position
  offsets = [[10.4, None],  # Sunday
             [6.4, 8.8],   # Monday
             [2.4, 4.8],   # Tuesday, [day_duration , night_duration]
             [5.6, None],   # Wednesday
             [4.0, 8.8],   # Thursday
             [2.4, 6.4],   # Friday
             [0.0, 0.8]]   # Saturday - two consecutive periods in morning

  # second durmuhurtam of tuesday uses night_duration instead of day_duration
  dur = [day_dur, day_dur]
  base = [srise, srise]
  if weekday == 2:  dur[1] = night_dur; base[1] = sset

  # compute start and end timings
  start_times = [0, 0]
  end_times = [0, 0]
  for i in range(0, 2):
    offset = offsets[weekday][i]
    if offset is not None:
      start_times[i] = base[i] + dur[i] * offsets[weekday][i] / 12
      end_times[i] = start_times[i] + day_dur * 0.8 / 12

      # convert to local time
      start_times[i] = (start_times[i] - jd) * 24 + tz
      end_times[i] = (end_times[i] - jd) * 24 + tz

  return [start_times, end_times]  # in decimal hours

def abhijit_muhurta(jd, place):
  """Abhijit muhurta is the 8th muhurta (middle one) of the 15 muhurtas
  during the day_duration (~12 hours)"""
  lat, lon, tz = place
  # tz already extracted from tuple above
  srise = swe.rise_trans(jd - tz/24, swe.SUN, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_RISE)[1][0]
  sset = swe.rise_trans(jd - tz/24, swe.SUN, geopos = (lon, lat, 0), rsmi = _rise_flags + swe.CALC_SET)[1][0]
  day_dur = (sset - srise)

  start_time = srise + 7 / 15 * day_dur
  end_time = srise + 8 / 15 * day_dur

  # to local time
  return [(start_time - jd) * 24 + tz, (end_time - jd) * 24 + tz]

# 'jd' can be any time: ex, 2015-09-19 14:20 UTC
# today = swe.julday(2015, 9, 19, 14 + 20./60)
def planetary_positions(jd, place):
  """Computes instantaneous planetary positions
     (i.e., which celestial object lies in which constellation)

     Also gives the nakshatra-pada division
   """
  tz = place[2] if isinstance(place, tuple) else place.timezone
  jd_ut = jd - tz / 24.

  positions = []
  for planet in planet_list:
    if planet != swe.KETU:
      nirayana_long = sidereal_longitude(jd_ut, planet)
    else: # Ketu
      nirayana_long = ketu(sidereal_longitude(jd_ut, swe.RAHU))

    # 12 zodiac signs span 360°, so each one takes 30°
    # 0 = Mesha, 1 = Vrishabha, ..., 11 = Meena
    constellation = int(nirayana_long / 30)
    coordinates = to_dms(nirayana_long % 30)
    positions.append([planet, constellation, coordinates, nakshatra_pada(nirayana_long)])

  return positions

def ascendant(jd, place):
  """Lagna (=ascendant) calculation at any given time & place"""
  lat, lon, tz = place
  jd_utc = jd - (tz / 24.)
  set_ayanamsa_mode() # needed for swe.houses_ex()

  # returns two arrays, cusps and ascmc, where ascmc[0] = Ascendant
  nirayana_lagna = swe.houses_ex(jd_utc, lat, lon, flags = swe.FLG_SIDEREAL)[1][0]
  # 12 zodiac signs span 360°, so each one takes 30°
  # 0 = Mesha, 1 = Vrishabha, ..., 11 = Meena
  constellation = int(nirayana_lagna / 30)
  coordinates = to_dms(nirayana_lagna % 30)

  reset_ayanamsa_mode()
  return [constellation, coordinates, nakshatra_pada(nirayana_lagna)]

# http://www.oocities.org/talk2astrologer/LearnAstrology/Details/Navamsa.html
# Useful for making D9 divisional chart
def navamsa_from_long(longitude):
  """Calculates the navamsa-sign in which given longitude falls
  0 = Aries, 1 = Taurus, ..., 11 = Pisces
  """
  one_pada = (360 / (12 * 9))  # There are also 108 navamsas
  one_sign = 12 * one_pada    # = 40 degrees exactly
  signs_elapsed = longitude / one_sign
  fraction_left = signs_elapsed % 1
  return int(fraction_left * 12)

def navamsa(jd, place):
  """Calculates navamsa of all planets"""
  tz = place[2] if isinstance(place, tuple) else place.timezone
  jd_utc = jd - tz / 24.

  positions = []
  for planet in planet_list:
    if planet != swe.KETU:
      nirayana_long = sidereal_longitude(jd_utc, planet)
    else: # Ketu
      nirayana_long = ketu(sidereal_longitude(jd_utc, swe.RAHU))

    positions.append([planet, navamsa_from_long(nirayana_long)])

  return positions

# Test functions and unused calculations removed for production build.