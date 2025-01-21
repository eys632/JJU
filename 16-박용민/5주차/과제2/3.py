import os
from bs4 import BeautifulSoup

def evaluate_html_file(file_path):
    """Evaluates the quality of an HTML file based on its structure and content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse the HTML
        soup = BeautifulSoup(content, 'html.parser')
        
        # Evaluation criteria
        evaluation = {
            'meta_tags': len(soup.find_all('meta')),
            'div_elements': len(soup.find_all('div')),
            'span_elements': len(soup.find_all('span')),
            'page_count': len(soup.find_all('a', attrs={'name': True})),
        }

        # Scoring logic
        total_score = (
            evaluation['meta_tags'] * 2 +
            evaluation['div_elements'] * 1 +
            evaluation['span_elements'] * 0.5 +
            evaluation['page_count'] * 5
        )

        max_score = 100
        final_score = min(total_score, max_score)

        return evaluation, final_score

    except Exception as e:
        print(f"Error during evaluation: {e}")
        return None, 0


def save_evaluation_to_md(evaluation, final_score, output_file):
    """Saves the evaluation result to a markdown file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as md_file:
            md_file.write("# HTML Evaluation Report\n\n")
            md_file.write("## Evaluation Details\n")
            for key, value in evaluation.items():
                md_file.write(f"- **{key.replace('_', ' ').title()}**: {value}\n")

            md_file.write("\n## Final Score\n")
            md_file.write(f"- **Score**: {final_score}/100\n")

        print(f"Evaluation report saved to {output_file}")

    except Exception as e:
        print(f"Error during file save: {e}")


def ask_and_answer():
    """Simulates a Q&A session about the evaluation."""
    questions = [
        "What is the purpose of this evaluation?",
        "How are the scores calculated?",
        "What does a higher score indicate?",
        "What are the limitations of this evaluation?",
    ]

    answers = {
        questions[0]: "The purpose is to assess the structure and content quality of an HTML file based on predefined criteria.",
        questions[1]: "Scores are calculated using the number of meta tags, div elements, span elements, and page anchors in the HTML file, with different weights assigned to each.",
        questions[2]: "A higher score indicates better adherence to the evaluated structural elements, suggesting a well-formed HTML document.",
        questions[3]: "The evaluation is limited to structural elements and does not consider semantic correctness or visual layout.",
    }

    print("\nQ&A Session:\n")
    for question in questions:
        print(f"Q: {question}")
        print(f"A: {answers[question]}\n")


# Example usage
input_file = 'C:/Users/박용민/OneDrive/바탕 화면/비트컴퓨터/5주차/과제2/result3.txt'  # Update with the correct path if needed
output_file = 'C:/Users/박용민/OneDrive/바탕 화면/비트컴퓨터/5주차/과제2/score3.MD'

# Evaluate and save the report
evaluation, score = evaluate_html_file(input_file)
if evaluation:
    save_evaluation_to_md(evaluation, score, output_file)

# Conduct Q&A session
ask_and_answer()
