from datetime import datetime

def save_result(file_path: str, question: str, answer: str):
    """결과를 지정된 경로의 파일에 저장"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n\n## Run Result at {}\n".format(timestamp))
        f.write(f"**Question**: {question}\n\n**Answer**:\n{answer}\n")
