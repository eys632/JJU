<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> 4bfc78dda3c025a2a8419034bcdfb001c0766dea
import os

os.environ["OPENAI_API_KEY"] = ""

os.environ["UPSTAGE_API_KEY"] = ""

os.environ["LANGCHAIN_API_KEY"] = ""
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "test_JJU_YEOMYEONGGU"


<<<<<<< HEAD
>>>>>>> 4bfc78dda3c025a2a8419034bcdfb001c0766dea
=======
>>>>>>> 4bfc78dda3c025a2a8419034bcdfb001c0766dea
# pip install -q langchain_upstage
from langchain_upstage import UpstageLayoutAnalysisLoader

# 파일 경로
file_path = "비디오 트랜스포머 연구 동향.pdf"

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
for doc in docs[:3]:
    print(doc)
    print("=" * 50)
