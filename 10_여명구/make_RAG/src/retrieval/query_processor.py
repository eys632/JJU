# src/retrieval/query_processor.py
from typing import List, Tuple, Dict, Any
from ..embeddings.embedding_model import EmbeddingModel
from ..embeddings.vector_db import FaissVectorDB

class QueryProcessor:
    def __init__(self, embedding_model: EmbeddingModel, vector_db: FaissVectorDB):
        self.embedding_model = embedding_model
        self.vector_db = vector_db

    def process_query(self, query: str, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        query_embedding = self.embedding_model.embed_texts([query])
        results = self.vector_db.search(query_embedding, top_k=top_k)
        return results
