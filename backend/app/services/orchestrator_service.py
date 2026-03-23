from __future__ import annotations

from collections.abc import AsyncGenerator

from app.agents.advisor_agent import AdvisorAgent
from app.agents.chart_agent import BirthChartAgent
from app.agents.eastern_advisor_agent import EasternAdvisorAgent
from app.agents.eastern_chart_agent import EasternChartAgent
from app.agents.eastern_interpretation_agent import EasternInterpretationAgent
from app.agents.eastern_supervisor_agent import EasternSupervisorAgent
from app.agents.element_balance_agent import ElementBalanceAgent
from app.agents.face_agent import FaceAnalysisAgent
from app.agents.interpretation_agent import InterpretationAgent
from app.agents.palm_agent import PalmAnalysisAgent
from app.agents.period_insight_agent import PeriodInsightAgent
from app.agents.reflection_agent import ReflectionAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.agents.safety_agent import SafetyAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.transit_agent import TransitAgent
from app.config import get_settings
from app.models.agent_models import AgentStatus
from app.models.request_models import AnalyzeRequest
from app.models.response_models import FinalReportResponse, ReportMetadata
from app.prompts.global_prompts import DISCLAIMER_TEXT
from app.services.stream_service import StreamService
from app.utils.formatters import build_final_report
from app.utils.validators import validate_chat_request


