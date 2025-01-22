texts = [
    "안녕, 만나서 반가워.",
    "LangChain simplifies the process of building applications with large language models",
    "랭체인 한국어 튜토리얼은 LangChain의 공식 문서, cookbook 및 다양한 실용 예제를 바탕으로 하여 사용자가 LangChain을 더 쉽고 효과적으로 활용할 수 있도록 구성되어 있습니다. ",
    "LangChain은 초거대 언어모델로 애플리케이션을 구축하는 과정을 단순화합니다.",
    "Retrieval-Augmented Generation (RAG) is an effective technique for improving AI responses.",
]

from langchain_community.embeddings import OllamaEmbeddings

ollama_embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    # model="chatfire/bge-m3:q8_0" # BGE-M3
)

# 쿼리 임베딩
embedded_query = ollama_embeddings.embed_query("LangChain 에 대해서 상세히 알려주세요.")
# 임베딩 차원 출력
# print(len(embedded_query))

# 문서 임베딩
embedded_documents = ollama_embeddings.embed_documents(texts)

import numpy as np

# 질문(embedded_query): LangChain 에 대해서 알려주세요.
similarity = (np.array(embedded_query) @ np.array(embedded_documents).T) / len(embedded_query) # + 정규화화

# 유사도 기준 내림차순 정렬
sorted_idx = (np.array(embedded_query) @ np.array(embedded_documents).T).argsort()[::-1]

# 결과 출력
print("[Query] LangChain 에 대해서 알려주세요.\n====================================")
for i, idx in enumerate(sorted_idx):
    print(f"[{i}] 유사도: {similarity[idx]:.3f} | {texts[idx]}")
    print()
