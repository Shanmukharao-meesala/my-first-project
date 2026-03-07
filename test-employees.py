with open("employees.txt","w") as f:
     f.write("ramana\n")
     f.write("shannu\n")
     f.write("hemansh\n")
try:
   with open("employees.txt","r") as f:
        print(f.read())
except:
       print("file ledhu")  
