from flask import Flask
import random

app = Flask(__name__)

colors = ["red", "blue", "green", "yellow", "purple", "orange"]

@app.route('/')
def home():
    color = random.choice(colors)

    return f"""
    <html>
    <head>
        <title>Fun Color Game</title>
    </head>

    <body style="text-align:center; font-family: Arial; background:{color}; color:white;">

        <h1>🎨 Click for Magic Color 🎨</h1>

        <p style="font-size:20px;">Background Color: {color.upper()}</p>

        <a href="/" style="
            padding:15px 25px;
            background:white;
            color:black;
            text-decoration:none;
            border-radius:10px;
            font-size:18px;
        ">
            Click Me 😄
        </a>

    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
