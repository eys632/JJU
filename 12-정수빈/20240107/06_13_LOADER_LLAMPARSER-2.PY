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
    "langchain-upstage",
]

for package in required_packages:
    subprocess.run(["pip", "install", package], check=True)

# 환경 변수 로드
load_dotenv()

# API 키 설정
LLAMA_CLOUD_API_KEY = 'llx-X6UdtzuQtj8K6TJrPkDBG1Y7fdXkllC8nKBoePRFUmMQrQvv'
UPSTAGE_API_KEY = "up_AN4XzqiBeoH6zJxdJf6fHLixWrEre"

nest_asyncio.apply()

# 파일 경로
file_path = "SPRI_AI_Brief_2023년12월호_F.pdf"

# LLAMAPARSER 설정
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

parser = LlamaParse(
    api_key=LLAMA_CLOUD_API_KEY,
    result_type="markdown",
    num_workers=8,
    verbose=True,
    language="ko",
)

# LLAMAPARSER 파싱
file_extractor = {".pdf": parser}
documents_llama = SimpleDirectoryReader(
    input_files=[file_path],
    file_extractor=file_extractor,
).load_data()

# LLAMAPARSER 결과 저장
docs_llama_page = [doc.to_langchain_format() for doc in documents_llama]

# UPSTAGE 설정
from langchain_upstage import UpstageLayoutAnalysisLoader

# 페이지 단위로 UPSTAGE 파싱
loader_page = UpstageLayoutAnalysisLoader(
    file_path,
    output_type="text",
    split="page",
    use_ocr=True,
    exclude=["header", "footer"],
    api_key=UPSTAGE_API_KEY,
)

# 요소 단위로 UPSTAGE 파싱
loader_element = UpstageLayoutAnalysisLoader(
    file_path,
    output_type="text",
    split="element",
    use_ocr=True,
    exclude=["header", "footer"],
    api_key=UPSTAGE_API_KEY,
)

# UPSTAGE 결과 저장
docs_upstage_page = loader_page.load()
docs_upstage_element = loader_element.load()

# 결과 비교 및 저장
comparison_results = []
for idx, (llama_doc, upstage_page_doc) in enumerate(zip(docs_llama_page, docs_upstage_page)):
    comparison = {
        "page": idx + 1,
        "llama_content": llama_doc.page_content[:500],  # 500자까지 미리보기
        "upstage_page_content": upstage_page_doc.page_content[:500],
    }
    comparison_results.append(comparison)

for idx, upstage_element_doc in enumerate(docs_upstage_element[:10]):  # 최대 10개 요소 출력
    comparison = {
        "element": idx + 1,
        "upstage_element_content": upstage_element_doc.page_content[:500],
    }
    comparison_results.append(comparison)

# 출력 결과 저장
output_file = "comparison_results.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for result in comparison_results:
        if "page" in result:
            f.write(f"Page {result['page']}\n")
            f.write(f"LLAMAPARSER Content:\n{result['llama_content']}\n\n")
            f.write(f"UPSTAGE Page Content:\n{result['upstage_page_content']}\n\n")
        elif "element" in result:
            f.write(f"Element {result['element']}\n")
            f.write(f"UPSTAGE Element Content:\n{result['upstage_element_content']}\n\n")

print(f"Comparison results saved to {output_file}")