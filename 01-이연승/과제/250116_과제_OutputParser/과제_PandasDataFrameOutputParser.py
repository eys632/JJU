from dotenv import load_dotenv
import os
import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PandasDataFrameOutputParser
from langchain_openai import ChatOpenAI

# 환경 변수 로드
load_dotenv()

# API 키 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT_ID = os.getenv("LANGCHAIN_PROJECT_ID")

# ChatOpenAI 모델 초기화
model = ChatOpenAI(temperature=0, model_name="gpt-4o")

# PandasDataFrameOutputParser 초기화 (예제 데이터프레임 포함)
example_dataframe = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [30, 35], "Occupation": ["Engineer", "Doctor"]})
output_parser = PandasDataFrameOutputParser(dataframe=example_dataframe)

# 출력 형식 지침 가져오기
format_instructions = output_parser.get_format_instructions()

# 프롬프트 템플릿 설정
prompt = PromptTemplate(
    template="Generate a Pandas DataFrame based on the following description:\n{description}\n{format_instructions}",
    input_variables=["description"],
    partial_variables={"format_instructions": format_instructions},
)

# 데이터프레임 생성 함수
def generate_dataframe(description):
    # 프롬프트 생성
    prompt_text = prompt.format(description=description)
    # 모델 호출
    response = model.invoke(prompt_text)
    # 데이터프레임 파싱
    try:
        return output_parser.parse(response.content)
    except Exception as e:
        print(f"Error parsing the response: {e}")
        return None

# 사용 예시
if __name__ == "__main__":
    description = "Create a DataFrame with columns 'Name', 'Age', and 'Occupation' and add three rows of data."
    try:
        result = generate_dataframe(description)
        if result is not None:
            print("Generated DataFrame:")
            print(result)
        else:
            print("No DataFrame was generated.")
    except Exception as e:
        print(f"An error occurred: {e}")
