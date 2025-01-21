from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def analyze_with_gpt(file_type, loader_results_and_split_results):
    model = ChatOpenAI(
        model="gpt-4o",
        max_tokens=2048,
        temperature=0
    )

    loader_results, split_results = loader_results_and_split_results

    # 사용된 splitter 목록 생성
    splitter_list = "\n".join([
        f"- {result['splitter']}" for result in split_results
    ])

    # PromptTemplate 정의
    prompt_template = PromptTemplate(
        input_variables=["file_type", "splitter_list", "split_results"],
        template="""
        당신은 파일 분석 전문가입니다. {file_type} 파일에 대한 분석을 수행해주세요.

        1. 사용한 loader의 목록을 적어주세요:

        2. 사용 가능한 Splitter 목록을 적어주세요:
        {splitter_list}

        3. 분석해야 할 내용:
        {split_results}

        다음 형식으로 상세한 분석 결과를 제공해주세요:

        1. 데이터 요약:
        [텍스트 내용의 주요 포인트 요약]

        2. 데이터 품질 평가 점수:
        | 항목 | 점수 (0~100) | 설명 |
        |------|--------------|------|
        | 텍스트 정확성 | XX | 설명 |
        | 세부 정보 보존 | XX | 설명 |
        | 구조적 완성도 | XX | 설명 |
        | 가독성 | XX | 설명 |
        | 문맥 일관성 | XX | 설명 |

        3. 데이터 품질에 대한 종합적 평가:
        1. loader모델들 중 가장 효과적인 모델:
        2. splitter모델들 중 가장 효과적인 모델:
        [전반적인 데이터 품질에 대한 평가 및 개선점 제안]
        """
    )

    # LLMChain 생성 및 실행
    chain = LLMChain(llm=model, prompt=prompt_template)

    result = chain.run({
        "file_type": file_type,
        "splitter_list": splitter_list,
        "split_results": str(split_results)[:1000]  # 너무 긴 텍스트는 일부만 전달
    })

    return result