from app.agents.base import BaseAgent
from app.models.request_models import AnalyzeRequest
from app.models.response_models import ChartData, RetrievalChunk
from app.services.rag_service import RAGService


class RetrievalAgent(BaseAgent):
    def __init__(self) -> None:
        self.rag_service = RAGService()
        super().__init__(
            name="retrieval",
            description="Fetches concise, safe Vedic context from the optional RAG store.",
        )

    async def execute(self, request: AnalyzeRequest, chart_data: ChartData) -> list[RetrievalChunk]:
        query = (
            f"{request.question}. Ascendant: {chart_data.ascendant}. "
            f"Moon sign: {chart_data.moon_sign}. Sun sign: {chart_data.sun_sign}."
        )
        return await self.rag_service.retrieve(query)
