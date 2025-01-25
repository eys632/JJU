import shutil
import os
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_upstage import UpstageEmbeddings
from langchain_chroma import Chroma

# 환경 변수 로드
from dotenv import load_dotenv
load_dotenv()

# 데이터 정의
texts = [
    "안녕, 만나서 반가워.",
    "LangChain simplifies the process of building applications with large language models",
    "랭체인 한국어 튜토리얼은 LangChain의 공식 문서, cookbook 및 다양한 실용 예제를 바탕으로 하여 사용자가 LangChain을 더 쉽고 효과적으로 활용할 수 있도록 구성되어 있습니다.",
    "LangChain은 초거대 언어모델로 애플리케이션을 구축하는 과정을 단순화합니다.",
    "Retrieval-Augmented Generation (RAG) is an effective technique for improving AI responses.",
]

query = "LangChain 에 대해서 상세히 알려주세요."
DB_PATH_OPENAI = "./chroma_db_openai"
DB_PATH_UPSTAGE = "./chroma_db_upstage"

# 안전한 디렉토리 삭제 함수
def safe_delete_directory(directory_path):
    def onerror(func, path, exc_info):
        print(f"Error deleting file: {path}. Skipping.")
        os.chmod(path, 0o777)  # 권한 수정 후 재시도
        func(path)

    if os.path.exists(directory_path):
        try:
            shutil.rmtree(directory_path, onerror=onerror)
            print(f"Deleted directory: {directory_path}")
        except Exception as e:
            print(f"Failed to delete directory: {directory_path}. Error: {e}")

# Chroma DB 생성 함수
def create_chroma_db(texts, embedding_model, db_path, collection_name):
    # 기존 DB 삭제
    safe_delete_directory(db_path)

    # Chroma 데이터베이스 생성
    db = Chroma.from_texts(
        texts=texts,
        embedding=embedding_model,
        persist_directory=db_path,
        collection_name=collection_name
    )
    return db

# 유사도 검색 및 결과 출력 함수
def search_similarity(db, query, model_name):
    # 유사도 검색
    results = db.similarity_search_with_score(query=query, k=5)

    # 결과 출력
    print(f"\n[{model_name}] Query: {query}\n{'='*40}")
    for i, (document, score) in enumerate(results):
        print(f"[{i}] 유사도: {score:.3f} | {document.page_content}")

# Main: OpenAI와 Upstage 결과 비교
if __name__ == "__main__":
    # OpenAI 임베딩 모델
    openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    openai_db = create_chroma_db(
        texts=texts,
        embedding_model=openai_embeddings,
        db_path=DB_PATH_OPENAI,
        collection_name="openai_collection"
    )

    # Upstage 임베딩 모델
    upstage_embeddings = UpstageEmbeddings(model="solar-embedding-1-large-query")
    upstage_db = create_chroma_db(
        texts=texts,
        embedding_model=upstage_embeddings,
        db_path=DB_PATH_UPSTAGE,
        collection_name="upstage_collection"
    )

    # OpenAI 결과 검색 및 출력
    search_similarity(
        db=openai_db,
        query=query,
        model_name="OpenAI Embeddings"
    )

    # Upstage 결과 검색 및 출력
    search_similarity(
        db=upstage_db,
        query=query,
        model_name="Upstage Embeddings"
    )
