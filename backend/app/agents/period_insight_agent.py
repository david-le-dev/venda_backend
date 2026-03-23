from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import AgentOutput, EasternChartData
from app.prompts.global_prompts import GLOBAL_SYSTEM_PROMPT
from app.services.gemini_service import GeminiService


EASTERN_PERIOD_PROMPT = """
You are the Period Insight Agent for Eastern Destiny.
Interpret near-term cycles with East Asian symbolic language around timing, readiness, discipline, and momentum.
Avoid certainty. Focus on patterns, pacing, opportunities, and emotional maturity.
""".strip()


class PeriodInsightAgent(BaseAgent):
    def __init__(self) -> None:
        self.gemini_service = GeminiService()
        super().__init__(
            name="period_insight",
            description="Explains symbolic upcoming cycles for Eastern Destiny mode.",
        )

    async def execute(self, request: AnalyzeRequest, chart_data: EasternChartData) -> AgentOutput:
        period = request.time_focus or ("this year" if request.language == "en" else "giai đoạn sắp tới")
        prompt = f"""
{EASTERN_PERIOD_PROMPT}

Language: {request.language}
Question: {request.question}
Requested time focus: {period}
Resolved timezone: {chart_data.timezone_name or 'unresolved'}
Timezone confidence: {chart_data.timezone_confidence or 'low'}
Year pillar: {chart_data.year_pillar}
Dominant elements: {", ".join(chart_data.dominant_elements)}
Weaker elements: {", ".join(chart_data.weaker_elements)}
Confidence note: {chart_data.confidence_note}
If timezone confidence is not high, avoid exact-sounding statements tied to boundary-sensitive pillar changes.
Do not present month/day/hour pillars as exact calculations in this version.
""".strip()
        text = await self.gemini_service.generate_text(system_prompt=GLOBAL_SYSTEM_PROMPT, user_prompt=prompt)
        return AgentOutput(agent="transit", status="completed", content=text)
