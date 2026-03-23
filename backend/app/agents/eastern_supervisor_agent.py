from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import AgentOutput, EasternChartData


ELEMENT_LABELS_VI = {
    "Wood": "Mộc",
    "Fire": "Hỏa",
    "Earth": "Thổ",
    "Metal": "Kim",
    "Water": "Thủy",
}

BRANCH_LABELS_VI = {
    "Rat": "Tý",
    "Ox": "Sửu",
    "Tiger": "Dần",
    "Rabbit": "Mão",
    "Dragon": "Thìn",
    "Snake": "Tỵ",
    "Horse": "Ngọ",
    "Goat": "Mùi",
    "Monkey": "Thân",
    "Rooster": "Dậu",
    "Dog": "Tuất",
    "Pig": "Hợi",
}

STEM_LABELS_VI = {
    "Jia": "Giáp",
    "Yi": "Ất",
    "Bing": "Bính",
    "Ding": "Đinh",
    "Wu": "Mậu",
    "Ji": "Kỷ",
    "Geng": "Canh",
    "Xin": "Tân",
    "Ren": "Nhâm",
    "Gui": "Quý",
}


class EasternSupervisorAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="eastern_supervisor",
            description="Shapes a coherent Eastern Destiny reading and keeps the tone elegant.",
        )

    async def build_summary(self, request: AnalyzeRequest, chart_data: EasternChartData) -> AgentOutput:
        if request.language == "vi":
            dominant = ", ".join(_element_vi(item) for item in chart_data.dominant_elements)
            animal = BRANCH_LABELS_VI.get(chart_data.zodiac_animal, chart_data.zodiac_animal)
            content = (
                f"Chào {request.name}. Bản đọc Eastern Destiny này dùng các trụ biểu tượng, ngũ hành, và nhịp vận khí như một lăng kính chiêm nghiệm. "
                f"Trọng tâm hiện tại nghiêng về {dominant} cùng hình tượng {animal}, gợi ra một giai đoạn đáng chú ý về nhịp sống, lựa chọn, và cách bạn điều hòa nội lực."
            )
        else:
            content = (
                f"Hello {request.name}. This Eastern Destiny reading uses symbolic pillars, five-element balance, and seasonal momentum as a reflective lens. "
                f"The current emphasis leans toward {', '.join(chart_data.dominant_elements)} with the imagery of the {chart_data.zodiac_animal}, suggesting a phase worth noticing for rhythm, choice, and inner balance."
            )
        return AgentOutput(agent="summary", status="completed", content=content)

    async def build_pillar_overview(self, request: AnalyzeRequest, chart_data: EasternChartData) -> AgentOutput:
        if request.language == "vi":
            content = (
                f"Trụ năm hiện được tính là {_pillar_vi(chart_data.year_pillar)}, trụ tháng là {_pillar_vi(chart_data.month_pillar)}, "
                f"trụ ngày là {_pillar_vi(chart_data.day_pillar)}, và trụ giờ là {_pillar_vi(chart_data.hour_pillar)}. "
                f"Cách tính hiện tại là bản xấp xỉ theo mốc Lập Xuân, ranh giới tiết khí phổ biến, và ngày gốc Giáp Tý tham chiếu; "
                f"vì vậy nó phù hợp hơn cho chiêm nghiệm định hướng hơn là khẳng định mệnh lý tuyệt đối. "
                f"Từ bộ trụ này, khí chất tổng thể được gợi ra theo hướng {_core_vi(chart_data.symbolic_core[0])} "
                f"và học cách giữ nhịp thông qua {_core_vi(chart_data.symbolic_core[2])}."
            )
        else:
            content = (
                f"Your current calculation gives the year pillar {chart_data.year_pillar}, month pillar {chart_data.month_pillar}, "
                f"day pillar {chart_data.day_pillar}, and hour pillar {chart_data.hour_pillar}. "
                f"This version is still an approximation using a simple Li Chun cutoff, common seasonal boundaries, and a Jia-Zi reference day, "
                f"so it is better treated as symbolic orientation rather than absolute destiny math. "
                f"From that structure, the overall temperament suggests {chart_data.symbolic_core[0].lower()} while maturing through {chart_data.symbolic_core[2].lower()}."
            )
        return AgentOutput(agent="pillars", status="completed", content=content)

    async def build_question_focus(self, request: AnalyzeRequest) -> AgentOutput:
        if request.language == "vi":
            content = (
                f"Với câu hỏi '{request.question}', hệ thống ưu tiên đọc những mẫu vận động liên quan đến nhịp phát triển, sự sẵn sàng, và cách bạn tích lũy nội lực trước khi mở rộng."
            )
        else:
            content = (
                f"For the question '{request.question}', the system is prioritizing themes around readiness, momentum, and how you consolidate inner strength before expansion."
            )
        return AgentOutput(agent="question_focus", status="completed", content=content)

    async def build_encouragement(self, request: AnalyzeRequest) -> AgentOutput:
        if request.language == "vi":
            content = (
                "Hãy xem Eastern Destiny như một tấm bản đồ biểu tượng chứ không phải khuôn mẫu cố định. "
                "Nhịp sống của bạn vẫn sáng rõ nhất qua lựa chọn, kỷ luật, và cách bạn bồi đắp nội lực mỗi ngày."
            )
        else:
            content = (
                "Treat Eastern Destiny as a symbolic map rather than a fixed script. "
                "Your direction is still shaped most clearly by your choices, discipline, and the way you cultivate inner steadiness."
            )
        return AgentOutput(agent="encouragement", status="completed", content=content)


def _element_vi(value: str) -> str:
    return ELEMENT_LABELS_VI.get(value, value)


def _pillar_vi(value: str) -> str:
    if value == "Time not provided":
        return "chưa có dữ liệu giờ sinh"
    parts = value.split()
    if len(parts) != 3:
        return value
    stem, element, branch = parts
    return f"{STEM_LABELS_VI.get(stem, stem)} {_element_vi(element)} {BRANCH_LABELS_VI.get(branch, branch)}"


def _core_vi(value: str) -> str:
    lowered = value.lower()
    if "primary momentum" in lowered:
        element = value.split()[0]
        return f"{_element_vi(element)} như một động lực chính"
    if "supporting tendency" in lowered:
        element = value.split()[0]
        return f"{_element_vi(element)} như một xu hướng hỗ trợ"
    if "discipline and adaptation" in lowered:
        return "một thế cân bằng giữa kỷ luật và khả năng thích nghi"
    return value
