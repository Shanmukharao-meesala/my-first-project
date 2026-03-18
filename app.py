from flask import Flask

app = Flask(__name__)

students = [
   {"name": "shannu", "marks": 75},
   {"name": "chitti", "marks": 89},
   {"name": "bhavani", "marks": 80},
   {"name": "sai", "marks": 29},
]

@app.route('/')
def home():
    result = ""
    for student in students:
        if student["marks"] >= 40:
           status = "pass good luck"
        else:
             status = "fail better luck next time"
        result += f"{student['name']} - {student['marks']} - {status}<br>"
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

 
