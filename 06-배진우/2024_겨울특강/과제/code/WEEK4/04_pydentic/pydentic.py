import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessageChunk

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

class EmailSummary(BaseModel):
    person: str = Field(description="The sender of the email")
    email: str = Field(description="The email address of the sender")
    subject: str = Field(description="The subject of the email")
    summary: str = Field(description="A summary of the email content")
    date: str = Field(description="The meeting date and mentioned in the email content")

def Chat_llm():
    return ChatOpenAI(temperature=0, model_name="gpt-4o")

def email_read():
    with open(
        "06-배진우/2024_겨울특강/과제/WEEK4/04_pydentic/e-mail.txt",
        "r",
        encoding="utf-8"
    ) as f:
        email_conversation = f.read()
    return email_conversation

def stream_response(response, return_output=False) -> str:
    """
    Streams the response from the AI model, processing and printing each chunk.
    Optionally returns the concatenated text.
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

########################################################
# 체인에 연결하지 않고 단순 사용하는 예시 함수
########################################################

def NotUesOutputOarser():
    """체인 없이 단순 PromptTemplate + LLM 사용"""
    email_conversation = email_read()

    prompt = PromptTemplate.from_template(
        """
        Please extract the important parts of the following email.
        
        {email_conversation}
        """
    )

    llm = Chat_llm()
    chain_obj = prompt | llm
    answer = chain_obj.stream({"email_conversation": email_conversation})
    output = stream_response(answer, return_output=True)
    return output

########################################################
# 체인에 연결할 PromptTemplate & Parser 정의 함수
########################################################

def UseOutPutParser():
    """PydanticOutputParser를 반환"""
    parser = PydanticOutputParser(pydantic_object=EmailSummary)
    return parser

def build_prompt_chain():
    """
    체인에 연결할 PromptTemplate을 정의하고,
    parser.get_format_instructions()만 partial 적용 후 반환
    """
    parser = UseOutPutParser()
    prompt_template = PromptTemplate.from_template(
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
    # parser의 지시사항을 `format`에 partial 적용
    prompt_template = prompt_template.partial(format=parser.get_format_instructions())
    return prompt_template

########################################################
# 체인으로 묶는 예시: prompt_template | llm | parser
########################################################

def with_parser():
    """체인( Runnable ) 형식으로 prompt_template, llm, parser 연결해 사용"""
    llm = Chat_llm()
    parser = UseOutPutParser()
    prompt_template = build_prompt_chain()

    chain_obj = prompt_template | llm | parser
    email_conversation = email_read()

    # chain_obj.invoke() 에는 dict로 입력을 넣어야 함
    response = chain_obj.invoke(
        {
            "email_conversation": email_conversation,
            "question": "Extract the main content of the email.",
        }
    )
    return response

########################################################
# 실제 실행 (Reply.json 저장)
########################################################

if __name__ == "__main__":
    # 1) Output Parser 미사용 결과
    not_use_output_parser_result = NotUesOutputOarser()
    
    # 2) 체인으로 Pydantic parser 결과 받기
    with_parser_result = with_parser()  # Pydantic 모델 인스턴스

    # JSON에 저장할 내용 구성
    data_to_save = {
        "NotUseOutputParser": not_use_output_parser_result,
        "WithParserResult": with_parser_result.dict(),
    }

    # Reply.json 에 결과 저장
    import json
    with open("06-배진우/2024_겨울특강/과제/WEEK4/04_pydentic/Reply.json", "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)
    
    print("\n\n[INFO] Reply.json 저장 완료.")
