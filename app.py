def add(a, b):
     return a + b

def subtraction(a, b):
     return a - b

def multiply(a, b):
     return a * b

print("CALCULATOR APP")

a = int(input("Enter first number: "))
b = int(input("Enter secound number: "))

print("addition:", add(a, b))
print("subtraction", subtraction(a, b))
print("multiplication", multiply(a, b))
