import yaml
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate

def parse_answer(answer_text):
    """answer 필드를 중간 답변과 최종 답변으로 분리"""
    parts = answer_text.strip().split("\n최종 답변은:")
    intermediate_answers = parts[0].strip() if len(parts) > 1 else ""
    final_answer = parts[1].strip() if len(parts) > 1 else ""
    return intermediate_answers, final_answer

def load_prompt_from_yaml(yaml_file_path: str):
    """YAML 파일에서 데이터를 읽어 Prompt를 생성"""
    with open(yaml_file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    examples_data = []
    for example in data.get("examples", []):
        question = example.get("question", "")
        raw_answer = example.get("answer", "")
        intermediate_answers, final_answer = parse_answer(raw_answer)
        examples_data.append({
            "question": question,
            "intermediate_answers": intermediate_answers,
            "final_answer": final_answer,
        })
    
    # Prompt 템플릿
    example_prompt = PromptTemplate.from_template(
        """
        Question:
        {question}
        
        Additional Questions and Intermediate Answers:
        {intermediate_answers}
        
        Final Answer:
        {final_answer}
        """
    )
    
    # Suffix 추가 (질문을 입력하는 영역)
    suffix = "\nProvide the most accurate and concise answer based on the examples above."

    # FewShotPromptTemplate 생성
    prompt = FewShotPromptTemplate(
        examples=examples_data,
        example_prompt=example_prompt,
        suffix=suffix,
        input_variables=["question"],
    )
    return prompt
