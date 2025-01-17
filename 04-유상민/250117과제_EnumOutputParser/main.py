from langchain.output_parsers.enum import EnumOutputParser
from enum import Enum
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


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
    NAVY = "남색"
    MAROON = "적갈색"
    OLIVE = "올리브색"
    TEAL = "틸색"
    INDIGO = "남보라색"
    GOLD = "금색"
    BEIGE = "베이지색"  
    CHARCOAL = "차콜색"  

parser = EnumOutputParser(enum=Colors)



prompt = PromptTemplate.from_template(
    """ 다음의 물체는 어떤 색깔인가요?
    Object: {object}

    instructions: {instructions}

    출력은 무조건 색깔 하나를 골라서 출력해야 합니다.

    """
).partial(instructions=parser.get_format_instructions())


llm = ChatOpenAI(temperature=0, model_name="gpt-4o")

chain= prompt | llm | parser

response = chain.invoke({"object": "책상"})

print(response)
