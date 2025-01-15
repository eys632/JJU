import streamlit as st

# 제목 표시
st.title("Streamlit 계산기")

# 입력받기
num1 = st.number_input("첫 번째 숫자를 입력하세요", value=0.0)
num2 = st.number_input("두 번째 숫자를 입력하세요", value=0.0)

# 연산 선택
operation = st.radio("연산을 선택하세요", ("더하기", "빼기", "곱하기", "나누기"))

# 계산 버튼
if st.button("계산"):
    if operation == "더하기":
        result = num1 + num2
        st.success(f"결과: {result}")
    elif operation == "빼기":
        result = num1 - num2
        st.success(f"결과: {result}")
    elif operation == "곱하기":
        result = num1 * num2
        st.success(f"결과: {result}")
    elif operation == "나누기":
        if num2 != 0:
            result = num1 / num2
            st.success(f"결과: {result}")
        else:
            st.error("0으로 나눌 수 없습니다.")
