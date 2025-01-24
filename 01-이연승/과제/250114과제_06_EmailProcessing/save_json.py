import json

def save_to_json(data, filename):
    """
    데이터를 JSON 파일로 저장
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
