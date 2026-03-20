from flask import Flask, redirect, request, session
import random

app = Flask(__name__)
app.secret_key = 'shannuhousie2024'

HOST_PASSWORD = "Shannu@0987"

game_state = {
    'tickets': {},
    'called_numbers': [],
    'players': {},
    'max_players': 0,
    'game_started': False,
    'game_over': False,
    'game_code': None,
    'winners': {
        'jaldi5': None,
        'line1': None,
        'line2': None,
        'line3': None,
        'housie': None
    }
}

def generate_ticket():
    ticket = []
    used_numbers = set()
    for row in range(3):
        row_data = []
        blanks = random.sample(range(9), 4)
        for col in range(9):
            if col in blanks:
                row_data.append(0)
            else:
                start = col * 10 + 1
                end = min(start + 9, 91)
                num = random.randint(start, end - 1)
                while num in used_numbers:
                    num = random.randint(start, end - 1)
                used_numbers.add(num)
                row_data.append(num)
        ticket.append(row_data)
    return ticket

STYLES = '''
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
    background: linear-gradient(135deg, #1a0533 0%, #2d0a5e 50%, #1a0533 100%);
    min-height: 100vh;
    font-family: Arial, sans-serif;
    color: white;
}
.container {
    max-width: 420px;
    margin: 0 auto;
    padding: 20px 15px;
    text-align: center;
}
.logo {
    font-size: 2em;
    font-weight: bold;
    color: #FFD700;
    text-shadow: 0 0 20px #FFD700;
    margin-bottom: 5px;
}
.subtitle { color: #c9a0ff; font-size: 0.9em; margin-bottom: 20px; }
.card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,215,0,0.3);
    border-radius: 20px;
    padding: 25px 20px;
    margin: 15px 0;
}
.btn {
    display: inline-block;
    padding: 14px 30px;
    border-radius: 25px;
    font-size: 1.1em;
    font-weight: bold;
    cursor: pointer;
    border: none;
    margin: 8px;
    touch-action: manipulation;
    text-decoration: none;
}
.btn:active { transform: scale(0.95); }
.btn-gold { background: linear-gradient(45deg, #FFD700, #FFA500); color: black; }
.btn-purple { background: linear-gradient(45deg, #7B2FBE, #9D4EDD); color: white; }
.btn-green { background: linear-gradient(45deg, #2d6a4f, #52b788); color: white; }
.btn-red { background: linear-gradient(45deg, #c1121f, #e63946); color: white; }
.btn-full { width: 90%; display: block; margin: 10px auto; }
input[type=text], input[type=password], input[type=number] {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    border: 2px solid rgba(255,215,0,0.4);
    background: rgba(255,255,255,0.1);
    color: white;
    font-size: 1.1em;
    margin: 10px 0;
    outline: none;
    text-align: center;
}
input::placeholder { color: #aaa; }
input:focus { border-color: #FFD700; }
.game-code {
    font-size: 3.5em;
    font-weight: bold;
    color: #FFD700;
    letter-spacing: 8px;
    text-shadow: 0 0 20px #FFD700;
    margin: 10px 0;
    font-family: monospace;
}
.ticket-table {
    border-collapse: collapse;
    width: 100%;
    margin: 10px auto;
}
.ticket-table td {
    border: 1px solid rgba(255,215,0,0.3);
    text-align: center;
    padding: 10px 2px;
    font-weight: bold;
    font-size: 1em;
    border-radius: 4px;
}
.td-blank { background: rgba(0,0,0,0.4); }
.td-normal { background: rgba(255,255,255,0.1); color: white; }
.td-ticked {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: black;
    border-radius: 8px;
}
.td-manual-hit {
    background: linear-gradient(135deg, #52b788, #2d6a4f);
    color: white;
    cursor: pointer;
}
.win-banner {
    background: linear-gradient(45deg, #FFD700, #FFA500);
    color: black;
    padding: 15px;
    border-radius: 15px;
    font-size: 1.2em;
    font-weight: bold;
    margin: 10px 0;
    animation: pulse 0.8s infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.03); }
}
.number-display {
    font-size: 5em;
    color: #FFD700;
    font-weight: bold;
    text-shadow: 0 0 30px #FFD700;
    margin: 10px 0;
}
.called-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    justify-content: center;
    margin: 10px auto;
    max-width: 360px;
}
.num-ball {
    width: 33px;
    height: 33px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-size: 0.78em;
    font-weight: bold;
}
.ball-called { background: linear-gradient(135deg, #FFD700, #FFA500); color: black; }
.ball-pending { background: rgba(255,255,255,0.08); color: #666; }
.player-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: rgba(255,255,255,0.07);
    border-radius: 10px;
    margin: 5px 0;
    font-size: 0.9em;
}
.stats-row {
    display: flex;
    justify-content: space-around;
    margin: 10px 0;
}
.stat-box {
    background: rgba(255,255,255,0.1);
    padding: 8px 15px;
    border-radius: 10px;
    font-size: 0.9em;
    text-align: center;
}
.stat-box span { color: #FFD700; font-size: 1.3em; font-weight: bold; display: block; }
.winner-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 12px;
    background: rgba(255,215,0,0.1);
    border: 1px solid rgba(255,215,0,0.3);
    border-radius: 10px;
    margin: 5px 0;
}
.error { color: #FF4444; margin: 5px 0; font-size: 0.95em; }
</style>
'''

