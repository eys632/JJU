from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os

# 오늘 날짜를 반환하는 함수 정의
def get_today():
    return datetime.now().strftime("%B %d")

# PromptTemplate 정의
prompt = PromptTemplate(
    template="오늘 날짜는 {today} 입니다. 오늘이 생일인 {n}명을 나열해 주세요. 생년월일을 표기해주세요",
    input_variables=["n"],
    partial_variables={
        "today": get_today  # dictionary 형태로 partial_variables 전달
    },
)

# OpenAI API 키 설정
os.environ["OPENAI_API_KEY"] = ""

# OpenAI 모델 설정
model = ChatOpenAI(
    model="gpt-4o",
    max_tokens=3000,
    temperature=0.1,
)

# 파이프라인 방식으로 연결 (LLMChain 대신)
chain = prompt | model

# 체인 실행
try:
    # 사용자 입력값: 출력할 유명인의 수 설정 (예: 5명)
    result = chain.invoke({"n": 5})  # 결과는 AIMessage 객체로 반환됨
    print(result.content)  # AIMessage 객체에서 content 속성에 접근
except Exception as e:
    print(f"오류 발생: {e}")
