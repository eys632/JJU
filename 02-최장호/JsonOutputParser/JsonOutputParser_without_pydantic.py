from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import os

os.environ['OPENAI_API_KEY'] = '****'
os.environ['LANGCHAIN_API_KEY'] = '****'
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = '03-04'

model = ChatOpenAI(
    temperature=0,
    model = "gpt-4o"
)

# 질의
question = "UCL 18-19시즌 손흥민의 활약에 대해 알려주세요.  이 설명은 `description`에, 관련 키워드는 `hashtags`에 담아주세요."


# JSON 출력 파서 초기화
parser = JsonOutputParser()

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

print(response)