from langchain_upstage import UpstageLayoutAnalysisLoader
import os

# 파일 경로
file_path = "C:/Python_workspace/bit/sub/data_all/분류시스템의 분류 규칙 발견을 위한 유전자 알고리즘.pdf"

os.environ["UPSTAGE_API_KEY"] = 'up_FKv3fStbT3fKdLbUBTduTfBxThViC'

# -------------------------------------------------------------------
# 문서 로더 설정
loader = UpstageLayoutAnalysisLoader(
    file_path,
    output_type="text",
    split="page",
    use_ocr=True,
    exclude=["header", "footer"],
)

# 문서 로드
docs = loader.load()

# 결과 출력
# for doc in docs[:3]:
    # print(doc)

# -------------------------------------------------------------------
# 문서 로더 설정
loader = UpstageLayoutAnalysisLoader(
    file_path,
    output_type="text",
    split="element",
    use_ocr=True,
    exclude=["header", "footer"],
)

# 문서 로드
docs = loader.load()

# 결과 출력
for doc in docs[:3]:
    print(doc)