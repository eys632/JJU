from langchain.storage import InMemoryStore
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import ParentDocumentRetriever
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# ===== 문서 로드 =====
# 텍스트 파일을 로드하여 문서 리스트를 생성합니다.
file_path = r"10_여명구\data\appendix-keywords.txt"
loader = TextLoader(file_path, encoding="utf-8")
docs = loader.load()

# ===== 분할기 설정 =====
# 부모 문서를 생성하는 분할기 (큰 단위 청크)
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
# 자식 문서를 생성하는 분할기 (작은 단위 청크)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200)

# ===== 데이터베이스 및 저장소 생성 =====
# 자식 문서의 임베딩 저장 및 검색을 위한 벡터 저장소
vectorstore = Chroma(
    collection_name="split_parents",
    embedding_function=OpenAIEmbeddings()
)

# 부모 문서를 저장하는 메모리 저장소
store = InMemoryStore()

# ===== ParentDocumentRetriever 초기화 =====
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

# ===== 문서 추가 =====
# 로드된 문서를 검색기에 추가
retriever.add_documents(docs, ids=None, add_to_docstore=True)

# ===== 유사도 검색 =====
# 쿼리를 사용하여 자식 청크 검색
query = "Word2Vec"
sub_docs = vectorstore.similarity_search(query)
print("\n[유사도 검색 결과 - 자식 청크]")
print(sub_docs[0].page_content)

# ===== 부모 문서 검색 =====
# 자식 청크의 부모 문서를 검색하여 가져옵니다.
retrieved_docs = retriever.invoke(query)

# 검색된 부모 문서의 정보 출력
print("\n[검색된 부모 문서]")
print(f"문서 길이: {len(retrieved_docs[0].page_content)}")
print("문서 내용 :")
print(retrieved_docs[0].page_content)
