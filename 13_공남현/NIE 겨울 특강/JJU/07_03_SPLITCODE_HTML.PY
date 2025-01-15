from langchain.text_splitter import RecursiveCharacterTextSplitter

# HTML 텍스트 파일 읽기
file_path = r"C:\Users\Administrator\Desktop\NIE 겨울 특강\JJU\html_jju.txt"  # 파일 경로 수정
with open(file_path, "r", encoding="utf-8") as file:
    html_text = file.read()

# RecursiveCharacterTextSplitter 생성
html_splitter = RecursiveCharacterTextSplitter(
    chunk_size=60,           # 각 청크의 최대 크기
    chunk_overlap=0          # 청크 간 중복 없음
)

# HTML 텍스트를 분할하여 문서 생성
html_docs = html_splitter.create_documents([html_text])

# 분할된 문서 출력
for i, doc in enumerate(html_docs):
    print(f"--- Document {i+1} ---")
    print(doc.page_content)
