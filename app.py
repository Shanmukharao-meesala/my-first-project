from flask import Flask, request, redirect, url_for

app = Flask(__name__)

tasks = []

@app.route('/')
def home():
    task_list = ""
    for i, task in enumerate(tasks):
        task_list += f"""
        <li>
            {i+1}. {task}
            <a href="/delete/{i}" style="color:red; text-decoration:none;"> ❌ </a>
        </li>
        """

    return f"""
    <html>
    <head>
        <title>To-Do App</title>
    </head>
    <body style="font-family: Arial; text-align: center;">

        <h1>📝 My To-Do List</h1>

        <form method="POST" action="/add">
            <input name="task" placeholder="Enter new task" required>
            <button>Add Task</button>
        </form>

        <ul style="list-style: none;">
            {task_list}
        </ul>

    </body>
    </html>
    """

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        tasks.append(task)
    return redirect(url_for('home'))

@app.route('/delete/<int:index>')
def delete(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
