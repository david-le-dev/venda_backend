from __future__ import annotations

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from app.models.response_models import EasternChartData
from app.utils.timezone import resolve_timezone


class EasternDestinyService:
    """Approximate East Asian destiny calculator for progressive improvement.

    Current accuracy level:
    - Year pillar: computed from an approximate Li Chun date per year.
    - Month pillar: computed from approximate principal solar-term dates.
    - Day pillar: derived from a Jia-Zi base-day reference.
    - Hour pillar: derived from day stem + hour branch if birth time is present.

    Replace this service later with a full Can Chi / Four Pillars engine for
    production-grade precision.
    """

    HEAVENLY_STEMS = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
    EARTHLY_BRANCHES = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
    ELEMENT_BY_STEM = {
        "Jia": "Wood",
        "Yi": "Wood",
        "Bing": "Fire",
        "Ding": "Fire",
        "Wu": "Earth",
        "Ji": "Earth",
        "Geng": "Metal",
        "Xin": "Metal",
        "Ren": "Water",
        "Gui": "Water",
    }
    MONTH_START_STEM_INDEX = {
        "Jia": 2,
        "Ji": 2,
        "Yi": 4,
        "Geng": 4,
        "Bing": 6,
        "Xin": 6,
        "Ding": 8,
        "Ren": 8,
        "Wu": 0,
        "Gui": 0,
    }
    HOUR_START_STEM_INDEX = {
        "Jia": 0,
        "Ji": 0,
        "Yi": 2,
        "Geng": 2,
        "Bing": 4,
        "Xin": 4,
        "Ding": 6,
        "Ren": 6,
        "Wu": 8,
        "Gui": 8,
    }
    ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
    # Nạp Âm element for each pair of years in the 60-year sexagenary cycle.
    # Index = ((year - 4) % 60) // 2
    # Pair 0: Giáp Tý/Ất Sửu, Pair 1: Bính Dần/Đinh Mão, ...
    NAP_AM_ELEMENTS = [
        "Metal", "Fire",  "Wood",  "Earth", "Metal",  # pairs 0-4  (1984-1993)
        "Fire",  "Water", "Earth", "Metal", "Wood",   # pairs 5-9  (1994-2003)
        "Water", "Earth", "Fire",  "Wood",  "Water",  # pairs 10-14 (2004-2013)
        "Metal", "Fire",  "Wood",  "Earth", "Metal",  # pairs 15-19 (2014-2023)
        "Fire",  "Water", "Earth", "Metal", "Wood",   # pairs 20-24 (2024-2033)
        "Water", "Earth", "Fire",  "Wood",  "Water",  # pairs 25-29 (2034-2043)
    ]
    REFERENCE_TIMEZONE = "Asia/Shanghai"
    JIA_ZI_DAY_REFERENCE = date(1984, 2, 2)
    PRINCIPAL_SOLAR_TERMS = (
        ("li_chun", 2, 4.6295, 3.87),
        ("jing_zhe", 3, 6.3826, 5.63),
        ("qing_ming", 4, 5.59, 4.81),
        ("li_xia", 5, 6.318, 5.52),
        ("mang_zhong", 6, 6.5, 5.678),
        ("xiao_shu", 7, 7.928, 7.108),
        ("li_qiu", 8, 8.35, 7.5),
        ("bai_lu", 9, 8.44, 7.646),
        ("han_lu", 10, 9.098, 8.318),
        ("li_dong", 11, 8.218, 7.438),
        ("da_xue", 12, 7.9, 7.18),
        ("xiao_han", 1, 6.11, 5.4055),
    )
    SOLAR_TERM_ADJUSTMENTS = {
        "li_chun": {2021: -1},
        "jing_zhe": {2084: 1},
        "qing_ming": {2008: 1},
        "li_xia": {1911: 1},
        "mang_zhong": {1902: 1},
        "xiao_shu": {2016: 1},
        "li_qiu": {2002: 1},
        "bai_lu": {1927: 1},
        "han_lu": {2089: 1},
        "li_dong": {2089: 1},
        "da_xue": {1954: 1},
        "xiao_han": {1982: 1, 2019: -1},
    }

    async def build_chart(
        self,
        *,
        birth_date: str,
        birth_time: str | None,
        birth_place: str,
        gender: str | None,
    ) -> EasternChartData:
        born_on = date.fromisoformat(birth_date)
        timezone_name, timezone_confidence = resolve_timezone(birth_place)
        born_at = self._birth_datetime(birth_date, birth_time, timezone_name)

        year_stem, year_branch, effective_year = self._year_pillar(born_on, born_at, timezone_name)
        month_stem, month_branch = self._month_pillar(born_on, born_at, year_stem, timezone_name)
        day_stem, day_branch = self._day_pillar(born_on, birth_time)
        hour_stem, hour_branch = self._hour_pillar(birth_time, day_stem)

        nap_am = self._nap_am_element(effective_year)
        dominant_elements = list(dict.fromkeys([nap_am, self.ELEMENT_BY_STEM[day_stem]]))
        if len(dominant_elements) == 1:
            dominant_elements.append(self.ELEMENT_BY_STEM[month_stem])
        weaker_elements = [element for element in self.ELEMENTS if element not in dominant_elements][:2]

        confidence_note = self._build_confidence_note(
            birth_time=birth_time,
            timezone_name=timezone_name,
            timezone_confidence=timezone_confidence,
        )

        return EasternChartData(
            year_pillar=self._format_pillar(year_stem, year_branch),
            month_pillar=self._format_pillar(month_stem, month_branch),
            day_pillar=self._format_pillar(day_stem, day_branch),
            hour_pillar=self._format_pillar(hour_stem, hour_branch) if hour_stem and hour_branch else "Time not provided",
            zodiac_animal=year_branch,
            dominant_elements=dominant_elements,
            weaker_elements=weaker_elements,
            symbolic_core=[
                f"{dominant_elements[0]} as a primary momentum",
                f"{dominant_elements[-1]} as a supporting tendency",
                "A reflective balance between discipline and adaptation",
            ],
            timezone_name=timezone_name,
            timezone_confidence=timezone_confidence,
            confidence_note=confidence_note,
        )

    def _year_pillar(self, born_on: date, born_at: datetime | None, timezone_name: str | None) -> tuple[str, str, int]:
        li_chun = self._principal_term_datetime(born_on.year, "li_chun", timezone_name)
        has_crossed = born_at >= li_chun if born_at else born_on >= li_chun.date()
        effective_year = born_on.year if has_crossed else born_on.year - 1
        stem = self.HEAVENLY_STEMS[(effective_year - 4) % 10]
        branch = self.EARTHLY_BRANCHES[(effective_year - 4) % 12]
        return stem, branch, effective_year

    def _nap_am_element(self, effective_year: int) -> str:
        pair = ((effective_year - 4) % 60) // 2
        return self.NAP_AM_ELEMENTS[pair]

    def _month_pillar(
        self,
        born_on: date,
        born_at: datetime | None,
        year_stem: str,
        timezone_name: str | None,
    ) -> tuple[str, str]:
        month_order = self._solar_month_order(born_on, born_at, timezone_name)
        branch_index = (2 + month_order) % 12  # Tiger month starts the cycle
        stem_index = (self.MONTH_START_STEM_INDEX[year_stem] + month_order) % 10
        return self.HEAVENLY_STEMS[stem_index], self.EARTHLY_BRANCHES[branch_index]

    def _day_pillar(self, born_on: date, birth_time: str | None) -> tuple[str, str]:
        effective_date = born_on
        if birth_time:
            hour, minute = (int(part) for part in birth_time.split(":")[:2])
            if hour == 23 and minute >= 0:
                effective_date = date.fromordinal(born_on.toordinal() + 1)

        delta = self._julian_day_number(effective_date) - self._julian_day_number(self.JIA_ZI_DAY_REFERENCE)
        stem = self.HEAVENLY_STEMS[delta % 10]
        branch = self.EARTHLY_BRANCHES[delta % 12]
        return stem, branch

    def _hour_pillar(self, birth_time: str | None, day_stem: str) -> tuple[str | None, str | None]:
        if not birth_time:
            return None, None
        hour, minute = (int(part) for part in birth_time.split(":")[:2])
        total_minutes = hour * 60 + minute
        branch_index = ((total_minutes + 60) // 120) % 12
        stem_index = (self.HOUR_START_STEM_INDEX[day_stem] + branch_index) % 10
        return self.HEAVENLY_STEMS[stem_index], self.EARTHLY_BRANCHES[branch_index]

    def _solar_month_order(self, born_on: date, born_at: datetime | None, timezone_name: str | None) -> int:
        boundaries = [
            self._principal_term_datetime(born_on.year, "li_chun", timezone_name),
            self._principal_term_datetime(born_on.year, "jing_zhe", timezone_name),
            self._principal_term_datetime(born_on.year, "qing_ming", timezone_name),
            self._principal_term_datetime(born_on.year, "li_xia", timezone_name),
            self._principal_term_datetime(born_on.year, "mang_zhong", timezone_name),
            self._principal_term_datetime(born_on.year, "xiao_shu", timezone_name),
            self._principal_term_datetime(born_on.year, "li_qiu", timezone_name),
            self._principal_term_datetime(born_on.year, "bai_lu", timezone_name),
            self._principal_term_datetime(born_on.year, "han_lu", timezone_name),
            self._principal_term_datetime(born_on.year, "li_dong", timezone_name),
            self._principal_term_datetime(born_on.year, "da_xue", timezone_name),
        ]
        if born_at:
            born_value = born_at
        elif timezone_name:
            born_value = datetime.combine(born_on, time.min, tzinfo=ZoneInfo(timezone_name))
        else:
            born_value = datetime.combine(born_on, time.min)
        if born_value < boundaries[0]:
            xiao_han = self._principal_term_datetime(born_on.year, "xiao_han", timezone_name)
            return 11 if born_value >= xiao_han else 10

        for index, boundary in enumerate(boundaries[1:], start=1):
            if born_value < boundary:
                return index - 1

        next_xiao_han = self._principal_term_datetime(born_on.year + 1, "xiao_han", timezone_name)
        return 10 if born_value < next_xiao_han else 11

    def _format_pillar(self, stem: str, branch: str) -> str:
        return f"{stem} {self.ELEMENT_BY_STEM[stem]} {branch}"

    def _julian_day_number(self, value: date) -> int:
        year = value.year
        month = value.month
        day = value.day

        a = (14 - month) // 12
        y = year + 4800 - a
        m = month + 12 * a - 3

        return day + ((153 * m + 2) // 5) + 365 * y + (y // 4) - (y // 100) + (y // 400) - 32045

    def _principal_term_date(self, year: int, term_name: str, timezone_name: str | None = None) -> date:
        return self._principal_term_datetime(year, term_name, timezone_name).date()

    def _principal_term_datetime(self, year: int, term_name: str, timezone_name: str | None = None) -> datetime:
        month, coefficient = self._principal_term_meta(year, term_name)
        y = year % 100
        raw_day = y * 0.2422 + coefficient - int((y - 1) / 4)
        raw_day += self.SOLAR_TERM_ADJUSTMENTS.get(term_name, {}).get(year, 0)

        day = int(raw_day)
        seconds = round((raw_day - day) * 86400)
        if seconds >= 86400:
            seconds -= 86400
            day += 1

        reference_dt = datetime(year, month, day, tzinfo=ZoneInfo(self.REFERENCE_TIMEZONE)) + timedelta(seconds=seconds)
        if timezone_name:
            return reference_dt.astimezone(ZoneInfo(timezone_name))
        return reference_dt.replace(tzinfo=None)

    def _principal_term_meta(self, year: int, term_name: str) -> tuple[int, float]:
        for name, month, twentieth_c, twenty_first_c in self.PRINCIPAL_SOLAR_TERMS:
            if name == term_name:
                coefficient = twentieth_c if year <= 2000 else twenty_first_c
                return month, coefficient
        raise ValueError(f"Unsupported solar term: {term_name}")

    def _birth_datetime(self, birth_date: str, birth_time: str | None, timezone_name: str | None) -> datetime | None:
        if not birth_time:
            return None
        hour, minute = (int(part) for part in birth_time.split(":")[:2])
        birth_dt = datetime.fromisoformat(f"{birth_date}T{hour:02d}:{minute:02d}:00")
        if timezone_name:
            return birth_dt.replace(tzinfo=ZoneInfo(timezone_name))
        return birth_dt

    def _build_confidence_note(
        self,
        *,
        birth_time: str | None,
        timezone_name: str | None,
        timezone_confidence: str,
    ) -> str:
        timezone_note = (
            f"Birthplace timezone was mapped to {timezone_name} with {timezone_confidence} confidence. "
            if timezone_name
            else "Birthplace timezone could not be resolved, so seasonal boundaries were compared using civil-date fallback. "
        )
        time_note = (
            "Hour pillar depends on the provided birth time."
            if birth_time
            else "Hour pillar is omitted because birth time was not provided."
        )
        return (
            "Year pillar uses an approximate Li Chun datetime. "
            "Month pillar uses approximate principal solar-term datetimes. "
            "Day pillar is derived through a Julian-day offset from a Jia-Zi reference day, with a late-night rollover. "
            f"{timezone_note}{time_note}"
        )
