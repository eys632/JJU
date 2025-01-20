from sentence_transformers import SentenceTransformer, util

def generate_embeddings(texts, model_name="BAAI/bge-m3", api_key=None):
    """
    텍스트 임베딩 생성 함수.
    :param texts: 텍스트 조각 리스트
    :param model_name: 사용할 HuggingFace 모델 이름
    :param api_key: HuggingFace API 키
    :return: 생성된 텍스트 임베딩
    """
    if api_key:
        model = SentenceTransformer(model_name, use_auth_token=api_key)
    else:
        model = SentenceTransformer(model_name)
    return model.encode(texts, convert_to_tensor=True)

def find_most_similar(question, document_chunks, embeddings, model_name="BAAI/bge-m3", api_key=None):
    """
    질문과 문서 조각 간 유사도 계산 함수.
    :param question: 질문 문자열
    :param document_chunks: 문서 조각 리스트
    :param embeddings: 문서 조각 임베딩
    :param model_name: 사용할 HuggingFace 모델 이름
    :param api_key: HuggingFace API 키
    :return: 가장 유사한 문서 조각과 유사도 점수
    """
    if api_key:
        model = SentenceTransformer(model_name, use_auth_token=api_key)
    else:
        model = SentenceTransformer(model_name)
    question_embedding = model.encode(question, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(question_embedding, embeddings)
    best_match_idx = scores.argmax().item()
    return document_chunks[best_match_idx], scores[0][best_match_idx].item()
