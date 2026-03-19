from flask import Flask, redirect
import random

app = Flask(__name__)

team1 = "RCB 🔴"
team2 = "CSK 🟡"

team1_score = 0
team2_score = 0
balls = 0
innings = 1
game_over = False
last_result = ""
target = 0

def play_ball():
    return random.choice([0, 1, 2, 3, 4, 6, "OUT"])

@app.route('/')
def home():
    global innings, balls, team1_score, team2_score, game_over, target, last_result

    # decide sound
    sound = ""
    if "OUT" in last_result:
        sound = "https://www.soundjay.com/button/beep-10.mp3"
    elif any(x in last_result for x in ["4", "6"]):
        sound = "https://www.soundjay.com/human/applause-8.mp3"
    else:
        sound = "https://www.soundjay.com/button/button-3.mp3"

    if game_over:
        result = "Match Draw 🤝"
        if team1_score > team2_score:
            result = f"{team1} Wins 🏆"
        elif team2_score > team1_score:
            result = f"{team2} Wins 🏆"

        return f"""
        <html>
        <body style="text-align:center; background:black; color:white;">
            <h1>🏏 FINAL RESULT</h1>
            <h2>{team1}: {team1_score}</h2>
            <h2>{team2}: {team2_score}</h2>
            <h1>{result}</h1>

            <audio autoplay>
                <source src="https://www.soundjay.com/human/cheering-1.mp3">
            </audio>

            <a href="/restart">Play Again 🔄</a>
        </body>
        </html>
        """

    team = team1 if innings == 1 else team2
    chase = f"🎯 Target: {target}" if innings == 2 else ""

    return f"""
    <html>
    <head>
    <style>
        body {{
            text-align:center;
            font-family:Arial;
            background-image:url('https://images.unsplash.com/photo-1505842465776-3f6f4c8c6b63');
            background-size:cover;
            color:white;
        }}

        .card {{
            background: rgba(0,0,0,0.7);
            padding:20px;
            border-radius:15px;
            margin:50px;
        }}

        .btn {{
            padding:20px;
            background:orange;
            color:white;
            font-size:22px;
            border-radius:15px;
            text-decoration:none;
        }}
    </style>
    </head>

    <body>

        <div class="card">
            <h1>🏏 IPL GAME</h1>

            <h2>{team} Batting</h2>
            <h3>Balls: {balls}/6</h3>

            <h2>RCB: {team1_score} | CSK: {team2_score}</h2>
            <h3>{chase}</h3>

            <h1>{last_result}</h1>

            <a href="/play" class="btn">🏏 HIT</a>
        </div>

        <audio autoplay>
            <source src="{sound}">
        </audio>

    </body>
    </html>
    """

@app.route('/play')
def play():
    global team1_score, team2_score, balls, innings, game_over, last_result, target

    result = play_ball()
    balls += 1
    last_result = f"{result}"

    if innings == 1:
        if result != "OUT":
            team1_score += result
    else:
        if result != "OUT":
            team2_score += result

    if balls == 6 and innings == 1:
        innings = 2
        balls = 0
        target = team1_score + 1

    elif balls == 6 and innings == 2:
        game_over = True

    if innings == 2 and team2_score >= target:
        game_over = True

    return redirect('/')

@app.route('/restart')
def restart():
    global team1_score, team2_score, balls, innings, game_over, last_result, target
    team1_score = 0
    team2_score = 0
    balls = 0
    innings = 1
    game_over = False
    last_result = ""
    target = 0
    return redirect('/')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)
