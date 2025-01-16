# 필요한 라이브러리 임포트
import os
import yaml
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.example_selectors import (
    SemanticSimilarityExampleSelector,
    MaxMarginalRelevanceExampleSelector,
)
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

# 1. 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

# 2. Chroma VectorStore 및 임베딩 설정
chroma = Chroma("fewshot_chat", OpenAIEmbeddings())

# 3. Examples 데이터 로드 (YAML 파일 사용)
with open(r"10_여명구\02_Prompt\data\Example_Selector2.yaml", "r", encoding="utf-8") as f:
    examples_data = yaml.safe_load(f)
    examples = examples_data["examples"]

print(examples)

# 4. Example Prompt 설정
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{instruction}:\n{input}"),
        ("ai", "{answer}"),
    ]
)

# 5. SemanticSimilarityExampleSelector 설정
semantic_selector = SemanticSimilarityExampleSelector.from_examples(
    examples=examples,
    embeddings=OpenAIEmbeddings(),
    vectorstore_cls=chroma,
    k=1,  # 선택할 예제 수
)

# 6. MaxMarginalRelevanceExampleSelector 설정
mmr_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    examples=examples,
    embeddings=OpenAIEmbeddings(),
    vectorstore_cls=chroma,
    k=1,  # 선택할 예제 수
)

# 7. FewShotPromptTemplate 설정 (각 Selector 사용)
semantic_prompt = FewShotChatMessagePromptTemplate(
    example_selector=semantic_selector,
    example_prompt=example_prompt,
)

mmr_prompt = FewShotChatMessagePromptTemplate(
    example_selector=mmr_selector,
    example_prompt=example_prompt,
)

# 8. 최종 ChatPromptTemplate 설정
def create_final_prompt(few_shot_prompt):
    return ChatPromptTemplate.from_messages(
        [
            ("system", "너는 도움을 주는 어시스턴트야."),
            few_shot_prompt,
            ("human", "{instruction}\n{input}"),
        ]
    )

semantic_final_prompt = create_final_prompt(semantic_prompt)
mmr_final_prompt = create_final_prompt(mmr_prompt)

# 9. LLM 설정
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=OPENAI_API_KEY,
)

# 10. 입력 질문

# question = {
#     "instruction": "회의록을 작성해 주세요",
#     "input": "2023년 12월 26일, ABC 기술 회사의 제품 개발 팀은 새로운 모바일 애플리케이션 프로젝트에 대한 주간 진행 상황 회의를 가졌다. 이 회의에는 프로젝트 매니저인 최현수, 주요 개발자인 황지연, UI/UX 디자이너인 김태영이 참석했다. 회의의 주요 목적은 프로젝트의 현재 진행 상황을 검토하고, 다가오는 마일스톤에 대한 계획을 수립하는 것이었다. 각 팀원은 자신의 작업 영역에 대한 업데이트를 제공했고, 팀은 다음 주까지의 목표를 설정했다.",
# }

question = {
    "instruction": "당신은 영화 리뷰 요약 전문가입니다. 주어진 리뷰를 간결하게 요약해 주세요.",
    "input": """
    이 영화는 시각적으로 놀라운 경험을 제공합니다. 감독의 독특한 연출 방식과
    배우들의 열연이 어우러져 작품의 완성도를 높였습니다.
    하지만 지나치게 복잡한 스토리 때문에 중반부에서 약간의 혼란을 느꼈습니다.
    """,
}

# 11. 체인 생성 및 실행
def execute_chain(prompt, question, llm):
    chain = prompt | llm
    return chain.invoke(question)

# 12. 결과 비교
print("=== Semantic Similarity Example Selector 결과 ===")
semantic_response = execute_chain(semantic_final_prompt, question, llm)
print(semantic_response.content)

print("\n=== 응답 메타데이터 (Semantic Similarity) ===")
print({key: value for key, value in semantic_response.__dict__.items() if key != 'content'})

print("\n=== Max Marginal Relevance Example Selector 결과 ===")
mmr_response = execute_chain(mmr_final_prompt, question, llm)
print(mmr_response.content)

print("\n=== 응답 메타데이터 (MMR) ===")
print({key: value for key, value in mmr_response.__dict__.items() if key != 'content'})