@app.route('/')
def welcome():
    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shannu Housie 🎰</title>
{STYLES}
</head><body>
<div class="container">
    <div style="font-size:3em; margin:15px 0;">🎰</div>
    <div class="logo">Shannu Housie</div>
    <div class="subtitle">🪙 Family Housie Game 🪙</div>
    <div style="font-size:2em; margin:10px 0;">👨‍👩‍👧‍👦</div>

    <div class="card">
        <a href="/host-login" class="btn btn-gold btn-full">🎯 Host Login</a>
        <div style="color:#aaa; margin:10px 0;">— or —</div>
        <form method="POST" action="/join-code">
            <p style="color:#FFD700; margin-bottom:8px;">🎮 Join with Game Code:</p>
            <input type="text" name="code" placeholder="Enter 5-digit code" maxlength="5">
            <button type="submit" class="btn btn-purple btn-full">🎫 Join Game</button>
        </form>
    </div>

    <div style="color:#555; font-size:0.8em; margin-top:15px;">
        Shannu Housie Game v2.0 🎰
    </div>
</div>
</body></html>'''

@app.route('/host-login', methods=['GET', 'POST'])
def host_login():
    error = ''
    if request.method == 'POST':
        pwd = request.form.get('password', '')
        max_p = request.form.get('max_players', '0')
        host_play = request.form.get('host_play', 'no')
        if pwd == HOST_PASSWORD:
            try:
                max_p = int(max_p)
                if 2 <= max_p <= 20:
                    game_state['max_players'] = max_p
                    game_state['game_code'] = str(random.randint(10000, 99999))
                    game_state['called_numbers'] = []
                    game_state['players'] = {}
                    game_state['game_started'] = False
                    game_state['game_over'] = False
                    game_state['tickets'] = {}
                    game_state['winners'] = {
                        'jaldi5': None, 'line1': None,
                        'line2': None, 'line3': None, 'housie': None
                    }
                    session['role'] = 'host'

                    if host_play == 'yes':
                        ticket_num = 1
                        game_state['tickets'][ticket_num] = generate_ticket()
                        game_state['players']['Host'] = {
                            'ticket': ticket_num,
                            'ready': False,
                            'tick_mode': 'auto',
                            'manual_ticked': []
                        }
                        session['player_name'] = 'Host'

                    return redirect('/host')
                else:
                    error = 'Players must be 2-20!'
            except:
                error = 'Enter valid number!'
        else:
            error = '❌ Wrong password!'

    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Host Login 🎯</title>
{STYLES}
</head><body>
<div class="container">
    <div style="font-size:2.5em; margin:10px 0;">🎯</div>
    <div class="logo" style="font-size:1.5em;">Host Login</div>

    <div class="card">
        <form method="POST">
            <p style="color:#FFD700; margin-bottom:5px;">🔐 Password:</p>
            <input type="password" name="password" placeholder="Enter host password">

            <p style="color:#FFD700; margin:15px 0 5px;">👥 Number of Players (2-20):</p>
            <input type="number" name="max_players" placeholder="Ex: 8" min="2" max="20">

            <p style="color:#FFD700; margin:15px 0 8px;">🎮 Host play చేస్తారా?</p>
            <div style="display:flex; gap:10px; justify-content:center; margin-bottom:10px;">
                <label style="background:rgba(255,255,255,0.1); padding:10px 15px; border-radius:10px; cursor:pointer;">
                    <input type="radio" name="host_play" value="yes"> ✅ Yes
                </label>
                <label style="background:rgba(255,255,255,0.1); padding:10px 15px; border-radius:10px; cursor:pointer;">
                    <input type="radio" name="host_play" value="no" checked> ❌ No
                </label>
            </div>

            {"<p class='error'>" + error + "</p>" if error else ""}
            <button type="submit" class="btn btn-gold btn-full" style="margin-top:10px;">
                🚀 Create Game
            </button>
        </form>
    </div>
    <a href="/" style="color:#aaa; font-size:0.9em;">← Back</a>
</div>
</body></html>'''

