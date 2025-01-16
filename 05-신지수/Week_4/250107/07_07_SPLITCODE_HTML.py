from langchain.text_splitter import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter

file_path = "C:\Users\s0108\OneDrive\바탕 화면\549f0860-4cef-4488-afbd-c3d130b34d56_Export-b79b42ff-cfa8-4610-baf7-90b326dfcb9b\자기소개서 16d4276c0c1f80a28f59f2042b7eeeed.html"  # 분할할 텍스트의 파일 경로를 지정합니다.

# HTML 헤더로 텍스트를 분할하는 데 사용할 HTML 헤더 태그와 헤더 이름을 지정합니다.

headers_to_split_on = [  # 분할할 HTML 헤더 태그와 해당 헤더의 이름을 지정합니다.
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
    ("h4", "Header 4"),
]

# HTML 헤더를 기준으로 텍스트를 분할하는 HTMLHeaderTextSplitter 객체를 생성합니다.
html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# 파일에서 텍스트를 읽어옵니다.
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# HTML 헤더를 기준으로 텍스트를 분할합니다.
html_header_splits = html_splitter.split_text(html_content)

chunk_size = 500  # 텍스트를 분할할 청크의 크기를 지정합니다.
chunk_overlap = 30  # 분할된 청크 간의 중복되는 문자 수를 지정합니다.
text_splitter = RecursiveCharacterTextSplitter(  # 텍스트를 재귀적으로 분할하는 RecursiveCharacterTextSplitter 객체를 생성합니다.
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)

# HTML 헤더로 분할된 텍스트를 다시 청크 크기에 맞게 분할합니다.
splits = text_splitter.split_documents(html_header_splits)

# 분할된 텍스트 중 80번째부터 85번째까지의 청크를 출력합니다.
for header in splits[80:85]:
    print(f"{header.page_content}")
    print(f"{header.metadata}", end="\n=====================\n")