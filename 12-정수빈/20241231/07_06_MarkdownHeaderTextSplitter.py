import os
from langchain_text_splitters import MarkdownHeaderTextSplitter

# 파일 경로 지정
file_path = r"C:\Users\82102\Desktop\비트\20241231\이력서.md"

# 파일 읽기
try:
    with open(file_path, "r", encoding="utf-8") as file:
        markdown_document = file.read()
except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {file_path}")
    exit()

# 파일 내용 일부 출력 (테스트 용도)
print("파일 내용 미리 보기:")
print(markdown_document[:100], "\n")

# 문서를 분할할 헤더 레벨과 해당 레벨의 이름 정의
headers_to_split_on = [
    ("#", "Header 1"),   
    ("##", "Header 2"),  
    ("###", "Header 3"), 
]

# 마크다운 헤더 분할기 생성
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False,  
)

# 헤더 기준으로 문서 분할
md_header_splits = markdown_splitter.split_text(markdown_document)

# 결과 저장 디렉토리 생성
output_dir = "sub/MD_STATEMENT"
os.makedirs(output_dir, exist_ok=True)  # 디렉토리 없으면 생성

# 분할된 결과를 파일로 저장
print("분할된 결과 저장:")
for i, header in enumerate(md_header_splits):
    # 파일 이름 생성
    filename = f"section_{i+1}.md"
    filepath = os.path.join(output_dir, filename)
    
    # 파일 쓰기
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header.page_content)
    
    print(f"저장 완료: {filepath}")
