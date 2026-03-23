from __future__ import annotations

from app.config import get_settings
from app.models.response_models import RetrievalChunk
from app.rag.chroma_store import ChromaStore
from app.utils.logging import get_logger


class RAGService:
    """Queries ChromaDB when enabled and falls back to safe local context."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.logger = get_logger(__name__)
        self.store = ChromaStore(
            persist_dir=self.settings.chroma_persist_dir,
            collection_name=self.settings.rag_collection_name,
        )

    async def retrieve(self, query: str, top_k: int = 3) -> list[RetrievalChunk]:
        if not self.settings.enable_rag:
            return []

        try:
            collection = self.store.get_collection()
            if collection is None:
                return self._fallback_chunks(query)

            results = collection.query(query_texts=[query], n_results=top_k)
            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            chunks: list[RetrievalChunk] = []
            for index, document in enumerate(documents):
                metadata = metadatas[index] if index < len(metadatas) else {}
                chunks.append(
                    RetrievalChunk(
                        source_tag=str(metadata.get("source", f"rag-{index + 1}")),
                        content=document,
                    )
                )
            return chunks or self._fallback_chunks(query)
        except BaseException as exc:  # pragma: no cover
            self.logger.warning("Chroma query failed, using fallback context: %s", exc)
            return self._fallback_chunks(query)

    def _fallback_chunks(self, query: str) -> list[RetrievalChunk]:
        return [
            RetrievalChunk(
                source_tag="safe-vedic-summary",
                content=(
                    "Vedic symbolism is best framed as reflective guidance around tendencies, "
                    "timing, and self-awareness rather than fixed destiny."
                ),
            ),
            RetrievalChunk(source_tag="question-context", content=f"User focus: {query}"),
        ]
