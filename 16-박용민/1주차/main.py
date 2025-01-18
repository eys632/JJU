import streamlit as st
def add(x, y):
      return x + y
def subtract(x, y):
  return x - y
def sultply(x, y):
  return x * y
def divide(x, y):
  return x / y
print("골라주세요")
print("1. 더하기")
print("2. 빼기")
print("3. 곱하기")
print("4. 나누기")

st.button("리셋", type="primary")
if st.button("1"):
    num1 = float(input("enter first number "))
    num2 = float(input("enter second number "))
    st.write(add(num1, num2))
elif st.button("2"):
    num1 = float(input("enter first number "))
    num2 = float(input("enter second number "))
    st.write(subtract(num1, num2))
elif st.button("3"):
    num1 = float(input("enter first number "))
    num2 = float(input("enter second number "))
    st.write(sultply(num1, num2))
elif st.button("4"):
    num1 = float(input("enter first number "))
    num2 = float(input("enter second number "))
    st.write(divide(num1, num2))
else:
      print("invalid input")
