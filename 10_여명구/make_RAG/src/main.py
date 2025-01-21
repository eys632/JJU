# src/main.py

import os

# 로더, 임베딩, 검색, 생성 로직을 상대 임포트로 불러온다.
from .loaders.pdf_loader import load_pdf
from .embeddings.embedding_model import EmbeddingModel
from .embeddings.vector_db import FaissVectorDB
from .retrieval.query_processor import QueryProcessor
from .generation.answer_generator import AnswerGenerator

def main():
    # (1) PDF 문서 로딩
    # 예: 루트 폴더에 data/sample.pdf 가 있다고 가정
    # (1) 경로 단순화: "data/sample.pdf"
    pdf_path = "data/29회 보험중개사 시험 합격자 명단.pdf"
    
    # 파일이 실제로 있는지 체크 (디버깅용)
    if not os.path.isfile(pdf_path):
        print(f"Error: File not found -> {os.path.abspath(pdf_path)}")
        return
    
    pdf_docs = load_pdf(pdf_path)

    # (2) 임베딩 모델 초기화
    embedding_model = EmbeddingModel(model_name="sentence-transformers/all-mpnet-base-v2")

    # (3) 벡터 DB 초기화
    vector_db = FaissVectorDB(embedding_dim=768)

    # (4) 문서 임베딩 및 DB 저장
    doc_texts = [doc.content for doc in pdf_docs]
    doc_metas = []
    for doc in pdf_docs:
        meta = {
            "source": doc.metadata.get("source", ""),
            "page": doc.metadata.get("page", ""),
            "content": doc.content
        }
        doc_metas.append(meta)

    doc_embeddings = embedding_model.embed_texts(doc_texts)
    vector_db.add_documents(doc_embeddings, doc_metas)

    # (5) 질의
    query_processor = QueryProcessor(embedding_model, vector_db)
    question = "PDF 문서에서 언급된 주요 내용은 무엇인가요?"
    retrieved_docs = query_processor.process_query(question, top_k=3)

    # (6) 답변 생성
    # .env에서 OPENAI_API_KEY를 불러옴
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    answer_generator = AnswerGenerator(api_key=openai_api_key, model="gpt-4o")
    answer = answer_generator.generate_answer(question, retrieved_docs, max_tokens=500)

    print("=== 질문 ===")
    print(question)
    print("\n=== 답변 ===")
    print(answer)

if __name__ == "__main__":
    main()
