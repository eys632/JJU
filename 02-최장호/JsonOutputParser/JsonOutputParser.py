from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import os

os.environ['OPENAI_API_KEY'] = '****'
os.environ['LANGCHAIN_API_KEY'] = '****'
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = '03-04'

model = ChatOpenAI(
    temperature=0,
    model = "gpt-4o"
)

class Topic(BaseModel):
  description: str = Field(description="주제에 대한 간결한 설명")
  hashtags: str = Field(description="해시태그 형식의 키워드(2개 이상)")

parser = JsonOutputParser(pydantic_object=Topic)

prompt = ChatPromptTemplate(
  [
    ("system","당신은 친절한 AI 어시스턴트 입니다. 질문에 간결하게 답변하세요."),
    ("user","#Format:{format_instructions}\n\n#Question:{question}")
  ]
)

prompt = prompt.partial(format_instructions=parser.get_format_instructions())

chain = prompt | model | parser

response = chain.invoke({"question":"한국인 EPL 득점왕 시즌 알려줘"})

print(response)