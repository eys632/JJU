import os

os.environ['OPENAI_API_KEY']=''

from langchain_teddynote.messages import stream_response #스트리밍 출력
from langchain_core.prompts import PromptTemplate

# template 정의
template = "{country}의 수도는 어디인가요?"

# form_template 메소드를 이용하여 PromptTemplate 객체 생성
prompt_template = PromptTemplate.from_template(template)

# prompt 생성
prompt = prompt_template.format(country="대한민국")

from langchain_openai import ChatOpenAI

model = ChatOpenAI(
      model ="gpt-3.5-turbo",
      max_tokens=2048,
      temperature=0.1,
)

prompt = prompt_template.from_template("{topic} 에 대해 쉽게 설명해주세요.")

model = ChatOpenAI()

chain = prompt | model

input = {"topic":"인공지능 모델의 학습 원리"}

a = chain.invoke(input)

print(a)