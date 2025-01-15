import os

os.environ["OPENAI_API_KEY"] = ""

os.environ["UPSTAGE_API_KEY"] = ""

# 환경 초기화 및 필요한 라이브러리 임포트
from langchain_upstage import UpstageLayoutAnalysisLoader

# 파일 경로 재설정
file_path = "비디오 트랜스포머 연구 동향.pdf"

# split="page"로 설정
loader_page = UpstageLayoutAnalysisLoader(
    file_path,
    output_type="text",
    split="page",  # 페이지 단위로 분할
    use_ocr=True,
    exclude=["header", "footer"]
)
docs_page = loader_page.load()

# split="element"로 설정
loader_element = UpstageLayoutAnalysisLoader(
    file_path,
    output_type="text",
    split="element",  # 요소 단위로 분할
    use_ocr=True,
    exclude=["header", "footer"]
)
docs_element = loader_element.load()

# 결과 비교 출력
print("=== 결과: split='page' ===")
for i, doc in enumerate(docs_page[:3]):
    print(f"문서 {i + 1}:\n{doc}\n{'=' * 50}")

print("\n=== 결과: split='element' ===")
for i, doc in enumerate(docs_element[:3]):
    print(f"문서 {i + 1}:\n{doc}\n{'=' * 50}")