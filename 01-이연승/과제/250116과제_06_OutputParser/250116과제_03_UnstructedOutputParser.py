from dotenv import load_dotenv
import os
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 환경 변수 로드
load_dotenv()

# API 키 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT_ID = os.getenv("LANGCHAIN_PROJECT_ID")

def main():
    # 응답 스키마 설정
    response_schemas = [
        ResponseSchema(name="answer", description="사용자의 질문에 대한 답변"),
        ResponseSchema(
            name="source",
            description="사용자의 질문에 답하기 위해 사용된 '출처', '웹사이트' 이어야 합니다.",
        ),
    ]
    # 구조화된 출력 파서 초기화
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    
    # 출력 형식 지시사항
    format_instructions = output_parser.get_format_instructions()
    prompt = PromptTemplate(
        template="answer the users question as best as possible.\n{format_instructions}\n{question}",
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions},
    )
    
    # 모델 초기화 및 체인 연결
    model = ChatOpenAI(temperature=0, model='gpt-4o')  # ChatOpenAI 모델 초기화
    chain = prompt | model | output_parser  # 프롬프트, 모델, 출력 파서를 연결

    # 질문에 답변 실행
    question = "조선 왕들 순서 알려줘"
    response = chain.invoke({"question": question})
    
    # 결과 출력
    print(response)

if __name__ == "__main__":
    main()
