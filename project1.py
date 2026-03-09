def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b

try:
    a = int(input("Enter first number: "))
    b = int(input("Enter secound number: "))


    result1 = add(a, b)
    result2 = subtract(a, b)
    result3 = multiply(a, b)


    print("ADDITION:", result1)
    print("SUBTRACTION:", result2)
    print("MULTIPLY:", result3)

    with open("calculator.txt","w") as f:
         f.write(f"Addition: {result1}\n")
         f.write(f"Subtraction: {result2}\n")
         f.write(f"Multiply: {result3}\n")

except  Exception as e:
        print("Error:",e)
