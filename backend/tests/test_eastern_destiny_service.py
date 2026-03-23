import asyncio
import unittest

from app.services.eastern_destiny_service import EasternDestinyService
from app.utils.timezone import resolve_timezone


class EasternDestinyServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = EasternDestinyService()

    def build_chart(self, birth_date: str, birth_time: str):
        return asyncio.run(
            self.service.build_chart(
                birth_date=birth_date,
                birth_time=birth_time,
                birth_place="Ho Chi Minh City, Vietnam",
                gender="female",
            )
        )

    def test_year_pillar_changes_across_approx_li_chun_2000(self) -> None:
        before = self.build_chart("2000-02-04", "10:30")
        after = self.build_chart("2000-02-04", "16:30")

        self.assertEqual(before.year_pillar, "Ji Earth Rabbit")
        self.assertEqual(before.month_pillar, "Ding Fire Ox")
        self.assertEqual(after.year_pillar, "Geng Metal Dragon")
        self.assertEqual(after.month_pillar, "Wu Earth Tiger")

    def test_month_pillar_changes_across_approx_jing_zhe_2000(self) -> None:
        before = self.build_chart("2000-03-06", "08:00")
        after = self.build_chart("2000-03-06", "10:00")

        self.assertEqual(before.month_pillar, "Wu Earth Tiger")
        self.assertEqual(after.month_pillar, "Ji Earth Rabbit")

    def test_day_pillar_rolls_over_at_zi_hour(self) -> None:
        before = self.build_chart("2000-03-10", "22:59")
        after = self.build_chart("2000-03-10", "23:00")

        self.assertNotEqual(before.day_pillar, after.day_pillar)

    def test_timezone_resolution_for_vietnam(self) -> None:
        timezone_name, confidence = resolve_timezone("Ho Chi Minh City, Vietnam")

        self.assertEqual(timezone_name, "Asia/Ho_Chi_Minh")
        self.assertEqual(confidence, "high")

    def test_timezone_resolution_handles_vietnamese_diacritics(self) -> None:
        timezone_name, confidence = resolve_timezone("Thành phố Hồ Chí Minh, Việt Nam")

        self.assertEqual(timezone_name, "Asia/Ho_Chi_Minh")
        self.assertEqual(confidence, "high")

    def test_timezone_resolution_handles_country_aliases(self) -> None:
        timezone_name, confidence = resolve_timezone("New York, USA")

        self.assertEqual(timezone_name, "America/New_York")
        self.assertEqual(confidence, "high")

    def test_chart_carries_timezone_metadata(self) -> None:
        chart = asyncio.run(
            self.service.build_chart(
                birth_date="2000-03-10",
                birth_time="10:00",
                birth_place="Tokyo, Japan",
                gender="female",
            )
        )

        self.assertEqual(chart.timezone_name, "Asia/Tokyo")
        self.assertEqual(chart.timezone_confidence, "high")
        self.assertIn("Birthplace timezone was mapped", chart.confidence_note)


if __name__ == "__main__":
    unittest.main()
