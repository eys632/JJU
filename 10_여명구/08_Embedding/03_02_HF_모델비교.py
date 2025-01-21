from dotenv import load_dotenv
import os
import numpy as np
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from FlagEmbedding import BGEM3FlagModel
from PyPDF2 import PdfReader

# 환경 변수 로드
load_dotenv()

# PDF 파일 로드 함수
def load_pdf_to_texts(pdf_path):
    print("[INFO] Loading PDF file and extracting texts...")
    reader = PdfReader(pdf_path)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text())
    print("[INFO] PDF text extraction complete.")
    return texts

# PDF 경로
pdf_path = r"10_여명구\data\로봇 공학에서의 인공지능 적용.pdf"  # 실제 PDF 파일 경로로 변경
texts = load_pdf_to_texts(pdf_path)

# 쿼리 목록
queries = [
    "YETI 프레임워크는 기존 HoloAssist와 비교했을 때 어떤 주요 개선점을 제공하는가?",
    "YETI가 프로액티브 개입을 위해 사용하는 주요 특징 신호는 무엇이며, 이들이 어떻게 동작하는가?",
    "SSIM(Structural Similarity Index Measure)이 YETI에서 어떤 역할을 하며, 특정 프레임을 필터링하는 이유는 무엇인가?",
    "YETI 알고리즘에서 설정 가능한 주요 하이퍼파라미터(예: SSIM 임계값, Conversation Interval 등)의 값과 그 중요성은 무엇인가?",
    "YETI의 글로벌(Global) 및 로컬(Local) 접근 방식의 차이는 무엇이며, 각각의 장단점은 무엇인가?",
    "YETI가 실시간으로 개입 결정을 내리는 데 있어 기존 분류기(Random Forest, MLP 등)보다 적합한 이유는 무엇인가?",
    "YETI 프레임워크가 AR 기기를 활용하여 사용자와 협업할 때 발생하는 주요 도전 과제는 무엇이며, 이를 어떻게 해결했는가?",
    "YETI가 HoloAssist 데이터셋의 프로액티브 개입 유형(예: Confirm Action, Correct Mistake, Follow Up)별로 어떻게 성능을 발휘했는가?",
    "YETI가 특정 작업(예: 컴퓨터 조립, 커피 만들기 등)에서 사용자의 안전을 보장하기 위해 어떤 방식으로 개입하는가?",
    "향후 YETI 프레임워크를 개선하거나 확장하기 위해 계획 중인 연구 방향이나 가능성은 무엇인가?",
]

# 공통 처리 함수 (HuggingFace)
def process_huggingface_model(model_name, texts, queries, model_kwargs=None, encode_kwargs=None):
    print(f"[INFO] Processing HF model: {model_name}")
    hf_embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs or {},
        encode_kwargs=encode_kwargs or {},
    )
    print("[INFO] Embedding documents...")
    embedded_documents = hf_embeddings.embed_documents(texts)
    print("[INFO] Document embedding complete.")
    results = []

    for query in queries:
        print(f"[INFO] Processing query: {query}")
        embedded_query = hf_embeddings.embed_query(query)
        similarity_scores = np.array(embedded_query) @ np.array(embedded_documents).T
        sorted_idx = similarity_scores.argsort()[::-1]
        print(f"[DEBUG] Query Scores: {similarity_scores}")
        results.append({"query": query, "scores": similarity_scores, "sorted_idx": sorted_idx})
        print(f"[INFO] Query processing complete for: {query}")

    return results