@app.route('/join-code', methods=['POST'])
def join_code():
    code = request.form.get('code', '').strip()
    if code == game_state.get('game_code'):
        session['verified_code'] = code
        return redirect('/player-login')
    else:
        return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wrong Code</title>
{STYLES}
</head><body>
<div class="container">
    <div style="font-size:3em; margin:30px 0;">❌</div>
    <div class="logo" style="color:#FF4444;">Wrong Code!</div>
    <p style="color:#aaa; margin:15px 0;">Code తప్పుగా ఉంది. మళ్ళీ try చేయండి.</p>
    <a href="/" class="btn btn-gold">← Try Again</a>
</div>
</body></html>'''

@app.route('/player-login', methods=['GET', 'POST'])
def player_login():
    if session.get('verified_code') != game_state.get('game_code'):
        return redirect('/')

    error = ''
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        tick_mode = request.form.get('tick_mode', 'auto')
        if not name:
            error = 'Name enter చేయండి!'
        elif len(name) > 20:
            error = 'Name too long! (max 20)'
        elif game_state['max_players'] == 0:
            error = '⏳ Host ఇంకా game set చేయలేదు!'
        elif len(game_state['players']) >= game_state['max_players']:
            error = '❌ Game Full!'
        elif game_state['game_started']:
            error = '❌ Game already started!'
        elif name.lower() == 'host':
            error = '❌ This name is reserved!'
        elif name in game_state['players']:
            error = '❌ Name already taken!'
        else:
            ticket_num = len(game_state['players']) + 1
            game_state['tickets'][ticket_num] = generate_ticket()
            game_state['players'][name] = {
                'ticket': ticket_num,
                'ready': False,
                'tick_mode': tick_mode,
                'manual_ticked': []
            }
            session['player_name'] = name
            session['role'] = 'player'
            return redirect(f'/ticket/{ticket_num}')

    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Join Game 🎫</title>
{STYLES}
</head><body>
<div class="container">
    <div style="font-size:2.5em; margin:10px 0;">🎫</div>
    <div class="logo" style="font-size:1.5em;">Join Game</div>
    <div style="color:#52b788; margin-bottom:15px;">✅ Code Verified!</div>

    <div class="card">
        <form method="POST">
            <p style="color:#FFD700; margin-bottom:5px;">👤 Your Name:</p>
            <input type="text" name="name" placeholder="Enter your name" maxlength="20">

            <p style="color:#FFD700; margin:15px 0 10px;">🎯 Tick Mode:</p>
            <div style="display:flex; gap:10px; justify-content:center; margin-bottom:10px;">
                <label style="background:rgba(255,255,255,0.1); padding:10px 15px; border-radius:10px; cursor:pointer;">
                    <input type="radio" name="tick_mode" value="auto" checked> ✅ Auto
                </label>
                <label style="background:rgba(255,255,255,0.1); padding:10px 15px; border-radius:10px; cursor:pointer;">
                    <input type="radio" name="tick_mode" value="manual"> 👆 Manual
                </label>
            </div>

            {"<p class='error'>" + error + "</p>" if error else ""}
            <button type="submit" class="btn btn-purple btn-full">
                🎮 Get My Ticket!
            </button>
        </form>
    </div>

    <div style="color:#888; font-size:0.85em;">
        Players: {len(game_state['players'])}/{game_state['max_players']}
    </div>
</div>
</body></html>'''

