from __future__ import annotations

from typing import Any


class ChromaStore:
    """Small wrapper around ChromaDB collection access and seeding."""

    def __init__(self, persist_dir: str, collection_name: str) -> None:
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self._client = None
        self._collection = None
        self._disabled = False

    def get_collection(self) -> Any | None:
        if self._disabled:
            return None
        if self._collection is not None:
            return self._collection

        try:
            import chromadb

            self._client = chromadb.PersistentClient(path=self.persist_dir)
            self._collection = self._client.get_or_create_collection(name=self.collection_name)
            return self._collection
        except BaseException:
            # Chroma can raise Rust-backed panics that do not inherit from Exception.
            self._disabled = True
            self._client = None
            self._collection = None
            return None
