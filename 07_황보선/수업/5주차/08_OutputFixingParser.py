import os
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

os.environ['OPENAI_API_KEY']=''
os.environ['LANGCHAIN_TRACING_V2']=''
os.environ['LANGCHAIN_ENDPOINT']=''
os.environ['LANGCHAIN_API_KEY']=''
os.environ['LANGCHAIN_PROJECT']=''

class Actor(BaseModel):
    name: str = Field(description="name of an actor")
    film_names: List[str] = Field(description="list of names of films they starred in")


actor_query = "Generate the filmography for a random actor."

parser = PydanticOutputParser(pydantic_object=Actor)

# 잘못된 형식을 일부러 입력
base_Actor = "{'name': 'Tom Hanks', 'film_names': ['Forrest Gump']}"

# 잘못된 형식으로 입력된 데이터를 파싱하려고 시도
parser.parse(base_Actor)

from langchain.output_parsers import OutputFixingParser

new_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI(model='gpt-4o'))

new_parser

final_actor = new_parser.parse(base_Actor)

print(final_actor)