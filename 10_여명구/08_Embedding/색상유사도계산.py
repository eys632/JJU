import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers.enum import EnumOutputParser
from sklearn.metrics.pairwise import cosine_similarity
from enum import Enum

# 환경변수 로드
load_dotenv()

# OpenAI 임베딩 설정
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)

# 색깔 리스트
colors = ["red", "blue", "green", "yellow", "purple", "orange"]

# 색깔 임베딩 생성
embedded_colors = embeddings.embed_documents(colors)

# 유사도 계산 함수
def find_similar_color(object_description):
    # 객체 설명 임베딩 생성
    object_embedding = embeddings.embed_documents([object_description])[0]
    
    # 유사도 계산
    similarities = cosine_similarity([object_embedding], embedded_colors)[0]
    
    # 각 색깔과의 유사도 출력
    for color, similarity in zip(colors, similarities):
        print(f"{color}: {similarity:.4f}")
    
    # 가장 유사한 색깔 찾기
    most_similar_index = similarities.argmax()
    return colors[most_similar_index], similarities[most_similar_index]

# Enum 클래스 정의
class Colors(Enum):
    RED = "빨간색"
    GREEN = "초록색"
    BLUE = "파란색"
    BROWN = "갈색"
    YELLOW = "노란색"
    BLACK = "검은색"
    WHITE = "하얀색"

# 커스텀 파서 정의
class CustomEnumOutputParser(EnumOutputParser):
    def parse(self, response: str):
        try:
            # EnumOutputParser의 기본 동작 호출
            return super().parse(response)
        except ValueError:
            # 기본 파싱 실패 시 예외 처리
            raise ValueError("비슷한 색깔이 없습니다. 주어진 옵션 중에서 선택할 수 없습니다.")

# 커스텀 파서 생성
parser = CustomEnumOutputParser(enum=Colors)

# 프롬프트 템플릿 생성
prompt = PromptTemplate.from_template(
    """
    다음의 물체는 어떤 색깔인가요?
    최대한 비슷한 색깔을 알려줘. : {options}

    Object: {object}

    Instructions: {instructions}
    """
).partial(
    instructions=parser.get_format_instructions(),
    options=", ".join([color.value for color in Colors])
)

# 프롬프트와 ChatOpenAI, 파서를 연결
chain = prompt | ChatOpenAI(model="gpt-4o") | parser

# 테스트
object_description = "apple"
similar_color, similarity_score = find_similar_color(object_description)
print(f"가장 유사한 색깔: {similar_color} (유사도: {similarity_score:.4f})")

try:
    # 체인 호출 및 결과 반환
    response = chain.invoke({"object": object_description})  # 테스트 케이스
    print(f"프롬프트 결과: {response}")
except ValueError as e:
    # 예외 발생 시 사용자에게 피드백
    print(str(e))

# 최종 결과 결정
if response == Colors.RED.value:
    final_color = "red"
elif response == Colors.GREEN.value:
    final_color = "green"
elif response == Colors.BLUE.value:
    final_color = "blue"
elif response == Colors.BROWN.value:
    final_color = "brown"
elif response == Colors.YELLOW.value:
    final_color = "yellow"
elif response == Colors.BLACK.value:
    final_color = "black"
elif response == Colors.WHITE.value:
    final_color = "white"
else:
    final_color = similar_color

print(f"최종 유사한 색깔: {final_color}")