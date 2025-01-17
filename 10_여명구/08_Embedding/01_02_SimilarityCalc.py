# API 키를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API 키 정보 로드
load_dotenv()

from langchain_openai import OpenAIEmbeddings

# OpenAI의 "text-embedding-3-large" 모델을 사용하여 임베딩을 생성합니다.
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024) # 차원 조정

sentence1 = "안녕하세요? 반갑습니다."
sentence2 = "안녕하세요? 반갑습니다!"
sentence3 = "안녕하세요? 만나서 반가워요."
sentence4 = "Hi, nice to meet you."
sentence5 = "I like to eat apples."

from sklearn.metrics.pairwise import cosine_similarity

sentences = [sentence1, sentence2, sentence3, sentence4, sentence5]
embedded_sentences = embeddings.embed_documents(sentences)

# def similarity(a, b):
#     return cosine_similarity([a], [b])[0][0]

# for i, sentence in enumerate(embedded_sentences):
#     for j, other_sentence in enumerate(embedded_sentences):
#         if i < j:
#             print(
#                 f"[유사도 {similarity(sentence, other_sentence):.4f}] {sentences[i]} \t <=====> \t {sentences[j]}"
#             )

for i, sentence in enumerate(embedded_sentences):
    for j, other_sentence in enumerate(embedded_sentences):
        if i < j:
            print(
                f"[유사도 {cosine_similarity([sentence], [other_sentence])[0][0]:.4f}] {sentences[i]} \t <=====> \t {sentences[j]}"
            )
