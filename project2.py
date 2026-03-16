def add(a, b):
    return a + b
def  subtract(a, b):
     return a - b
def multiply(a, b):
    return a * b


while True:
      print("\nCALCULATOR MENU")
      print("1. ADD")
      print("2. SUBTRACT")
      print("3. MULTIPLY")
      print("4. EXIT")

      choice = input("choose option:")

      if choice == "4":
            print("program ended")
            break

      try:

          a = int(input("enter first number:"))
          b = int(input("enter secound number"))

          if choice == "1":
             result = add(a, b)

          elif choice == "2":
            result = subtract(a, b)

          elif choice == "3":
            result = multiply(a, b)

          else:
             print("invalid option")
             continue
             print("result:",result)

          with open("calculator.txt","a") as f:
                  f.write(f"{a} {choice} {b} = {result}\n")
      except exception as e:
             print("error:",e)
