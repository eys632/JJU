import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessageChunk
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 파일 경로
file_path = '/workspaces/JJU-1/04-유상민/WEEK4/04_PYDENTIC/E-MAIL.txt'

# 파일 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    email_conversation = file.read()

# 이메일 요약용 데이터 모델
class EmailSummary(BaseModel):
    sender: str = Field(description="The sender of the email")
    recipient: str = Field(description="The recipient of the email")
    cc: str = Field(description="CC recipients")
    content: str = Field(description="The content of the email")
    is_spam: str = Field(description="Is the email spam or not")
    summary: str = Field(description="Summary of the email content")
    reply: str = Field(description="Generated reply to the email")

# Output Parser
parser = PydanticOutputParser(pydantic_object=EmailSummary)

# Prompt 템플릿
prompt = PromptTemplate.from_template(
    """
You are a helpful assistant.

QUESTION:
{question}

EMAIL CONVERSATION:
{email_conversation}

FORMAT:
{format}
"""
)
prompt = prompt.partial(format=parser.get_format_instructions())

# LLM 초기화
llm = ChatOpenAI(model='gpt-4o', temperature=0,openai_api_key=OPENAI_API_KEY)

# 체인 생성
chain = prompt | llm | parser

# 요약 및 회신 생성
response = chain.invoke({
    "email_conversation": email_conversation,
    "question": "Extract key information, summarize the email, and generate a reply.",
})

# 결과 출력
print("Extracted Information:")
print(response)

# 결과 저장
output_file = 'reply.md'
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(f"**Summary**:\n{response.summary}\n\n")
    file.write(f"**Reply**:\n{response.reply}\n")

print(f"Reply saved to {output_file}.")
