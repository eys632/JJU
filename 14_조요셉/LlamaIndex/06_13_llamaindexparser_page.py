import os
import nest_asyncio

LLAMA_CLOUD_API_KEY = os.environ['LLAMA_CLOUD_API_KEY']
nest_asyncio.apply()

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

# 파서 설정
parser = LlamaParse(
    result_type="text",  # "markdown"과 "text" 사용 가능
    num_workers=8,  # worker 수 (기본값: 4)
    split="page", # "element"와 "page" 사용 가능
    verbose=True,
    language="ko",
    api_key=LLAMA_CLOUD_API_KEY,
    exclude=["header", "footer"],
)

# SimpleDirectoryReader를 사용하여 파일 파싱
file_extractor = {".pdf": parser}

# LlamaParse로 파일 파싱
documents = SimpleDirectoryReader(
    input_files=["data\Don't Do RAG.pdf"],
    file_extractor=file_extractor,
).load_data()

"""### Llamaindex -> LangChain Document로 변환"""

docs = [doc.to_langchain_format() for doc in documents]

print(len(docs))
print(docs[0].metadata)
print(docs[0].page_content)

