from langchain_teddynote.messages import stream_response # 스트리밍 출력
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

os.environ['OPENAI_API_KEY']='path/to/your/openai/api/key'

model = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    max_tokens=2048,
    temperature=0.1,
)

# template 정의
template = '{country1}과 {country2}의 수도는 어디인가요?'

# PromptTemplate 객체를 활용하여 prompt_template 생성
prompt = PromptTemplate(
    template=template,
    input_variables=['country1'],
    partial_variables={
        'country2': '미국', # dictionary 형태로 partial_variables를 전달
    }
)

prompt.format(country1='대한민국')

prompt_partial = prompt.partial(country2='캐나다')



# 객체 생성
chain = prompt | model

print(chain.invoke({'country1':'대한민국', 'country2':'호주'}).content)