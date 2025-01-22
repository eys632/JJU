import openai
import os
import numpy as np
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API Key is missing. Please set it in your environment variables.")

# PDF 파일 로드 함수
def load_pdf_to_texts(pdf_path):
    print("[INFO] Loading PDF file and extracting texts...")
    reader = PdfReader(pdf_path)
    texts = [page.extract_text() for page in reader.pages]
    print("[INFO] PDF text extraction complete.")
    return texts

# OpenAI Embedding 함수
def get_openai_embedding(text):
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response["data"][0]["embedding"]
    except Exception as e:
        print(f"[ERROR] OpenAI API 호출 중 오류 발생: {e}")
        return None

# 텍스트 크기 제한 함수
MAX_TOKENS = 2048

def truncate_text(text, max_tokens=MAX_TOKENS):
    return text[:max_tokens]

# 모델 처리 함수
def process_model(model_name, texts, queries, method="huggingface"):
    print(f"[INFO] Processing model: {model_name}")
    results = []

    if method == "huggingface":
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        embedded_documents = embeddings.embed_documents(texts)
        for query in queries:
            embedded_query = embeddings.embed_query(query)
            similarity_scores = np.array(embedded_query) @ np.array(embedded_documents).T
            results.append({"query": query, "scores": similarity_scores})

    elif method == "openai":
        embedded_documents = [get_openai_embedding(text) for text in texts]
        embedded_documents = [doc for doc in embedded_documents if doc is not None]

        if not embedded_documents:
            print("[ERROR] No valid embeddings for documents.")
            return

        for query in queries:
            embedded_query = get_openai_embedding(query)
            if embedded_query is None:
                print(f"[ERROR] Failed to process query: {query}")
                continue

            similarity_scores = np.dot(embedded_query, np.array(embedded_documents).T)
            results.append({"query": query, "scores": similarity_scores})

    print(f"[INFO] Processing complete for model: {model_name}")
    return results

# PDF 경로
pdf_path = r"10_여명구\data\로봇 공학에서의 인공지능 적용.pdf"  # 실제 PDF 파일 경로로 변경
texts = load_pdf_to_texts(pdf_path)
texts = [truncate_text(text) for text in texts]  # 텍스트 길이 제한

# 쿼리 목록
queries = [
    "YETI 프레임워크는 기존 HoloAssist와 비교했을 때 어떤 주요 개선점을 제공하는가?",
    "YETI가 프로액티브 개입을 위해 사용하는 주요 특징 신호는 무엇이며, 이들이 어떻게 동작하는가?",
]
queries = [truncate_text(query) for query in queries]

# 모델 목록
models = [
    {"name": "intfloat/multilingual-e5-large-instruct", "method": "huggingface"},
    {"name": "google/flan-t5-large", "method": "huggingface"},
    {"name": "text-embedding-ada-002", "method": "openai"},
    {"name": "sentence-transformers/all-MiniLM-L12-v2", "method": "huggingface"},
]

# 모델 실행 및 결과 저장
all_results = []
for model in models:
    model_name = model["name"]
    method = model["method"]
    print(f"\n[INFO] Starting model: {model_name}")

    results = process_model(model_name, texts, queries, method=method)
    if results:
        all_results.append({"model": model_name, "results": results})
    else:
        print(f"[ERROR] No results for model: {model_name}")

# 쿼리별 모델 유사도 점수 출력
for idx, query in enumerate(queries):
    print(f"\n=== Query {idx + 1}: {query} ===")
    for result in all_results:
        model_name = result["model"]
        scores = result["results"][idx]["scores"]
        best_score = max(scores)
        print(f"{model_name}: {best_score:.4f}")
