queries = [
    "YETI 프레임워크는 기존 HoloAssist와 비교했을 때 어떤 주요 개선점을 제공하는가?",
    "YETI가 프로액티브 개입을 위해 사용하는 주요 특징 신호는 무엇이며, 이들이 어떻게 동작하는가?",
    "SSIM(Structural Similarity Index Measure)이 YETI에서 어떤 역할을 하며, 특정 프레임을 필터링하는 이유는 무엇인가?",
    "YETI 알고리즘에서 설정 가능한 주요 하이퍼파라미터(예: SSIM 임계값, Conversation Interval 등)의 값과 그 중요성은 무엇인가?",
    "YETI의 글로벌(Global) 및 로컬(Local) 접근 방식의 차이는 무엇이며, 각각의 장단점은 무엇인가?",
    "YETI가 실시간으로 개입 결정을 내리는 데 있어 기존 분류기(Random Forest, MLP 등)보다 적합한 이유는 무엇인가?",
    "YETI 프레임워크가 AR 기기를 활용하여 사용자와 협업할 때 발생하는 주요 도전 과제는 무엇이며, 이를 어떻게 해결했는가?",
    "YETI가 HoloAssist 데이터셋의 프로액티브 개입 유형(예: Confirm Action, Correct Mistake, Follow Up)별로 어떻게 성능을 발휘했는가?",
    "YETI가 특정 작업(예: 컴퓨터 조립, 커피 만들기 등)에서 사용자의 안전을 보장하기 위해 어떤 방식으로 개입하는가?",
    "향후 YETI 프레임워크를 개선하거나 확장하기 위해 계획 중인 연구 방향이나 가능성은 무엇인가?",
]

def generate_questions():
    return queries


def search_answers(chroma_db, questions, k=1):
    retriever = chroma_db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    results = []
    for question in questions:
        response = retriever.invoke(question)
        results.append({
            "질문": question,
            "답변": response[0].page_content if response else "No answer found"
        })
    return results

if __name__ == "__main__":
    from chroma_db_setup import setup_chroma_db, load_and_split_text, DB_PATH, COLLECTION_NAME
    split_docs = load_and_split_text("extracted_texts/pypdf_text.txt")
    chroma_db = setup_chroma_db(split_docs, DB_PATH, COLLECTION_NAME)

    questions = generate_questions()
    qa_results = search_answers(chroma_db, questions)

    print("질의응답 결과:")
    for result in qa_results:
        print(result)
