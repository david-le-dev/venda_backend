from __future__ import annotations

import re
import unicodedata


TIMEZONE_KEYWORDS: list[tuple[tuple[str, ...], str, str]] = [
    (("ho chi minh", "hcmc", "sai gon", "saigon"), "Asia/Ho_Chi_Minh", "high"),
    (("ha noi", "hanoi"), "Asia/Ho_Chi_Minh", "high"),
    (("da nang", "danang"), "Asia/Ho_Chi_Minh", "high"),
    (("viet nam", "vietnam", "vn"), "Asia/Ho_Chi_Minh", "high"),
    (("bangkok", "thailand", "thai lan"), "Asia/Bangkok", "high"),
    (("singapore",), "Asia/Singapore", "high"),
    (("kuala lumpur", "malaysia"), "Asia/Kuala_Lumpur", "high"),
    (("jakarta",), "Asia/Jakarta", "high"),
    (("indonesia",), "Asia/Jakarta", "low"),
    (("manila", "philippines"), "Asia/Manila", "high"),
    (("hong kong",), "Asia/Hong_Kong", "high"),
    (("taipei", "taiwan"), "Asia/Taipei", "high"),
    (("shanghai", "beijing", "guangzhou", "shenzhen"), "Asia/Shanghai", "high"),
    (("china", "trung quoc"), "Asia/Shanghai", "medium"),
    (("tokyo", "japan", "nhat ban"), "Asia/Tokyo", "high"),
    (("seoul",), "Asia/Seoul", "high"),
    (("south korea", "korea", "han quoc"), "Asia/Seoul", "medium"),
    (("delhi", "mumbai", "kolkata"), "Asia/Kolkata", "high"),
    (("india", "an do"), "Asia/Kolkata", "medium"),
    (("london",), "Europe/London", "high"),
    (("united kingdom", "england", "uk", "anh"), "Europe/London", "medium"),
    (("paris", "france", "phap"), "Europe/Paris", "high"),
    (("berlin", "germany", "duc"), "Europe/Berlin", "high"),
    (("sydney", "melbourne"), "Australia/Sydney", "high"),
    (("australia", "uc"), "Australia/Sydney", "low"),
    (("new york",), "America/New_York", "high"),
    (("los angeles", "san francisco"), "America/Los_Angeles", "high"),
    (("chicago", "houston"), "America/Chicago", "high"),
    (("toronto",), "America/Toronto", "high"),
    (("vancouver",), "America/Vancouver", "high"),
    (("united states", "usa", "u s a", "my"), "America/New_York", "low"),
    (("canada",), "America/Toronto", "low"),
]


def resolve_timezone(birth_place: str) -> tuple[str | None, str]:
    normalized = _normalize_place(birth_place)
    for aliases, timezone_name, confidence in TIMEZONE_KEYWORDS:
        if any(_contains_alias(normalized, alias) for alias in aliases):
            return timezone_name, confidence
    return None, "low"


def _normalize_place(value: str) -> str:
    lowered = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").lower()
    cleaned = re.sub(r"[^a-z0-9]+", " ", lowered)
    return " ".join(cleaned.split())


def _contains_alias(normalized_place: str, alias: str) -> bool:
    pattern = rf"(^|\s){re.escape(alias)}($|\s)"
    return re.search(pattern, normalized_place) is not None
