from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import AgentOutput, EasternChartData
from app.prompts.global_prompts import GLOBAL_SYSTEM_PROMPT
from app.services.gemini_service import GeminiService


EASTERN_INTERPRETATION_PROMPT = """
You are the Eastern Interpretation Agent.
Use East Asian symbolic destiny framing such as pillars, elemental balance, rhythm, and temperament.
Write in a modern, elegant, non-deterministic tone.
Focus on personality tendencies, strengths, growth edges, relationship style, and work style.
""".strip()


class EasternInterpretationAgent(BaseAgent):
    def __init__(self) -> None:
        self.gemini_service = GeminiService()
        super().__init__(
            name="eastern_interpretation",
            description="Translates symbolic Eastern destiny data into personality and life tendencies.",
        )

    async def execute(self, request: AnalyzeRequest, chart_data: EasternChartData) -> AgentOutput:
        prompt = f"""
{EASTERN_INTERPRETATION_PROMPT}

Language: {request.language}
Name: {request.name}
Gender: {request.gender or 'not provided'}
Question: {request.question}
Birth place: {request.birth_place}
Resolved timezone: {chart_data.timezone_name or 'unresolved'}
Timezone confidence: {chart_data.timezone_confidence or 'low'}
Year pillar: {chart_data.year_pillar}
Zodiac animal: {chart_data.zodiac_animal}
Dominant elements: {", ".join(chart_data.dominant_elements)}
Weaker elements: {", ".join(chart_data.weaker_elements)}
Symbolic core: {", ".join(chart_data.symbolic_core)}
Confidence note: {chart_data.confidence_note}
If timezone confidence is not high, be extra careful with exact-sounding claims around thresholds or pillar precision.
Do not present month/day/hour pillars as exact calculations in this version.
""".strip()
        text = await self.gemini_service.generate_text(system_prompt=GLOBAL_SYSTEM_PROMPT, user_prompt=prompt)
        return AgentOutput(agent="tendencies", status="completed", content=text)
