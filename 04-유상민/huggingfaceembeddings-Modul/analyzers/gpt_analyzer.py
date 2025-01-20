from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def analyze_with_gpt(file_type, loader_results_and_split_results, document_content):
    """
    문서 내용을 기반으로 생성된 질문에 대해 답변을 제공.
    """
    # GPT 모델 초기화
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0,  # 답변의 일관성과 정확성을 높이기 위해 온도를 낮게 설정
    )

    # 로더 및 스플리터 결과 분리
    loader_results, split_results = loader_results_and_split_results

    # Splitter 목록 생성
    splitter_list = "\n".join([
        f"- {result['splitter']}" for result in split_results
    ])

    # 프롬프트 템플릿 정의
    prompt_template = PromptTemplate(
        input_variables=["file_type", "splitter_list", "split_results", "document_content"],
        template="""
        다음 문서 내용을 기반으로 생성된 질문 목록에 대해 정확하고 구체적인 답변을 제공하세요.
        각 답변은 반드시 문서 내용을 참조해야 합니다.

        문서 내용:
        {document_content}

        사용 가능한 Splitter 목록:
        {splitter_list}

        분석해야 할 내용:
        {split_results}
        """
    )

    # LLMChain 생성 및 실행
    chain = LLMChain(llm=model, prompt=prompt_template)

    # GPT 모델 실행
    result = chain.run({
        "file_type": file_type,
        "splitter_list": splitter_list,
        "split_results": str(split_results)[:1000],
        "document_content": document_content[:2000]  # 문서 내용 길이 제한
    })

    return result


def generate_questions(document_content):
    """
    문서 내용을 기반으로 10개의 질문 생성.
    """
    # GPT 모델 초기화
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0,  # 질문의 정확성과 반복성을 보장하기 위해 온도를 낮게 설정
    )

    # 프롬프트 템플릿 정의
    prompt = PromptTemplate(
        input_variables=["document"],
        template="""
        다음 문서 내용을 기반으로 10개의 질문을 생성해주세요:

        문서 내용:
        {document}

        """
    )

    # LLMChain 생성 및 실행
    chain = LLMChain(llm=model, prompt=prompt)

    # 질문 생성
    questions = chain.run({"document": document_content})

    # 질문 리스트 반환
    return [q.strip() for q in questions.split("\n") if q.strip()]
