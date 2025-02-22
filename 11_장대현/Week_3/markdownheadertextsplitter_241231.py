# -*- coding: utf-8 -*-
"""MarkdownHeaderTextSplitter_241231.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z5HSfaCGqJw37_1EDP9E6ZSDTIcqkH4X

## 1. MarkdownHeaderTextSplitter

- `markdown_document` 변수에 마크다운 형식의 문서가 할당됩니다.

- `headers_to_split_on` 리스트에는 마크다운 헤더 레벨과 해당 레벨의 이름이 튜플 형태로 정의됩니다.
- `MarkdownHeaderTextSplitter` 클래스를 사용하여 `markdown_splitter` 객체를 생성하며, `headers_to_split_on` 매개변수로 분할 기준이 되는 헤더 레벨을 전달합니다.
- split_text 메서드를 호출하여 `markdown_document`를 헤더 레벨에 따라 분할합니다.
"""

from langchain.text_splitter import MarkdownHeaderTextSplitter

# 확장자가 .md인 파일을 불러오는 함수 정의
def process_markdown_file(file_path, output_file):
    try:
        # 파일을 읽어오기
        with open(file_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()

        # 헤더 구조를 정의
        headers_to_split_on = [
            ("#", "Header 1"),  # Level 1 Header
            ("##", "Header 2"), # Level 2 Header
            ("###", "Header 3") # Level 3 Header
        ]

        # MarkdownHeaderTextSplitter로 내용을 처리
        header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        split_sections = header_splitter.split_text(markdown_content)

        # 처리 결과를 하나의 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as output_file:
            for section in split_sections:
                header = section.metadata
                content = section.page_content
                output_file.write(f"# {header}\n\n")  # 헤더를 파일에 추가
                output_file.write(content)  # 내용을 파일에 추가
                output_file.write("\n\n---\n\n")  # 섹션 구분선 추가

        print(f"All sections saved to {output_file.name}")

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# .md 파일 경로와 출력 파일 경로를 지정
file_path = "/content/testresume.md"
output_file = "/content/processed_resume.md"  # 출력 파일 경로 지정

process_markdown_file(file_path, output_file)