from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None, # 보통 2000개 정도가 적당함
    timeout=None,
    max_retries=2,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

prompt = '비트코인?'

result = llm.invoke('광화문의 주소는?')
result