import streamlit as st

st.title("계산기")

num1 = st.number_input("첫 번째 숫자를 입력", value=0.0)
op = st.selectbox("연산자를 선택하시오", ["+", "-", "*", "/"])
num2 = st.number_input("두 번째 숫자를 입력", value=0.0)

if st.button("계산하기"):
    if op == '+':
        result = num1 + num2
    elif op == '-':
        result = num1 - num2
    elif op == '*':
        result = num1 * num2
    elif op == '/':
        if num2 != 0:
            result = num1 / num2
        else:
            result = "0으로 나눌 수 없습니다."
    st.write("결과:", result)
    st.image("marmot.jpg", caption="Here you go~")
