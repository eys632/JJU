import os
import yaml
import numpy as np
from dotenv import load_dotenv
from scipy.spatial.distance import cosine
from langchain_openai import OpenAIEmbeddings

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API 키

# OpenAI 임베딩 생성
embeddings = OpenAIEmbeddings()

# 예제 데이터 로드 (YAML 파일 사용)
with open(r"10_여명구\02_Prompt\data\Example_Selector2.yaml", "r", encoding="utf-8") as f:
    yaml_data = yaml.safe_load(f)
    examples = yaml_data["examples"]

# 입력 데이터 정의
input_question = {
    "instruction": "당신은 영화 리뷰 요약 전문가입니다. 주어진 리뷰를 간결하게 요약해 주세요.",
    "input": """
    이 영화는 시각적으로 놀라운 경험을 제공합니다. 감독의 독특한 연출 방식과
    배우들의 열연이 어우러져 작품의 완성도를 높였습니다.
    하지만 지나치게 복잡한 스토리 때문에 중반부에서 약간의 혼란을 느꼈습니다.
    """,
}

# 입력 데이터를 임베딩으로 변환
input_embedding = embeddings.embed_query(input_question["input"])

# 각 예제와 입력 데이터의 유사도 계산
similarities = []
for example in examples:
    # 예제 데이터를 임베딩으로 변환
    example_embedding = embeddings.embed_query(example["input"])
    
    # 코사인 유사도 계산 (1 - cosine distance)
    similarity = 1 - cosine(input_embedding, example_embedding)
    
    # 결과 저장
    similarities.append({
        "example": example,
        "similarity": similarity,
    })

# 유사도 기준으로 정렬 (높은 순서대로)
similarities = sorted(similarities, key=lambda x: x["similarity"], reverse=True)

# 결과 출력
print("=== 유사도 검사 결과 ===")
for i, sim in enumerate(similarities, start=1):
    print(f"\n{i}. 유사도 점수: {sim['similarity']:.4f}")
    print(f"Instruction: {sim['example']['instruction']}")
    print(f"Input: {sim['example']['input']}")
    print(f"Answer: {sim['example']['answer']}")
