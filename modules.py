import datetime
import os

print(datetime.date.today())
print(os.getcwd())

os.makedirs("test-folder", exist_ok=True)
print("folder created!")
