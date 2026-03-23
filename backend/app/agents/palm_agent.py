from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import AgentOutput
from app.prompts.agent_prompts import PALM_PROMPT
from app.prompts.global_prompts import GLOBAL_SYSTEM_PROMPT
from app.services.gemini_service import GeminiService


class PalmAnalysisAgent(BaseAgent):
    def __init__(self) -> None:
        self.gemini_service = GeminiService()
        super().__init__(
            name="palm_analysis",
            description="Generates symbolic palm-reading reflections from optional hand images.",
        )

    async def execute(self, request: AnalyzeRequest) -> AgentOutput:
        assert request.palm_image is not None
        prompt = (
            f"{PALM_PROMPT}\n\n"
            f"Language: {request.language}\n"
            f"Question context: {request.question}\n"
            "Comment on visible line clarity and symbolic traditional themes only."
        )
        text = await self.gemini_service.analyze_image(
            system_prompt=GLOBAL_SYSTEM_PROMPT,
            user_prompt=prompt,
            image_base64=request.palm_image.data_base64,
            mime_type=request.palm_image.mime_type,
        )
        return AgentOutput(agent="palm", status="completed", content=text)
