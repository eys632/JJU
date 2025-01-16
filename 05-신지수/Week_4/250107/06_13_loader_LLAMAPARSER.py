import os
import nest_asyncio
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

LLAMA_CLOUD_API_KEY = 'llx-wj5USY9tnVxJP0LJNAXluPEukvYKOu0Gr8PIOVBSSyMA7ymO'
nest_asyncio.apply()

os.environ["OPENAI_API_KEY"] = 'API 키'

documents = LlamaParse(
    use_vendor_multimodal_model=True,
    vendor_multimodal_model_name="openai-gpt4o",
    vendor_multimodal_api_key=os.environ["OPENAI_API_KEY"],
    result_type="markdown",
    language="ko",
    api_key=LLAMA_CLOUD_API_KEY,
    page_separator="/n=================/n",
)

# parsing 된 결과
parsed_docs = documents.load_data(file_path="sub/data_all/02 논문작성법.pdf")
docs = [doc.to_langchain_format() for doc in parsed_docs]

print(docs[0].page_content)

# parsing instruction 설정
parsing_instruction = "You are parsing a brief of AI Report. Please extract tables in markdown format."

print(len(docs))
print(docs[0].page_content)