import os
<<<<<<< HEAD
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

=======

# API 키 가져오기
os.environ['OPENAI_API_KEY'] = ''
>>>>>>> 4bfc78dda3c025a2a8419034bcdfb001c0766dea
from langchain_teddynote.messages import stream_response
from langchain_core.prompts import PromptTemplate

# template 정의
template = '{country}의 수도는 어디인가요?'

# from_template 메소드를 이용하여 prompt template 객체 생성
prompt_template = PromptTemplate.from_template(template)
# print(prompt_template)

# 새로운 프롬프트 객체 생성
# 다목적 사용 가능
# prompt = prompt_template.format(country= '대한민국')

# 프롬프트 생성할때 기존 rule에 맞게
# 기존에 정의된 템플릿(PromptTemplate)에서 값을 채워 생성
prompt = PromptTemplate.from_template("{topic}의 수도는 어디인가요?")
# print(prompt)

from langchain_openai import ChatOpenAI

# OpenAI 모델 초기화
model = ChatOpenAI(
<<<<<<< HEAD
    model='gpt-4o',
    max_tokens=2048,
    temperature=0.1,
    api_key=OPENAI_API_KEY,
=======
    model='gpt-3.5-turbo',
    max_tokens=2048,
    temperature=0.1,
>>>>>>> 4bfc78dda3c025a2a8419034bcdfb001c0766dea
)

chain = prompt | model
# print(prompt)

input={'topic': '미국'}
# print(input)

output = chain.invoke(input)
# print(output)


# 국가 리스트
countries = ["대한민국", "일본", "미국", "프랑스", "독일"]

# 각 국가에 대해 프롬프트 생성 및 결과 출력
for country in countries:
    # 프롬프트 생성
    filled_prompt = prompt.format(topic=country)
    
    # 모델 실행
    response = model.invoke(filled_prompt)
    
    # for chunk in stream_response(filled_prompt, model):
        # print(chunk, end="")
    # 결과 출력
    # print('\n')
    # content만 출력
    print(f"**{country}**:\n{response.content}\n")
    # 한줄씩만 출력
    # print(f"**{country}**:\n{response.content.split('.')[0].strip()}\n")