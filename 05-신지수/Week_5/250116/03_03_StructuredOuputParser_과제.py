import os

# 환경 변수 설정 (API 키 및 LangChain 설정)
os.environ["OPENAI_API_KEY"] = """OPENAI_API 키 입력"""
os.environ["LANGCHAIN_API_KEY"] = """LANGCHAIN_API 키 입력"""
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "LANGCHAIN_PROJECT 입력"

# 필수 라이브러리의 설치 코드
# pip install langchain langchain-core langchain-openai openai

from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 응답 스키마 정의 (사용자 질문에 대한 답변과 출처)
response_schemas = [
    ResponseSchema(name="answer", description="사용자의 질문에 대한 답변"),
    ResponseSchema(
        name="source",
        description="사용자의 질문에 답하기 위해 사용된 `출처`, `웹사이트주소` 이여야 합니다.",
    ),
]

# 구조화된 출력 파서를 초기화합니다.
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 출력 형식 지시사항을 가져옵니다.
format_instructions = output_parser.get_format_instructions()

# 프롬프트 템플릿 정의
prompt = PromptTemplate(
    template="""answer the users question as best as possible.
    {format_instructions}
    {question}""",
    input_variables=["question"],
    partial_variables={"format_instructions": format_instructions},
)

# 모델 초기화 (GPT-4o 사용, 온도 설정 0으로 고정)
model = ChatOpenAI(temperature=0, model='gpt-4o')

# 체인 생성: 프롬프트 -> 모델 -> 출력 파서
chain = prompt | model | output_parser

# 사용자 질문에 대한 체인 실행
response = chain.invoke({'question': '조선시대 양들을 순서대로 알려줘'})

# 결과 출력
print(response)