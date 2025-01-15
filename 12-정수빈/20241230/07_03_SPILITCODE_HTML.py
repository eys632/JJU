from langchain.text_splitter import RecursiveCharacterTextSplitter

# 파일 읽기
file_path = "html_jju.txt"  # 실제 파일 경로
with open(file_path, 'r', encoding='utf-8') as file:
    html_text = file.read()

# RecursiveCharacterTextSplitter 설정
html_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 청크 크기 설정
    chunk_overlap=50  # 중복 간격 설정
)

# HTML 텍스트를 분할하여 문서 생성
html_docs = html_splitter.create_documents([html_text])

# 분할된 문서 출력
for idx, doc in enumerate(html_docs):
    print(f"Document {idx + 1}:\n")
    print(doc.page_content.strip())
    print("**************************************************\n")