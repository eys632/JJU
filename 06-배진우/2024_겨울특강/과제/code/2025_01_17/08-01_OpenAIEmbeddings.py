from langchain_openai.embeddings import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os
from googletrans import Translator
import re
import asyncio

# .env 파일 로드
load_dotenv()

# 환경 변수 불러오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

# 번역기 초기화
translator = Translator()

async def translate_to_english(text):
    try:
        translated = await translator.translate(text, dest='en')
        return translated.text
    except Exception as e:
        print(f"번역 오류: {e}")
        return text  # 번역에 실패하면 원문 반환

def preprocess(text):
    # 소문자 변환
    text = text.lower()
    # 특수 문자 제거
    text = re.sub(r'[^\w\s]', '', text)
    # 불필요한 공백 제거
    text = text.strip()
    return text

async def main():
    # 문장 정의
    sentence1 = "안녕하세요? 반갑습니다."
    sentence2 = "안녕하세요? 반갑습니다!"
    sentence3 = "안녕하세요? 만나서 반가워요."
    sentence4 = "Hi, nice to meet you."
    sentence5 = "I like to eat apples."

    sentences = [sentence1, sentence2, sentence3, sentence4, sentence5]

    # 모든 문장을 영어로 번역 및 전처리
    translated_sentences = []
    for sentence in sentences:
        translated = await translate_to_english(sentence)
        preprocessed = preprocess(translated)
        translated_sentences.append(preprocessed)

    # 임베딩 모델 초기화
    scaled_embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)

    # 임베딩 생성
    embedded_sentences = scaled_embeddings.embed_documents(translated_sentences)

    def similarity(a, b):
        return cosine_similarity([a], [b])[0][0]

    # 유사도 계산 및 출력 준비
    similarity_results = []

    for i, sentence in enumerate(embedded_sentences):
        for j, other_sentence in enumerate(embedded_sentences):
            if i < j:
                similarity_score = similarity(sentence, other_sentence)
                result_line = f"[유사도 {similarity_score:.4f}] {sentences[i]} \t <=====> \t {sentences[j]}"
                print(result_line)
                similarity_results.append(result_line)

    # 실행 중인 스크립트의 파일 이름을 기반으로 결과 파일 이름 생성
    try:
        current_file = os.path.basename(__file__)  # 예: '08-01_OpenAIEmbeddings.py'
    except NameError:
        # Jupyter Notebook 등에서 __file__이 정의되지 않은 경우
        current_file = "script"

    filename_without_ext = os.path.splitext(current_file)[0]  # '08-01_OpenAIEmbeddings'
    output_filename = f"06-배진우/2024_겨울특강/과제/code/2025_01_17/{filename_without_ext}_result.txt"

    # 결과를 파일에 저장
    try:
        with open(output_filename, "w", encoding="utf-8") as file:
            for line in similarity_results:
                file.write(line + "\n")
        print(f"\n유사도 결과가 '{output_filename}' 파일에 저장되었습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    asyncio.run(main())
