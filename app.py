from flask import Flask, redirect, request, session, jsonify
import random

app = Flask(__name__)
app.secret_key = 'shannuhousie2024'

HOST_PASSWORD = "Shannu@0987"

game_state = {
    'tickets': {},
    'called_numbers': [],
    'players': {},
    'max_players': 0,
    'tickets_per_player': 1,
    'game_started': False,
    'game_over': False,
    'game_code': None,
    'prizes': {
        'jaldi5': 'Winner!',
        'line1': 'Winner!',
        'line2': 'Winner!',
        'line3': 'Winner!',
        'housie': 'Winner!'
    },
    'winners': {
        'jaldi5': None,
        'line1': None,
        'line2': None,
        'line3': None,
        'housie': None
    },
    'latest_winner': None
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

TICKET_COLORS = [
    ('rgba(255,107,107,0.15)', '#FF6B6B'),
    ('rgba(78,205,196,0.15)', '#4ECDC4'),
    ('rgba(255,215,0,0.15)', '#FFD700'),
    ('rgba(157,78,221,0.15)', '#9D4EDD'),
    ('rgba(82,183,136,0.15)', '#52b788'),
    ('rgba(255,165,0,0.15)', '#FFA500'),
    ('rgba(100,149,237,0.15)', '#6495ED'),
    ('rgba(255,105,180,0.15)', '#FF69B4'),
]

STYLES = '''
<style>
* { margin:0; padding:0; box-sizing:border-box; }

@keyframes float {
    0%,100% { transform: translateY(0px) rotate(0deg); opacity:0.3; }
    50% { transform: translateY(-25px) rotate(15deg); opacity:0.5; }
}
@keyframes fall {
    0% { transform: translateY(-50px) rotate(0deg); opacity:0.8; }
    100% { transform: translateY(110vh) rotate(720deg); opacity:0; }
}
@keyframes pulse {
    0%,100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
@keyframes glow {
    0%,100% { text-shadow: 0 0 20px #FFD700, 0 0 40px #FFD700; }
    50% { text-shadow: 0 0 40px #FFD700, 0 0 80px #FFD700, 0 0 120px #FFA500; }
}
@keyframes slideDown {
    from { transform: translateY(-100px); opacity:0; }
    to { transform: translateY(0); opacity:1; }
}
@keyframes confettiFall {
    0% { transform: translateY(-20px) rotate(0deg); opacity:1; }
    100% { transform: translateY(100vh) rotate(720deg); opacity:0; }
}
@keyframes winnerPop {
    0% { transform: scale(0); opacity:0; }
    60% { transform: scale(1.1); }
    100% { transform: scale(1); opacity:1; }
}
@keyframes numberPop {
    0% { transform: scale(0.5); opacity:0; }
    70% { transform: scale(1.2); }
    100% { transform: scale(1); opacity:1; }
}
@keyframes drumRoll {
    0%,100% { transform: rotate(-5deg); }
    50% { transform: rotate(5deg); }
}

body {
    background: radial-gradient(ellipse at center, #0d0d2b 0%, #1a0533 40%, #0a0a1a 100%);
    min-height: 100vh;
    font-family: Arial, sans-serif;
    color: white;
    overflow-x: hidden;
}
.bg-canvas {
    position: fixed; top:0; left:0;
    width:100%; height:100%;
    pointer-events:none; z-index:0;
    overflow:hidden;
}
.floating-item {
    position:absolute;
    animation: float ease-in-out infinite;
}
.falling-item {
    position:absolute;
    animation: fall linear forwards;
}
.container {
    max-width: 440px;
    margin: 0 auto;
    padding: 15px;
    text-align: center;
    position: relative;
    z-index: 1;
}
.logo {
    font-size: 2em;
    font-weight: bold;
    color: #FFD700;
    animation: glow 2s ease-in-out infinite;
}
.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,215,0,0.3);
    border-radius: 18px;
    padding: 18px 15px;
    margin: 10px 0;
    backdrop-filter: blur(10px);
}
.btn {
    display: inline-block;
    padding: 13px 28px;
    border-radius: 25px;
    font-size: 1.05em;
    font-weight: bold;
    cursor: pointer;
    border: none;
    margin: 6px;
    touch-action: manipulation;
    text-decoration: none;
    transition: all 0.2s;
}
.btn:active { transform: scale(0.95); }
.btn-gold { background: linear-gradient(45deg,#FFD700,#FFA500); color:black; box-shadow:0 0 15px rgba(255,215,0,0.4); }
.btn-purple { background: linear-gradient(45deg,#7B2FBE,#9D4EDD); color:white; box-shadow:0 0 15px rgba(157,78,221,0.4); }
.btn-green { background: linear-gradient(45deg,#2d6a4f,#52b788); color:white; }
.btn-red { background: linear-gradient(45deg,#c1121f,#e63946); color:white; }
.btn-outline { background:transparent; border:2px solid #FFD700; color:#FFD700; }
.btn-blue { background: linear-gradient(45deg,#1a6985,#4ECDC4); color:white; }
.btn-full { width:90%; display:block; margin:8px auto; }

input[type=text],input[type=password],input[type=number] {
    width:100%; padding:13px;
    border-radius:12px;
    border:2px solid rgba(255,215,0,0.4);
    background:rgba(255,255,255,0.08);
    color:white; font-size:1.05em;
    margin:7px 0; outline:none; text-align:center;
}
input::placeholder { color:#666; }
input:focus { border-color:#FFD700; }

.game-code {
    font-size:3.5em; font-weight:bold;
    color:#FFD700; letter-spacing:10px;
    animation: glow 2s infinite; font-family:monospace;
}
.number-display {
    font-size:4.5em; font-weight:bold;
    color:#FFD700; animation: glow 1s infinite, numberPop 0.5s ease;
    margin:5px 0;
}
.ticket-wrap {
    border-radius:15px; overflow:hidden;
    margin:8px 0;
    border:2px solid rgba(255,255,255,0.1);
}
.ticket-label {
    padding:5px; font-size:0.8em;
    font-weight:bold; letter-spacing:1px;
}
.ticket-table { border-collapse:collapse; width:100%; }
.ticket-table td {
    border:1px solid rgba(255,255,255,0.15);
    text-align:center; padding:9px 2px;
    font-weight:bold; font-size:0.95em;
}
.td-blank { background:rgba(0,0,0,0.5); }
.td-normal { background:rgba(20,10,40,0.8); color:white; }
.td-ticked {
    background:linear-gradient(135deg,#FFD700,#FFA500);
    color:black; font-size:1em;
}
.td-manual-hit {
    background:linear-gradient(135deg,#2d0a5e,#7B2FBE);
    color:#FFD700; cursor:pointer;
    border:1px solid #FFD700 !important;
}
.win-banner {
    background:linear-gradient(45deg,#FFD700,#FFA500);
    color:black; padding:12px;
    border-radius:15px; font-size:1.1em;
    font-weight:bold; margin:8px 0;
    animation: pulse 0.6s infinite;
    box-shadow:0 0 25px rgba(255,215,0,0.7);
}
.global-winner {
    position:fixed; top:0; left:0;
    width:100%; z-index:1000;
    background:linear-gradient(45deg,#FFD700,#FFA500);
    color:black; padding:15px;
    text-align:center; font-size:1.2em;
    font-weight:bold;
    animation: slideDown 0.5s ease, winnerPop 0.5s ease;
    box-shadow:0 5px 30px rgba(255,215,0,0.8);
}
.called-grid {
    display:flex; flex-wrap:wrap;
    gap:3px; justify-content:center;
    margin:8px auto; max-width:360px;
}
.num-ball {
    width:31px; height:31px;
    display:flex; align-items:center;
    justify-content:center; border-radius:50%;
    font-size:0.75em; font-weight:bold;
}
.ball-called { background:linear-gradient(135deg,#FFD700,#FFA500); color:black; box-shadow:0 0 6px rgba(255,215,0,0.5); }
.ball-pending { background:rgba(255,255,255,0.06); color:#333; }
.player-item {
    display:flex; justify-content:space-between;
    align-items:center; padding:8px 12px;
    background:rgba(255,255,255,0.05);
    border-radius:10px; margin:4px 0;
    border:1px solid rgba(255,215,0,0.1);
}
.stats-row { display:flex; justify-content:space-around; margin:8px 0; gap:6px; }
.stat-box {
    background:rgba(255,255,255,0.07);
    padding:7px 8px; border-radius:10px;
    font-size:0.8em; text-align:center; flex:1;
    border:1px solid rgba(255,215,0,0.15);
}
.stat-box span { color:#FFD700; font-size:1.3em; font-weight:bold; display:block; }
.winner-row {
    display:flex; justify-content:space-between;
    padding:9px 12px;
    background:rgba(255,215,0,0.08);
    border:1px solid rgba(255,215,0,0.25);
    border-radius:10px; margin:5px 0;
}
.rules-item {
    display:flex; align-items:center; gap:10px;
    padding:9px 10px;
    background:rgba(255,255,255,0.04);
    border-radius:10px; margin:5px 0;
    text-align:left;
    border-left:3px solid #FFD700;
}
.error { color:#FF6B6B; margin:5px 0; font-size:0.9em; }
.prize-input {
    width:100%; padding:8px;
    border-radius:8px;
    border:1px solid rgba(255,215,0,0.3);
    background:rgba(255,255,255,0.08);
    color:white; font-size:0.9em;
    margin:3px 0; text-align:center;
}
</style>
'''

BG_SCRIPT = '''
<div class="bg-canvas" id="bgCanvas"></div>
<script>
(function(){
    var canvas = document.getElementById('bgCanvas');
    var items = ['🎰','🎱','⭐','🪙','🎫','🎲','✨','💫','🌟','🎮','🎯','🎊','🎉','💰'];
    for(var i=0;i<10;i++){
        var el = document.createElement('div');
        el.className='floating-item';
        el.innerText = items[Math.floor(Math.random()*items.length)];
        el.style.cssText = 'left:'+Math.random()*90+'%;top:'+Math.random()*85+'%;font-size:'+(1+Math.random())+'em;animation-duration:'+(2+Math.random()*3)+'s;animation-delay:'+Math.random()*3+'s;';
        canvas.appendChild(el);
    }
    function drop(){
        var el = document.createElement('div');
        el.className='falling-item';
        el.innerText = items[Math.floor(Math.random()*items.length)];
        el.style.cssText = 'left:'+Math.random()*100+'%;font-size:'+(0.8+Math.random()*0.8)+'em;animation-duration:'+(4+Math.random()*5)+'s;';
        canvas.appendChild(el);
        setTimeout(function(){el.remove();},10000);
    }
    setInterval(drop,700);
})();
</script>
'''

CONFETTI_SCRIPT = '''
<script>
function launchConfetti(){
    var colors=['#FFD700','#FF6B6B','#4ECDC4','#9D4EDD','#52b788','#FF69B4'];
    for(var i=0;i<60;i++){
        (function(i){
            setTimeout(function(){
                var el=document.createElement('div');
                el.style.cssText='position:fixed;top:-20px;left:'+Math.random()*100+'%;width:8px;height:8px;background:'+colors[Math.floor(Math.random()*colors.length)]+';border-radius:'+Math.random()*50+'%;z-index:9999;animation:confettiFall '+(1.5+Math.random()*2)+'s linear forwards;';
                document.body.appendChild(el);
                setTimeout(function(){el.remove();},4000);
            },i*50);
        })(i);
    }
}
</script>
'''

@app.route('/')
def intro():
    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shannu Housie 🎰</title>
{STYLES}
</head><body>
{BG_SCRIPT}
<div class="container">
    <div style="font-size:3.5em;margin:15px 0;">🎰</div>
    <div class="logo">Shannu Housie</div>
    <div style="color:#c9a0ff;font-size:0.9em;margin:5px 0 15px;">✨ The Ultimate Family Game ✨</div>

    <div class="card">
        <p style="color:#FFD700;font-size:1.05em;margin-bottom:12px;">📋 Game Rules:</p>
        <div class="rules-item"><span style="font-size:1.4em;">⭐</span><span><b>Jaldi 5</b> — Any 5 numbers tick avvali (First wins!)</span></div>
        <div class="rules-item"><span style="font-size:1.4em;">🥇</span><span><b>1st Line</b> — First row complete avvali</span></div>
        <div class="rules-item"><span style="font-size:1.4em;">🥈</span><span><b>2nd Line</b> — Second row complete avvali</span></div>
        <div class="rules-item"><span style="font-size:1.4em;">🥉</span><span><b>3rd Line</b> — Third row complete avvali</span></div>
        <div class="rules-item"><span style="font-size:1.4em;">🎉</span><span><b>Full House</b> — All numbers tick avvali</span></div>
    </div>

    <div class="card">
        <p style="color:#FFD700;font-size:1em;margin-bottom:10px;">👑 Leader (Host) చేసేవి:</p>
        <div style="text-align:left;font-size:0.9em;color:#c9a0ff;line-height:1.8;">
            🔐 Password తో login avvali<br>
            👥 Max players & tickets per player set cheyali<br>
            💰 Prizes set cheyachu (optional)<br>
            🎮 Game code players ki share cheyali<br>
            🎲 Number call cheyali<br>
            🚪 Game end cheyali
        </div>
    </div>

    <div class="card">
        <p style="color:#FFD700;font-size:1em;margin-bottom:10px;">🎫 Player చేసేవి:</p>
        <div style="text-align:left;font-size:0.9em;color:#c9a0ff;line-height:1.8;">
            🔢 Game code enter cheyali<br>
            👤 Name enter cheyali<br>
            🎯 Auto/Manual mode select cheyali<br>
            ✅ Ready button click cheyali<br>
            🎱 Number announce ayinaaka ticket check cheyali<br>
            🏆 Win aite celebrate cheyali!
        </div>
    </div>

    <div class="card" style="background:rgba(255,215,0,0.05);">
        <p style="color:#aaa;font-size:0.85em;margin-bottom:8px;">🎯 Tick Modes:</p>
        <div style="display:flex;gap:10px;text-align:left;font-size:0.85em;">
            <div style="flex:1;padding:8px;background:rgba(255,255,255,0.05);border-radius:8px;">
                <b style="color:#FFD700;">👆 Manual</b><br>
                <span style="color:#aaa;">Number vinnaaka meeru tap cheyali</span>
            </div>
            <div style="flex:1;padding:8px;background:rgba(255,255,255,0.05);border-radius:8px;">
                <b style="color:#52b788;">✅ Auto</b><br>
                <span style="color:#aaa;">Automatically tick avvutundi</span>
            </div>
        </div>
    </div>

    <a href="/home" class="btn btn-gold btn-full" style="font-size:1.3em;padding:18px;margin-top:10px;">
        🎮 Let\'s Play!
    </a>
    <div style="color:#333;font-size:0.75em;margin-top:8px;">Shannu Housie Game v3.0 🎰</div>
</div>
</body></html>'''

@app.route('/home')
def home():
    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shannu Housie 🎰</title>
{STYLES}
</head><body>
{BG_SCRIPT}
<div class="container">
    <div style="font-size:3em;margin:15px 0;">🎰</div>
    <div class="logo">Shannu Housie</div>
    <div style="color:#c9a0ff;font-size:0.9em;margin:5px 0 20px;">🪙 Family Housie Game 🪙</div>

    <div class="card">
        <a href="/host-login" class="btn btn-gold btn-full" style="font-size:1.2em;">
            👑 Leader Entry
        </a>
        <div style="color:#444;margin:10px 0;font-size:0.9em;">— or —</div>
        <p style="color:#FFD700;margin-bottom:8px;">🎮 Join with Game Code:</p>
        <form method="POST" action="/join-code">
            <input type="text" name="code" placeholder="Enter 5-digit code"
                   maxlength="5" style="font-size:1.8em;letter-spacing:8px;font-family:monospace;">
            <button type="submit" class="btn btn-purple btn-full" style="font-size:1.1em;">
                🎫 Join Game
            </button>
        </form>
    </div>
    <a href="/" style="color:#444;font-size:0.85em;">📋 Rules చూడు</a>
</div>
</body></html>'''

@app.route('/host-login', methods=['GET','POST'])
def host_login():
    error=''
    if request.method=='POST':
        pwd=request.form.get('password','')
        max_p=request.form.get('max_players','0')
        tpp=request.form.get('tickets_per_player','1')
        host_play=request.form.get('host_play','no')
        prizes={
            'jaldi5': request.form.get('prize_jaldi5','Winner!'),
            'line1': request.form.get('prize_line1','Winner!'),
            'line2': request.form.get('prize_line2','Winner!'),
            'line3': request.form.get('prize_line3','Winner!'),
            'housie': request.form.get('prize_housie','Winner!'),
        }
        if pwd==HOST_PASSWORD:
            try:
                max_p=int(max_p)
                tpp=int(tpp)
                if 2<=max_p<=20 and 1<=tpp<=4:
                    game_state.update({
                        'max_players':max_p,
                        'tickets_per_player':tpp,
                        'game_code':str(random.randint(10000,99999)),
                        'called_numbers':[],
                        'players':{},
                        'game_started':False,
                        'game_over':False,
                        'tickets':{},
                        'prizes':prizes,
                        'winners':{'jaldi5':None,'line1':None,'line2':None,'line3':None,'housie':None},
                        'latest_winner':None
                    })
                    session['role']='host'
                    if host_play=='yes':
                        game_state['players']['Host']={
                            'tickets':[],
                            'ready':False,
                            'tick_mode':'auto',
                            'manual_ticked':[],
                            'color_idx':0
                        }
                        for t in range(tpp):
                            tid=f'Host_t{t+1}'
                            game_state['tickets'][tid]=generate_ticket()
                            game_state['players']['Host']['tickets'].append(tid)
                        session['player_name']='Host'
                    return redirect('/host')
                else:
                    error='Players: 2-20, Tickets: 1-4!'
            except:
                error='Valid numbers enter cheyandi!'
        else:
            error='❌ Wrong password!'

    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Leader Entry 👑</title>
{STYLES}
</head><body>
{BG_SCRIPT}
<div class="container">
    <div style="font-size:2.5em;margin:15px 0;">👑</div>
    <div class="logo" style="font-size:1.6em;">Leader Entry</div>
    <div style="color:#c9a0ff;font-size:0.85em;margin-bottom:15px;">Game create cheyandi</div>

    <div class="card">
        <form method="POST">
            <p style="color:#FFD700;margin-bottom:5px;">🔐 Password:</p>
            <input type="password" name="password" placeholder="Leader password">

            <p style="color:#FFD700;margin:12px 0 5px;">👥 Max Players (2-20):</p>
            <input type="number" name="max_players" placeholder="Ex: 8" min="2" max="20">

            <p style="color:#FFD700;margin:12px 0 8px;">🎫 Tickets per Player:</p>
            <div style="display:flex;gap:8px;justify-content:center;margin-bottom:10px;">
                {"".join(f'<label style="background:rgba(255,255,255,0.08);padding:10px 16px;border-radius:10px;cursor:pointer;border:1px solid rgba(255,215,0,0.3);"><input type="radio" name="tickets_per_player" value="{i}"> {i}</label>' for i in range(1,5))}
            </div>

            <p style="color:#FFD700;margin:12px 0 8px;">🏆 Prizes (optional):</p>
            <input class="prize-input" type="text" name="prize_jaldi5" placeholder="⭐ Jaldi 5 prize (e.g. Rs.50)">
            <input class="prize-input" type="text" name="prize_line1" placeholder="🥇 1st Line prize">
            <input class="prize-input" type="text" name="prize_line2" placeholder="🥈 2nd Line prize">
            <input class="prize-input" type="text" name="prize_line3" placeholder="🥉 3rd Line prize">
            <input class="prize-input" type="text" name="prize_housie" placeholder="🎉 Full House prize (e.g. Rs.200)">

            <p style="color:#FFD700;margin:12px 0 8px;">🎮 Leader kuda play chestara?</p>
            <div style="display:flex;gap:10px;justify-content:center;margin-bottom:10px;">
                <label style="background:rgba(255,255,255,0.08);padding:12px 20px;border-radius:12px;cursor:pointer;border:1px solid rgba(255,215,0,0.3);">
                    <input type="radio" name="host_play" value="yes"> ✅ Yes
                </label>
                <label style="background:rgba(255,255,255,0.08);padding:12px 20px;border-radius:12px;cursor:pointer;border:1px solid rgba(255,215,0,0.3);">
                    <input type="radio" name="host_play" value="no" checked> ❌ No
                </label>
            </div>

            {"<p class='error'>"+error+"</p>" if error else ""}
            <button type="submit" class="btn btn-gold btn-full" style="margin-top:10px;font-size:1.2em;">
                🚀 Create Game
            </button>
        </form>
    </div>
    <a href="/home" style="color:#444;font-size:0.9em;">← Back</a>
</div>
</body></html>'''

@app.route('/join-code', methods=['POST'])
def join_code():
    code=request.form.get('code','').strip()
    if code==game_state.get('game_code'):
        session['verified_code']=code
        return redirect('/player-login')
    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Wrong Code</title>
{STYLES}
</head><body>
{BG_SCRIPT}
<div class="container" style="padding-top:80px;">
    <div style="font-size:4em;">❌</div>
    <div class="logo" style="color:#FF6B6B;margin-top:10px;">Wrong Code!</div>
    <p style="color:#aaa;margin:15px 0;">Code తప్పుగా ఉంది!</p>
    <a href="/home" class="btn btn-gold">← Try Again</a>
</div>
</body></html>'''

@app.route('/player-login', methods=['GET','POST'])
def player_login():
    if session.get('verified_code')!=game_state.get('game_code'):
        return redirect('/home')
    error=''
    if request.method=='POST':
        name=request.form.get('name','').strip()
        tick_mode=request.form.get('tick_mode','manual')
        if not name:
            error='Name enter cheyandi!'
        elif len(name)>20:
            error='Name too long!'
        elif game_state['max_players']==0:
            error='⏳ Leader game set cheyyaledu!'
        elif len(game_state['players'])>=game_state['max_players']:
            error='❌ Game Full!'
        elif game_state['game_started']:
            error='❌ Game already started!'
        elif name.lower()=='host':
            error='❌ Reserved name!'
        elif name in game_state['players']:
            error='❌ Name already taken!'
        else:
            color_idx=len(game_state['players'])%len(TICKET_COLORS)
            tpp=game_state['tickets_per_player']
            game_state['players'][name]={
                'tickets':[],
                'ready':False,
                'tick_mode':tick_mode,
                'manual_ticked':[],
                'color_idx':color_idx
            }
            for t in range(tpp):
                tid=f'{name}_t{t+1}'
                game_state['tickets'][tid]=generate_ticket()
                game_state['players'][name]['tickets'].append(tid)
            session['player_name']=name
            session['role']='player'
            return redirect('/play')

    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Join Game 🎫</title>
{STYLES}
</head><body>
{BG_SCRIPT}
<div class="container">
    <div style="font-size:2.5em;margin:15px 0;">🎫</div>
    <div class="logo" style="font-size:1.5em;">Join Game</div>
    <div style="color:#52b788;margin-bottom:15px;">✅ Code Verified!</div>

    <div class="card">
        <form method="POST">
            <p style="color:#FFD700;margin-bottom:5px;">👤 Your Name:</p>
            <input type="text" name="name" placeholder="Enter your name" maxlength="20">

            <p style="color:#FFD700;margin:12px 0 8px;">🎯 Tick Mode:</p>
            <div style="display:flex;gap:10px;justify-content:center;margin-bottom:10px;">
                <label style="background:rgba(255,255,255,0.08);padding:12px 20px;border-radius:12px;cursor:pointer;border:1px solid rgba(255,215,0,0.3);flex:1;">
                    <input type="radio" name="tick_mode" value="manual" checked> 👆 Manual
                </label>
                <label style="background:rgba(255,255,255,0.08);padding:12px 20px;border-radius:12px;cursor:pointer;border:1px solid rgba(255,215,0,0.3);flex:1;">
                    <input type="radio" name="tick_mode" value="auto"> ✅ Auto
                </label>
            </div>

            {"<p class='error'>"+error+"</p>" if error else ""}
            <button type="submit" class="btn btn-purple btn-full" style="font-size:1.2em;">
                🎮 Get My Ticket!
            </button>
        </form>
    </div>
    <div style="color:#555;font-size:0.85em;">Players: {len(game_state["players"])}/{game_state["max_players"]}</div>
</div>
</body></html>'''

@app.route('/play')
def play():
    player_name=session.get('player_name')
    if not player_name or player_name not in game_state['players']:
        return redirect('/home')

    player=game_state['players'][player_name]
    called=game_state['called_numbers']
    called_set=set(called)
    manual_ticked=set(player.get('manual_ticked',[]))
    tick_mode=player.get('tick_mode','manual')
    winners=game_state['winners']
    prizes=game_state.get('prizes',{})
    color_idx=player.get('color_idx',0)
    bg_color,accent=TICKET_COLORS[color_idx%len(TICKET_COLORS)]

    effective_ticked=called_set if tick_mode=='auto' else manual_ticked

    # Check wins for all tickets
    my_wins=[]
    for prize in ['jaldi5','line1','line2','line3','housie']:
        if winners[prize]==player_name:
            my_wins.append(prize)

    all_nums_total=[]
    for tid in player['tickets']:
        td=game_state['tickets'][tid]
        all_nums_total.extend([n for row in td for n in row if n!=0])

    ticked_count=sum(1 for n in all_nums_total if n in effective_ticked)

    # Check wins
    jaldi_count=sum(1 for n in all_nums_total if n in effective_ticked)
    if jaldi_count>=5 and not winners['jaldi5']:
        winners['jaldi5']=player_name
        game_state['latest_winner']={'prize':'jaldi5','name':player_name,'label':'⭐ Jaldi 5','prize_val':prizes.get('jaldi5','')}

    for tid in player['tickets']:
        td=game_state['tickets'][tid]
        for i,row in enumerate(td):
            row_nums=[n for n in row if n!=0]
            if row_nums and all(n in effective_ticked for n in row_nums):
                key=f'line{i+1}'
                if not winners[key]:
                    winners[key]=player_name
                    labels={'line1':'🥇 1st Line','line2':'🥈 2nd Line','line3':'🥉 3rd Line'}
                    game_state['latest_winner']={'prize':key,'name':player_name,'label':labels[key],'prize_val':prizes.get(key,'')}

        all_t=[n for row in td for n in row if n!=0]
        if all_t and all(n in effective_ticked for n in all_t) and not winners['housie']:
            winners['housie']=player_name
            game_state['latest_winner']={'prize':'housie','name':player_name,'label':'🎉 Full House','prize_val':prizes.get('housie','')}

    # Build tickets HTML
    tickets_html=''
    for t_idx,tid in enumerate(player['tickets']):
        td=game_state['tickets'][tid]
        rows_html=''
        for row in td:
            rows_html+='<tr>'
            for cell in row:
                if cell==0:
                    rows_html+='<td class="td-blank"></td>'
                elif tick_mode=='auto' and cell in called_set:
                    rows_html+=f'<td class="td-ticked">✓{cell}</td>'
                elif tick_mode=='manual' and cell in manual_ticked:
                    rows_html+=f'<td class="td-ticked">✓{cell}</td>'
                elif tick_mode=='manual' and cell in called_set:
                    rows_html+=f'<td class="td-manual-hit" onclick="manualTick({cell})">?</td>'
                else:
                    rows_html+=f'<td class="td-normal">{cell}</td>'
            rows_html+='</tr>'
        tickets_html+=f'''
        <div class="ticket-wrap" style="background:{bg_color};border-color:{accent}44;">
            <div class="ticket-label" style="background:{accent}33;color:{accent};">
                🎫 Ticket {t_idx+1} — {player_name}
            </div>
            <table class="ticket-table">{rows_html}</table>
        </div>'''

    # Win messages
    win_msgs=''
    labels_map={'housie':'🎉 HOUSIE! YOU WIN!','line3':'🥉 3rd Line Win!','line2':'🥈 2nd Line Win!','line1':'🥇 1st Line Win!','jaldi5':'⭐ Jaldi 5 Win!'}
    for prize in ['housie','line3','line2','line1','jaldi5']:
        if winners[prize]==player_name:
            pval=prizes.get(prize,'')
            win_msgs+=f'<div class="win-banner">{labels_map[prize]} {pval}</div>'
            break

    last_num=called[-1] if called else None
    game_status='✅ Game Running!' if game_state['game_started'] else '⏳ Waiting to start...'
    ready=player['ready']
    is_host=session.get('role')=='host'

    # Latest winner banner
    lw=game_state.get('latest_winner')
    latest_winner_html=''
    if lw:
        latest_winner_html=f'''
        <div id="winnerBanner" class="global-winner" onclick="this.style.display=\'none\'">
            🏆 {lw["label"]} — {lw["name"]}! {lw.get("prize_val","")} 🎊
        </div>
        <script>
        launchConfetti();
        setTimeout(function(){{
            var b=document.getElementById("winnerBanner");
            if(b)b.style.display="none";
        }},5000);
        </script>'''

    # Voice
    voice_js=''
    if last_num and game_state['game_started']:
        voice_js=f'''
        var ls=sessionStorage.getItem("ls");
        if(ls!="{last_num}"){{
            sessionStorage.setItem("ls","{last_num}");
            setTimeout(function(){{
                if("speechSynthesis" in window){{
                    window.speechSynthesis.cancel();
                    var m=new SpeechSynthesisUtterance("Number {last_num}");
                    m.lang="en-IN"; m.rate=0.75; m.pitch=1; m.volume=1;
                    window.speechSynthesis.speak(m);
                }}
            }},300);
        }}'''

    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>🎫 {player_name}</title>
<meta http-equiv="refresh" content="3">
{STYLES}
{CONFETTI_SCRIPT}
</head><body>
{BG_SCRIPT}
{latest_winner_html}
<div class="container">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <div style="font-size:1.1em;font-weight:bold;color:{accent};">🎫 {player_name}</div>
        {"<a href='/host' class='btn btn-gold' style='padding:7px 14px;font-size:0.8em;'>👑 Panel</a>" if is_host else ""}
    </div>

    <div style="color:#888;font-size:0.78em;margin-bottom:5px;">
        {game_status} | {"👆 Manual" if tick_mode=="manual" else "✅ Auto"}
    </div>

    {"<div class='number-display'>"+str(last_num)+"</div>" if last_num and game_state["game_started"] else "<div style='height:15px'></div>"}

    {win_msgs}

    {tickets_html}

    {"" if game_state["game_started"] else
        ("<form method='POST' action='/ready'><button type='submit' class='btn btn-green btn-full'>✅ I am Ready!</button></form>"
         if not ready else
         "<div class='card' style='color:#52b788;padding:10px;font-size:0.9em;'>✅ Ready! Waiting... ⏳</div>")}

    <div class="stats-row" style="margin-top:8px;">
        <div class="stat-box">Called<span>{len(called)}</span></div>
        <div class="stat-box">Left<span>{90-len(called)}</span></div>
        <div class="stat-box">Ticked<span>{ticked_count}</span></div>
    </div>

    <div style="color:#333;font-size:0.7em;margin-top:5px;word-break:break-all;">
        Last 10: {", ".join(map(str,called[-10:])) if called else "None yet"}
    </div>

    <div style="display:flex;gap:8px;justify-content:center;margin-top:12px;">
        <a href="/home" class="btn btn-outline" style="padding:9px 18px;font-size:0.85em;">🏠 Home</a>
        <a href="/quit" class="btn btn-red" style="padding:9px 18px;font-size:0.85em;">🚪 Quit</a>
    </div>
</div>
<script>
window.onload=function(){{{voice_js}}}
function manualTick(num){{
    fetch("/manual-tick/"+num,{{method:"POST"}}).then(function(){{location.reload();}});
}}
</script>
</body></html>'''

@app.route('/ready', methods=['POST'])
def ready():
    name=session.get('player_name')
    if name and name in game_state['players']:
        game_state['players'][name]['ready']=True
    return redirect('/play')

@app.route('/manual-tick/<int:num>', methods=['POST'])
def manual_tick(num):
    name=session.get('player_name')
    if name and name in game_state['players']:
        if num in set(game_state['called_numbers']):
            mt=game_state['players'][name]['manual_ticked']
            if num not in mt:
                mt.append(num)
    return 'ok'

@app.route('/quit')
def quit_game():
    name=session.get('player_name')
    if name and name in game_state['players']:
        del game_state['players'][name]
    session.clear()
    return redirect('/home')

@app.route('/host')
def host():
    if session.get('role')!='host':
        return redirect('/home')

    called=game_state['called_numbers']
    remaining=[n for n in range(1,91) if n not in called]
    players=game_state['players']
    winners=game_state['winners']
    prizes=game_state.get('prizes',{})
    ready_count=sum(1 for p in players.values() if p['ready'])
    total=len(players)
    max_p=game_state['max_players']
    all_ready=(total==max_p and ready_count==total and total>0)

    players_html=''.join(f'''
    <div class="player-item">
        <span>{"✅" if d["ready"] else "⏳"} {n}</span>
        <span style="color:#aaa;font-size:0.8em;">{len(d["tickets"])}🎫 | {"👆" if d["tick_mode"]=="manual" else "✅"}</span>
    </div>''' for n,d in players.items())

    labels={'jaldi5':'⭐ Jaldi 5','line1':'🥇 1st Line','line2':'🥈 2nd Line','line3':'🥉 3rd Line','housie':'🎉 Full House'}
    winner_html=''.join(f'''
    <div class="winner-row">
        <span>{labels[p]}</span>
        <span style="color:#FFD700;font-weight:bold;">🏆 {w} — {prizes.get(p,"")}</span>
    </div>''' for p,w in winners.items() if w)

    last_num=called[-1] if called else '-'
    code=game_state.get('game_code','-----')
    host_ticket=session.get('player_name')=='Host'

    lw=game_state.get('latest_winner')
    lw_html=''
    if lw:
        lw_html=f'''
        <div id="winnerBanner" class="global-winner" onclick="this.style.display=\'none\'">
            🏆 {lw["label"]} — {lw["name"]}! {lw.get("prize_val","")} 🎊
        </div>
        <script>
        launchConfetti();
        setTimeout(function(){{var b=document.getElementById("winnerBanner");if(b)b.style.display="none";}},5000);
        </script>'''

    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Leader Panel 👑</title>
{STYLES}
{CONFETTI_SCRIPT}
</head><body>
{BG_SCRIPT}
{lw_html}
<div class="container">
    <div class="logo" style="font-size:1.4em;">👑 Leader Panel</div>

    <div class="card" style="padding:12px;">
        <p style="color:#aaa;font-size:0.82em;margin-bottom:5px;">🎮 Game Code:</p>
        <div class="game-code">{code}</div>
        <p style="color:#555;font-size:0.72em;">Share this with players</p>
    </div>

    <div class="stats-row">
        <div class="stat-box">Players<span>{total}/{max_p}</span></div>
        <div class="stat-box">Ready<span>{ready_count}</span></div>
        <div class="stat-box">Called<span>{len(called)}</span></div>
        <div class="stat-box">Left<span>{len(remaining)}</span></div>
    </div>

    {"<div class='win-banner'>🎉 All Players Ready! Start!</div>" if all_ready and not game_state['game_started'] else ""}

    <div class="number-display">{last_num}</div>

    {"<form method='POST' action='/call'><button type='submit' class='btn btn-gold btn-full' style='font-size:1.3em;padding:16px;'>🎲 Call Number</button></form>" if remaining and not game_state['game_over'] else ""}
    {"<div class='win-banner'>🎉 All 90 Numbers Called!</div>" if not remaining else ""}

    {"<a href='/play' class='btn btn-purple btn-full'>🎫 My Ticket</a>" if host_ticket else ""}

    <form method="POST" action="/end-game">
        <button type="submit" class="btn btn-red btn-full">🚪 End Game</button>
    </form>

    {f"<div class='card'><h3 style='color:#FFD700;margin-bottom:8px;'>🏆 Winners</h3>{winner_html}</div>" if winner_html else ""}

    <div class="card">
        <p style="color:#FFD700;margin-bottom:8px;">👥 Players ({total}/{max_p})</p>
        {players_html if players_html else "<p style='color:#444;'>Waiting for players...</p>"}
    </div>

    <div class="called-grid">
        {"".join(f'<div class="num-ball {"ball-called" if n in called else "ball-pending"}">{n}</div>' for n in range(1,91))}
    </div>

    <br>
    <a href="/reset" style="color:#FF4444;font-size:0.9em;display:block;margin-top:5px;">🔄 Reset / New Game</a>
</div>
</body></html>'''

@app.route('/call', methods=['POST'])
def call_number():
    if session.get('role')!='host':
        return redirect('/home')
    remaining=[n for n in range(1,91) if n not in game_state['called_numbers']]
    if remaining:
        num=random.choice(remaining)
        game_state['called_numbers'].append(num)
        game_state['game_started']=True
        game_state['latest_winner']=None
    return redirect('/host')

@app.route('/end-game', methods=['POST'])
def end_game():
    if session.get('role')!='host':
        return redirect('/home')
    game_state['game_over']=True
    return redirect('/game-over')

@app.route('/game-over')
def game_over_page():
    winners=game_state['winners']
    prizes=game_state.get('prizes',{})
    labels={'jaldi5':'⭐ Jaldi 5','line1':'🥇 1st Line','line2':'🥈 2nd Line','line3':'🥉 3rd Line','housie':'🎉 Full House'}
    winner_html=''.join(f'''
    <div class="winner-row" style="margin:7px 0;">
        <span style="font-size:1em;">{labels[p]}</span>
        <div style="text-align:right;">
            <div style="color:#FFD700;font-weight:bold;">🏆 {w}</div>
            {"<div style='color:#52b788;font-size:0.8em;'>"+prizes[p]+"</div>" if prizes.get(p) else ""}
        </div>
    </div>''' for p,w in winners.items() if w)

    return f'''<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Game Over 🎰</title>
{STYLES}
{CONFETTI_SCRIPT}
</head><body>
{BG_SCRIPT}
<div class="container">
    <div style="font-size:3.5em;margin:20px 0;">🎰</div>
    <div class="logo">Game Over!</div>
    <div style="color:#c9a0ff;margin:8px 0 20px;font-size:0.95em;">Thanks for playing Shannu Housie! 🪙</div>

    <div class="card">
        <h3 style="color:#FFD700;margin-bottom:12px;font-size:1.2em;">🏆 Final Winners</h3>
        {winner_html if winner_html else "<p style='color:#444;'>No winners recorded</p>"}
    </div>

    <div style="font-size:2em;margin:15px 0;">🪙 🎫 🎰 🎫 🪙</div>
    <div style="color:#333;font-size:0.75em;margin-bottom:20px;">Shannu Housie Game v3.0</div>

    <a href="/reset" class="btn btn-gold btn-full" style="font-size:1.2em;">🔄 Play Again</a>
</div>
<script>window.onload=function(){{launchConfetti();}}</script>
</body></html>'''

@app.route('/reset')
def reset():
    game_state.update({
        'called_numbers':[],'players':{},'max_players':0,
        'tickets_per_player':1,'game_started':False,'game_over':False,
        'game_code':None,'tickets':{},
        'prizes':{'jaldi5':'Winner!','line1':'Winner!','line2':'Winner!','line3':'Winner!','housie':'Winner!'},
        'winners':{'jaldi5':None,'line1':None,'line2':None,'line3':None,'housie':None},
        'latest_winner':None
    })
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)