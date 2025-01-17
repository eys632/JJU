import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

# OpenAI 객체를 생성합니다.
model = ChatOpenAI(temperature=0, model_name="gpt-4o")

# 질의 작성
question = "현재 인공지능 시장에 대해 날짜와 함께 알려줘. 관련 설명은 'description', 관련 키워드는 'hashtags'에 담아줘."

# JSON 출력 파서 초기화
parser = JsonOutputParser()

# 프롬프트 템플릿을 설정합니다.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 친절한 AI 어시스턴트 입니다. 질문에 간결하게 답변하세요."),
        ("user", "#Format: {format_instructions}\n\n#Question: {question}"),
    ]
)

# 지시사항을 프롬프트에 주입합니다.
prompt = prompt.partial(format_instructions=parser.get_format_instructions())

# 프롬프트, 모델, 파서를 연결하는 체인 생성
chain = prompt | model | parser

# 체인을 호출하여 쿼리 실행
response = chain.invoke({"question": question})

# 출력을 확인합니다.
print(response)
