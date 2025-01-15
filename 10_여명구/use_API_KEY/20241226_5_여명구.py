<<<<<<< HEAD
from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
=======
import os
from datetime import datetime
from langchain_core.prompts import PromptTemplate
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

# OpenAI API 키 설정
# 4o
# os.environ['OPENAI_API_KEY'] = ''
# # 3.5
os.environ['OPENAI_API_KEY'] = ''
>>>>>>> 4bfc78dda3c025a2a8419034bcdfb001c0766dea

# 날짜 함수 정의
def get_today():
    return datetime.now().strftime("%B %d")  # 날짜 포맷: YYYY-MM-DD

# 프롬프트 템플릿 정의
prompt = PromptTemplate(
    template=(
        "오늘의 날짜는 {today}입니다. "
        "오늘이 생일인 유명인 {n}명을 나열해 주세요. "
        "반드시 {today} 날짜와 일치하는 사람만 포함하세요."
        "생년월일을 함께 표기해 주세요."
    ),
    input_variables=["n"],  # 입력값
    partial_variables={"today": get_today}  # 날짜를 동적으로 삽입
)

# OpenAI 모델 초기화
model = ChatOpenAI(
    # model="gpt-4o",
    model="gpt-3.5-turbo",
    max_tokens=1024,
    temperature=0.7,
)

# 체인 생성 (사용자 방식)
chain = prompt | model

print(chain.invoke({"n": 4}).content)
# 실행 및 결과 출력
# response = chain.invoke({"n": 2})  # n 값 전달
# print("오늘이 생일인 유명인 리스트:")
# print(response.content)