# 파일 경로 설정
file_path = "/content/김가은자소서.txt"

# 파일을 열고 내용을 읽어서 file_content 변수에 저장합니다.
with open(file_path, encoding='utf-8') as f:
    file_content = f.read()

# 파일의 처음 500글자를 출력합니다.
print(file_content[:500])

# langchain의 CharacterTextSplitter를 임포트합니다.
from langchain.text_splitter import CharacterTextSplitter

# CharacterTextSplitter를 사용하여 텍스트를 청크로 분할하는 설정을 합니다.
text_splitter = CharacterTextSplitter(
    separator="\n\n",       # 텍스트를 분할할 때 사용할 구분자 (기본값은 "\n\n")
    chunk_size=210,         # 각 청크의 최대 크기
    chunk_overlap=0,        # 청크 간의 중첩 크기
    length_function=len     # 텍스트의 길이를 측정하는 함수
)

# 파일 내용을 청크로 분할하여 documents 리스트에 저장합니다.
documents = text_splitter.create_documents([file_content])

# 첫 번째 청크의 길이를 출력합니다.
print(len(documents[0].page_content))

# 첫 번째 청크의 내용을 출력합니다.
print(documents[0])

# 문서에 대한 메타데이터 리스트를 정의합니다.
metadatas = [
    {"document": 1},
    # {"document": 2},  # 필요시 추가 가능
]

# 메타데이터를 포함하여 문서를 다시 생성합니다.
documents_with_metadata = text_splitter.create_documents(
    [file_content],
    metadatas=metadatas
)

# 메타데이터가 포함된 첫 번째 문서를 출력합니다.
print(documents_with_metadata[0])

# 전체 문서의 개수를 출력합니다.
print(len(documents_with_metadata))

# 두 번째 문서가 존재할 경우 해당 문서의 메타데이터를 출력합니다.
if len(documents_with_metadata) > 1:
    print(documents_with_metadata[1].metadata)

# split_text 메소드를 사용하여 텍스트를 분할한 결과를 출력합니다.
chunks = text_splitter.split_text(file_content)
print(chunks)
