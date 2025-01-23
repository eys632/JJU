from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 현재 디렉토리를 기준으로 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_FILE = os.path.join(BASE_DIR, "extracted_texts/pypdf_text.txt")
DB_PATH = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "documents"

def load_and_split_text(file_path, chunk_size=600):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
    return text_splitter.split_text(text)

def setup_chroma_db(split_docs, db_path, collection_name):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY")  # API 키 로드
    )
    db = Chroma.from_texts(
        texts=split_docs,
        embedding=embeddings,
        persist_directory=db_path,
        collection_name=collection_name,
    )
    return db

if __name__ == "__main__":
    split_docs = load_and_split_text(TEXT_FILE)
    chroma_db = setup_chroma_db(split_docs, DB_PATH, COLLECTION_NAME)
    print("ChromaDB 설정 완료")