# 공통 처리 함수 (FlagEmbedding)
def process_flag_model(model_name, texts, queries, return_type="dense", **kwargs):
    print(f"[INFO] Processing FlagEmbedding model: {model_name}")
    flag_embeddings = BGEM3FlagModel(model_name, use_fp16=True)
    if return_type == "dense":
        print("[INFO] Embedding documents using dense vectors...")
        embedded_documents = flag_embeddings.encode(
            texts, batch_size=kwargs.get("batch_size", 12), max_length=kwargs.get("max_length", 8192)
        )["dense_vecs"]
    elif return_type == "lexical":
        print("[INFO] Embedding documents using lexical vectors...")
        embedded_documents = flag_embeddings.encode(texts, return_sparse=True)
        if embedded_documents is None or "lexical_weights" not in embedded_documents:
            raise ValueError("[ERROR] Lexical embedding failed. The model did not return lexical_weights.")
    elif return_type == "colbert":
        print("[INFO] Embedding documents using ColBERT vectors...")
        embedded_documents = flag_embeddings.encode(texts, return_colbert_vecs=True)
        if embedded_documents is None or "colbert_vecs" not in embedded_documents:
            raise ValueError("[ERROR] ColBERT embedding failed. The model did not return colbert_vecs.")
    else:
        raise ValueError(f"Invalid return_type: {return_type}")

    results = []

    for query in queries:
        print(f"[INFO] Processing query: {query}")
        if return_type == "dense":
            embedded_query = flag_embeddings.encode([query], batch_size=1)["dense_vecs"][0]
            similarity_scores = np.array(embedded_query) @ np.array(embedded_documents).T
        elif return_type == "lexical":
            query_embedding = flag_embeddings.encode([query], return_sparse=True)
            if query_embedding is None or "lexical_weights" not in query_embedding:
                raise ValueError("[ERROR] Query lexical embedding failed.")

            similarity_scores = [
                flag_embeddings.compute_lexical_matching_score(
                    embedded_documents["lexical_weights"][i],
                    query_embedding["lexical_weights"][0],
                ) for i in range(len(embedded_documents["lexical_weights"]))
            ]
        elif return_type == "colbert":
            query_embedding = flag_embeddings.encode([query], return_colbert_vecs=True)
            if query_embedding is None or "colbert_vecs" not in query_embedding:
                raise ValueError("[ERROR] Query ColBERT embedding failed.")

            similarity_scores = [
                flag_embeddings.colbert_score(
                    embedded_documents["colbert_vecs"][i],
                    query_embedding["colbert_vecs"][0],
                ) for i in range(len(embedded_documents["colbert_vecs"]))
            ]

        print(f"[DEBUG] Query Scores: {similarity_scores}")
        sorted_idx = np.argsort(similarity_scores)[::-1]
        results.append({"query": query, "scores": similarity_scores, "sorted_idx": sorted_idx})
        print(f"[INFO] Query processing complete for: {query}")

    return results

# 모델 목록
models = [
    {
        "name": "intfloat/multilingual-e5-large-instruct",
        "type": "huggingface",
        "model_kwargs": {"device": "cpu"},
        "encode_kwargs": {"normalize_embeddings": True},
    },
    {
        "name": "BAAI/bge-m3",
        "type": "huggingface",
        "model_kwargs": {"device": "cpu"},
        "encode_kwargs": {"normalize_embeddings": True},
    },
    {
        "name": "BAAI/bge-m3",
        "type": "flag",
        "return_type": "dense",
    },
    {
        "name": "BAAI/bge-m3",
        "type": "flag",
        "return_type": "lexical",
    },
    {
        "name": "BAAI/bge-m3",
        "type": "flag",
        "return_type": "colbert",
    },
]

# 모델별 처리 실행 및 결과 비교
final_results = {}
for model in models:
    if model["type"] == "huggingface":
        print(f"[INFO] Starting HuggingFace model: {model['name']}")
        results = process_huggingface_model(
            model["name"], texts, queries, model["model_kwargs"], model["encode_kwargs"]
        )
    elif model["type"] == "flag":
        print(f"[INFO] Starting FlagEmbedding model: {model['name']} ({model['return_type']})")
        results = process_flag_model(
            model["name"], texts, queries, return_type=model["return_type"]
        )
    final_results[model["name"] + "_" + model.get("return_type", "default")] = results
    print(f"[INFO] Completed processing for model: {model['name']}")

# 각 쿼리에 대해 모델별 유사도 점수를 출력
for idx, query in enumerate(queries):
    print(f"\n[Query]: {query}")
    max_score = -1
    best_model = None
    best_document = None

    for model_name, results in final_results.items():
        score = max(results[idx]["scores"])
        best_idx = np.argmax(results[idx]["scores"])
        print(f"  {model_name}: Highest Score = {score:.4f}")

        if score > max_score:
            max_score = score
            best_model = model_name
            best_document = texts[results[idx]["sorted_idx"][0]][:300]  # 문서 내용을 300자까지만 표시

    print(f"\n=== Best Model ===")
    print(f"Model: {best_model}")
    print(f"Document Snippet: {best_document}...")
    print(f"Score: {max_score:.4f}")
    print("-" * 50)
