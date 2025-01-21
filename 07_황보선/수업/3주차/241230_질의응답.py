# import os
# import google.generativeai as genai

# os.environ["GEMINI_API_KEY"]= ''
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# # Create the model
# generation_config = {
#   "temperature": 1,
#   "top_p": 0.95,
#   "top_k": 64,
#   "max_output_tokens": 8192,
#   "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#   model_name="gemini-2.0-flash-thinking-exp-1219",
#   generation_config=generation_config,
# )

# chat_session = model.start_chat(
#   history=[
#   ]
# )

# response = chat_session.send_message("발이 네개인 동물 3종류 나열")

# print(response.text)

# filepath: /c:/Users/user/Desktop/비트교육_방학특강/241230_질의응답.py


# flask를 사용하여 웹 인터페이스 구현
# from flask import Flask, request, render_template
# import os
# import google.generativeai as genai

# app = Flask(__name__)

# os.environ["GEMINI_API_KEY"] = ''
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# generation_config = {
#   "temperature": 1,
#   "top_p": 0.95,
#   "top_k": 64,
#   "max_output_tokens": 8192,
#   "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#   model_name="gemini-2.0-flash-thinking-exp-1219",
#   generation_config=generation_config,
# )

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/ask', methods=['POST'])
# def ask():
#     question = request.form['question']
#     chat_session = model.start_chat(history=[])
#     response = chat_session.send_message(question)
#     return render_template('index.html', question=question, answer=response.text)

# if __name__ == '__main__':
#     app.run(debug=True)

