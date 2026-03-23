from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import AgentOutput, ChartData, RetrievalChunk
from app.prompts.agent_prompts import INTERPRETATION_PROMPT
from app.prompts.global_prompts import GLOBAL_SYSTEM_PROMPT
from app.services.gemini_service import GeminiService


class InterpretationAgent(BaseAgent):
    def __init__(self) -> None:
        self.gemini_service = GeminiService()
        super().__init__(
            name="interpretation",
            description="Turns chart structure and retrieved context into reflective insights.",
        )

    async def execute(
        self,
        request: AnalyzeRequest,
        chart_data: ChartData,
        retrieval_chunks: list[RetrievalChunk],
    ) -> AgentOutput:
        context = "\n".join(f"- {chunk.content}" for chunk in retrieval_chunks) or "- No external context."
        prompt = f"""
{INTERPRETATION_PROMPT}

Language: {request.language}
Question: {request.question}
Birth place: {request.birth_place}
Ascendant: {chart_data.ascendant}
Moon sign: {chart_data.moon_sign}
Sun sign: {chart_data.sun_sign}
Confidence note: {chart_data.confidence_note}
Key planets:
{", ".join(f"{item.planet} in {item.sign} house {item.house}" for item in chart_data.key_planets[:5])}

Retrieved context:
{context}
""".strip()
        text = await self.gemini_service.generate_text(
            system_prompt=GLOBAL_SYSTEM_PROMPT,
            user_prompt=prompt,
        )
        return AgentOutput(agent="interpretation", status="completed", content=text)
