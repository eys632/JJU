import google.generativeai as genai

# API 설정
genai.configure(api_key="AIzaSyAUw7PRvxZgtMcP-5EDPA_5uF_63rRbG3g")

# 생성 설정
generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# 모델 초기화
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# 채팅 세션 시작
chat_session = model.start_chat(history=[])

print("AI와 대화를 시작합니다. 종료하려면 'exit'를 입력하세요.\n")

# 대화 루프
while True:
    user_input = input("You: ")  # 사용자 입력 받기
    if user_input.lower() == "exit":  # "exit" 입력 시 종료
        print("대화를 종료합니다.")
        break

    # 메시지 전송 및 응답 받기
    response = chat_session.send_message(user_input)
    print(f"AI: {response.text}\n")  # AI 응답 출력
