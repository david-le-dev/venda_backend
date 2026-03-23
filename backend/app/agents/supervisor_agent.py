from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import AgentOutput


class SupervisorAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="supervisor",
            description="Plans execution order, merges outputs, and ensures language consistency.",
        )

    async def execute(self, request: AnalyzeRequest, warnings: list[str]) -> AgentOutput:
        if request.language == "vi":
            greeting = f"Chào {request.name}. " if request.name else ""
            time_note = (
                "Thời gian sinh chưa có, vì vậy một số chi tiết sẽ được diễn giải mềm hơn."
                if warnings
                else "Thông tin sinh có vẻ đủ để tạo một bản đọc mang tính chiêm nghiệm."
            )
            content = (
                f"{greeting}Bản đọc này tập trung vào câu hỏi '{request.question}'. "
                f"Chủ đề chính sẽ xoay quanh tự nhận thức, xu hướng tính cách, và các nhắc nhở thực tế. "
                f"{time_note}"
            )
        else:
            greeting = f"Hello {request.name}. " if request.name else ""
            time_note = (
                "Birth time is missing, so some chart details should be read with lower confidence."
                if warnings
                else "Your birth details are sufficient for a reflective symbolic reading."
            )
            content = (
                f"{greeting}This reading centers on your question '{request.question}'. "
                f"It will focus on symbolic personality patterns, timing themes, and practical next steps. "
                f"{time_note}"
            )
        return AgentOutput(agent="summary", status="completed", content=content)

    async def build_question_focus(self, request: AnalyzeRequest) -> AgentOutput:
        if request.language == "vi":
            focus = request.time_focus or "giai đoạn gần đây"
            content = (
                f"Trong câu hỏi này, hệ thống ưu tiên đọc các mẫu hình liên quan đến '{focus}'. "
                "Bản đọc sẽ nhấn mạnh các cơ hội để cân bằng nội lực, cách ra quyết định, "
                "và những chủ đề đang được kích hoạt để bạn tự chiêm nghiệm."
            )
        else:
            focus = request.time_focus or "the near-term period"
            content = (
                f"For this question, the system is prioritizing symbolic themes connected to '{focus}'. "
                "The reading will emphasize decision-making energy, personal development patterns, "
                "and the kinds of opportunities or tensions that may be worth noticing."
            )
        return AgentOutput(agent="question_focus", status="completed", content=content)

    async def build_encouragement(self, request: AnalyzeRequest) -> AgentOutput:
        if request.language == "vi":
            content = (
                "Hãy xem bản đọc này như một tấm gương để tự chiêm nghiệm. "
                "Lựa chọn, kỷ luật, và cách bạn phản hồi với cuộc sống vẫn là yếu tố quan trọng nhất."
            )
        else:
            content = (
                "Treat this reading as a reflective mirror rather than a fixed script. "
                "Your choices, consistency, and self-awareness remain the strongest influences."
            )
        return AgentOutput(agent="encouragement", status="completed", content=content)
