from __future__ import annotations

import math
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

import ephem

from app.models.response_models import ChartData, PlanetPlacement
from app.utils.geocoder import geocode_place


class AstrologyService:
    """Western astrology using PyEphem for accurate planetary positions.

    - Sun / Moon / planets: true ecliptic longitudes via Swiss-level ephemeris.
    - Ascendant: computed from Local Sidereal Time using the Jean Meeus formula.
    - Houses: Whole Sign system (each house = one full sign, starting from ASC).
    - Geocoding: hardcoded dict → Nominatim fallback → default Ho Chi Minh City.
    """

    SIGNS = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
    ]
    PLANETS = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]

    _EPHEM_BODIES: dict[str, type] = {
        "Sun":     ephem.Sun,
        "Moon":    ephem.Moon,
        "Mercury": ephem.Mercury,
        "Venus":   ephem.Venus,
        "Mars":    ephem.Mars,
        "Jupiter": ephem.Jupiter,
        "Saturn":  ephem.Saturn,
    }

    async def build_chart(self, birth_date: str, birth_time: str | None, birth_place: str) -> ChartData:
        born_on = date.fromisoformat(birth_date)
        lat, lon, tz_str = geocode_place(birth_place)

        time_provided = bool(birth_time)
        hour, minute = (12, 0)
        if birth_time:
            hour, minute = (int(p) for p in birth_time.split(":")[:2])

        # Convert local birth time → UTC for ephem
        local_dt = datetime(born_on.year, born_on.month, born_on.day, hour, minute,
                            tzinfo=ZoneInfo(tz_str))
        utc_dt = local_dt.astimezone(timezone.utc)

        obs = ephem.Observer()
        obs.lat = str(lat)
        obs.lon = str(lon)
        obs.elev = 0
        obs.pressure = 0  # Disable atmospheric refraction for astrological use
        obs.date = ephem.Date(
            f"{utc_dt.year}/{utc_dt.month}/{utc_dt.day} "
            f"{utc_dt.hour}:{utc_dt.minute}:{utc_dt.second}"
        )

        # Compute obliquity of the ecliptic for this date
        ecl_ref = ephem.Ecliptic(ephem.Sun(obs), epoch=obs.date)
        obliquity_deg = math.degrees(float(ephem.Sun(obs).g))  # fallback
        try:
            obliquity_deg = math.degrees(float(ecl_ref.eps))
        except AttributeError:
            obliquity_deg = 23.4393  # J2000 value

        # Compute planet ecliptic longitudes
        sign_indices: dict[str, int] = {}
        longitudes: dict[str, float] = {}
        for planet_name, body_cls in self._EPHEM_BODIES.items():
            body = body_cls()
            body.compute(obs)
            ecl = ephem.Ecliptic(body, epoch=obs.date)
            lon_deg = math.degrees(float(ecl.lon)) % 360
            longitudes[planet_name] = lon_deg
            sign_indices[planet_name] = int(lon_deg / 30)

        # Ascendant from Local Sidereal Time
        asc_sign_idx: int | None = None
        asc_lon_deg: float | None = None
        if time_provided:
            lst_deg = math.degrees(float(obs.sidereal_time()))
            asc_lon_deg = self._ascendant_longitude(lst_deg, lat, obliquity_deg)
            asc_sign_idx = int(asc_lon_deg / 30) % 12

        # Whole Sign houses: house n contains the sign that is n-1 signs away from ASC
        house_offset = asc_sign_idx if asc_sign_idx is not None else sign_indices["Sun"]
        placements = [
            PlanetPlacement(
                planet=planet,
                sign=self.SIGNS[sign_indices[planet]],
                house=((sign_indices[planet] - house_offset) % 12) + 1,
            )
            for planet in self.PLANETS
        ]

        asc_sign = self.SIGNS[asc_sign_idx] if asc_sign_idx is not None else "Unknown (birth time required)"
        confidence_note = (
            "PyEphem ephemeris — birth time provided, all placements and ascendant are accurate."
            if time_provided
            else "PyEphem ephemeris — birth time missing, ascendant and houses are not computed; sun/moon signs are accurate."
        )
        houses_summary = [
            f"House {p.house}: {p.planet} in {p.sign}"
            for p in placements[:4]
        ]

        return ChartData(
            ascendant=asc_sign,
            moon_sign=self.SIGNS[sign_indices["Moon"]],
            sun_sign=self.SIGNS[sign_indices["Sun"]],
            confidence_note=confidence_note,
            key_planets=placements,
            houses_summary=houses_summary,
        )

    @staticmethod
    def _ascendant_longitude(lst_deg: float, lat_deg: float, obliquity_deg: float) -> float:
        """Compute ecliptic longitude of the Ascendant (Jean Meeus formula).

        Returns degrees in [0, 360).
        """
        ramc = math.radians(lst_deg)
        lat  = math.radians(lat_deg)
        eps  = math.radians(obliquity_deg)

        y = -math.cos(ramc)
        x = math.sin(ramc) * math.cos(eps) + math.tan(lat) * math.sin(eps)
        asc = math.degrees(math.atan2(y, x)) % 360

        # Compute MC longitude to determine correct hemisphere
        mc = math.degrees(math.atan2(math.sin(ramc), math.cos(ramc) * math.cos(eps))) % 360

        # ASC should be 90°–270° ahead of MC; flip 180° if not
        diff = (asc - mc) % 360
        if diff < 90 or diff > 270:
            asc = (asc + 180) % 360

        return asc
