<<<<<<< HEAD
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

=======
import os
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_teddynote.messages import stream_response # 스트리밍 출력

# OpenAI API 키 설정
os.environ['OPENAI_API_KEY'] = ''
>>>>>>> 4bfc78dda3c025a2a8419034bcdfb001c0766dea
# 템플릿 정의
template = "{country1}과 {country2}의 수도는 각각 어디인가요?"

# 프롬프트 템플릿 생성
prompt = PromptTemplate(
    template=template,
    input_variables=["country1"],
    partial_variables={"country2": "미국"}  # 기본값으로 설정된 country2
)

# OpenAI 모델 초기화
model = ChatOpenAI(
<<<<<<< HEAD
    model="gpt-4o",
    max_tokens=2048,
    temperature=0.1,
    api_key=OPENAI_API_KEY,
=======
    model="gpt-3.5-turbo",
    max_tokens=2048,
    temperature=0.1,
>>>>>>> 4bfc78dda3c025a2a8419034bcdfb001c0766dea
)

# 프롬프트 채우기 (country1만 동적으로 설정)
prompt_partial = prompt.partial(country2="미국")

# chain 생성
chain =prompt_partial | model

# 실행 및 결과 출력
# response = chain.invoke({"country1": "대한민국"})
# print(response.content)
print(chain.invoke({"country1": "대한민국", "country2": "일본", "country" : "미국"}).content)