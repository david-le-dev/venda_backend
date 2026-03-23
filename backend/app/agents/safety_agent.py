from app.agents.base import BaseAgent
from app.models.request_models import ReadingMode
from app.models.response_models import AgentOutput
from app.services.safety_service import SafetyService


class SafetyAgent(BaseAgent):
    def __init__(self) -> None:
        self.safety_service = SafetyService()
        super().__init__(
            name="safety",
            description="Checks disclaimer, tone, banned claims, and final language integrity.",
        )

    async def execute(
        self,
        reading_mode: ReadingMode,
        language: str,
        sections: list[AgentOutput],
    ) -> tuple[list[AgentOutput], list[str]]:
        return self.safety_service.review_sections(reading_mode=reading_mode, language=language, sections=sections)
