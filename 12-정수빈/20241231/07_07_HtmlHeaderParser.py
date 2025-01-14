from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter
import os

# 파일 경로 지정
file_path = r"C:\Users\82102\Desktop\비트\20241231\이력서2.html"  # 로컬 HTML 파일 경로
output_file = "HTMLHEADER_TEXTSPLITTER_RESULT.TXT"  # 저장할 결과 파일 이름

# 분할할 헤더 태그와 이름 정의
headers_to_split_on = [

    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
    ("h4", "Header 4"),
]

# HTML 헤더를 기준으로 텍스트를 분할하는 객체 생성
html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# 로컬 HTML 파일에서 텍스트 읽기
try:
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {file_path}")
    exit()

# HTML 헤더를 기준으로 텍스트 분할
html_header_splits = html_splitter.split_text(html_content)

# RecursiveCharacterTextSplitter를 사용하여 추가로 분할
chunk_size = 500
chunk_overlap = 30
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)
splits = text_splitter.split_documents(html_header_splits)

# 결과를 파일로 저장
with open(output_file, "w", encoding="utf-8") as f:
    for i, header in enumerate(splits):
        f.write(f"Chunk {i+1}\n")
        f.write(f"Content:\n{header.page_content}\n")
        f.write(f"Metadata:\n{header.metadata}\n")
        f.write("=====================\n")

print(f"결과가 {output_file}에 저장되었습니다.")
