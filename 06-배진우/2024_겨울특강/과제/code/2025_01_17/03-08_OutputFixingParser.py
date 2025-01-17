from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경 변수 불러오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

# Pydantic 모델 정의
class Actor(BaseModel):
    name: str = Field(description="Name of an actor")
    film_names: List[str] = Field(description="List of names of films they starred in")


# 유효하지 않은 JSON 문자열
base_Actor = "{'name': 'Tom Hanks', 'film_names': ['Forrest Gump']}"

# PydanticOutputParser 설정
parser = PydanticOutputParser(pydantic_object=Actor)

# OutputFixingParser 설정
llm = ChatOpenAI(model="gpt-4o")
new_parser = OutputFixingParser.from_llm(
    parser=parser,
    llm=llm
)

# JSON 파싱 및 수정
try:
    actor = new_parser.parse(base_Actor)
    print(actor)
except Exception as e:
    print(f"Error: {e}")
