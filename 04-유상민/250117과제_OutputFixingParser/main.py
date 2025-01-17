from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers import OutputFixingParser
from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class Actor(BaseModel):
    name: str = Field(description="name of an actor")
    film_names: List[str] = Field(description="list of names of films they starred in")
    
actor_query = "Generate the filmography for a random actor."

parser = PydanticOutputParser(pydantic_object=Actor)

base_Actor = "{'name': 'Tom Hanks', 'film_names': ['Forest Gump']}"

new_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI(model = 'gpt-4o'))

final_Actor = new_parser.parse(base_Actor)

final_Actor