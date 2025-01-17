import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

from langchain.output_parsers.enum import EnumOutputParser
from enum import Enum

class Colors(Enum):
    # RED = "빨간색"
    GREEN = "초록색"
    BLUE = "파란색"
    BROWN = "갈색"
    YELLOW = "노란색"
    BLACK = "검은색"
    WHITE = "하얀색"

class CustomEnumOutputParser(EnumOutputParser):
    def parse(self, response: str):
        try:
            # EnumOutputParser의 기본 동작 호출
            return super().parse(response)
        except ValueError:
            # 기본 파싱 실패 시 예외 처리
            raise ValueError("비슷한 색깔이 없습니다. 주어진 옵션 중에서 선택할 수 없습니다.")
        
# EnumOutputParser 인스턴스 생성
# parser = EnumOutputParser(enum=Colors)

# 커스텀 파서 생성(예외처리 추가)
parser = CustomEnumOutputParser(enum=Colors)

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 프롬프트 템플릿을 생성합니다.
prompt = PromptTemplate.from_template(
    """
    다음의 물체는 어떤 색깔인가요?
    최대한 비슷한 색깔을 알려줘. : {options}

    Object: {object}

    Instructions: {instructions}
    """
    # 파서에서 지시사항 형식을 가져와 부분적으로 적용합니다.
    ).partial(
        instructions=parser.get_format_instructions(),
        options=", ".join([color.value for color in Colors])
              )

# 프롬프트와 ChatOpenAI, 파서를 연결합니다.
chain = prompt | ChatOpenAI(model="gpt-4o") | parser

# response = chain.invoke({"object": "장미"})  # "하늘" 에 대한 체인 호출 실행
# print(response)

try:
    # 체인 호출 및 결과 반환
    response = chain.invoke({"object": "장미"})  # 테스트 케이스
    print(response)
except ValueError as e:
    # 예외 발생 시 사용자에게 피드백
    print(str(e))