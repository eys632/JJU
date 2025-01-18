import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

from langchain.output_parsers import DatetimeOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 날짜 및 시간 출력 파서
output_parser = DatetimeOutputParser()
output_parser.format = "%Y-%m-%d-%H:%M:%S"

# 사용자 질문에 대한 답변 템플릿
template = """
Answer the users question:

#Format Instructions: 
{format_instructions}

#Question: 
{question}

#Answer:
"""

prompt = PromptTemplate.from_template(
    template,
    partial_variables={
        "format_instructions": output_parser.get_format_instructions()
    },  # 지침을 템플릿에 적용
)

model = ChatOpenAI(model='gpt-4o')

chain = prompt | model | output_parser

# 체인을 호출하여 질문에 대한 답변을 받습니다.
response = chain.invoke({"question": "현재 시각 알려줘."})

print(response)