# main.py

import os
from dotenv import load_dotenv
from langchain.output_parsers import EnumOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI  # 최신 패키지에서 임포트
from colors import Colors  # colors.py에서 Colors 임포트
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# .env 파일 로드
load_dotenv()

# 환경 변수 불러오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Environment variable OPENAI_API_KEY is not set.")

# EnumOutputParser 초기화
parser = EnumOutputParser(enum=Colors)

# 사용 가능한 색상 목록 생성
colors_list = ", ".join([color.value for color in Colors])

# PromptTemplate 정의 (동적 질문을 위해 {object}와 {colors_list} 사용)
prompt = PromptTemplate.from_template(
    """
질문에 답할 때는 반드시 다음 색상 중 하나만 선택해서 대답해주세요.
{colors_list}
답변은 단어로 해주세요. (예: 파란색)
질문: {object}의 색깔은 무엇인가요?
답변:
    """
).partial(instructions=parser.get_format_instructions())

# ChatOpenAI 초기화
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4o",
    openai_api_key=OPENAI_API_KEY
)

# 체인 구성
chain = prompt | llm | parser

# 체인 호출 예시
def ask_color(object_name: str):
    try:
        response = chain.invoke({"object": object_name, "colors_list": colors_list})
        logger.info(f"Response for '{object_name}': {response}")
        return response.value  # Enum 멤버의 값을 반환
    except Exception as e:
        logger.error(f"Error occurred while processing '{object_name}': {e}")
        return None

if __name__ == "__main__":
    objects = ["하늘", "사과", "더불어민주당"]
    for obj in objects:
        color = ask_color(obj)
        print(f"{obj}의 색깔: {color}")