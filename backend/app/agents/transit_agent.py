from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import AgentOutput, ChartData
from app.prompts.agent_prompts import TRANSIT_PROMPT
from app.prompts.global_prompts import GLOBAL_SYSTEM_PROMPT
from app.services.gemini_service import GeminiService


class TransitAgent(BaseAgent):
    def __init__(self) -> None:
        self.gemini_service = GeminiService()
        super().__init__(
            name="transit",
            description="Explains future timing windows using tool-derived transit data.",
        )

    async def execute(self, request: AnalyzeRequest, chart_data: ChartData) -> AgentOutput:
        period = request.time_focus or ("this year" if request.language == "en" else "giai đoạn sắp tới")
        prompt = f"""
{TRANSIT_PROMPT}

Language: {request.language}
Question: {request.question}
Requested time focus: {period}
Chart anchors: ascendant {chart_data.ascendant}, moon sign {chart_data.moon_sign}, sun sign {chart_data.sun_sign}.
Confidence note: {chart_data.confidence_note}
""".strip()
        text = await self.gemini_service.generate_text(
            system_prompt=GLOBAL_SYSTEM_PROMPT,
            user_prompt=prompt,
        )
        return AgentOutput(agent="transit", status="completed", content=text)
