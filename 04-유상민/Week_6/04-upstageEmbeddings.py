import os
import numpy as np
from langchain_upstage import UpstageEmbeddings

# Set environment variables securely (Replace with actual keys or manage through environment variables)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# Sample data
texts = [
    "안녕, 만나서 반가워.",
    "LangChain simplifies the process of building applications with large language models",
    "랭체인 한국어 튜토리얼은 LangChain의 공식 문서, cookbook 및 다양한 실용 예제를 바탕으로 하여 사용자가 LangChain을 더 쉽고 효과적으로 활용할 수 있도록 구성되어 있습니다.",
    "LangChain은 초거대 언어모델로 애플리케이션을 구축하는 과정을 단순화합니다.",
    "Retrieval-Augmented Generation (RAG) is an effective technique for improving AI responses.",
]

# Function for Upstage Embeddings
def upstage_embeddings(query, texts):
    query_embeddings = UpstageEmbeddings(model="solar-embedding-1-large-query")
    passage_embeddings = UpstageEmbeddings(model="solar-embedding-1-large-passage")

    embedded_query = query_embeddings.embed_query(query)
    embedded_documents = passage_embeddings.embed_documents(texts)

    similarities = np.array(embedded_query) @ np.array(embedded_documents).T
    sorted_idx = similarities.argsort()[::-1]

    print(f"[Query] {query}\n{'=' * 40}")
    for i, idx in enumerate(sorted_idx):
        print(f"[{i}] {texts[idx]}")

# Main function
def main():
    query = "LangChain 에 대해서 알려주세요."

    print("\n=== Upstage Embeddings ===")
    upstage_embeddings(query, texts)

if __name__ == "__main__":
    main()
