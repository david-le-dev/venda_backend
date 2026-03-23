from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import AgentOutput
from app.prompts.agent_prompts import FACE_PROMPT
from app.prompts.global_prompts import GLOBAL_SYSTEM_PROMPT
from app.services.gemini_service import GeminiService


class FaceAnalysisAgent(BaseAgent):
    def __init__(self) -> None:
        self.gemini_service = GeminiService()
        super().__init__(
            name="face_analysis",
            description="Provides gentle, non-sensitive facial reflection from optional images.",
        )

    async def execute(self, request: AnalyzeRequest) -> AgentOutput:
        assert request.face_image is not None
        prompt = (
            f"{FACE_PROMPT}\n\n"
            f"Language: {request.language}\n"
            f"Question context: {request.question}\n"
            "Describe visible expression, presentation style, and overall emotional tone gently."
        )
        text = await self.gemini_service.analyze_image(
            system_prompt=GLOBAL_SYSTEM_PROMPT,
            user_prompt=prompt,
            image_base64=request.face_image.data_base64,
            mime_type=request.face_image.mime_type,
        )
        return AgentOutput(agent="face", status="completed", content=text)
