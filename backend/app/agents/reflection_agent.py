from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import AgentOutput, EasternChartData


class ReflectionAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="reflection_questions",
            description="Produces compact reflection questions for Eastern Destiny mode.",
        )

    async def execute(self, request: AnalyzeRequest, chart_data: EasternChartData) -> AgentOutput:
        if request.language == "vi":
            content = (
                "1. Trong giai đoạn này, tôi cần nuôi dưỡng phẩm chất nào để cân bằng nội lực?\n"
                "2. Tôi đang phản ứng theo thói quen cũ, hay đang chủ động chọn một nhịp sống trưởng thành hơn?\n"
                "3. Nếu muốn đi xa hơn trong 12 tháng tới, tôi nên kiên định với điều gì?"
            )
        else:
            content = (
                "1. What quality would help me balance my inner momentum in this phase?\n"
                "2. Am I reacting from an old pattern, or choosing a more mature rhythm?\n"
                "3. If I want steadier progress over the next 12 months, what should I stay committed to?"
            )
        return AgentOutput(agent="reflection_questions", status="completed", content=content)
