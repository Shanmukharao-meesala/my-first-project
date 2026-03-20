from flask import Flask, redirect, request, session
import random
import math

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

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(10deg); }
}
@keyframes fall {
    0% { transform: translateY(-100px) rotate(0deg); opacity:1; }
    100% { transform: translateY(100vh) rotate(360deg); opacity:0; }
}
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
@keyframes glow {
    0%, 100% { text-shadow: 0 0 20px #FFD700, 0 0 40px #FFD700; }
    50% { text-shadow: 0 0 40px #FFD700, 0 0 80px #FFD700, 0 0 120px #FFA500; }
}
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
@keyframes blink {
    0%, 100% { opacity:1; }
    50% { opacity:0.3; }
}
@keyframes slideIn {
    from { transform: translateY(-50px); opacity:0; }
    to { transform: translateY(0); opacity:1; }
}

body {
    background: radial-gradient(ellipse at center, #0d0d2b 0%, #1a0533 40%, #0d0d0d 100%);
    min-height: 100vh;
    font-family: Arial, sans-serif;
    color: white;
    overflow-x: hidden;
}

.bg-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.floating-item {
    position: absolute;
    font-size: 1.5em;
    animation: float 3s ease-in-out infinite;
    opacity: 0.3;
}

.falling-item {
    position: absolute;
    font-size: 1.2em;
    animation: fall linear infinite;
    opacity: 0.6;
}

.container {
    max-width: 420px;
    margin: 0 auto;
    padding: 20px 15px;
    text-align: center;
    position: relative;
    z-index: 1;
}

.logo {
    font-size: 2.2em;
    font-weight: bold;
    color: #FFD700;
    animation: glow 2s ease-in-out infinite;
    margin-bottom: 5px;
}

.subtitle {
    color: #c9a0ff;
    font-size: 0.95em;
    margin-bottom: 15px;
}

.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,215,0,0.4);
    border-radius: 20px;
    padding: 20px 15px;
    margin: 12px 0;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(255,215,0,0.1);
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
    transition: all 0.2s;
    position: relative;
    overflow: hidden;
}
.btn:active { transform: scale(0.95); }
.btn-gold {
    background: linear-gradient(45deg, #FFD700, #FFA500);
    color: black;
    box-shadow: 0 0 15px rgba(255,215,0,0.5);
}
.btn-purple {
    background: linear-gradient(45deg, #7B2FBE, #9D4EDD);
    color: white;
    box-shadow: 0 0 15px rgba(157,78,221,0.5);
}
.btn-green {
    background: linear-gradient(45deg, #2d6a4f, #52b788);
    color: white;
    box-shadow: 0 0 15px rgba(82,183,136,0.4);
}
.btn-red {
    background: linear-gradient(45deg, #c1121f, #e63946);
    color: white;
    box-shadow: 0 0 15px rgba(230,57,70,0.4);
}
.btn-outline {
    background: transparent;
    border: 2px solid #FFD700;
    color: #FFD700;
}
.btn-full { width: 90%; display: block; margin: 8px auto; }

input[type=text], input[type=password], input[type=number] {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    border: 2px solid rgba(255,215,0,0.4);
    background: rgba(255,255,255,0.08);
    color: white;
    font-size: 1.1em;
    margin: 8px 0;
    outline: none;
    text-align: center;
}
input::placeholder { color: #888; }
input:focus { border-color: #FFD700; box-shadow: 0 0 10px rgba(255,215,0,0.3); }

.game-code {
    font-size: 3.5em;
    font-weight: bold;
    color: #FFD700;
    letter-spacing: 10px;
    animation: glow 2s ease-in-out infinite;
    font-family: monospace;
    margin: 10px 0;
}

.number-display {
    font-size: 5em;
    color: #FFD700;
    font-weight: bold;
    animation: glow 1s ease-in-out infinite;
    margin: 10px 0;
}

.ticket-table {
    border-collapse: collapse;
    width: 100%;
    margin: 10px auto;
    border-radius: 10px;
    overflow: hidden;
}
.ticket-table td {
    border: 1px solid rgba(255,215,0,0.2);
    text-align: center;
    padding: 10px 2px;
    font-weight: bold;
    font-size: 1em;
}
.td-blank { background: rgba(0,0,0,0.5); }
.td-normal { background: rgba(30,20,60,0.8); color: white; }
.td-ticked {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: black;
    font-size: 1.1em;
    animation: pulse 0.5s ease-in-out;
}
.td-manual-hit {
    background: linear-gradient(135deg, #2d0a5e, #7B2FBE);
    color: #FFD700;
    cursor: pointer;
    border: 1px solid #FFD700 !important;
}

.win-banner {
    background: linear-gradient(45deg, #FFD700, #FFA500);
    color: black;
    padding: 15px;
    border-radius: 15px;
    font-size: 1.2em;
    font-weight: bold;
    margin: 10px 0;
    animation: pulse 0.6s infinite;
    box-shadow: 0 0 30px rgba(255,215,0,0.8);
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
    transition: all 0.3s;
}
.ball-called {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: black;
    box-shadow: 0 0 8px rgba(255,215,0,0.6);
}
.ball-pending { background: rgba(255,255,255,0.07); color: #444; }

.player-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    margin: 5px 0;
    border: 1px solid rgba(255,215,0,0.1);
}
.stats-row {
    display: flex;
    justify-content: space-around;
    margin: 10px 0;
    gap: 8px;
}
.stat-box {
    background: rgba(255,255,255,0.08);
    padding: 8px 10px;
    border-radius: 12px;
    font-size: 0.85em;
    text-align: center;
    flex: 1;
    border: 1px solid rgba(255,215,0,0.2);
}
.stat-box span {
    color: #FFD700;
    font-size: 1.4em;
    font-weight: bold;
    display: block;
}
.winner-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 12px;
    background: rgba(255,215,0,0.08);
    border: 1px solid rgba(255,215,0,0.3);
    border-radius: 12px;
    margin: 6px 0;
}
.error { color: #FF6B6B; margin: 5px 0; font-size: 0.9em; }

.rules-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    margin: 6px 0;
    text-align: left;
    border-left: 3px solid #FFD700;
}

.neon-text {
    color: #00FFFF;
    text-shadow: 0 0 10px #00FFFF, 0 0 20px #00FFFF;
}
</style>
'''

BG_ITEMS = '''
<div class="bg-canvas" id="bgCanvas"></div>
<script>
(function() {
    var canvas = document.getElementById('bgCanvas');
    var items = ['🎰','🎱','⭐','🪙','🎫','🎲','✨','💫','🌟','🎮','🎯','🎊'];
    
    // Floating items
    for(var i = 0; i < 8; i++) {
        var el = document.createElement('div');
        el.className = 'floating-item';
        el.innerText = items[Math.floor(Math.random()*items.length)];
        el.style.left = (Math.random()*90) + '%';
        el.style.top = (Math.random()*80) + '%';
        el.style.animationDelay = (Math.random()*3) + 's';
        el.style.animationDuration = (2+Math.random()*3) + 's';
        canvas.appendChild(el);
    }
    
    // Falling items
    function createFalling() {
        var el = document.createElement('div');
        el.className = 'falling-item';
        el.innerText = items[Math.floor(Math.random()*items.length)];
        el.style.left = (Math.random()*100) + '%';
        el.style.animationDuration = (3+Math.random()*5) + 's';
        el.style.animationDelay = '0s';
        document.getElementById('bgCanvas').appendChild(el);
        setTimeout(function(){ el.remove(); }, 8000);
    }
    setInterval(createFalling, 800);
})();
</script>
'''

@app.route('/')
def intro():
    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shannu Housie 🎰</title>
{STYLES}
<style>
.intro-title {{
    font-size: 1.3em;
    color: #c9a0ff;
    margin-bottom: 5px;
    animation: slideIn 0.5s ease;
}}
</style>
</head><body>
{BG_ITEMS}
<div class="container">
    <div style="font-size:4em; margin:20px 0; animation: spin 3s linear infinite; display:inline-block;">🎰</div>
    <div class="logo">Shannu Housie</div>
    <div class="subtitle">✨ The Ultimate Family Game ✨</div>

    <div class="card">
        <p style="color:#FFD700; font-size:1.1em; margin-bottom:15px;">📋 How to Play:</p>

        <div class="rules-item">
            <span style="font-size:1.5em;">⭐</span>
            <span><b>Jaldi 5</b> — Any 5 numbers tick avvali</span>
        </div>
        <div class="rules-item">
            <span style="font-size:1.5em;">🥇</span>
            <span><b>1st Line</b> — First row complete avvali</span>
        </div>
        <div class="rules-item">
            <span style="font-size:1.5em;">🥈</span>
            <span><b>2nd Line</b> — Second row complete avvali</span>
        </div>
        <div class="rules-item">
            <span style="font-size:1.5em;">🥉</span>
            <span><b>3rd Line</b> — Third row complete avvali</span>
        </div>
        <div class="rules-item">
            <span style="font-size:1.5em;">🎉</span>
            <span><b>Full House</b> — All numbers tick avvali</span>
        </div>

        <div style="margin-top:15px; padding:10px; background:rgba(255,215,0,0.1); border-radius:10px; font-size:0.85em; color:#c9a0ff;">
            🎯 <b>Auto mode:</b> Numbers automatically tick avvutai<br>
            👆 <b>Manual mode:</b> Mee number vinnaaka meeru tick cheyali
        </div>
    </div>

    <a href="/home" class="btn btn-gold btn-full" style="font-size:1.3em; padding:18px;">
        🎮 Let\'s Play!
    </a>

    <div style="color:#444; font-size:0.75em; margin-top:10px;">
        Shannu Housie Game v2.0 🎰
    </div>
</div>
</body></html>'''

@app.route('/home')
def home():
    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shannu Housie 🎰</title>
{STYLES}
</head><body>
{BG_ITEMS}
<div class="container">
    <div style="font-size:3em; margin:15px 0;">🎰</div>
    <div class="logo">Shannu Housie</div>
    <div class="subtitle">🪙 Family Housie Game 🪙</div>

    <div class="card">
        <a href="/host-login" class="btn btn-gold btn-full" style="font-size:1.2em;">
            👑 Leader Entry
        </a>

        <div style="color:#666; margin:10px 0; font-size:0.9em;">— or —</div>

        <p style="color:#FFD700; margin-bottom:8px; font-size:1em;">🎮 Join with Game Code:</p>
        <form method="POST" action="/join-code">
            <input type="text" name="code" placeholder="Enter 5-digit code"
                   maxlength="5" style="font-size:1.5em; letter-spacing:5px; font-family:monospace;">
            <button type="submit" class="btn btn-purple btn-full">🎫 Join Game</button>
        </form>
    </div>

    <a href="/" style="color:#555; font-size:0.85em;">← Rules చూడు</a>
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
<title>Leader Entry 👑</title>
{STYLES}
</head><body>
{BG_ITEMS}
<div class="container">
    <div style="font-size:2.5em; margin:15px 0;">👑</div>
    <div class="logo" style="font-size:1.6em;">Leader Entry</div>
    <div class="subtitle">Game create cheyandi</div>

    <div class="card">
        <form method="POST">
            <p style="color:#FFD700; margin-bottom:5px;">🔐 Password:</p>
            <input type="password" name="password" placeholder="Enter leader password">

            <p style="color:#FFD700; margin:15px 0 5px;">👥 Number of Players (2-20):</p>
            <input type="number" name="max_players" placeholder="Ex: 8" min="2" max="20">

            <p style="color:#FFD700; margin:15px 0 8px;">🎮 Leader kuda play chestara?</p>
            <div style="display:flex; gap:10px; justify-content:center; margin-bottom:10px;">
                <label style="background:rgba(255,255,255,0.08); padding:12px 20px; border-radius:12px; cursor:pointer; border:1px solid rgba(255,215,0,0.3);">
                    <input type="radio" name="host_play" value="yes"> ✅ Yes
                </label>
                <label style="background:rgba(255,255,255,0.08); padding:12px 20px; border-radius:12px; cursor:pointer; border:1px solid rgba(255,215,0,0.3);">
                    <input type="radio" name="host_play" value="no" checked> ❌ No
                </label>
            </div>

            {"<p class='error'>" + error + "</p>" if error else ""}
            <button type="submit" class="btn btn-gold btn-full" style="margin-top:10px; font-size:1.2em;">
                🚀 Create Game
            </button>
        </form>
    </div>
    <a href="/home" style="color:#555; font-size:0.9em;">← Back</a>
</div>
</body></html>'''

@app.route('/join-code', methods=['POST'])
def join_code():
    code = request.form.get('code', '').strip()
    if code == game_state.get('game_code'):
        session['verified_code'] = code
        return redirect('/player-login')
    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wrong Code</title>
{STYLES}
</head><body>
{BG_ITEMS}
<div class="container" style="padding-top:80px;">
    <div style="font-size:4em;">❌</div>
    <div class="logo" style="color:#FF6B6B; margin-top:10px;">Wrong Code!</div>
    <p style="color:#aaa; margin:15px 0;">Code తప్పుగా ఉంది!</p>
    <a href="/home" class="btn btn-gold">← Try Again</a>
</div>
</body></html>'''

@app.route('/player-login', methods=['GET', 'POST'])
def player_login():
    if session.get('verified_code') != game_state.get('game_code'):
        return redirect('/home')

    error = ''
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        tick_mode = request.form.get('tick_mode', 'manual')
        if not name:
            error = 'Name enter చేయండి!'
        elif len(name) > 20:
            error = 'Name too long!'
        elif game_state['max_players'] == 0:
            error = '⏳ Leader ఇంకా game set చేయలేదు!'
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
{BG_ITEMS}
<div class="container">
    <div style="font-size:2.5em; margin:15px 0;">🎫</div>
    <div class="logo" style="font-size:1.5em;">Join Game</div>
    <div style="color:#52b788; margin-bottom:15px; font-size:1em;">✅ Code Verified!</div>

    <div class="card">
        <form method="POST">
            <p style="color:#FFD700; margin-bottom:5px;">👤 Your Name:</p>
            <input type="text" name="name" placeholder="Enter your name" maxlength="20">

            <p style="color:#FFD700; margin:15px 0 10px;">🎯 Tick Mode:</p>
            <div style="display:flex; gap:10px; justify-content:center; margin-bottom:10px;">
                <label style="background:rgba(255,255,255,0.08); padding:12px 20px; border-radius:12px; cursor:pointer; border:1px solid rgba(255,215,0,0.3); flex:1;">
                    <input type="radio" name="tick_mode" value="manual" checked> 👆 Manual
                </label>
                <label style="background:rgba(255,255,255,0.08); padding:12px 20px; border-radius:12px; cursor:pointer; border:1px solid rgba(255,215,0,0.3); flex:1;">
                    <input type="radio" name="tick_mode" value="auto"> ✅ Auto
                </label>
            </div>

            {"<p class='error'>" + error + "</p>" if error else ""}
            <button type="submit" class="btn btn-purple btn-full" style="font-size:1.2em;">
                🎮 Get My Ticket!
            </button>
        </form>
    </div>

    <div style="color:#666; font-size:0.85em;">
        Players: {len(game_state['players'])}/{game_state['max_players']}
    </div>
</div>
</body></html>'''

@app.route('/ticket/<int:num>')
def ticket(num):
    player_name = session.get('player_name')
    if not player_name or player_name not in game_state['players']:
        return redirect('/home')

    player = game_state['players'][player_name]
    if player['ticket'] != num:
        return redirect(f'/ticket/{player["ticket"]}')

    ticket_data = game_state['tickets'][num]
    called = game_state['called_numbers']
    called_set = set(called)
    manual_ticked = set(player.get('manual_ticked', []))
    tick_mode = player.get('tick_mode', 'manual')
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
                ticket_html += f'<td class="td-manual-hit" onclick="manualTick({cell})">👆?</td>'
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

    last_num = called[-1] if called else None
    game_status = "✅ Game Running!" if game_state['game_started'] else "⏳ Waiting to start..."
    ready = player['ready']
    is_host = session.get('role') == 'host'

    # Voice — only speak new number
    voice_js = ""
    if last_num and game_state['game_started']:
        voice_js = f'''
        var lastSpoken = sessionStorage.getItem('lastSpoken');
        if(lastSpoken != '{last_num}') {{
            sessionStorage.setItem('lastSpoken', '{last_num}');
            setTimeout(function() {{
                if('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance('Number {last_num}');
                    msg.lang = 'en-IN';
                    msg.rate = 0.75;
                    msg.pitch = 1;
                    msg.volume = 1;
                    window.speechSynthesis.speak(msg);
                }}
            }}, 500);
        }}'''

    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🎫 {player_name}</title>
<meta http-equiv="refresh" content="3">
{STYLES}
</head><body>
{BG_ITEMS}
<div class="container">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <div class="logo" style="font-size:1.2em;">🎫 {player_name}</div>
        {"<a href='/host' class='btn btn-gold' style='padding:8px 15px; font-size:0.85em;'>🎯 Panel</a>" if is_host else ""}
    </div>

    <div style="color:#c9a0ff; font-size:0.8em; margin-bottom:5px;">
        {game_status} | {"👆 Manual" if tick_mode == "manual" else "✅ Auto"}
    </div>

    {"<div class='number-display'>" + str(last_num) + "</div>" if last_num and game_state['game_started'] else "<div style='height:20px;'></div>"}

    {win_msg}

    <div class="card" style="padding:10px;">
        <table class="ticket-table">{ticket_html}</table>
    </div>

    {"" if game_state['game_started'] else
        ("<form method='POST' action='/ready'><button type='submit' class='btn btn-green btn-full'>✅ I am Ready!</button></form>"
         if not ready else
         "<div class='card' style='color:#52b788; padding:12px; font-size:0.95em;'>✅ Ready! Waiting for others... ⏳</div>")}

    <div class="stats-row">
        <div class="stat-box">Called<span>{len(called)}</span></div>
        <div class="stat-box">Left<span>{90-len(called)}</span></div>
        <div class="stat-box">Ticked<span>{ticked_count}</span></div>
    </div>

    <div style="color:#444; font-size:0.72em; margin-top:5px; word-break:break-all;">
        Last 10: {", ".join(map(str, called[-10:])) if called else "None yet"}
    </div>

    <div style="display:flex; gap:10px; justify-content:center; margin-top:15px;">
        <a href="/home" class="btn btn-outline" style="padding:10px 20px; font-size:0.9em;">🏠 Home</a>
        <a href="/quit" class="btn btn-red" style="padding:10px 20px; font-size:0.9em;">🚪 Quit</a>
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
    return redirect('/home')

@app.route('/manual-tick/<int:num>', methods=['POST'])
def manual_tick(num):
    name = session.get('player_name')
    if name and name in game_state['players']:
        if num in set(game_state['called_numbers']):
            mt = game_state['players'][name]['manual_ticked']
            if num not in mt:
                mt.append(num)
    return 'ok'

@app.route('/quit')
def quit_game():
    name = session.get('player_name')
    if name and name in game_state['players']:
        del game_state['players'][name]
    session.clear()
    return redirect('/home')

@app.route('/host')
def host():
    if session.get('role') != 'host':
        return redirect('/home')

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
            <span style="color:#aaa; font-size:0.8em;">#{data["ticket"]} | {"👆" if data["tick_mode"]=="manual" else "✅"}</span>
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
                <span style="color:#FFD700; font-weight:bold;">🏆 {winners[prize]}</span>
            </div>'''

    last_num = called[-1] if called else "-"
    game_code = game_state.get('game_code', '-----')
    host_ticket = session.get('player_name') == 'Host'

    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Leader Panel 👑</title>
{STYLES}
</head><body>
{BG_ITEMS}
<div class="container">
    <div class="logo" style="font-size:1.5em;">👑 Leader Panel</div>

    <div class="card" style="padding:15px;">
        <p style="color:#aaa; font-size:0.85em; margin-bottom:5px;">🎮 Game Code — Share with players:</p>
        <div class="game-code">{game_code}</div>
        <p style="color:#666; font-size:0.75em;">Players enter this code at home page</p>
    </div>

    <div class="stats-row">
        <div class="stat-box">Players<span>{total_players}/{max_p}</span></div>
        <div class="stat-box">Ready<span>{ready_count}</span></div>
        <div class="stat-box">Called<span>{len(called)}</span></div>
        <div class="stat-box">Left<span>{len(remaining)}</span></div>
    </div>

    {"<div class='win-banner'>🎉 All Players Ready! Call First Number!</div>" if all_ready and not game_state['game_started'] else ""}

    <div class="number-display">{last_num}</div>

    {"<form method='POST' action='/call'><button type='submit' class='btn btn-gold btn-full' style='font-size:1.3em; padding:18px;'>🎲 Call Number</button></form>"
     if remaining and not game_state['game_over'] else ""}

    {"<div class='win-banner'>🎉 All 90 Numbers Called!</div>" if not remaining else ""}

    {"<a href='/ticket/1' class='btn btn-purple btn-full' style='margin-bottom:5px;'>🎫 My Ticket</a>" if host_ticket else ""}

    <form method="POST" action="/end-game">
        <button type="submit" class="btn btn-red btn-full">🚪 End Game</button>
    </form>

    {f"<div class='card'><h3 style='color:#FFD700; margin-bottom:10px;'>🏆 Winners</h3>{winner_html}</div>" if winner_html else ""}

    <div class="card">
        <p style="color:#FFD700; margin-bottom:8px;">👥 Players ({total_players}/{max_p})</p>
        {players_html if players_html else "<p style='color:#555;'>Waiting for players...</p>"}
    </div>

    <div class="called-grid">
        {"".join(f'<div class="num-ball {"ball-called" if n in called else "ball-pending"}">{n}</div>' for n in range(1, 91))}
    </div>

    <br>
    <a href="/reset" style="color:#FF4444; font-size:0.9em; display:block; margin-top:5px;">🔄 Reset / New Game</a>
</div>
</body></html>'''

@app.route('/call', methods=['POST'])
def call_number():
    if session.get('role') != 'host':
        return redirect('/home')
    remaining = [n for n in range(1, 91) if n not in game_state['called_numbers']]
    if remaining:
        num = random.choice(remaining)
        game_state['called_numbers'].append(num)
        game_state['game_started'] = True
    return redirect('/host')

@app.route('/end-game', methods=['POST'])
def end_game():
    if session.get('role') != 'host':
        return redirect('/home')
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
                <span style="font-size:1.1em;">{label}</span>
                <span style="color:#FFD700; font-weight:bold;">🏆 {winners[prize]}</span>
            </div>'''

    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Game Over 🎰</title>
{STYLES}
</head><body>
{BG_ITEMS}
<div class="container">
    <div style="font-size:4em; margin:20px 0;">🎰</div>
    <div class="logo">Game Over!</div>
    <div style="color:#c9a0ff; margin:10px 0 20px; font-size:1em;">
        Thanks for playing Shannu Housie! 🪙
    </div>

    <div class="card">
        <h3 style="color:#FFD700; margin-bottom:15px; font-size:1.3em;">🏆 Final Winners</h3>
        {winner_html if winner_html else "<p style='color:#555;'>No winners recorded</p>"}
    </div>

    <div style="font-size:2.5em; margin:15px 0;">🪙 🎫 🎰 🎫 🪙</div>
    <div style="color:#444; font-size:0.8em; margin-bottom:20px;">Shannu Housie Game v2.0</div>

    <a href="/reset" class="btn btn-gold btn-full" style="font-size:1.2em;">
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
