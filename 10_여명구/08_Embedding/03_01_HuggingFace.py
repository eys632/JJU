from dotenv import load_dotenv
import os
import warnings

# 환경 변수 로드
load_dotenv()

HUGGINGFACEHUB_API_TOKEN=os.getenv("HUGGINGFACEHUB_API_TOKEN")

# 경고 무시
warnings.filterwarnings("ignore")

# ./cache/ 경로에 다운받도록 설정
os.environ["HF_HOME"]="./cache/"

texts = [
    "안녕, 만나서 반가워.",
    "LangChain simplifies the process of building applications with large language models",
    "랭체인 한국어 튜토리얼은 LangChain의 공식 문서, cookbook 및 다양한 실용 예제를 바탕으로 하여 사용자가 LangChain을 더 쉽고 효과적으로 활용할 수 있도록 구성되어 있습니다. ",
    "LangChain은 초거대 언어모델로 애플리케이션을 구축하는 과정을 단순화합니다.",
    "Retrieval-Augmented Generation (RAG) is an effective technique for improving AI responses.",
]

from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

model_name = "intfloat/multilingual-e5-large-instruct"

hf_embeddings = HuggingFaceEndpointEmbeddings(
    model=model_name,
    task="feature-extraction",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
)

# print(hf_embeddings)

# %%time 시간 측정정
# Document Embedding 수행
embedded_documents = hf_embeddings.embed_documents(texts)

print("[HuggingFace Endpoint Embedding]")
print(f"Model: \t\t{model_name}")
print(f"Dimension(Documents): \t{len(embedded_documents[0])}")

# Document Embedding 수행
embedded_query = hf_embeddings.embed_query("RAG에 대해서 알려주세요.")

print(f"Dimension(Query): \t{len(embedded_query)}")

import numpy as np

# 질문(embedded_query): LangChain 에 대해서 알려주세요.
print(f"각 질문과 쿼리의 유사도 계산: \t{np.array(embedded_query) @ np.array(embedded_documents).T}")

sorted_idx = (np.array(embedded_query) @ np.array(embedded_documents).T).argsort()[::-1] # 유사도 점수를 오름차순으로 정렬
print(sorted_idx)

print("[Query] LangChain 에 대해서 알려주세요.\n====================================")
for i, idx in enumerate(sorted_idx):
    print(f"[{i}] {texts[idx]}")
    print()
