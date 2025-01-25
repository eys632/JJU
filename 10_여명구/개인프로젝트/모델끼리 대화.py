import openai
import os
from dotenv import load_dotenv
# pip install openai==0.28 버전 맞춰야 함.

load_dotenv()
OPEMAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI API 키 설정
openai.api_key = OPEMAI_API_KEY

def chat_about_make_tool():
    model_a_message = "안녕하세요, 저는 모델 A입니다. 오늘은 Make라는 업무 자동화 툴에 대해 이야기해볼까요?"
    system_a = (
        "당신은 모델 A입니다. Make라는 업무 자동화 툴(이전 이름: Integromat)에 대해 설명하고, "
        "그 기능, 장점, 활용 사례를 논의하세요. 대화가 충분히 진행되면 종료를 제안하세요."
    )
    system_b = (
        "당신은 모델 B입니다. Make라는 업무 자동화 툴에 대해 토론하며, "
        "그 도구의 장단점과 적합한 활용 방안을 이야기하세요. 대화가 더 이상 이어지기 어렵다면 종료를 제안하세요."
    )

    for turn in range(50):  # 최대 50회 반복
        # 모델 A의 응답 생성
        response_a = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_a},
                {"role": "user", "content": model_a_message}
            ]
        )
        model_a_response = response_a['choices'][0]['message']['content']
        print(f"모델 A: {model_a_response}")

        # 모델 A가 대화를 종료할지 판단
        if "종료" in model_a_response or "더 이상 할 말이 없습니다" in model_a_response:
            print("대화가 모델 A에 의해 종료되었습니다.")
            break

        # 모델 B의 응답 생성
        response_b = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_b},
                {"role": "user", "content": model_a_response}
            ]
        )
        model_b_response = response_b['choices'][0]['message']['content']
        print(f"모델 B: {model_b_response}")

        # 모델 B가 대화를 종료할지 판단
        if "종료" in model_b_response or "더 이상 할 말이 없습니다" in model_b_response:
            print("대화가 모델 B에 의해 종료되었습니다.")
            break

        # 다음 대화 준비
        model_a_message = model_b_response

# 시작하기
chat_about_make_tool()
