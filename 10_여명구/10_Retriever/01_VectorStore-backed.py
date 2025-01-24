from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_upstage import UpstageEmbeddings
from langchain_core.runnables import ConfigurableField

# 환경 변수 로드
load_dotenv()

# ========================= 모듈화된 함수들 =========================
# 문서 로드 및 분할 함수
def load_and_split_documents(file_path, chunk_size=300, chunk_overlap=0):
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)

# FAISS 데이터베이스 생성 함수
def create_faiss_db(split_docs, embeddings):
    return FAISS.from_documents(split_docs, embeddings)

# 검색 결과 출력 함수
def print_results(docs, title):
    print(f"\n=== {title} ===")
    for doc in docs:
        print(doc.page_content)
        print("=" * 100)

# 검색 설정 함수
def configure_retriever(db, search_type="similarity", search_kwargs={}):
    """
    FAISS 데이터베이스에서 검색기 설정
    :param db: FAISS 데이터베이스 객체
    :param search_type: 검색 유형 ('similarity', 'similarity_score_threshold', 'mmr')
    :param search_kwargs: 검색에 사용할 추가 매개변수
    :return: 설정된 검색기 객체
    """
    return db.as_retriever(search_type=search_type, search_kwargs=search_kwargs)

# 검색 실행 함수
def perform_search(retriever, query, config=None):
    return retriever.invoke(query, config=config) if config else retriever.invoke(query)

# ========================= 메인 실행 함수 =========================
def main():
    # 파일 경로 설정
    file_path = "10_여명구/data/appendix-keywords.txt"

    # 1. 문서 로드 및 분할
    split_docs = load_and_split_documents(file_path)

    # 2. 기본 OpenAI 임베딩 및 FAISS 데이터베이스 생성
    embeddings = OpenAIEmbeddings()
    db = create_faiss_db(split_docs, embeddings)

    # 3. 기본 검색
    retriever = configure_retriever(db)
    docs = perform_search(retriever, "임베딩(Embedding)은 무엇인가요?")
    print_results(docs, "기본 검색 결과")

    # 4. Max Marginal Relevance (MMR) 검색
    retriever = configure_retriever(db, search_type="mmr", search_kwargs={"k": 2, "fetch_k": 10, "lambda_mult": 0.6})
    docs = perform_search(retriever, "임베딩(Embedding)은 무엇인가요?")
    print_results(docs, "MMR 검색 결과")

    # 5. 유사도 점수 임계값 검색
    retriever = configure_retriever(db, search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.8})
    docs = perform_search(retriever, "Word2Vec 은 무엇인가요?")
    print_results(docs, "유사도 점수 임계값 검색 결과")

    # 6. top_k 검색
    retriever = configure_retriever(db, search_kwargs={"k": 1})
    docs = perform_search(retriever, "임베딩(Embedding)은 무엇인가요?")
    print_results(docs, "Top-K 검색 결과")

    # 7. 동적 설정 검색
    retriever = db.as_retriever(search_kwargs={"k": 1}).configurable_fields(
        search_type=ConfigurableField(id="search_type", name="Search Type", description="The search type to use"),
        search_kwargs=ConfigurableField(id="search_kwargs", name="Search Kwargs", description="The search kwargs to use"),
    )
    config = {"configurable": {"search_kwargs": {"k": 3}}}
    docs = perform_search(retriever, "임베딩(Embedding)은 무엇인가요?", config=config)
    print_results(docs, "동적 설정 검색 결과 - Top-K")

    config = {
        "configurable": {
            "search_type": "similarity_score_threshold",
            "search_kwargs": {"score_threshold": 0.8},
        }
    }
    docs = perform_search(retriever, "Word2Vec 은 무엇인가요?", config=config)
    print_results(docs, "동적 설정 검색 결과 - 유사도 점수 임계값")

    config = {
        "configurable": {
            "search_type": "mmr",
            "search_kwargs": {"k": 2, "fetch_k": 10, "lambda_mult": 0.6},
        }
    }
    docs = perform_search(retriever, "Word2Vec 은 무엇인가요?", config=config)
    print_results(docs, "동적 설정 검색 결과 - MMR")

    # 8. Upstage 임베딩 검색
    doc_embedder = UpstageEmbeddings(model="solar-embedding-1-large-passage")
    split_docs = load_and_split_documents(file_path)
    db = create_faiss_db(split_docs, doc_embedder)

    query_embedder = UpstageEmbeddings(model="solar-embedding-1-large-query")
    query_vector = query_embedder.embed_query("임베딩(Embedding)은 무엇인가요?")

    docs = db.similarity_search_by_vector(query_vector, k=2)
    print_results(docs, "Upstage 임베딩 검색 결과")

if __name__ == "__main__":
    main()
