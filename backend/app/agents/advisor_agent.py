from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import AgentOutput, ChartData
from app.prompts.agent_prompts import ADVISOR_PROMPT
from app.prompts.global_prompts import GLOBAL_SYSTEM_PROMPT
from app.services.gemini_service import GeminiService


class AdvisorAgent(BaseAgent):
    def __init__(self) -> None:
        self.gemini_service = GeminiService()
        super().__init__(
            name="advisor",
            description="Converts themes into practical, empowering guidance.",
        )

    async def execute(
        self,
        request: AnalyzeRequest,
        chart_data: ChartData,
        interpretation: AgentOutput,
        transit: AgentOutput,
    ) -> AgentOutput:
        prompt = f"""
{ADVISOR_PROMPT}

Language: {request.language}
Question: {request.question}
Chart anchors: ascendant {chart_data.ascendant}, moon sign {chart_data.moon_sign}.
Interpretation draft: {interpretation.content}
Transit draft: {transit.content}
""".strip()
        text = await self.gemini_service.generate_text(
            system_prompt=GLOBAL_SYSTEM_PROMPT,
            user_prompt=prompt,
        )
        return AgentOutput(agent="advisor", status="completed", content=text)
