from flask import Flask, request, redirect

app = Flask(__name__)

tasks = []

@app.route('/')
def home():
    task_list = "".join(f"<li>{t} <a href='/delete/{i}'>❌</a></li>" 
                        for i, t in enumerate(tasks))
    return f"""
        <h1>To-Do List</h1>
        <form method="POST" action="/add">
            <input name="task" placeholder="New task">
            <button>Add</button>
        </form>
        <ul>{task_list}</ul>
    """

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        tasks.append(task)
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    tasks.pop(index)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


