from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import os
import json

# 임베딩 모델 초기화
model = SentenceTransformer('all-MiniLM-L6-v2')

# 유사도 계산 함수
def calculate_similarity(question, answer):
    q_embedding = model.encode([question])
    a_embedding = model.encode([answer])
    similarity = cosine_similarity(q_embedding, a_embedding)
    return similarity[0][0]

# 키워드 기반 점수 계산
def calculate_keyword_score(answer, keywords):
    return sum(answer.count(keyword) for keyword in keywords) * 0.1  # 키워드 1개당 0.1점

# 점수 계산 함수
def score_responses(results):
    keywords = ["SSIM", "Global", "Local", "YETI", "HoloAssist"]  # 중요한 키워드
    for result in results:
        length_score = len(result["답변"]) / 100  # 답변 길이 기반 점수
        similarity_score = calculate_similarity(result["질문"], result["답변"])  # 질문-답변 유사도 점수
        keyword_score = calculate_keyword_score(result["답변"], keywords)  # 키워드 점수
        result["점수"] = round(length_score + similarity_score + keyword_score, 2)  # 최종 점수
    return results

# 결과 저장
def save_results_to_json(results, file_path="scored_results.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # 기존 JSON 파일 불러오기
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = os.path.join(BASE_DIR, "qa_results.json")  # 질문-답변 JSON 파일
    OUTPUT_FILE = os.path.join(BASE_DIR, "scored_results.json")  # 점수화 결과 저장 경로

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)

    # 점수 계산 및 저장
    scored_results = score_responses(results)
    save_results_to_json(scored_results, OUTPUT_FILE)

    print(f"점수화된 결과가 {OUTPUT_FILE}에 저장되었습니다.")
