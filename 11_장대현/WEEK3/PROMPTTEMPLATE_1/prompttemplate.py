import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import load_prompt

# YAML 파일에서 PromptTemplate 불러오기
startup_prompt = load_prompt("C:/Users/wkdeo/OneDrive - 전주대학교/문서/GitHub/JJU/11_장대현/data/startup_analysis.yaml", encoding="utf-8")

# LLM 초기화
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
    max_tokens=None,
    timeout=None,
    max_retries=3
)

# Input 데이터 정의
input_data = {
    "startup_name": "SpaceX",
    "industry": "우주 탐사 및 항공",
    "key_challenges": "고비용의 연구 개발, 안전성 확보, 정부 규제 및 인증"
}

# Prompt 실행
formatted_prompt = startup_prompt.format(**input_data)
response = llm.invoke(formatted_prompt)

# 결과 출력
print("### 분석 결과 ###\n", response.content)

# 분석 결과를 파일로 저장
output_file = "C:/Users/wkdeo/OneDrive - 전주대학교/문서/GitHub/JJU/11_장대현/data/answerfromllm.txt"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(response.content)

print(f"분석 결과가 {output_file} 파일에 저장되었습니다.")
