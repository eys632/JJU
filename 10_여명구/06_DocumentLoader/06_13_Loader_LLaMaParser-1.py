import os

os.environ["OPENAI_API_KEY"] = ""

os.environ["LLAMA_CLOUD_API_KEY"] = ""

import nest_asyncio
nest_asyncio.apply()

# pip install -q llama-index-core llama-parse llama-index-readers-file python-dotenv

from llama_parse import LlamaParse

# parsing instruction 지정(질문문)
parsing_instruction = (
    "You are parsing a brief of AI Report. Please extract tables in markdown format. Please answer in Korean."
)

parser = LlamaParse(
    use_vendor_multimodal_model=True,
    vendor_multimodal_model_name="openai-gpt4o",
    # vendor_multimodal_api_key=OPENAI_API_KEY,
    # api_key = LLAMA_CLOUD_API_KEY,
    result_type="markdown",
    language="ko",
    parsing_instruction=parsing_instruction,
    # skip_diagonal_text=True,
    # page_separator="\n=================\n"
)


# parsing 된 결과
parsed_docs = parser.load_data(file_path="비디오 트랜스포머 연구 동향.pdf")
# print(parsed_docs[0])

# pip install -q langchain_community
docs = [doc.to_langchain_format() for doc in parsed_docs]

print(docs[0].page_content)