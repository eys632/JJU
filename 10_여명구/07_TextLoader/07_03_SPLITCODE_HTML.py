from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
with open(r'C:\Users\brigh\Desktop\비트교육\html_jju.txt', 'r', encoding='utf-8') as file:
    html_text = file.read()

html_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.HTML,
    chunk_size=60,
    chunk_overlap=0
)

html_docs = html_splitter.create_documents([html_text])

for idx, doc in enumerate(html_docs, start=1):
    print(doc.page_content)
