import os

UPSTAGE_API_KEY = os.environ['UPSTAGE_API_KEY']
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
LANGCHAIN_API_KEY = os.environ["LANGCHAIN_API_KEY"]
LANGCHAIN_TRACING_V2 = os.environ['LANGCHAIN_TRACING_V2']
LANGCHAIN_ENDPOINT = os.environ['LANGCHAIN_ENDPOINT']
LANGCHAIN_PROJECT = os.environ['LANGCHAIN_PROJECT']

from langchain_teddynote import logging

# 프로젝트 이름을 입력합니다.
logging.langsmith("Test_JJU_JosephCho")

from langchain_upstage import UpstageLayoutAnalysisLoader

# 파일 경로
file_path = "data\Don't Do RAG.pdf"

# 문서 로더 설정
loader = UpstageLayoutAnalysisLoader(
    file_path,
    output_type="text", # "text"과 "HTML" 사용 가능
    split="element",
    use_ocr=True,
    exclude=["header", "footer"],
    api_key=os.environ.get("UPSTAGE_API_KEY"),
)

# 문서 로드
docs = loader.load()

# 결과 출력
print(len(docs))
print(docs[0].metadata)
print(docs[0].page_content)
