from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

class EmailSummary(BaseModel):
    sender: str = Field(description="메일 발신자")
    recipient: str = Field(description="메일 수신자")
    subject: str = Field(description="메일 제목")
    summary: str = Field(description="메일 본문 요약")
    date: str = Field(description="메일 발송 날짜")

parser = PydanticOutputParser(pydantic_object=EmailSummary)

def summarize_email(email_data, api_key):
    """
    이메일 내용을 요약하고 JSON 형식으로 반환
    """
    prompt = PromptTemplate.from_template(
        """
        You are a helpful assistant. Extract the main points of the email below in KOREAN.

        EMAIL DETAILS:
        Sender: {sender}
        Recipient: {recipient}
        Subject: {subject}
        Date: {date}
        Body: {body}

        FORMAT:
        {format}
        """
    )
    prompt = prompt.partial(format=parser.get_format_instructions())

    llm = ChatOpenAI(temperature=0, model_name="gpt-4", api_key=api_key)
    chain = prompt | llm | parser

    response = chain.invoke({
        "sender": email_data["sender"],
        "recipient": email_data["recipient"],
        "subject": email_data["subject"],
        "date": email_data["date"],
        "body": email_data["body"]
    })
    return response.dict()
