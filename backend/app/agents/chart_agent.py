from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import ChartData
from app.services.astrology_service import AstrologyService


class BirthChartAgent(BaseAgent):
    def __init__(self) -> None:
        self.astrology_service = AstrologyService()
        super().__init__(
            name="birth_chart",
            description="Produces structured Vedic chart data from validated birth details.",
        )

    async def execute(self, request: AnalyzeRequest) -> ChartData:
        return await self.astrology_service.build_chart(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            birth_place=request.birth_place,
        )
