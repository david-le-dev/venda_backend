from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

from app.models.response_models import FinalReportResponse
from app.services.orchestrator_service import OrchestratorService
from app.utils.request_parsers import parse_analyze_request


router = APIRouter()
orchestrator = OrchestratorService()


@router.post("/analyze/report", response_model=FinalReportResponse)
async def analyze_report(request: Request) -> FinalReportResponse:
    parsed_request = await parse_analyze_request(request)
    return await orchestrator.generate_report(parsed_request)


@router.post("/analyze/stream")
async def analyze_stream(request: Request) -> EventSourceResponse:
    parsed_request = await parse_analyze_request(request)
    return EventSourceResponse(orchestrator.stream_report(parsed_request))
