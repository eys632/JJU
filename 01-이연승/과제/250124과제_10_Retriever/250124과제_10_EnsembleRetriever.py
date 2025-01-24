from dotenv import load_dotenv
import os
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import ConfigurableField
from langchain.retrievers import EnsembleRetriever

def load_env_variables():
    """ api 로드"""
    load_dotenv()
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "LANGCHAIN_API_KEY": os.getenv("LANGCHAIN_API_KEY"),
        "LANGCHAIN_TRACING_V2": os.getenv("LANGCHAIN_TRACING_V2"),
        "LANGCHAIN_ENDPOINT": os.getenv("LANGCHAIN_ENDPOINT"),
        "LANGCHAIN_PROJECT_ID": os.getenv("LANGCHAIN_PROJECT_ID"),
    }

def initialize_retrievers(doc_list):
    """BM25Retriever, FAISS retriever 초기화"""
    # BM25 Retriever 초기화
    bm25_retriever = BM25Retriever.from_texts(doc_list)
    bm25_retriever.k = 1  # 검색 결과 개수 설정

    # FAISS Retriever 초기화
    embedding = OpenAIEmbeddings()
    faiss_vectorstore = FAISS.from_texts(doc_list, embedding)
    faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k": 1})

    return bm25_retriever, faiss_retriever

def create_ensemble_retriever(bm25_retriever, faiss_retriever, weights=[0.7, 0.3]):
    """EnsembleRetriever 생성"""
    return EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever],
        weights=weights,
    )

def configure_ensemble_retriever(ensemble_retriever):
    """EnsembleRetriever에 ConfigurableField 추가"""
    return ensemble_retriever.configurable_fields(
        weights=ConfigurableField(
            id="ensemble_weights",
            name="Ensemble Weights",
            description="Ensemble Weights",
        )
    )

def get_retriever_results(query, bm25_retriever, faiss_retriever, ensemble_retriever, config_1, config_2):
    """각 리트리버의 결과 반환"""
    bm25_result = bm25_retriever.invoke(query)
    faiss_result = faiss_retriever.invoke(query)

    # 기본 앙상블 리트리버
    ensemble_result = ensemble_retriever.invoke(query)

    # 구성 변경된 앙상블 리트리버
    docs_1 = ensemble_retriever.invoke(query, config=config_1)
    docs_2 = ensemble_retriever.invoke(query, config=config_2)

    return bm25_result, faiss_result, ensemble_result, docs_1, docs_2

if __name__ == "__main__":
    # 환경 변수 로드
    env_vars = load_env_variables()

    # 샘플 문서 리스트
    doc_list = [
        "I like apples",
        "I like apple company",
        "I like apple's iphone",
        "Apple is my favorite company",
        "I like apple's ipad",
        "I like apple's macbook",
    ]

    # 리트리버 초기화
    bm25_retriever, faiss_retriever = initialize_retrievers(doc_list)

    # 앙상블 리트리버 생성 및 구성
    ensemble_retriever = create_ensemble_retriever(bm25_retriever, faiss_retriever)
    ensemble_retriever = configure_ensemble_retriever(ensemble_retriever)

    # 질문
    query = "my favorite fruit is apple"

    # 구성 변경
    config_1 = {"configurable": {"ensemble_weights": [0.9, 0.1]}}
    config_2 = {"configurable": {"ensemble_weights": [0.3, 0.7]}}

    # 결과 출력
    bm25_result, faiss_result, ensemble_result, docs_1, docs_2 = get_retriever_results(
        query, bm25_retriever, faiss_retriever, ensemble_retriever, config_1, config_2
    )

    print(docs_1, docs_2)
