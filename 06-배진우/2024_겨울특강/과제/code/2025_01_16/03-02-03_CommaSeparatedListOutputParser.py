from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
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

output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()
prompt = PromptTemplate(
    template="List five {subject}.\n{format_instructions}",
    input_variables=["subject"], 
    partial_variables={"format_instructions": format_instructions},
)
model = ChatOpenAI(temperature=0)

chain = prompt | model | output_parser
response = chain.invoke({"subject": "한국인이 좋아하는 아이스크림 5종류"})
print(response)
