import datetime
from langchain.output_parsers import DatetimeOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT_ID = os.getenv("LANGCHAIN_PROJECT_ID")

# 날짜 및 시간 출력 파서
output_parser = DatetimeOutputParser()
output_parser.format = "%Y-%m-%d"

# 사용자 질문에 대한 답변 템플릿
template = """Answer the users question:\n\n#Format Instructions: \n{format_instructions}\n\n#Question: \n{question}\n\n#Answer:"""

prompt = PromptTemplate.from_template(
    template,
    partial_variables={
        "format_instructions": output_parser.get_format_instructions()
    },  # 지침을 템플릿에 적용
)

llm = ChatOpenAI(temperature=0)
# Chain 생성
chain = prompt | ChatOpenAI() | output_parser

response = chain.invoke({"question": "What is the date today?"})

print(response.strftime("%Y-%m-%d"))