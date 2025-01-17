import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

import pprint
from typing import Any, Dict

import pandas as pd
from langchain.output_parsers import PandasDataFrameOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


# ChatOpenAI 모델 초기화 (gpt-3.5-turbo 모델 사용을 권장합니다)
model = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

# 출력 목적으로만 사용됩니다.
def format_parser_output(parser_output: Dict[str, Any]) -> None:
    # 파서 출력의 키들을 순회합니다.
    for key in parser_output.keys():
        # 각 키의 값을 딕셔너리로 변환합니다.
        parser_output[key] = parser_output[key].to_dict()
    # 예쁘게 출력합니다.
    return pprint.PrettyPrinter(width=4, compact=True).pprint(parser_output)

# 원하는 Pandas DataFrame을 정의합니다.
df = pd.read_csv("10_여명구/data/titanic.csv")

# print(df.head())

# 파서를 설정하고 프롬프트 템플릿에 지시사항을 주입합니다.
parser = PandasDataFrameOutputParser(dataframe=df)

print("파서의 지시사항을 출력.")
print(parser.get_format_instructions())

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],  # 입력 변수 설정
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    },  # 부분 변수 설정
)
chain = prompt | model | parser

# 행 조회 예시입니다.
df_query = "Retrieve the first row."

# 체인 실행
response = chain.invoke({"query": df_query})

print("\n결과 출력")
format_parser_output(response)
