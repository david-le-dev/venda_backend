import json
from collections.abc import Iterable

from app.models.agent_models import AgentStatus
from app.models.response_models import FinalReportResponse
from app.utils.logging import get_logger

class StreamService:
    """Formats status and content events for SSE consumers."""

    def __init__(self) -> None:
        self.logger = get_logger(__name__)

    def status_event(self, status: AgentStatus) -> dict[str, str]:
        return {"event": "status", "data": status.model_dump_json()}

    def chunk_events(self, report: str, chunk_size: int) -> Iterable[dict[str, str]]:
        for start in range(0, len(report), chunk_size):
            yield {"event": "chunk", "data": json.dumps({"text": report[start : start + chunk_size]})}

    def done_event(self, response: FinalReportResponse) -> dict[str, str]:
        return {"event": "done", "data": response.model_dump_json()}
