# src/embeddings/vector_db.py

import faiss
import numpy as np
from typing import List, Dict, Any

class FaissVectorDB:
    def __init__(self, embedding_dim: int):
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.doc_embeddings = np.empty((0, embedding_dim), dtype='float32')
        self.doc_metadata = []

    def add_documents(self, embeddings: np.ndarray, metadata_list: List[Dict[str, Any]]):
        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype(np.float32)

        self.index.add(embeddings)
        self.doc_embeddings = np.vstack([self.doc_embeddings, embeddings])
        self.doc_metadata.extend(metadata_list)

    def search(self, query_embedding: np.ndarray, top_k: int = 3):
        if query_embedding.dtype != np.float32:
            query_embedding = query_embedding.astype(np.float32)

        D, I = self.index.search(query_embedding, top_k)

        results = []
        for idx, score in zip(I[0], D[0]):
            meta = self.doc_metadata[idx]
            results.append((meta, float(score)))
        return results
