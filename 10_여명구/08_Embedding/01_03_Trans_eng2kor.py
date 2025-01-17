import asyncio
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from googletrans import Translator

# API 키 정보 로드
load_dotenv()

# OpenAI 임베딩 모델 초기화
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)

# 번역 함수 (모든 문장을 한국어로 번역)
translator = Translator()

async def translate_to_korean(sentence):
    result = await translator.translate(sentence, src='auto', dest='ko')
    return result.text

# 원본 문장 리스트
sentence1 = "안녕하세요? 반갑습니다."
sentence2 = "안녕하세요? 반갑습니다!"
sentence3 = "안녕하세요? 만나서 반가워요."
sentence4 = "Hi, nice to meet you."
sentence5 = "I like to eat apples."
sentences = [sentence1, sentence2, sentence3, sentence4, sentence5]

# 번역 작업을 비동기로 처리
async def translate_all_sentences(sentences):
    return await asyncio.gather(*[translate_to_korean(sentence) for sentence in sentences])

# 비동기로 번역 실행
translated_sentences = asyncio.run(translate_all_sentences(sentences))

# 번역된 문장을 임베딩
embedded_sentences = embeddings.embed_documents(translated_sentences)

# 유사도 계산 및 출력
for i, sentence in enumerate(embedded_sentences):
    for j, other_sentence in enumerate(embedded_sentences):
        if i < j:
            translated_text = f"(번역한 문장: {translated_sentences[j]})" if "Hi" in sentences[j] or "I like" in sentences[j] else ""
            print(
                f"[유사도 {cosine_similarity([sentence], [other_sentence])[0][0]:.4f}] {sentences[i]} \t <=====> \t {sentences[j]} {translated_text}"
            )
