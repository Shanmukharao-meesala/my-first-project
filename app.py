from flask import Flask

app = Flask(__name__)

def add(a, b):
    return a + b

def substract(a, b):
    return a - b

def multiply(a, b):
    return a * b

@app.route('/')
def home():
    result_add = add(10, 5)
    result_sub = substract(10, 5)
    result_mul = multiply(10, 5)
    return f"Addition: {result_add}, Subtraction: {result-sub}, Multiply: {result-mul}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
 