class OrchestratorService:
    """Coordinates VedaTwin and Eastern Destiny reading pipelines."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.stream_service = StreamService()
        self.supervisor = SupervisorAgent()
        self.chart_agent = BirthChartAgent()
        self.retrieval_agent = RetrievalAgent()
        self.interpretation_agent = InterpretationAgent()
        self.transit_agent = TransitAgent()
        self.advisor_agent = AdvisorAgent()

        self.eastern_supervisor = EasternSupervisorAgent()
        self.eastern_chart_agent = EasternChartAgent()
        self.element_balance_agent = ElementBalanceAgent()
        self.eastern_interpretation_agent = EasternInterpretationAgent()
        self.period_insight_agent = PeriodInsightAgent()
        self.eastern_advisor_agent = EasternAdvisorAgent()
        self.reflection_agent = ReflectionAgent()

        self.face_agent = FaceAnalysisAgent()
        self.palm_agent = PalmAnalysisAgent()
        self.safety_agent = SafetyAgent()

    async def generate_report(self, request: AnalyzeRequest) -> FinalReportResponse:
        return await self._run_pipeline(request)

    async def stream_report(self, request: AnalyzeRequest) -> AsyncGenerator[dict[str, str], None]:
        warnings = validate_chat_request(request)
        validator_message = (
            "Validating Eastern Destiny input..."
            if request.reading_mode == "eastern_destiny" and request.language == "en"
            else "Đang kiểm tra đầu vào Eastern Destiny..."
            if request.reading_mode == "eastern_destiny"
            else "Validating the incoming reading request."
            if request.language == "en"
            else "Đang kiểm tra thông tin đầu vào."
        )
        yield self.stream_service.status_event(
            AgentStatus(agent="validator", state="running", message=validator_message)
        )

        if warnings:
            yield self.stream_service.status_event(
                AgentStatus(agent="validator", state="warning", message=" ".join(warnings))
            )

        for agent_name, message in self._status_plan(request):
            yield self.stream_service.status_event(AgentStatus(agent=agent_name, state="running", message=message))

        response = await self._run_pipeline(request)
        for warning in response.metadata.warnings:
            yield self.stream_service.status_event(AgentStatus(agent="safety", state="warning", message=warning))
        for event in self.stream_service.chunk_events(response.report, self.settings.stream_chunk_size):
            yield event
        yield self.stream_service.done_event(response)

    async def _run_pipeline(self, request: AnalyzeRequest) -> FinalReportResponse:
        if request.reading_mode == "eastern_destiny":
            return await self._run_eastern_destiny_pipeline(request)
        return await self._run_vedatwin_pipeline(request)

    async def _run_vedatwin_pipeline(self, request: AnalyzeRequest) -> FinalReportResponse:
        warnings = validate_chat_request(request)
        sections = [
            await self.supervisor.execute(request=request, warnings=warnings),
            await self.supervisor.build_question_focus(request),
        ]

        chart_data = await self.chart_agent.execute(request)
        retrieval_chunks = await self.retrieval_agent.execute(request, chart_data)
        interpretation = await self.interpretation_agent.execute(request, chart_data, retrieval_chunks)
        transit = await self.transit_agent.execute(request, chart_data)
        advisor = await self.advisor_agent.execute(request, chart_data, interpretation, transit)

        sections.extend([interpretation, transit])
        face_used, palm_used = await self._append_optional_visual_sections(request, sections)
        sections.extend([advisor, await self.supervisor.build_encouragement(request)])

        safe_sections, safety_warnings = await self.safety_agent.execute(request.reading_mode, request.language, sections)
        report = build_final_report(
            language=request.language,
            reading_mode=request.reading_mode,
            disclaimer=DISCLAIMER_TEXT[request.reading_mode][request.language],
            sections=safe_sections,
        )
        return FinalReportResponse(
            language=request.language,
            reading_mode=request.reading_mode,
            report=report,
            sections=safe_sections,
            metadata=ReportMetadata(
                reading_mode=request.reading_mode,
                used_rag=bool(retrieval_chunks),
                face_analysis_used=face_used,
                palm_analysis_used=palm_used,
                warnings=warnings + safety_warnings,
            ),
        )

    async def _run_eastern_destiny_pipeline(self, request: AnalyzeRequest) -> FinalReportResponse:
        warnings = validate_chat_request(request)
        chart_data = await self.eastern_chart_agent.execute(request)
        warnings.extend(self._eastern_precision_warnings(request, chart_data))

        sections = [
            await self.eastern_supervisor.build_summary(request, chart_data),
            await self.eastern_supervisor.build_pillar_overview(request, chart_data),
            await self.element_balance_agent.execute(request, chart_data),
        ]

        tendencies = await self.eastern_interpretation_agent.execute(request, chart_data)
        question_focus = await self.eastern_supervisor.build_question_focus(request)
        period = await self.period_insight_agent.execute(request, chart_data)
        advisor = await self.eastern_advisor_agent.execute(request, chart_data, tendencies, period)
        reflection_questions = await self.reflection_agent.execute(request, chart_data)

        sections.extend([tendencies, question_focus, period])
        face_used, palm_used = await self._append_optional_visual_sections(request, sections)
        sections.extend([advisor, reflection_questions, await self.eastern_supervisor.build_encouragement(request)])

        safe_sections, safety_warnings = await self.safety_agent.execute(request.reading_mode, request.language, sections)
        report = build_final_report(
            language=request.language,
            reading_mode=request.reading_mode,
            disclaimer=DISCLAIMER_TEXT[request.reading_mode][request.language],
            sections=safe_sections,
        )
        return FinalReportResponse(
            language=request.language,
            reading_mode=request.reading_mode,
            report=report,
            sections=safe_sections,
            metadata=ReportMetadata(
                reading_mode=request.reading_mode,
                used_rag=False,
                face_analysis_used=face_used,
                palm_analysis_used=palm_used,
                warnings=warnings + safety_warnings,
            ),
        )

    async def _append_optional_visual_sections(self, request: AnalyzeRequest, sections: list) -> tuple[bool, bool]:
        face_used = False
        if request.face_image and self.settings.enable_face_analysis:
            sections.append(await self.face_agent.execute(request))
            face_used = True

        palm_used = False
        if request.palm_image and self.settings.enable_palm_analysis:
            sections.append(await self.palm_agent.execute(request))
            palm_used = True
        return face_used, palm_used

    def _status_plan(self, request: AnalyzeRequest) -> list[tuple[str, str]]:
        if request.reading_mode == "eastern_destiny":
            if request.language == "vi":
                steps = [
                    ("eastern_chart", "Đang ánh xạ các trụ biểu tượng."),
                    ("elements", "Đang đọc thế cân bằng ngũ hành."),
                    ("tendencies", "Đang diễn giải xu hướng tính cách và đời sống."),
                    ("transit", "Đang chiêm nghiệm chu kỳ và giai đoạn sắp tới."),
                ]
            else:
                steps = [
                    ("eastern_chart", "Mapping symbolic pillars..."),
                    ("elements", "Reading five-element balance..."),
                    ("tendencies", "Interpreting personality tendencies..."),
                    ("transit", "Reflecting on upcoming cycles..."),
                ]
        else:
            if request.language == "vi":
                steps = [
                    ("supervisor", "Đang lập kế hoạch cho quy trình agent."),
                    ("birth_chart", "Đang tạo dữ liệu lá số cấu trúc."),
                    ("retrieval", "Đang truy xuất bối cảnh chiêm tinh phụ trợ."),
                    ("interpretation", "Đang diễn giải tính cách và xu hướng nổi bật."),
                    ("transit", "Đang phân tích những chủ đề theo giai đoạn thời gian."),
                ]
            else:
                steps = [
                    ("supervisor", "Planning the agent workflow."),
                    ("birth_chart", "Building structured chart data."),
                    ("retrieval", "Retrieving grounded symbolic context."),
                    ("interpretation", "Interpreting core personality themes."),
                    ("transit", "Analyzing time-based patterns and momentum."),
                ]

        if request.face_image and self.settings.enable_face_analysis:
            steps.append(
                ("face", "Integrating visual symbolism from the optional face image...")
                if request.reading_mode == "eastern_destiny" and request.language == "en"
                else ("face", "Đang tích hợp biểu tượng thị giác từ ảnh khuôn mặt tùy chọn...")
                if request.reading_mode == "eastern_destiny"
                else ("face", "Reviewing the optional face image for symbolic presentation cues.")
                if request.language == "en"
                else ("face", "Đang đọc các dấu hiệu trình bày từ ảnh khuôn mặt tùy chọn.")
            )
        if request.palm_image and self.settings.enable_palm_analysis:
            steps.append(
                ("palm", "Integrating visual symbolism from the optional palm image...")
                if request.reading_mode == "eastern_destiny" and request.language == "en"
                else ("palm", "Đang tích hợp biểu tượng thị giác từ ảnh bàn tay tùy chọn...")
                if request.reading_mode == "eastern_destiny"
                else ("palm", "Reviewing the optional palm image for symbolic line patterns.")
                if request.language == "en"
                else ("palm", "Đang đọc các đường nét biểu tượng từ ảnh bàn tay tùy chọn.")
            )

        if request.reading_mode == "eastern_destiny":
            steps.extend(
                [
                    ("advisor", "Generating practical guidance...") if request.language == "en" else ("advisor", "Đang tạo gợi ý thực tế..."),
                    ("safety", "Running safety review...") if request.language == "en" else ("safety", "Đang chạy bước rà soát an toàn..."),
                    ("finalize", "Finalizing Eastern Destiny report...") if request.language == "en" else ("finalize", "Đang hoàn thiện báo cáo Eastern Destiny..."),
                ]
            )
        else:
            steps.extend(
                [
                    ("advisor", "Shaping practical, empowering guidance.") if request.language == "en" else ("advisor", "Đang chuyển hóa thành gợi ý thực tế và nâng đỡ."),
                    ("safety", "Running a final safety and language review.") if request.language == "en" else ("safety", "Đang kiểm tra an toàn và tính nhất quán ngôn ngữ."),
                ]
            )
        return steps

    def _eastern_precision_warnings(self, request: AnalyzeRequest, chart_data) -> list[str]:
        warnings: list[str] = []
        if chart_data.timezone_confidence == "low":
            warnings.append(
                "Birthplace could not be mapped confidently to a timezone, so Eastern Destiny thresholds are being treated more softly."
                if request.language == "en"
                else "Nơi sinh chưa được ánh xạ múi giờ đủ chắc, nên các mốc chuyển trụ của Eastern Destiny đang được diễn giải mềm hơn."
            )
        elif chart_data.timezone_confidence == "medium":
            warnings.append(
                f"Birthplace timezone was inferred as {chart_data.timezone_name}, but the mapping is still approximate."
                if request.language == "en"
                else f"Múi giờ nơi sinh được suy là {chart_data.timezone_name}, nhưng mức ánh xạ vẫn chỉ ở mức gần đúng."
            )
        if not request.birth_time:
            warnings.append(
                "Birth time is missing, so hour pillar precision is unavailable."
                if request.language == "en"
                else "Chưa có giờ sinh nên không thể đảm bảo độ chính xác cho trụ giờ."
            )
        return warnings
