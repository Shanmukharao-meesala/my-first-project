import datetime
import os
try:
    current_date = datetime.datetime.now()
    current_folder = os.getcwd()

    print("Date:", current_date)
    print("Folder:", current_folder)

    with open("system_info.txt", "w") as f:
        f.write("Date: " + str(current_date)+"/n")
        f.write("Folder: " + current_folder)
    with open("system_info.txt", "r") as f:
         data = f.read()
         print("\nFile Content:")
         print(data)
except Exception as e:
       print("Error occured:", e)
