from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import AgentOutput, EasternChartData
from app.prompts.global_prompts import GLOBAL_SYSTEM_PROMPT
from app.services.gemini_service import GeminiService


EASTERN_ADVISOR_PROMPT = """
You are the Eastern Destiny Advisor Agent.
Convert symbolic insights into practical, calming, uplifting advice.
Emphasize choice, discipline, emotional steadiness, and reflective growth.
Avoid dependency language.
""".strip()


class EasternAdvisorAgent(BaseAgent):
    def __init__(self) -> None:
        self.gemini_service = GeminiService()
        super().__init__(
            name="eastern_advisor",
            description="Turns Eastern Destiny themes into practical guidance.",
        )

    async def execute(
        self,
        request: AnalyzeRequest,
        chart_data: EasternChartData,
        tendencies: AgentOutput,
        period: AgentOutput,
    ) -> AgentOutput:
        prompt = f"""
{EASTERN_ADVISOR_PROMPT}

Language: {request.language}
Question: {request.question}
Dominant elements: {", ".join(chart_data.dominant_elements)}
Weaker elements: {", ".join(chart_data.weaker_elements)}
Interpretation draft: {tendencies.content}
Period draft: {period.content}
""".strip()
        text = await self.gemini_service.generate_text(system_prompt=GLOBAL_SYSTEM_PROMPT, user_prompt=prompt)
        return AgentOutput(agent="advisor", status="completed", content=text)
