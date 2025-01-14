import google.generativeai as genai

# API 키를 직접 입력
api_key = "AIzaSyAFtlXiEWy_2Jc_5nf-dahslO0Ov9RmMv0"
genai.configure(api_key=api_key)

# 모델 설정
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",  # 필요에 따라 수정 가능
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

# 채팅 세션 시작
chat_session = model.start_chat(
  history=[]  # 대화 이력을 여기에 넣을 수 있습니다
)

# 메시지 전송 및 응답 받기
response = chat_session.send_message("안녕녕")

# 응답 출력
print(response.text)
