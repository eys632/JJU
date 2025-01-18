# utils/helper_functions.py

def preprocess_text(text: str) -> str:
    """
    텍스트 전처리 함수.
    :param text: 전처리할 텍스트
    :return: 전처리된 텍스트
    """
    return text.lower().strip()
