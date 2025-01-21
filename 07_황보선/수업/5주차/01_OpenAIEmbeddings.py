import os
from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

os.environ['OPENAI_API_KEY']=''
os.environ['LANGCHAIN_TRACING_V2']=''
os.environ['LANGCHAIN_ENDPOINT']=''
os.environ['LANGCHAIN_API_KEY']=''
os.environ['LANGCHAIN_PROJECT']=''

# OpenAI의 "text-embedding-3-large" 모델을 사용하여 임베딩을 생성합니다.
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

text = "임베딩 테스트를 하기 위한 샘플 문장입니다."

# 텍스트를 임베딩하여 쿼리 결과를 생성합니다.
query_result = embeddings.embed_query(text)

text_2 = '임베딩(Embedding)이란 데이터를 고차원에서 저차원 벡터로 변환해 컴퓨터가 효율적으로 이해하고 처리할 수 있도록 표현하는 방법'

doc_result = embeddings.embed_documents(
    [text_2, text_2, text_2, text_2]
) # 텍스트를 임베딩하여 문서 벡터를 생성

doc_result[0][:5]

print('len:', len(doc_result[0]))

# OpenAI의 "text-embedding-3-small" 모델을 사용하여 1024차원의 임베딩을 생성하는 객체를 초기화합니다.
scaled_embeddings = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=1024)

print(scaled_embeddings.embed_documents([text]))
print('')
print('len:', len(scaled_embeddings.embed_documents([text])[0]))

sentence1 = "안녕하세요? 반갑습니다."
sentence2 = "안녕하세요? 반갑습니다!"
sentence3 = "안녕하세요? 만나서 반가워요."
sentence4 = "Hi, nice to meet you."
sentence5 = "I like to eat apples."

sentences = [sentence1, sentence2, sentence3, sentence4, sentence5]
embedded_sentences = scaled_embeddings.embed_documents(sentences)

def similarity(a, b):
    return cosine_similarity([a], [b])[0][0]

# embedding 할때 언어가 달라지면 유사도 현저히 낮아짐

for i, sentence in enumerate(embedded_sentences):
    for j, other_sentence in enumerate(embedded_sentences):
        if i < j:
            print(
                f'[유사도 {similarity(sentence, other_sentence):.4f}] {sentences[i]} \t <====> \t {sentences[j]}'
            )