@app.route('/ticket/<int:num>')
def ticket(num):
    player_name = session.get('player_name')
    if not player_name or player_name not in game_state['players']:
        return redirect('/')

    player = game_state['players'][player_name]
    if player['ticket'] != num:
        return redirect(f'/ticket/{player["ticket"]}')

    ticket_data = game_state['tickets'][num]
    called = game_state['called_numbers']
    called_set = set(called)
    manual_ticked = set(player.get('manual_ticked', []))
    tick_mode = player.get('tick_mode', 'auto')
    winners = game_state['winners']

    effective_ticked = called_set if tick_mode == 'auto' else manual_ticked
    all_nums = [n for row in ticket_data for n in row if n != 0]
    ticked_count = sum(1 for n in all_nums if n in effective_ticked)

    if ticked_count >= 5 and not winners['jaldi5']:
        winners['jaldi5'] = player_name
    for i, row in enumerate(ticket_data):
        row_nums = [n for n in row if n != 0]
        if row_nums and all(n in effective_ticked for n in row_nums):
            key = f'line{i+1}'
            if not winners[key]:
                winners[key] = player_name
    if all(n in effective_ticked for n in all_nums) and not winners['housie']:
        winners['housie'] = player_name

    ticket_html = ""
    for row in ticket_data:
        ticket_html += "<tr>"
        for cell in row:
            if cell == 0:
                ticket_html += '<td class="td-blank"></td>'
            elif tick_mode == 'auto' and cell in called_set:
                ticket_html += f'<td class="td-ticked">✓{cell}</td>'
            elif tick_mode == 'manual' and cell in manual_ticked:
                ticket_html += f'<td class="td-ticked">✓{cell}</td>'
            elif tick_mode == 'manual' and cell in called_set:
                ticket_html += f'<td class="td-manual-hit" onclick="manualTick({cell})">👆{cell}</td>'
            else:
                ticket_html += f'<td class="td-normal">{cell}</td>'
        ticket_html += "</tr>"

    win_msg = ""
    labels = {
        'housie': '🎉 HOUSIE! YOU WIN! 🪙🪙🪙',
        'line3': '🥉 3rd Line Win! 🪙',
        'line2': '🥈 2nd Line Win! 🪙🪙',
        'line1': '🥇 1st Line Win! 🪙',
        'jaldi5': '⭐ Jaldi 5 Win! 🪙'
    }
    for prize, label in labels.items():
        if winners[prize] == player_name:
            win_msg = f'<div class="win-banner">{label}</div>'
            break

    last_num = called[-1] if called else "-"
    game_status = "✅ Game Running!" if game_state['game_started'] else "⏳ Waiting to start..."
    ready = player['ready']

    voice_js = ""
    if called and game_state['game_started']:
        voice_js = f'''
        var lastSpoken = localStorage.getItem('lastSpoken');
        if(lastSpoken != '{last_num}') {{
            localStorage.setItem('lastSpoken', '{last_num}');
            if('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("Number {last_num}");
                msg.lang = 'en-IN';
                msg.rate = 0.8;
                msg.volume = 1;
                window.speechSynthesis.speak(msg);
            }}
        }}'''

    is_host = session.get('role') == 'host'

    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🎫 {player_name}</title>
