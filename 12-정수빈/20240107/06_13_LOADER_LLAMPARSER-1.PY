import os
import subprocess
import nest_asyncio
from dotenv import load_dotenv

# 필요한 패키지 설치
required_packages = [
    "nest_asyncio",
    "llama-index-core",
    "llama-parse",
    "llama-index-readers-file",
    "python-dotenv",
    "langchain_community",
    "langchain-teddynote",
    "langchain-upstage",
]

for package in required_packages:
    subprocess.run(["pip", "install", package], check=True)

# 환경 변수 로드
load_dotenv()

# API 키 설정
LLAMA_CLOUD_API_KEY = 'llx-X6UdtzuQtj8K6TJrPkDBG1Y7fdXkllC8nKBoePRFUmMQrQvv'
UPSTAGE_API_KEY = "up_AN4XzqiBeoH6zJxdJf6fHLixWrEre"
OPENAI_API_KEY = "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"

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "test_jju_jeongsubin"

# LLAMAPARSER 설정
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

nest_asyncio.apply()

parser = LlamaParse(
    api_key=LLAMA_CLOUD_API_KEY,
    result_type="markdown",
    num_workers=8,
    verbose=True,
    language="ko",
)

# 파일 경로 설정
file_path = "SPRI_AI_Brief_2023년12월호_F.pdf"

# SimpleDirectoryReader를 사용하여 파일 파싱
file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader(
    input_files=[file_path],
    file_extractor=file_extractor,
).load_data()

# LLAMAPARSER 결과 변환 및 출력
docs_llama = [doc.to_langchain_format() for doc in documents]

print("=== LLAMAPARSER OUTPUT ===")
for doc in docs_llama[:3]:
    print(doc.metadata, doc.page_content)

# UPSTAGE 설정
from langchain_upstage import UpstageLayoutAnalysisLoader

loader = UpstageLayoutAnalysisLoader(
    file_path,
    output_type="text",
    split="page",
    use_ocr=True,
    exclude=["header", "footer"],
    api_key=UPSTAGE_API_KEY,
)

# UPSTAGE 결과 로드 및 출력
docs_upstage = loader.load()

print("=== UPSTAGE OUTPUT ===")
for doc in docs_upstage[:3]:
    print(doc)

# 결과 비교
print("=== RESULTS COMPARISON ===")
for idx, (doc_llama, doc_upstage) in enumerate(zip(docs_llama, docs_upstage)):
    print(f"Page {idx + 1} Comparison:")
    print(f"LLAMAPARSER: {doc_llama.page_content[:200]}...")
    print(f"UPSTAGE: {doc_upstage.page_content[:200]}...")