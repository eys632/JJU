# 환경 변수 로드
from dotenv import load_dotenv
load_dotenv()

# 필요한 모듈 임포트
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# --------------------------------------------------------
# 1. 데이터 로드 및 텍스트 분할
# --------------------------------------------------------

# 텍스트 분할 설정
text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=0)

# 텍스트 파일 로드 및 분할
loader1 = TextLoader(r"10_여명구\09_VectorStore\data\nlp-keywords.txt", encoding="utf-8")
loader2 = TextLoader(r"10_여명구\09_VectorStore\data\finance-keywords.txt", encoding="utf-8")

split_doc1 = loader1.load_and_split(text_splitter)
split_doc2 = loader2.load_and_split(text_splitter)

# --------------------------------------------------------
# 2. OpenAI 임베딩 모델과 Chroma 데이터베이스 생성
# --------------------------------------------------------

# OpenAI 임베딩 모델 설정
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Chroma 데이터베이스 생성
DB_PATH = "./chroma_db"

db = Chroma.from_documents(
    documents=split_doc1,
    embedding=embeddings,
    collection_name="my_db"
)

# Chroma 데이터베이스 디스크에 저장
persist_db = Chroma.from_documents(
    documents=split_doc1,
    embedding=OpenAIEmbeddings(),
    persist_directory=DB_PATH,
    collection_name="my_db"
)

# 저장된 데이터베이스 로드
load_db = Chroma(
    persist_directory=DB_PATH,
    embedding_function=OpenAIEmbeddings(),
    collection_name="my_db"
)

# 존재하지 않는 collection_name으로 로드
load_db2 = Chroma(
    persist_directory=DB_PATH,
    embedding_function=OpenAIEmbeddings(),
    collection_name="my_db2"
)

# --------------------------------------------------------
# 3. 문자열 리스트로 Chroma 데이터베이스 생성 및 유사도 검색
# --------------------------------------------------------

# 문자열 리스트로 Chroma 데이터베이스 생성
db2 = Chroma.from_texts(
    texts=[
        "Helllo. 반갑습니다.",
        "my name is 앤디입니다.",
        "Embedding을 사용하여 유사도를 계산합니다.",
    ],
    embedding=OpenAIEmbeddings(),
)

# 저장된 데이터 조회
db2_data = db2.get()

# 유사도 검색
db2_similar = db2.similarity_search(query="앤디", k=2)

# [문자열 리스트] 데이터베이스 정보 출력
print(f"[문자열 리스트] db2_길이: {len(db2_data['documents'])}")

# 각 Document 출력
print("\nDocuments:")
for idx, document in enumerate(db2_data['documents'], start=1):
    print(f"Document {idx}:\n{document}\n")

print("=" * 50)

# 유사도 검색 결과 출력
print("Similarity Search Results:")
for idx, result in enumerate(db2_similar, start=1):
    print(f"Result {idx}:\n{result.page_content}\n")

# --------------------------------------------------------
# 4. 새로운 Document 추가
# --------------------------------------------------------

# 새로운 Document 추가
db2.add_documents([
    Document(
        page_content="안녕하세요! 이번엔 도큐먼트를 새로 추가해 볼께요",
        metadata={"source": "mydata.txt"},
        id="1",
    )
])

# 추가된 Document 추가
db2.add_texts(
    texts=["2번 문서.", "3번 문서입니다."],
    metadatas=[{"source": "mydata.txt"}, {"source": "mydata.txt"}],
    ids=["2", "3"]
)

# 추가된 Document 출력
print("\nDocuments after adding new ones:")
for idx, document in enumerate(db2.get()["documents"], start=1):
    print(f"Document {idx}:\n{document}\n")

# 데이터베이스 리셋
db.reset_collection()
db2.reset_collection()

print(db2.get())  # 빈 데이터베이스 출력

# --------------------------------------------------------
# 5. 두 문서 결합 후 Chroma 데이터베이스 생성 및 MMR 탐색
# --------------------------------------------------------

# DB 생성: 두 문서를 합침
db = Chroma.from_documents(
    documents=split_doc1 + split_doc2,
    embedding=OpenAIEmbeddings(),
    collection_name="nlp",
)

# MMR 기반 탐색 설정
retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 2,  # 반환할 문서 수
        "lambda_mult": 0.25,  # MMR 결과의 다양성 조절
        "fetch_k": 10,  # MMR 알고리즘에 전달할 문서 수
        "filter": {"source": r"10_여명구\09_VectorStore\data\nlp-keywords.txt"},
    }
)

# MMR 탐색 수행
response = retriever.invoke("Word2Vec 에 대하여 알려줘")

# MMR 탐색 결과 출력
print(f"\n[MMR 기반 문서 탐색 결과]\n{len(response)}개의 문서:")
for doc in response:
    print(f"- {doc.page_content}")
