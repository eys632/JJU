import os
from dotenv import load_dotenv
from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    UnstructuredExcelLoader,
    TextLoader,
    JSONLoader,
    UnstructuredMarkdownLoader,
)
from langchain_community.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter,
)
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA

# .env 파일 로드
load_dotenv()

# API Key 가져오기
openai_api_key = os.getenv("OPENAI_API_KEY")

# API 키 확인
if not openai_api_key:
    raise ValueError("OpenAI API Key가 설정되지 않았습니다. .env 파일에서 확인하세요.")

# 로더와 스플리터 선택
def select_loader(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".pdf":
        return PyPDFLoader(file_path)
    elif extension == ".csv":
        return CSVLoader(file_path)
    elif extension in [".xls", ".xlsx"]:
        return UnstructuredExcelLoader(file_path)
    elif extension == ".txt":
        return TextLoader(file_path)
    elif extension == ".json":
        return JSONLoader(file_path)
    elif extension == ".md":
        return UnstructuredMarkdownLoader(file_path)
    else:
        raise ValueError(f"Unsupported file format: {extension}")

def select_splitter(file_type):
    if file_type in [".txt", ".md"]:
        return CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    elif file_type in [".pdf", ".csv", ".xls", ".xlsx"]:
        return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    elif file_type == ".json":
        return TokenTextSplitter(chunk_size=1000)
    else:
        return CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# RAG 파이프라인 구축
def build_rag_pipeline(file_path, query):
    loader = select_loader(file_path)
    file_type = os.path.splitext(file_path)[1].lower()
    documents = loader.load()

    splitter = select_splitter(file_type)
    split_docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = Chroma.from_documents(split_docs, embeddings)

    llm = OpenAI(api_key=openai_api_key, temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    response = qa_chain.run(query)
    return response

# 실행 예시
file_path = r"C:\Users\user\Desktop\2024년 2학기\딥러닝\2024비트특강\practice_2\리눅스운영체제 기말고사 답안 및 분포.pdf"  # 처리할 파일 경로
query = "점수 분포당 인원 수가 어떻게 돼?"
response = build_rag_pipeline(file_path, query)
print(response)
