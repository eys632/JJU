# API 키를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API 키 정보 로드
load_dotenv()

from langchain_openai import OpenAIEmbeddings

# OpenAI의 "text-embedding-3-large" 모델을 사용하여 임베딩을 생성합니다.
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024) # 차원 조정

text = "임베딩 테스트를 하기 위한 샘플 문장입니다."

# 텍스트를 임베딩하여 쿼리 결과를 생성합니다.
query_result = embeddings.embed_query(text)

print("쿼리 임베딩")
print(query_result[:5])
print(len(query_result)) # text-embedding-3 모델은 출력 임베딩 벡터의 크기를 1536차원으로 고정함.

doc_result = embeddings.embed_documents(
    [text, text, text, text]
)  # 텍스트를 임베딩하여 문서 벡터를 생성합니다.

print("도큐먼트 임베딩")
print(len(doc_result))
print(len(doc_result[0]))