<meta http-equiv="refresh" content="3">
{STYLES}
</head><body>
<div class="container">
    <div class="logo" style="font-size:1.3em;">🎫 {player_name}</div>
    <div style="color:#c9a0ff; font-size:0.8em; margin-bottom:5px;">
        {game_status} | {tick_mode.upper()} mode
    </div>

    {"<div class='number-display'>" + str(last_num) + "</div>" if game_state['game_started'] else ""}

    {win_msg}

    <table class="ticket-table">{ticket_html}</table>

    {"" if game_state['game_started'] else
        ("<form method='POST' action='/ready'><button type='submit' class='btn btn-green btn-full'>✅ I am Ready!</button></form>"
         if not ready else
         "<div class='card' style='color:#52b788; padding:12px;'>✅ Ready! Waiting for others...</div>")}

    {"<a href='/host' class='btn btn-gold' style='margin-top:5px; font-size:0.9em;'>🎯 Host Panel</a>" if is_host else ""}

    <div class="stats-row" style="margin-top:10px;">
        <div class="stat-box">Called<span>{len(called)}</span></div>
        <div class="stat-box">Left<span>{90-len(called)}</span></div>
        <div class="stat-box">Ticked<span>{ticked_count}</span></div>
    </div>

    <div style="color:#555; font-size:0.72em; margin-top:8px; word-break:break-all;">
        Last 10: {", ".join(map(str, called[-10:])) if called else "None"}
    </div>
</div>
<script>
window.onload = function() {{ {voice_js} }}
function manualTick(num) {{
    fetch('/manual-tick/' + num, {{method:'POST'}})
    .then(() => location.reload());
}}
</script>
</body></html>'''

@app.route('/ready', methods=['POST'])
def ready():
    name = session.get('player_name')
    if name and name in game_state['players']:
        game_state['players'][name]['ready'] = True
        return redirect(f'/ticket/{game_state["players"][name]["ticket"]}')
    return redirect('/')

@app.route('/manual-tick/<int:num>', methods=['POST'])
def manual_tick(num):
    name = session.get('player_name')
    if name and name in game_state['players']:
        if num in set(game_state['called_numbers']):
            mt = game_state['players'][name]['manual_ticked']
            if num not in mt:
                mt.append(num)
    return 'ok'

@app.route('/host')
def host():
    if session.get('role') != 'host':
        return redirect('/')

    called = game_state['called_numbers']
    remaining = [n for n in range(1, 91) if n not in called]
    players = game_state['players']
    winners = game_state['winners']
    ready_count = sum(1 for p in players.values() if p['ready'])
    total_players = len(players)
    max_p = game_state['max_players']
    all_ready = (total_players == max_p and ready_count == total_players and total_players > 0)

    players_html = ""
    for name, data in players.items():
        status = "✅" if data['ready'] else "⏳"
        players_html += f'''
        <div class="player-item">
            <span>{status} {name}</span>
            <span style="color:#aaa; font-size:0.8em;">#{data["ticket"]} | {data["tick_mode"]}</span>
        </div>'''

    winner_html = ""
    labels = {
        'jaldi5': '⭐ Jaldi 5',
        'line1': '🥇 1st Line',
        'line2': '🥈 2nd Line',
        'line3': '🥉 3rd Line',
        'housie': '🎉 Full House'
    }
    for prize, label in labels.items():
        if winners[prize]:
            winner_html += f'''
            <div class="winner-row">
                <span>{label}</span>
                <span style="color:#FFD700;">🏆 {winners[prize]}</span>
            </div>'''

    last_num = called[-1] if called else "-"
    game_code = game_state.get('game_code', '-----')

    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Host Panel 🎯</title>
{STYLES}
</head><body>
<div class="container">
    <div class="logo" style="font-size:1.4em;">🎯 Host Panel</div>

    <div class="card" style="padding:15px;">
        <p style="color:#aaa; font-size:0.85em; margin-bottom:5px;">🎮 Game Code — Share with players:</p>
        <div class="game-code">{game_code}</div>
        <p style="color:#aaa; font-size:0.75em;">Players: enter this code at home page</p>
    </div>

    <div class="stats-row">
        <div class="stat-box">Players<span>{total_players}/{max_p}</span></div>
        <div class="stat-box">Ready<span>{ready_count}</span></div>
        <div class="stat-box">Called<span>{len(called)}</span></div>
    </div>

    {"<div class='win-banner'>🎉 All Players Ready!</div>" if all_ready and not game_state['game_started'] else ""}

    <div class="number-display">{last_num}</div>

    {"<form method='POST' action='/call'><button type='submit' class='btn btn-gold btn-full'>🎲 Call Number</button></form>"
     if remaining and not game_state['game_over'] else ""}

    {"<div class='win-banner'>🎉 All 90 Numbers Called!</div>" if not remaining else ""}

    <form method="POST" action="/end-game">
        <button type="submit" class="btn btn-red btn-full">🚪 End Game</button>
    </form>

    {f"<div class='card'><h3 style='color:#FFD700; margin-bottom:10px;'>🏆 Winners</h3>{winner_html}</div>" if winner_html else ""}

    <div class="card">
        <p style="color:#FFD700; margin-bottom:8px;">
            👥 Players ({total_players}/{max_p})
        </p>
        {players_html if players_html else "<p style='color:#666;'>No players yet...</p>"}
    </div>

    <div class="called-grid">
        {"".join(f'<div class="num-ball {"ball-called" if n in called else "ball-pending"}">{n}</div>' for n in range(1, 91))}
    </div>

    <br>
    <a href="/reset" style="color:#FF4444; font-size:0.9em;">🔄 Reset / New Game</a>
</div>
</body></html>'''

