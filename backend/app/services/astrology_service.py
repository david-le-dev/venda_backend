from __future__ import annotations

import hashlib

from app.models.response_models import ChartData, PlanetPlacement


class AstrologyService:
    """Mock astrology adapter that can later be replaced by Kerykeion or VedAstro."""

    SIGNS = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]
    PLANETS = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]

    async def build_chart(self, birth_date: str, birth_time: str | None, birth_place: str) -> ChartData:
        seed = self._seed_value(f"{birth_date}|{birth_time or 'unknown'}|{birth_place}")
        ascendant = self.SIGNS[seed % len(self.SIGNS)]
        moon_sign = self.SIGNS[(seed + 3) % len(self.SIGNS)]
        sun_sign = self.SIGNS[(seed + 6) % len(self.SIGNS)]
        placements = [
            PlanetPlacement(
                planet=planet,
                sign=self.SIGNS[(seed + idx * 2) % len(self.SIGNS)],
                house=((seed + idx) % 12) + 1,
            )
            for idx, planet in enumerate(self.PLANETS)
        ]
        confidence_note = (
            "Birth time appears specific, so house-level interpretation can be a bit sharper."
            if birth_time
            else "Birth time is missing, so house and ascendant detail should be treated more softly."
        )
        houses_summary = [
            f"House {placement.house}: {placement.planet} in {placement.sign}"
            for placement in placements[:4]
        ]
        return ChartData(
            ascendant=ascendant,
            moon_sign=moon_sign,
            sun_sign=sun_sign,
            confidence_note=confidence_note,
            key_planets=placements,
            houses_summary=houses_summary,
        )

    def _seed_value(self, raw: str) -> int:
        return int(hashlib.md5(raw.encode("utf-8")).hexdigest(), 16)
