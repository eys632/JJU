import os

os.environ['OPENAI_API_KEY']=''

from langchain_teddynote.messages import stream_response #스트리밍 출력
from langchain_core.prompts import PromptTemplate

from langchain_core.prompts import PromptTemplate


from langchain_openai import ChatOpenAI

model = ChatOpenAI(
      model ="gpt-3.5-turbo",
      max_tokens=2048,
      temperature=0.1,
)

# template 정의
template = "{country1}과 {country2}의 수도는 각가 어디인가요?"

# Prompt Template 객체를 활용하여 prompt_template 생성
prompt = PromptTemplate(
    template=template,
    input_variables=["country1"],
    partial_variables={
        "country2":"미국"
    },
)

# prompt 생성
prompt.format(country1="대한민국")

prompt_partial = prompt.partial(country2="캐나다")

chain = prompt_partial | model

a = chain.invoke({"country1": "대한민국", "country2":"호주"}).content
print(a)