import pprint
from typing import Any, Dict
import pandas as pd
from langchain.output_parsers import PandasDataFrameOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ChatOpenAI 모델 초기화(gpt-3.5-turbo 모델 사용 권장)
model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# 출력 목적으로 사용
def format_parser_output(parser_output: Dict[str, Any]) -> None:
  # 파서 출력의 키들을 순회
  for key in parser_output.keys():
    # 각 키의 값을 딕셔너리로 변환
    parser_output[key] = parser_output[key].to_dict()
  # 출력 모양 설정
  return pprint.PrettyPrinter(width = 4, compact = True).pprint(parser_output)

df = pd.read_csv("/content/titanic.csv")

df.head()

# 파서를 설정하고 프롬프트 템플릿에 지시사항을 주입
parser = PandasDataFrameOutputParser(dataframe = df)

print(parser.get_format_instructions())

# 프롬프트 템플릿 설정
prompt = PromptTemplate(
    template = "Answer the user query.\n{format_instructions}\n{question}\n",
    input_variables = ["question"], # 입력 변수 설정
    partial_variables = {"format_instructions": parser.get_format_instructions()} # 부분 변수 설정
)

# 체인 생성
chain = prompt | model | parser

# 열 작업 예시
df_query = "Age column 을 조회해 주세요."

response = chain.invoke({"question": df_query})

response

# row 0 ~ 4의 평균 나이 계산
df["Age"].head().mean()

df_query = "Retrieve the average of the Ages from row 0 to 4."
parser_output = chain.invoke({"question": df_query})
print(parser_output)

df_query = "3등급 승객 중 40세 이상인 여성 승객의 평균 나이."
parser_output = chain.invoke({"question": df_query})
print(parser_output)