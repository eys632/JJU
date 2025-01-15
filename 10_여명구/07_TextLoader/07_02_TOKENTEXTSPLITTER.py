from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_topic_content(filepath):
    """
    1) 라인 단위로 읽어,
       - 주제 줄(새로운 토픽)을 만나면 이전 토픽+내용을 청크로 확정
       - '정의:', '예시:', '연관키워드:'로 시작하는 줄은 내용으로 저장
    2) 이렇게 만들어진 '주제+내용' 한 덩어리(원시 청크)를
    3) RecursiveCharacterTextSplitter로 재분할( chunk_size / chunk_overlap ) 적용
    """

    # --------------------------------------------------------------------------------
    # 1) 먼저 '주제+내용' 원시 청크 만들기
    # --------------------------------------------------------------------------------

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 줄 끝 개행 제거
    lines = [line.rstrip('\n') for line in lines]

    raw_chunks = []  # "주제+내용" 형태의 원시 청크들을 저장할 리스트
    current_topic = None
    current_content_lines = []

    def save_current_chunk():
        # current_topic + current_content_lines를 합쳐 하나의 텍스트로
        if current_topic:
            chunk_text = current_topic.strip()
            if current_content_lines:
                chunk_text += "\n\n" + "\n".join(current_content_lines).strip()
            if chunk_text.strip():
                raw_chunks.append(chunk_text)

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            # 빈 줄은 무시 (원한다면 content에 추가 가능)
            continue

        # 새 주제(Topic) 라인 판별:
        # - "정의:", "예시:", "연관키워드:"로 시작하지 않으면 '주제'로 간주
        if (not line_stripped.startswith("정의:") and
            not line_stripped.startswith("예시:") and
            not line_stripped.startswith("연관키워드:")):

            # 지금까지 모은 청크가 있으면 저장
            save_current_chunk()
            # 새 주제 시작
            current_topic = line_stripped
            current_content_lines = []
        else:
            # 정의/예시/연관키워드 등은 내용 부분에 쌓음
            current_content_lines.append(line_stripped)

    # 마지막 토픽+내용 처리
    save_current_chunk()

    # --------------------------------------------------------------------------------
    # 2) RecursiveCharacterTextSplitter를 이용해, 각 raw_chunk를 재분할
    # --------------------------------------------------------------------------------
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=250,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False
    )

    # raw_chunks 리스트 내 각 원시 청크를 다시 text_splitter로 나눔
    final_docs = []
    for raw_chunk in raw_chunks:
        # create_documents() -> 반환 결과가 Document 객체 리스트
        splitted_docs = text_splitter.create_documents([raw_chunk])
        final_docs.extend(splitted_docs)

    return final_docs


if __name__ == "__main__":
    file_path = r"C:\Users\brigh\Desktop\비트교육\appendix-keywords.txt"
    docs = split_topic_content(file_path)

    # 결과 확인
    for i, doc in enumerate(docs, start=1):
        print(f"[Chunk {i}] (길이: {len(doc.page_content)})")
        print(doc.page_content)
        print("-" * 40)
