from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import AgentOutput, EasternChartData


class ElementBalanceAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="element_balance",
            description="Explains the symbolic balance of the five elements.",
        )

    async def execute(self, request: AnalyzeRequest, chart_data: EasternChartData) -> AgentOutput:
        if request.language == "vi":
            dominant = ", ".join(ELEMENT_LABELS_VI.get(item, item) for item in chart_data.dominant_elements)
            weaker = ", ".join(ELEMENT_LABELS_VI.get(item, item) for item in chart_data.weaker_elements)
            content = (
                f"Ngũ hành nổi bật của bạn hiện nghiêng về {dominant}. "
                f"Điều này thường gợi ý cách vận hành thiên về {_core_vi(chart_data.symbolic_core[0])} và {_core_vi(chart_data.symbolic_core[1])}. "
                f"Những hành nên được nuôi dưỡng thêm là {weaker}, như một lời nhắc về cân bằng, độ mềm, và khả năng điều tiết nhịp sống."
            )
        else:
            content = (
                f"Your symbolic five-element balance leans toward {', '.join(chart_data.dominant_elements)}. "
                f"This can suggest a style shaped by {chart_data.symbolic_core[0].lower()} and {chart_data.symbolic_core[1].lower()}. "
                f"The elements that may benefit from more conscious support are {', '.join(chart_data.weaker_elements)}, pointing toward balance, softness, and better pacing."
            )
        return AgentOutput(agent="elements", status="completed", content=content)


ELEMENT_LABELS_VI = {
    "Wood": "Mộc",
    "Fire": "Hỏa",
    "Earth": "Thổ",
    "Metal": "Kim",
    "Water": "Thủy",
}


def _core_vi(value: str) -> str:
    lowered = value.lower()
    if "primary momentum" in lowered:
        element = value.split()[0]
        return f"{ELEMENT_LABELS_VI.get(element, element)} như một động lực chính"
    if "supporting tendency" in lowered:
        element = value.split()[0]
        return f"{ELEMENT_LABELS_VI.get(element, element)} như một xu hướng hỗ trợ"
    if "discipline and adaptation" in lowered:
        return "một thế cân bằng giữa kỷ luật và khả năng thích nghi"
    return value