@app.route('/call', methods=['POST'])
def call_number():
    if session.get('role') != 'host':
        return redirect('/')
    remaining = [n for n in range(1, 91) if n not in game_state['called_numbers']]
    if remaining:
        num = random.choice(remaining)
        game_state['called_numbers'].append(num)
        game_state['game_started'] = True
    return redirect('/host')

@app.route('/end-game', methods=['POST'])
def end_game():
    if session.get('role') != 'host':
        return redirect('/')
    game_state['game_over'] = True
    return redirect('/game-over')

@app.route('/game-over')
def game_over_page():
    winners = game_state['winners']
    labels = {
        'jaldi5': '⭐ Jaldi 5',
        'line1': '🥇 1st Line',
        'line2': '🥈 2nd Line',
        'line3': '🥉 3rd Line',
        'housie': '🎉 Full House'
    }
    winner_html = ""
    for prize, label in labels.items():
        if winners[prize]:
            winner_html += f'''
            <div class="winner-row" style="margin:8px 0;">
                <span>{label}</span>
                <span style="color:#FFD700;">🏆 {winners[prize]}</span>
            </div>'''

    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Game Over 🎰</title>
{STYLES}
</head><body>
<div class="container">
    <div style="font-size:3em; margin:20px 0;">🎰</div>
    <div class="logo">Game Over!</div>
    <div style="color:#c9a0ff; margin-bottom:20px;">
        Thanks for playing Shannu Housie! 🪙
    </div>

    <div class="card">
        <h3 style="color:#FFD700; margin-bottom:15px;">🏆 Final Winners</h3>
        {winner_html if winner_html else "<p style='color:#666;'>No winners recorded</p>"}
    </div>

    <div style="font-size:2em; margin:15px 0;">🪙🎫🎰🎫🪙</div>
    <div style="color:#555; font-size:0.8em;">Shannu Housie Game v2.0</div>

    <a href="/reset" class="btn btn-gold" style="margin-top:20px; display:inline-block;">
        🔄 Play Again
    </a>
</div>
</body></html>'''

@app.route('/reset')
def reset():
    game_state['called_numbers'] = []
    game_state['players'] = {}
    game_state['max_players'] = 0
    game_state['game_started'] = False
    game_state['game_over'] = False
    game_state['game_code'] = None
    game_state['tickets'] = {}
    game_state['winners'] = {
        'jaldi5': None, 'line1': None,
        'line2': None, 'line3': None, 'housie': None
    }
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
