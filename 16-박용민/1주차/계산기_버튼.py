import streamlit as st

# 함수 정의
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "0으로 나눌 수 없습니다."
    return x / y

# Streamlit 앱 제목
st.title("계산기")

# 초기값을 Session State에 저장
if "num1" not in st.session_state:
    st.session_state["num1"] = 0.0
if "num2" not in st.session_state:
    st.session_state["num2"] = 0.0
if "result" not in st.session_state:
    st.session_state["result"] = None

# 숫자 입력 받기
st.session_state["num1"] = st.number_input("첫 번째 숫자를 입력하세요", value=st.session_state["num1"], step=1.0)
st.session_state["num2"] = st.number_input("두 번째 숫자를 입력하세요", value=st.session_state["num2"], step=1.0)

# 버튼 UI 및 동작
st.write("원하는 연산을 선택하세요:")
if st.button("더하기"):
    st.session_state["result"] = add(st.session_state["num1"], st.session_state["num2"])

elif st.button("빼기"):
    st.session_state["result"] = subtract(st.session_state["num1"], st.session_state["num2"])

elif st.button("곱하기"):
    st.session_state["result"] = multiply(st.session_state["num1"], st.session_state["num2"])

elif st.button("나누기"):
    st.session_state["result"] = divide(st.session_state["num1"], st.session_state["num2"])

# 결과 표시
if st.session_state["result"] is not None:
    st.success(f"결과: {st.session_state['result']}")

# 리셋 버튼
if st.button("리셋"):
    # 리셋 시 세션 초기화
    for key in ["num1", "num2", "result"]:
        st.session_state[key] = 0.0 if key != "result" else None
