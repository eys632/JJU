import pprint
from typing import Any, Dict

import pandas as pd
from langchain.output_parsers import PandasDataFrameOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# ChatOpenAI 모델 초기화 (gpt-3.5-turbo 모델 사용을 권장합니다)
model = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

# 출력 목적으로만 사용됩니다.
def format_parser_output(parser_output: Dict[str, Any]) -> None:
    # 파서 출력의 키들을 순회합니다.
    for key in parser_output.keys():
        # 각 키의 값을 딕셔너리로 변환합니다.
        parser_output[key] = parser_output[key].to_dict()
    # 예쁘게 출력합니다.
    return pprint.PrettyPrinter(width=4, compact=True).pprint(parser_output)

df=pd.read_csv("/content/data/titanic.csv")

df.head()

# 파서를 설정하고 프롬프트 템플릿에 지시사항을 주입합니다.
parser = PandasDataFrameOutputParser(dataframe=df)

# 파서의 지시사항을 출력합니다.
print(parser.get_format_instructions())

# 열 작업 예시입니다.
df_query = "Age column 을 조회해 주세요."


# 프롬프트 템플릿을 설정합니다.
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],  # 입력 변수 설정
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    },  # 부분 변수 설정
)

# 체인 생성
chain = prompt | model | parser

response=chain.invoke({"query": df_query})

# 체인 실행
parser_output = chain.invoke({"query": df_query})

# 출력
format_parser_output(parser_output)

df["Age"].head().mean()

# 행 조회 예시입니다.
df_query = "Retrieve the first row."

# 체인 실행
parser_output = chain.invoke({"query": df_query})

# 결과 출력
format_parser_output(parser_output)

"""숙제

*3등칸 승객중 40세 이상인 여성승객의 평균나이   


"""

import pandas as pd

# 데이터셋 로드
file_path = '/content/data/titanic.csv'
data = pd.read_csv(file_path)

# 3등칸 여성 승객 중 40세 이상인 승객 필터링
filtered_data = data[(data['Pclass'] == 3) & (data['Sex'] == 'female') & (data['Age'] >= 40)]

# 평균 나이 계산
mean_age = filtered_data['Age'].mean()
print(mean_age)











