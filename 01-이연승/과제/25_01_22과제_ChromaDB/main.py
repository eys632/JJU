from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from sentence_transformers import SentenceTransformer

# Sentence-Transformers 모델 로드
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 벡터 저장을 위한 데이터베이스 초기화
persist_directory = "your_persist_directory"  # 데이터베이스가 저장될 디렉토리

def create_vector_database(text_data):
    """주어진 텍스트 데이터를 벡터화하여 Chroma 데이터베이스에 저장"""
    # 텍스트 데이터를 Document 객체로 변환
    documents = [Document(page_content=text) for text in text_data]
    
    # HuggingFaceEmbeddings로 감싸기
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Chroma 데이터베이스 생성 및 벡터 저장
    vectordb = Chroma.from_documents(documents, embedding_model, persist_directory=persist_directory)
    
    # 데이터베이스에 영속성 적용
    vectordb.persist()
    return vectordb

def search_query(query, vectordb, top_k=5):
    """주어진 쿼리에 대해 벡터 검색을 수행하고 결과를 반환"""
    search_results = vectordb.similarity_search(query, k=top_k)
    return search_results

# 예시 텍스트 데이터
text_data = [
    "경제와 관련된 텍스트 예시 1",
    "다음은 과학에 관한 텍스트 예시 2",
    "또 다른 경제에 관한 예시 3"
]

# 벡터 데이터베이스 생성
vectordb = create_vector_database(text_data)

# 예시 쿼리 검색
query = "경제에 대한 정보를 알고 싶어요"
results = search_query(query, vectordb)

# 검색 결과 출력
for idx, result in enumerate(results):
    print(f"--- Result {idx + 1} ---\n{result}")
