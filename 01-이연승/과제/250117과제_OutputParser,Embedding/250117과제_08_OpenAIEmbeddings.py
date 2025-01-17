import asyncio  # 비동기 실행을 위한 모듈
from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langdetect import detect  # 언어 감지
from googletrans import Translator  # 번역
import os

# 환경 변수 로드
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT_ID = os.getenv("LANGCHAIN_PROJECT_ID")

# OpenAI 임베딩 초기화
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)

# 번역기 초기화
translator = Translator()

async def preprocess(sentence):
    """
    문장을 처리하여 언어 감지 및 필요 시 번역.
    """
    detected_lang = detect(sentence)  # 언어 감지
    if detected_lang == 'ko':  # 한국어일 경우 영어로 번역
        translated = await translator.translate(sentence, src='ko', dest='en')
        print(f"Translated Sentence: {translated.text}")
        return translated.text
    return sentence  # 영어일 경우 그대로 반환

async def main():
    # 문장 리스트
    sentence1 = "안녕하세요? 반갑습니다."
    sentence2 = "안녕하세요? 반갑습니다!"
    sentence3 = "안녕하세요? 만나서 반가워요."
    sentence4 = "Hi, nice to meet you."
    sentence5 = "I like to eat apples."
    sentences = [sentence1, sentence2, sentence3, sentence4, sentence5]

    # 결과를 저장할 파일 열기
    with open("results.txt", "w", encoding="utf-8") as file:
        # 문장별로 번역 및 임베딩 처리
        embedded_sentences = [
            embeddings.embed_query(await preprocess(sentence)) for sentence in sentences
        ]

        # 코사인 유사도 계산 함수
        def similarity(a, b):
            return cosine_similarity([a], [b])[0][0]

        # 유사도 계산 및 출력
        for i, sentence in enumerate(embedded_sentences):
            for j, other_sentence in enumerate(embedded_sentences):
                if i < j:
                    result = (
                        f"[유사도 {similarity(sentence, other_sentence):.4f}] {sentences[i]} \t <=====> \t {sentences[j]}"
                    )
                    print(result)  # 화면에 출력
                    file.write(result + "\n")  # 파일에 저장

# 비동기 함수 실행
asyncio.run(main())
