from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# 환경 변수 로드
load_dotenv()

# API 키 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT_ID = os.getenv("LANGCHAIN_PROJECT_ID")

# OpenAI 모델 초기화
model = ChatOpenAI(temperature=0, model_name="gpt-4o")

# Pydantic 데이터 구조 정의
class Topic(BaseModel):
    description: str = Field(description="주제에 대한 간결한 설명")
    hashtags: str = Field(description="해시태그 형식의 키워드(2개 이상)")

# JSON 출력 파서 초기화
parser = JsonOutputParser(pydantic_object=Topic)

# 프롬프트 템플릿 설정
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 친절한 AI 어시스턴트입니다. 질문에 간결하게 답변하세요."),
        ("user", "주제에 대해 간략히 설명하고, 해시태그를 2개 이상 포함하세요.\n#Format: {format_instructions}")
    ]
)

# 주제에 대한 JSON 출력 생성 함수
def generate_topic(subject):
    # 프롬프트 생성
    prompt_text = prompt.format(subject=subject, format_instructions=parser.get_format_instructions())
    # 모델 실행
    response = model.invoke(prompt_text)
    # JSON 파싱 및 반환
    return parser.parse(response.content)

# 사용 예시
if __name__ == "__main__":
    subject = "AI의 미래"  # 예: AI의 미래
    try:
        result = generate_topic(subject)
        print(f"Generated JSON for '{subject}': {result}")
    except Exception as e:
        print(f"An error occurred: {e}")
