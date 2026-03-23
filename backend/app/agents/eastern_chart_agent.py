from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import EasternChartData
from app.services.eastern_destiny_service import EasternDestinyService


class EasternChartAgent(BaseAgent):
    def __init__(self) -> None:
        self.eastern_service = EasternDestinyService()
        super().__init__(
            name="eastern_chart",
            description="Builds symbolic East Asian destiny pillars and elemental structure.",
        )

    async def execute(self, request: AnalyzeRequest) -> EasternChartData:
        return await self.eastern_service.build_chart(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            birth_place=request.birth_place,
            gender=request.gender,
        )
