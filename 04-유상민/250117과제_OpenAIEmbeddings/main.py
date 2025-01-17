from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import asyncio

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

scaled_embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)

# 원본 문장
sentence1 = "안녕하세요? 반갑습니다."
sentence2 = "안녕하세요? 반갑습니다!"
sentence3 = "안녕하세요? 만나서 반가워요."
sentence4 = "Hi, nice to meet you."
sentence5 = "I like to eat apples."

sentences = [sentence1, sentence2, sentence3, sentence4, sentence5]

# Google Translator를 초기화
# source='ko'는 번역할 원본 언어를 한국어로 설정
# target='en'은 번역할 대상 언어를 영어로 설정
translator = GoogleTranslator(source='ko', target='en')

translated_sentences = [translator.translate(sentence) for sentence in sentences]

# 번역된 문장으로 임베딩 생성
embedded_sentences = scaled_embeddings.embed_documents(translated_sentences)

# 유사도 계산 함수
def similarity(a, b):
    return cosine_similarity([a], [b])[0][0]

# 유사도 출력
for i, sentence in enumerate(embedded_sentences):
    for j, other_sentence in enumerate(embedded_sentences):
        if i < j:
            print(
                f"[유사도{similarity(sentence, other_sentence):.4f}] {sentences[i]} \t <=======> \t{sentences[j]}"
            )