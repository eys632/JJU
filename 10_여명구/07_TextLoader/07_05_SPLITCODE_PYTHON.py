from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)

PYTHON_CODE = """
def calculator():
    print("계산기 프로그램에 오신 것을 환영합니다!")

    # 첫 번째 숫자 입력
    num1 = float(input("첫 번째 숫자를 입력하세요: "))

    # 두 번째 숫자 입력
    num2 = float(input("두 번째 숫자를 입력하세요: "))

    # 연산 선택
    print("원하는 연산을 선택하세요:")
    print("1. 더하기")
    print("2. 빼기")
    print("3. 곱하기")
    print("4. 나누기")
    operation = input("연산 번호를 입력하세요 (1/2/3/4): ")

    # 계산 수행
    if operation == "1":
        result = num1 + num2
        print(f"결과: {num1} + {num2} = {result}")
    elif operation == "2":
        result = num1 - num2
        print(f"결과: {num1} - {num2} = {result}")
    elif operation == "3":
        result = num1 * num2
        print(f"결과: {num1} × {num2} = {result}")
    elif operation == "4":
        if num2 != 0:
            result = num1 / num2
            print(f"결과: {num1} ÷ {num2} = {result}")
        else:
            print("오류: 0으로 나눌 수 없습니다.")
    else:
        print("잘못된 연산을 선택하셨습니다.")

# 계산기 함수 호출
if __name__ == "__main__":
    calculator()

"""

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=50,
    chunk_overlap=0,
)

python_docs = python_splitter.create_documents([PYTHON_CODE])

for idx, doc in enumerate(python_docs, start=1):
    print(doc.page_content)
