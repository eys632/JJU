from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


class Topic(BaseModel):
    description: str = Field(description="주제에 대한 간결한 설명")
    hashtags: str = Field(description="해시태그 형식의 키워드(2개 이상)")


# .env 파일 로드
load_dotenv()

# 환경 변수 불러오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

def Use_pydantic():
    model = ChatOpenAI(temperature=0, model_name="gpt-4o")
    parser = JsonOutputParser(pydantic_object=Topic)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "당신은 친절한 AI 어시스턴트 입니다. 질문에 간결하게 답변하세요."),
            ("user", "#Format: {format_instructions}\n\n#Question: {question}"),
        ]
    )

    prompt = prompt.partial(format_instructions=parser.get_format_instructions())
    chain = prompt | model | parser  
    question = "군대에 대해 자세히 알려줘"
    result =chain.invoke({"question": question}) 
    return result

def NotUse_pydantic():
    model = ChatOpenAI(temperature=0, model_name="gpt-4o")
    # 질의 작성
    question = "지구 온난화의 심각성 대해 알려주세요."
    # 파서를 설정하고 프롬프트 템플릿에 지시사항을 주입합니다.
    parser = JsonOutputParser()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "당신은 친절한 AI 어시스턴트 입니다. 질문에 간결하게 답변하세요."),
            ("user", "#Format: {format_instructions}\n\n#Question: {question}"),
        ]
    )
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())
    chain = prompt | model | parser  # 체인을 구성합니다.
    result = chain.invoke({"question": question})  # 체인을 호출하여 쿼리 실행
    return result

if __name__ == "__main__":
    # Pydantic을 사용하는 경우
    topic_result = Use_pydantic()
    print("Pydantic을 사용한 결과:")
    print(topic_result)
    
    # Pydantic을 사용하지 않는 경우
    non_pydantic_result = NotUse_pydantic()
    print("\nPydantic을 사용하지 않은 결과:")
    print(non_pydantic_result)