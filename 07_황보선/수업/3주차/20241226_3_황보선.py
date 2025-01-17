import os
from langchain_teddynote.messages import stream_response  # 스트리밍 출력
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# OpenAI API 키 설정
os.environ['OPENAI_API_KEY'] = 'path/to/your/openai/api/key'

# pip install langchain_teddynote langchain_core

# ChatOpenAI 모델 설정
model = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    max_tokens=2048,
    temperature=0.1,
)

# 템플릿 정의
template = '{country}의 수도는 어디인가요'

# PromptTemplate 객체 생성
prompt_template = PromptTemplate.from_template(template)
print(prompt_template)

# prompt 생성
prompt = prompt_template.format(country='대한민국')

# Chain 생성
chain = prompt_template | model

# 입력 데이터
input_data = {'country': '일본'}

# Chain 실행 및 결과 저장
response = chain.invoke(input_data)

# 결과 출력
print(response.content)
