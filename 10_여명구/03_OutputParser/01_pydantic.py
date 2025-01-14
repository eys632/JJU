import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessageChunk
import json

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
    From : str = Field(description="메일을 보낸 사람의 이름")
    Sender_email: str = Field(description="메일을 보낸 사람의 이메일 주소")
    Deliver_email: str = Field(description="메일을 받은 사람의 이메일 주소")
    Subject: str = Field(description="메일 제목")
    content: str = Field(description="메일의 내용")
    Is_spam: str = Field(description="스팸 여부 ('스팸' 또는 'no spam')")

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
with open(r"10_여명구\03_OutputParser\E-MAIL.txt", "r", encoding="utf-8") as file:
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

# 회신 프롬프트 템플릿 정의
reply_prompt = PromptTemplate.from_template(
    """
    You are a helpful assistant. Please write a reply email in KOREAN based on the following summarized email content.

    SUMMARY:
    {summary}

    Please ensure the tone of the email is polite and professional.
    """
)

# 요약 내용 포함하여 프롬프트 생성
reply_chain = reply_prompt | llm

# 체인 실행 및 회신 이메일 생성
reply_email = reply_chain.invoke(
    {
        "summary": response
    }
)

# 회신 이메일을 JSON 형식에 맞게 매핑
reply_email_content = {
    "To": response.Deliver_email if hasattr(response, 'Deliver_email') else "",
    "From": response.Sender_email if hasattr(response, 'Sender_email') else "",
    "Subject": f"RE: {response.Subject}" if hasattr(response, 'Subject') else "",
    "Body": reply_email.content if hasattr(reply_email, 'content') else str(reply_email)
}

# 같은 폴더 내에 JSON 파일로 저장
output_path = r"10_여명구\03_OutputParser\Reply_structured.json"
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(reply_email_content, json_file, ensure_ascii=False, indent=4)

# 회신 이메일 출력
print("\n[회신 이메일]")
print(reply_email_content)
