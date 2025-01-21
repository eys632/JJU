# -*- coding: utf-8 -*-
"""LangChain Example"""

import os
from langchain_teddynote.messages import stream_response
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# OpenAI API 키 설정
api_key = ''
os.environ['OPENAI_API_KEY'] = api_key

# ChatOpenAI 모델 초기화
model = ChatOpenAI(
    model='gpt-3.5-turbo',
    max_tokens=2048,
    temperature=0.1,
)

# 방법 1
print("**방법 1 실행 결과**")
template = "{country}의 수도는 어디인가요?"
prompt = PromptTemplate.from_template(template)
formatted_prompt = prompt.format(country="대한민국")
print("프롬프트:", formatted_prompt)

# 새 프롬프트 생성
prompt = PromptTemplate.from_template("(topic)에 대해 쉽게 설명해주세요.")
chain = prompt | model
input_data = {"topic": "인공지능 모델의 학습 원리"}
response = chain.invoke(input_data).content
print("응답:", response)

# 방법 2
print("\n**방법 2 실행 결과**")
template = "{country1}과 {country2}의 수도는 각각 어디인가요?"
prompt = PromptTemplate(
    template=template,
    input_variables=["country1"],
    partial_variables={"country2": "미국"},
)
formatted_prompt = prompt.format(country1="대한민국")
print("프롬프트:", formatted_prompt)

# Partial Prompt 생성
prompt_partial = prompt.partial(country2="캐나다")
print("Partial Prompt:", prompt_partial.template)

chain = prompt_partial | model
response = chain.invoke({"country1": "대한민국"}).content
print("응답:", response)
