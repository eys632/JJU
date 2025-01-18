import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain_openai import ChatOpenAI
from typing import List
import json

# 환경 변수 로드
load_dotenv()

# Pydantic 모델 정의
class Actor(BaseModel):
    name: str = Field(description="name of an actor")
    film_names: List[str] = Field(description="list of names of films they starred in")

# PydanticOutputParser 설정
parser = PydanticOutputParser(pydantic_object=Actor)

# LLM 설정 (OutputFixingParser에 사용)
llm = ChatOpenAI(model="gpt-4o")  # GPT-4 모델 사용
fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

# 데이터 처리 함수 정의
def parse_actor_data(data: str):
    try:
        # 입력 데이터를 JSON으로 변환
        json_data = json.loads(data)
        # 올바른 JSON 형식인지 검증하고 Pydantic 모델로 변환
        parsed_actor = parser.parse(json.dumps(json_data))
        print("Parsed Actor (Valid Input):")
        return parsed_actor
    except (ValidationError, json.JSONDecodeError):
        # 잘못된 형식일 경우 OutputFixingParser 사용
        print("Invalid input format detected. Attempting to fix...")
        try:
            fixed_actor = fixing_parser.parse(data)
            print("Parsed Actor (Fixed Input):")
            return fixed_actor
        except Exception as e:
            print(f"Failed to parse input: {e}")
            return None

# 테스트 데이터
valid_input = '{"name": "Tom Hanks", "film_names": ["Forrest Gump"]}'
invalid_input = "{'name': 'Tom Hanks', 'film_names': ['Forrest Gump']}"

# 테스트 실행
print("# 올바른 입력")
print(parse_actor_data(valid_input))

print("# 잘못된 입력")
print(parse_actor_data(invalid_input))
