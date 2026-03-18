from flask import Flask, redirect
import random

app = Flask(__name__)

# Game variables
team1_score = 0
team2_score = 0
balls = 0
innings = 1   # 1 = RCB, 2 = CSK
game_over = False

def play_ball():
    return random.choice([0, 1, 2, 4, 6, "OUT"])

@app.route('/')
def home():
    global innings, balls, team1_score, team2_score, game_over

    if game_over:
        if team1_score > team2_score:
            result = "🔴 RCB Wins!"
        elif team2_score > team1_score:
            result = "🟡 CSK Wins!"
        else:
            result = "🤝 Match Draw!"

        return f"""
        <html><body style="text-align:center; background:black; color:white;">
        <h1>🏏 IPL Match Result</h1>
        <h2>RCB: {team1_score}</h2>
        <h2>CSK: {team2_score}</h2>
        <h1>{result}</h1>
        <a href="/restart">🔄 Play Again</a>
        </body></html>
        """

    team = "🔴 RCB Batting" if innings == 1 else "🟡 CSK Batting"

    return f"""
    <html>
    <body style="text-align:center; background:lightgreen;">
        <h1>🏏 IPL Game</h1>
        <h2>{team}</h2>
        <h3>Balls: {balls}/6</h3>
        <h2>RCB: {team1_score} | CSK: {team2_score}</h2>

        <a href="/play" style="
            padding:15px;
            background:orange;
            color:white;
            border-radius:10px;
            text-decoration:none;
        ">🏏 Play Ball</a>
    </body>
    </html>
    """

@app.route('/play')
def play():
    global team1_score, team2_score, balls, innings, game_over

    result = play_ball()
    balls += 1

    if innings == 1:
        if result != "OUT":
            team1_score += result
    else:
        if result != "OUT":
            team2_score += result

    # Switch innings
    if balls == 6:
        balls = 0
        if innings == 1:
            innings = 2
        else:
            game_over = True

    # Chase win early
    if innings == 2 and team2_score > team1_score:
        game_over = True

    return f"""
    <html>
    <body style="text-align:center; background:yellow;">
        <h1>Result: {result}</h1>
        <h2>RCB: {team1_score} | CSK: {team2_score}</h2>
        <a href="/">➡️ Continue</a>
    </body>
    </html>
    """

@app.route('/restart')
def restart():
    global team1_score, team2_score, balls, innings, game_over
    team1_score = 0
    team2_score = 0
    balls = 0
    innings = 1
    game_over = False
    return redirect('/')

if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000, debug=True)


