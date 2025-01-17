# -*- coding: utf-8 -*-
# OpenAI Embeddings 및 유사도 계산 Python 스크립트

import os
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# OpenAI 및 LangChain API 키 설정
os.environ["OPENAI_API_KEY"] = "api-key"
os.environ["LANGCHAIN_API_KEY"] = "api-key"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "http://api.smith.langchain.com"
os.environ["LANGCHAINPROJECT"] = "03-08"

# OpenAI 임베딩 설정 (LangChain)
from langchain_openai import OpenAIEmbeddings

# 기본 임베딩 모델 로드
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Query 예제: 단일 문장 임베딩
text = "아무문장"
query_result = embeddings.embed_query(text)

# 결과 출력
print("Query 임베딩 결과 (앞 5개 요소):", query_result[:5])
print("Query 임베딩 차원:", len(query_result))

# Document 예제: 여러 문장 임베딩
text_2 = "임베딩은 고차원 데이터를 저차원 벡터로 변환하여 컴퓨터가 이해하고 처리할 수 있도록 표현하는 방법입니다."
doc_result = embeddings.embed_documents([text_2, text_2, text_2, text_2])

# 결과 출력
print("Document 임베딩 결과 (앞 5개 요소):", doc_result[0][:5])
print("Document 임베딩 차원:", len(doc_result[0]))

# 임베딩 차원 강제 변경 예제
scaled_embeddings = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=1024)
scaled_dim_result = scaled_embeddings.embed_documents([text])
print("강제 스케일링 임베딩 차원:", len(scaled_dim_result[0]))

# Sentence-BERT를 사용한 다국어 문장 유사도 계산
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# 예제 문장
sentence1 = "안녕하세요? 반갑습니다."
sentence2 = "안녕하세요? 반갑습니다!"
sentence3 = "안녕하세요? 만나서 반가워요."
sentence4 = "Hi, nice to meet you."
sentence5 = "I like to eat apples."

# 문장 리스트 및 임베딩 생성
sentences = [sentence1, sentence2, sentence3, sentence4, sentence5]
embedding_sentences = model.encode(sentences)

# 코사인 유사도 계산 함수
def similarity(a, b):
    return cosine_similarity([a], [b])[0][0]

# 유사도 출력
print("\n문장 간 코사인 유사도:")
for i, sentence in enumerate(embedding_sentences):
    for j, other_sentence in enumerate(embedding_sentences):
        if i < j:
            sim_score = similarity(sentence, other_sentence)
            print(
                f"[유사도 {sim_score:.4f}] {sentences[i]} \t <====> \t {sentences[j]}"
            )
