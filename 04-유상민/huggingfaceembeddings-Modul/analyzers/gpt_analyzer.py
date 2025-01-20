from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def analyze_with_gpt(file_type, loader_results_and_split_results, document_content):
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
    )

    loader_results, split_results = loader_results_and_split_results

    splitter_list = "\n".join([
        f"- {result['splitter']}" for result in split_results
    ])

    prompt_template = PromptTemplate(
        input_variables=["file_type", "splitter_list", "split_results", "document_content"],
        template="""
        다음 문서 내용을 기반으로 생성된 질문 목록에 대해 정확하고 구체적인 답변을 제공하세요.
        각 답변은 반드시 문서 내용을 참조해야 하며, JSON 형식으로 작성되어야 합니다.

        문서 내용:
        {document_content}

        사용 가능한 Splitter 목록:
        {splitter_list}

        분석해야 할 내용:
        {split_results}

        아래 형식에 맞게 질문과 답변을 JSON 형식으로 작성하세요:

        [
            {{
                "질문": "질문 내용",
                "답변": "질문에 대한 구체적이고 명확한 답변"
            }},
            {{
                "질문": "질문 내용",
                "답변": "질문에 대한 구체적이고 명확한 답변"
            }}
        ]
        """
    )

    chain = LLMChain(llm=model, prompt=prompt_template)

    result = chain.run({
        "file_type": file_type,
        "splitter_list": splitter_list,
        "split_results": str(split_results)[:1000],
        "document_content": document_content[:2000]  # 문서 내용 최대 2000자로 제한
    })

    return result



def generate_questions(document_content):
    model = ChatOpenAI(model="gpt-4o",temperature=0)
    prompt = PromptTemplate(
        input_variables=["document"],
        template="""
        다음 문서 내용을 기반으로 10개의 질문을 생성해주세요:

        문서 내용:
        {document}

        """
    )
    chain = LLMChain(llm=model, prompt=prompt)
    questions = chain.run({"document": document_content})
    return [q.strip() for q in questions.split("\n") if q.strip()]
