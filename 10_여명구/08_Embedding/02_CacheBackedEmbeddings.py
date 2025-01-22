from dotenv import load_dotenv
from langchain.storage import LocalFileStore
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
import os

# 환경 변수 로드
load_dotenv()

# 현재 파일 위치 기준 디렉토리 설정
current_dir = os.path.dirname(__file__)
cache_path = os.path.join(current_dir, "cache")  # 같은 폴더에 'cache' 디렉토리 생성

# OpenAI 임베딩 설정
embedding = OpenAIEmbeddings(model='text-embedding-3-small')

# 로컬 파일 저장소 설정
store = LocalFileStore(cache_path)

# 캐시를 지원하는 임베딩 생성
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=embedding,
    document_embedding_cache=store,
    namespace=embedding.model,
)

# 문서 로드 (인코딩 지정)
file_path = os.path.join("10_여명구", "data", "appendix-keywords.txt")
raw_documents = TextLoader(file_path, encoding="utf-8").load()

# 문자 단위로 텍스트 분할 설정
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)

# FAISS 데이터베이스 생성
db = FAISS.from_documents(documents, cached_embedder)
