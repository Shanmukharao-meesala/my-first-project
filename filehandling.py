
f = open("test.txt", "w")
f.write("hello shanmukha")
f.close()
f = open("test.txt", "r")
content = f.read()
print(content)
f.close()
