from dotenv import load_dotenv
import os
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 환경 변수 로드
load_dotenv()

# API 키 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT_ID = os.getenv("LANGCHAIN_PROJECT_ID")

# 콤마로 구분된 리스트 출력 파서 초기화
output_parser = CommaSeparatedListOutputParser()

# 출력 형식 지침 가져오기
format_instructions = output_parser.get_format_instructions()

# 프롬프트 템플릿 설정
prompt = PromptTemplate(
    template="List five {subject}.\n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions},
)

# ChatOpenAI 모델 초기화
model = ChatOpenAI(temperature=0)

# 주제에 대한 다섯 가지 항목 생성 함수
def generate_list(subject):
    # 프롬프트 템플릿에 주제 전달
    prompt_text = prompt.format(subject=subject)
    # 모델 실행
    response = model.invoke(prompt_text)
    # 결과를 문자열로 변환하여 출력 파서에 전달
    return output_parser.parse(response.content)

# 사용 예시
if __name__ == "__main__":
    subject = "한국 베스킨라빈스에서 가장 많이 팔리는 아이스크림림"  # 예: 유명 과학자
    try:
        result = generate_list(subject)
        print(f"Generated List for '{subject}': {result}")
    except Exception as e:
        print(f"An error occurred: {e}")
