import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index import GPTVectorStoreIndex
from llama_index.readers import SimpleDirectoryReader
from langchain.llms import OpenAI

# .env 파일 로드
load_dotenv()

# API Key 가져오기
openai_api_key = os.getenv("OPENAI_API_KEY")

# PDF 파일 파싱 및 인덱싱
def parse_pdf(file_path):
    parser = LlamaParse(result_type="markdown", verbose=True, language="ko")
    documents = SimpleDirectoryReader(
        input_files=[file_path],
        file_extractor={".pdf": parser}
    ).load_data()
    return documents

# PDF 파일 경로
pdf_file = "data/sample.pdf"

# 문서 파싱 및 인덱싱
documents = parse_pdf(pdf_file)
index = GPTVectorStoreIndex.from_documents(documents)

# 검색 및 생성
def pdf_rag(query):
    llm = OpenAI(api_key=openai_api_key, temperature=0)
    retrieved_docs = index.query(query)
    response = llm(retrieved_docs)
    print(response)

# 질문
query = "PDF 파일에서 2023년 AI 트렌드 요약"
pdf_rag(query)
