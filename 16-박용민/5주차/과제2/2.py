import re
import os

def analyze_content(content):
    """
    Analyze the content to extract key points and evaluate self-performance.
    """
    # Identify main topics mentioned
    topics = re.findall(r"[가-힣]+", content)
    unique_topics = set(topics)

    # Self-assessment summary
    summary = {
        "total_topics": len(unique_topics),
        "top_topics": list(unique_topics)[:5],  # Top 5 topics for simplicity
        "effort_assessment": "열심히 노력하고 성장하고자 하는 태도가 돋보입니다.",
        "weakness_assessment": "코드 작성과 관련된 초기 어려움 및 효율적 학습의 필요성을 언급.",
        "strength_assessment": "인공지능, 머신러닝 등 다양한 주제에 대한 관심과 실질적 성과."  
    }
    return summary

def generate_questions(content):
    """
    Generate self-reflection questions from the content.
    """
    questions = [
        "인공지능을 배우면서 가장 어려웠던 점은 무엇인가요?",
        "강화학습 프로젝트에서 개선할 수 있는 부분은 무엇이었나요?",
        "대학생활에서 가장 자랑스러운 성과는 무엇인가요?"
    ]
    return questions

def calculate_score(content):
    """
    Calculate a simple score based on the content length and effort.
    """
    word_count = len(content.split())
    score = min(100, word_count // 10)  # Example scoring mechanism
    return score

def create_markdown(summary, questions, score):
    """
    Create a markdown file with the self-evaluation results.
    """
    md_content = f"""# 자기평가 결과

## 분석 요약
- 총 주제 수: {summary['total_topics']}
- 주요 주제: {', '.join(summary['top_topics'])}

### 강점 분석
{summary['strength_assessment']}

### 약점 분석
{summary['weakness_assessment']}

### 노력 분석
{summary['effort_assessment']}

## 생성된 질문
"""

    for idx, question in enumerate(questions, 1):
        md_content += f"{idx}. {question}\n"

    md_content += f"\n## 최종 점수\n- 점수: {score}/100"

    output_path = "self_evaluation.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Markdown file saved to {os.path.abspath(output_path)}")

if __name__ == "__main__":
    # Load content
    file_path = "C:/Users/박용민/OneDrive/바탕 화면/비트컴퓨터/5주차/과제2/result2.txt"  # Replace with the appropriate file path
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Analyze the content
    summary = analyze_content(content)
    questions = generate_questions(content)
    score = calculate_score(content)

    # Create Markdown file
    create_markdown(summary, questions, score)
