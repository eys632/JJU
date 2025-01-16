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

choice = input("enter choice(1/2/3/4) ")
num1 = float(input("enter first number "))
num2 = float(input("enter second number "))
if choice == "1":
  print(num1, "+", num2, "=", add(num1, num2))
elif choice == "2":
  print(num1, "-", num2, "=", subtract(num1, num2))
elif choice == "3":
  print(num1, "x", num2, "=", sultply(num1, num2))
elif choice == "4":
  print(num1, "/", num2, "=", divide(num1, num2))
else:
  print("invalid input")