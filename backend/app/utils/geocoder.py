from __future__ import annotations

import re
import unicodedata
from functools import lru_cache

# Hardcoded lat/lon/timezone for common cities (fast, no API needed)
_CITY_DATA: dict[str, tuple[float, float, str]] = {
    # Vietnam
    "ho chi minh": (10.8231, 106.6297, "Asia/Ho_Chi_Minh"),
    "saigon":       (10.8231, 106.6297, "Asia/Ho_Chi_Minh"),
    "hcmc":         (10.8231, 106.6297, "Asia/Ho_Chi_Minh"),
    "ha noi":       (21.0278, 105.8342, "Asia/Ho_Chi_Minh"),
    "hanoi":        (21.0278, 105.8342, "Asia/Ho_Chi_Minh"),
    "da nang":      (16.0544, 108.2022, "Asia/Ho_Chi_Minh"),
    "danang":       (16.0544, 108.2022, "Asia/Ho_Chi_Minh"),
    "can tho":      (10.0452, 105.7469, "Asia/Ho_Chi_Minh"),
    "hai phong":    (20.8449, 106.6881, "Asia/Ho_Chi_Minh"),
    "nha trang":    (12.2388, 109.1967, "Asia/Ho_Chi_Minh"),
    "viet nam":     (16.0000, 106.0000, "Asia/Ho_Chi_Minh"),
    "vietnam":      (16.0000, 106.0000, "Asia/Ho_Chi_Minh"),
    # Thailand
    "bangkok":      (13.7563, 100.5018, "Asia/Bangkok"),
    "thailand":     (13.7563, 100.5018, "Asia/Bangkok"),
    # Singapore
    "singapore":    (1.3521,  103.8198, "Asia/Singapore"),
    # Malaysia
    "kuala lumpur": (3.1390,  101.6869, "Asia/Kuala_Lumpur"),
    "malaysia":     (3.1390,  101.6869, "Asia/Kuala_Lumpur"),
    # Indonesia
    "jakarta":      (-6.2088, 106.8456, "Asia/Jakarta"),
    "indonesia":    (-6.2088, 106.8456, "Asia/Jakarta"),
    # Philippines
    "manila":       (14.5995, 120.9842, "Asia/Manila"),
    # Hong Kong
    "hong kong":    (22.3193, 114.1694, "Asia/Hong_Kong"),
    # Taiwan
    "taipei":       (25.0330, 121.5654, "Asia/Taipei"),
    "taiwan":       (25.0330, 121.5654, "Asia/Taipei"),
    # China
    "beijing":      (39.9042, 116.4074, "Asia/Shanghai"),
    "shanghai":     (31.2304, 121.4737, "Asia/Shanghai"),
    "guangzhou":    (23.1291, 113.2644, "Asia/Shanghai"),
    "shenzhen":     (22.5431, 114.0579, "Asia/Shanghai"),
    "china":        (35.8617, 104.1954, "Asia/Shanghai"),
    # Japan
    "tokyo":        (35.6762, 139.6503, "Asia/Tokyo"),
    "osaka":        (34.6937, 135.5023, "Asia/Tokyo"),
    "japan":        (35.6762, 139.6503, "Asia/Tokyo"),
    # South Korea
    "seoul":        (37.5665, 126.9780, "Asia/Seoul"),
    "korea":        (37.5665, 126.9780, "Asia/Seoul"),
    # India
    "mumbai":       (19.0760,  72.8777, "Asia/Kolkata"),
    "delhi":        (28.6139,  77.2090, "Asia/Kolkata"),
    "new delhi":    (28.6139,  77.2090, "Asia/Kolkata"),
    "kolkata":      (22.5726,  88.3639, "Asia/Kolkata"),
    "india":        (20.5937,  78.9629, "Asia/Kolkata"),
    # UK
    "london":       (51.5074,  -0.1278, "Europe/London"),
    # France
    "paris":        (48.8566,   2.3522, "Europe/Paris"),
    # Germany
    "berlin":       (52.5200,  13.4050, "Europe/Berlin"),
    # USA
    "new york":     (40.7128, -74.0060, "America/New_York"),
    "los angeles":  (34.0522, -118.2437, "America/Los_Angeles"),
    "chicago":      (41.8781, -87.6298, "America/Chicago"),
    "houston":      (29.7604, -95.3698, "America/Chicago"),
    # Canada
    "toronto":      (43.6532, -79.3832, "America/Toronto"),
    "vancouver":    (49.2827, -123.1207, "America/Vancouver"),
    # Australia
    "sydney":       (-33.8688, 151.2093, "Australia/Sydney"),
    "melbourne":    (-37.8136, 144.9631, "Australia/Sydney"),
}

_DEFAULT: tuple[float, float, str] = (10.8231, 106.6297, "Asia/Ho_Chi_Minh")


def _normalize(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9 ]+", " ", nfkd.lower()).strip()


@lru_cache(maxsize=256)
def geocode_place(birth_place: str) -> tuple[float, float, str]:
    """Return (lat, lon, tz_str) for a birth place string.

    Priority:
    1. Hardcoded dictionary (instant, no network)
    2. Nominatim + timezonefinder (network, ~1–2 s first call)
    3. Default: Ho Chi Minh City
    """
    normalized = _normalize(birth_place)

    for key, coords in _CITY_DATA.items():
        if key in normalized:
            return coords

    try:
        from geopy.geocoders import Nominatim
        from timezonefinder import TimezoneFinder

        geolocator = Nominatim(user_agent="vedatwin_astrology", timeout=5)
        location = geolocator.geocode(birth_place)
        if location:
            tf = TimezoneFinder()
            tz_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)
            if tz_str:
                return location.latitude, location.longitude, tz_str
    except Exception:
        pass

    return _DEFAULT
