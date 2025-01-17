

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessageChunk

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LangChain 설정
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

# OpenAI LLM 초기화
llm = ChatOpenAI(temperature=0, model_name="gpt-4o", api_key=OPENAI_API_KEY)

# 실시간 스트리밍 응답 처리 함수
def stream_response(response, return_output=False):
    """
    AI 모델의 응답을 스트리밍 방식으로 처리하고 출력.
    
    Args:
        response (iterable): AI 모델의 응답 청크.
        return_output (bool, optional): True일 경우 전체 응답을 문자열로 반환.

    Returns:
        str: 전체 응답 문자열 (옵션).
    """
    answer = ""
    for token in response:
        if isinstance(token, AIMessageChunk):
            answer += token.content
            print(token.content, end="", flush=True)
        elif isinstance(token, str):
            answer += token
            print(token, end="", flush=True)
    if return_output:
        return answer

# Pydantic 데이터 모델 정의
class EmailSummary(BaseModel):
    person: str = Field(description="메일을 보낸 사람")
    email: str = Field(description="메일을 보낸 사람의 이메일 주소")
    subject: str = Field(description="메일 제목")
    summary: str = Field(description="메일 본문을 요약한 텍스트")
    Is_Spam: str = Field(description="Is the email or not, 만약 스팸이면 '스팸', 아니면 'no spam'이라고 입력해.")
    date: str = Field(description="메일 본문에 언급된 미팅 날짜와 시간")

# PydanticOutputParser 생성
parser = PydanticOutputParser(pydantic_object=EmailSummary)

# 프롬프트 템플릿 정의
prompt = PromptTemplate.from_template(
    """
    You are a helpful assistant. Please answer the following questions in KOREAN.

    QUESTION:
    {question}

    EMAIL CONVERSATION:
    {email_conversation}

    FORMAT:
    {format}
    """
)

# 템플릿에 출력 형식 포함
prompt = prompt.partial(format=parser.get_format_instructions())

# 이메일 내용 불러오기
email_path = r"C:\Users\PC\전주대학교_인공지능학과\실무인재(겨율특강)\SUB\DATA_ALL\E-MAIL.TXT"

with open(email_path, "r", encoding="utf-8") as file:
    email_conversation = file.read()


# LangChain 파이프라인 생성
chain = prompt | llm | parser

# 체인 실행 및 결과 출력
response = chain.invoke(
    {
        "email_conversation": email_conversation,
        "question": "이메일 내용중 주요 내용을 요약해줘.",
    }
)

# 결과 출력
print("\n[요약 결과]")
print(response)
print("\n")

# 결과를 MD 파일로 저장하는 코드

# MD 파일 저장 경로와 이름 설정
output_dir = r"C:\Users\PC\전주대학교_인공지능학과\실무인재(겨율특강)"
output_path = os.path.join(output_dir, "REPLY.md")

# 디렉토리 생성 (존재하지 않으면 생성)
os.makedirs(output_dir, exist_ok=True)

# MD 파일로 저장
md_content = f"""
# 이메일 요약 결과

## 보낸 사람
- **이름**: {response.person}
- **이메일**: {response.email}

## 이메일 정보
- **제목**: {response.subject}
- **요약**: {response.summary}
- **스팸 여부**: {response.Is_Spam}
- **날짜**: {response.date}
"""

# 파일 생성 및 저장
with open(output_path, "w", encoding="utf-8") as md_file:
    md_file.write(md_content)
