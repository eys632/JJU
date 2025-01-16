from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from itertools import chain
from langchain_core.prompts import PromptTemplate

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

with open(r"C:\Users\user\Desktop\2024년 2학기\2024비트특강\practice_2\Mail.txt", "r", encoding="cp949") as file:
    email_conversation = file.read()

print(email_conversation)

class EmailSummary(BaseModel):
    person: str = Field(description="The sender of the email")
    email: str = Field(description="The email address of the sender")
    subject: str = Field(description="The subject of the email")
    summary: str = Field(description="A summary of the email content")
    date: str = Field(description="The meeting date and time mentioned in the email content")
    recipient: str = Field(description="The recipient of the email")

parser = PydanticOutputParser(pydantic_object=EmailSummary)

prompt = PromptTemplate.from_template(
    '''
You are a helpful assistant.

QUESTION:
{question}

EMAIL CONVERSATION:
{email_conversation}

FORMAT:
{format}
''').partial(format=parser.get_format_instructions())

llm = ChatOpenAI(temperature=0, model_name="gpt-4o")

chain = prompt | llm | parser

response = chain.invoke({
    "email_conversation": email_conversation,
    "question": "이 이메일의 중요한 내용을 요약하세요."
})

print(response)