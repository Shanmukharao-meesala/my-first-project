from flask import Flask
import random

app = Flask(__name__)

emojis = ["😂", "😜", "🤪", "😎", "🥳", "🐵", "🐶", "🦄", "🐸"]

messages = [
    "Why did the cat laugh? Because it saw a funny mouse! 😆",
    "Why did the banana slip? Because it was too funny! 🍌😂",
    "Why is the monkey happy? It found a banana! 🐵",
    "Why is the dog laughing? It heard a joke! 🐶😄",
    "Unicorn says: Stay magical! 🦄✨",
    "Frog says: Ribbit and laugh! 🐸😂"
]

@app.route('/')
def home():
    emoji = random.choice(emojis)
    message = random.choice(messages)

    return f"""
    <html>
    <head>
        <title>Funny Cartoon App</title>
    </head>

    <body style="text-align:center; font-family: Comic Sans MS; background:yellow;">

        <h1>😂 Funny Cartoon World 😂</h1>

        <div style="font-size:80px;">
            {emoji}
        </div>

        <h2>{message}</h2>

        <br>

        <a href="/" style="
            padding:15px 25px;
            background:red;
            color:white;
            text-decoration:none;
            border-radius:10px;
            font-size:20px;
        ">
            Click Me For Fun 😄
        </a>

    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
