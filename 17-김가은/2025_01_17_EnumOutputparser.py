from langchain.output_parsers.enum import EnumOutputParser

from enum import Enum


class Colors(Enum):
    RED = "빨간색"
    GREEN = "초록색"
    BLUE = "파란색"
    YELLOW = "노란색"
    ORANGE = "주황색"
    PURPLE = "보라색"
    PINK = "분홍색"
    BROWN = "갈색"
    BLACK = "검정색"
    WHITE = "흰색"
    GRAY = "회색"
    CYAN = "청록색"
    MAGENTA = "자홍색"
    LIME = "라임색"
    INDIGO = "남색"
    VIOLET = "보랏빛"
    GOLD = "금색"
    SILVER = "은색"
    TEAL = "틸색"
    MAROON = "고동색"

parser = EnumOutputParser(enum=Colors)

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 프롬프트 템플릿을 생성합니다.
prompt = PromptTemplate.from_template(
    """다음의 물체는 어떤 색깔인가요?

Object: {object}

Instructions: {instructions}"""
    # 파서에서 지시사항 형식을 가져와 부분적으로 적용합니다.
).partial(instructions=parser.get_format_instructions())
# 프롬프트와 ChatOpenAI, 파서를 연결합니다.
chain = prompt | ChatOpenAI() | parser

from langchain_openai import ChatOpenAI

chain = prompt | ChatOpenAI(temperature=0, model="gpt-4o") | parser

response=chain.invoke({"object":"하늘"})

print(response)
