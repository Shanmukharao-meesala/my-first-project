from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>🐍 Snake Game by Shannu</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: linear-gradient(135deg, #0d2b0d, #1a4a1a, #0d3320);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-family: Arial, sans-serif;
            color: white;
        }
        h1 { font-size: 1.8em; color: #7FFF00; text-shadow: 0 0 10px #00FF00; margin-bottom: 5px; }
        .subtitle { font-size: 0.8em; color: #aaa; margin-bottom: 10px; }
        #scoreBoard { display: flex; gap: 20px; margin-bottom: 8px; font-size: 1em; }
        .score-item { background: rgba(0,0,0,0.4); padding: 5px 15px; border-radius: 20px; color: #FFD700; font-weight: bold; }
        canvas { border: 3px solid #7FFF00; border-radius: 10px; box-shadow: 0 0 20px #00FF0055; display: block; }
        .controls { display: grid; grid-template-columns: repeat(3, 65px); gap: 8px; margin-top: 15px; }
        .btn {
            background: rgba(0,100,0,0.6);
            border: 2px solid #7FFF00;
            color: #7FFF00;
            font-size: 1.6em;
            padding: 15px;
            border-radius: 10px;
            cursor: pointer;
            user-select: none;
            -webkit-user-select: none;
            touch-action: manipulation;
        }
        .btn:active { background: #7FFF00; color: black; }
        #settingsScreen {
            position: fixed; top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.9);
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            z-index: 100;
        }
        .settings-box {
            background: linear-gradient(135deg, #1a3a1a, #0d2b0d);
            border: 2px solid #7FFF00;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            width: 280px;
        }
        .settings-box h2 { color: #7FFF00; font-size: 1.5em; margin-bottom: 20px; }
        .speed-btns { display: flex; gap: 10px; justify-content: center; margin: 15px 0; }
        .speed-btn {
            padding: 10px 20px;
            border: 2px solid #7FFF00;
            background: transparent;
            color: #7FFF00;
            border-radius: 20px;
            cursor: pointer;
            font-size: 1em;
            touch-action: manipulation;
        }
        .speed-btn.active { background: #7FFF00; color: black; font-weight: bold; }
        #startBtn {
            margin-top: 20px; padding: 15px 40px;
            background: #7FFF00; color: black;
            border: none; border-radius: 25px;
            font-size: 1.2em; font-weight: bold;
            cursor: pointer; touch-action: manipulation;
        }
        #starTimer { width: 300px; height: 8px; background: rgba(255,255,255,0.2); border-radius: 5px; margin: 5px 0; display: none; }
        #starTimerBar { height: 100%; background: #FFD700; border-radius: 5px; transition: width 0.1s linear; }
        #pauseBtn {
            margin-top: 10px; padding: 8px 25px;
            background: rgba(255,255,255,0.1);
            border: 2px solid #7FFF00; color: #7FFF00;
            border-radius: 20px; font-size: 1em;
            cursor: pointer; touch-action: manipulation;
        }
    </style>
</head>
<body>

<div id="settingsScreen">
    <div class="settings-box">
        <h2>🐍 Snake Game</h2>
        <p style="color:#aaa; margin-bottom:15px;">by Shannu</p>
        <p style="color:#7FFF00; margin-bottom:10px;">Select Speed:</p>
        <div class="speed-btns">
            <button class="speed-btn" onclick="setSpeed(\'easy\', this)">Easy</button>
            <button class="speed-btn active" onclick="setSpeed(\'medium\', this)">Medium</button>
            <button class="speed-btn" onclick="setSpeed(\'hard\', this)">Hard</button>
        </div>
        <p style="color:#aaa; font-size:0.85em; margin-top:10px;">
            ⭐ Every 5 foods = Bonus Star!<br>
            Grab it fast for more points!
        </p>
        <button id="startBtn" onclick="startGame()">▶️ Start Game</button>
    </div>
</div>

<h1>🐍 Snake Game</h1>
<p class="subtitle">Created by Shannu 🌿</p>
<div id="scoreBoard">
    <div class="score-item">Score: <span id="scoreVal">0</span></div>
    <div class="score-item">Best: <span id="bestVal">0</span></div>
</div>
<div id="starTimer"><div id="starTimerBar" style="width:100%"></div></div>
<canvas id="canvas" width="300" height="300"></canvas>

<div class="controls">
    <div></div>
    <button class="btn" id="btnUp">⬆️</button>
    <div></div>
    <button class="btn" id="btnLeft">⬅️</button>
    <button class="btn" id="btnDown">⬇️</button>
    <button class="btn" id="btnRight">➡️</button>
</div>
<button id="pauseBtn" style="display:none" onclick="togglePause()">⏸ Pause</button>

<script>
    const canvas = document.getElementById(\'canvas\');
    const ctx = canvas.getContext(\'2d\');
    const box = 20;
    const GRID = 15;

    let snake, food, star, dx, dy, score, bestScore = 0;
    let gameLoop, foodCount, starActive, starInterval;
    let paused = false;
    let speed = 150;
    let speedMultiplier = 1;

    // Button controls - touch friendly
    function setupButtons() {
        const buttons = {
            \'btnUp\':    () => { if(dy === 0) { dx=0; dy=-1; } },
            \'btnDown\':  () => { if(dy === 0) { dx=0; dy=1; } },
            \'btnLeft\':  () => { if(dx === 0) { dx=-1; dy=0; } },
            \'btnRight\': () => { if(dx === 0) { dx=1; dy=0; } }
        };
        Object.entries(buttons).forEach(([id, fn]) => {
            const btn = document.getElementById(id);
            btn.addEventListener(\'touchstart\', (e) => { e.preventDefault(); fn(); }, {passive: false});
            btn.addEventListener(\'mousedown\', fn);
        });
    }

    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    function playSound(freq, duration, type=\'sine\') {
        try {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.frequency.value = freq;
            osc.type = type;
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        } catch(e) {}
    }

    function playStarSound() {
        playSound(880, 0.1);
        setTimeout(() => playSound(1100, 0.1), 100);
        setTimeout(() => playSound(1320, 0.2), 200);
    }
    function playEatSound() { playSound(440, 0.1, \'square\'); }
    function playGameOverSound() {
        playSound(200, 0.3, \'sawtooth\');
        setTimeout(() => playSound(150, 0.5, \'sawtooth\'), 300);
    }

    function setSpeed(s, btn) {
        document.querySelectorAll(\'.speed-btn\').forEach(b => b.classList.remove(\'active\'));
        btn.classList.add(\'active\');
        if(s === \'easy\') { speed = 220; speedMultiplier = 0.7; }
        else if(s === \'medium\') { speed = 150; speedMultiplier = 1; }
        else { speed = 80; speedMultiplier = 1.5; }
    }

    function startGame() {
        document.getElementById(\'settingsScreen\').style.display = \'none\';
        document.getElementById(\'pauseBtn\').style.display = \'inline-block\';
        document.getElementById(\'pauseBtn\').innerText = \'⏸ Pause\';
        document.getElementById(\'pauseBtn\').onclick = togglePause;
        snake = [{x:7, y:7}];
        dx = 1; dy = 0;
        score = 0; foodCount = 0;
        starActive = false; star = null;
        paused = false;
        placeFood();
        updateScoreDisplay();
        if(gameLoop) clearInterval(gameLoop);
        if(starInterval) clearInterval(starInterval);
        gameLoop = setInterval(update, speed);
        setupButtons();
    }

    function placeFood() {
        do {
            food = { x: Math.floor(Math.random()*GRID), y: Math.floor(Math.random()*GRID) };
        } while(snake.some(s => s.x===food.x && s.y===food.y));
    }

    function placeStar() {
        starActive = true;
        do {
            star = { x: Math.floor(Math.random()*GRID), y: Math.floor(Math.random()*GRID), timeLeft: 5 };
        } while(snake.some(s => s.x===star.x && s.y===star.y));

        document.getElementById(\'starTimer\').style.display = \'block\';
        document.getElementById(\'starTimerBar\').style.width = \'100%\';

        let elapsed = 0;
        if(starInterval) clearInterval(starInterval);
        starInterval = setInterval(() => {
            elapsed += 0.1;
            star.timeLeft = 5 - elapsed;
            document.getElementById(\'starTimerBar\').style.width = ((5-elapsed)/5*100) + \'%\';
            if(elapsed >= 5) {
                clearInterval(starInterval);
                starActive = false; star = null;
                document.getElementById(\'starTimer\').style.display = \'none\';
            }
        }, 100);
    }

    function getStarPoints(t) {
        if(t >= 4.5) return 50;
        if(t >= 3.5) return 40;
        if(t >= 2.5) return 30;
        if(t >= 1.5) return 20;
        return 10;
    }

    function updateScoreDisplay() {
        document.getElementById(\'scoreVal\').innerText = score;
        document.getElementById(\'bestVal\').innerText = bestScore;
    }

    function update() {
        if(paused) return;
        const head = {x: snake[0].x+dx, y: snake[0].y+dy};
        if(head.x<0||head.x>=GRID||head.y<0||head.y>=GRID) { gameOver(); return; }
        if(snake.some(s => s.x===head.x && s.y===head.y)) { gameOver(); return; }
        snake.unshift(head);

        if(starActive && star && head.x===star.x && head.y===star.y) {
            score += Math.round(getStarPoints(star.timeLeft) * speedMultiplier);
            playStarSound();
            clearInterval(starInterval);
            starActive = false; star = null;
            document.getElementById(\'starTimer\').style.display = \'none\';
            updateScoreDisplay();
            snake.pop();
        } else if(head.x===food.x && head.y===food.y) {
            score += Math.round(10 * speedMultiplier);
            foodCount++;
            playEatSound();
            placeFood();
            if(foodCount % 5 === 0) placeStar();
            updateScoreDisplay();
        } else {
            snake.pop();
        }
        if(score > bestScore) bestScore = score;
        draw();
    }

    function draw() {
        ctx.fillStyle = \'#0a1a0a\';
        ctx.fillRect(0, 0, 300, 300);

        ctx.fillStyle = \'rgba(100,200,100,0.08)\';
        for(let i=0;i<GRID;i++) for(let j=0;j<GRID;j++) {
            ctx.beginPath();
            ctx.arc(i*box+box/2, j*box+box/2, 1, 0, Math.PI*2);
            ctx.fill();
        }

        // Food
        ctx.fillStyle = \'#FF3333\';
        ctx.beginPath();
        ctx.arc(food.x*box+box/2, food.y*box+box/2, box/2-2, 0, Math.PI*2);
        ctx.fill();
        ctx.fillStyle = \'#00AA00\';
        ctx.fillRect(food.x*box+box/2-1, food.y*box+1, 2, 4);

        // Star
        if(starActive && star) drawStar(star.x*box+box/2, star.y*box+box/2, 5, box/2-1, box/4);

        // Snake
        const colors = [\'#FF6B6B\',\'#FFD93D\',\'#6BCB77\',\'#4D96FF\',\'#C77DFF\'];
        snake.forEach((s, i) => {
            ctx.fillStyle = i===0 ? \'#00FF00\' : colors[i % colors.length];
            ctx.beginPath();
            ctx.roundRect(s.x*box+1, s.y*box+1, box-2, box-2, 4);
            ctx.fill();
        });

        // Eyes
        ctx.fillStyle = \'black\';
        let ex = snake[0].x*box + (dx===1 ? box-5 : dx===-1 ? 3 : box/2-3);
        let ey = snake[0].y*box + (dy===1 ? box-5 : dy===-1 ? 3 : box/2-3);
        ctx.beginPath(); ctx.arc(ex, ey, 2, 0, Math.PI*2); ctx.fill();
    }

    function drawStar(cx, cy, spikes, outerR, innerR) {
        let rot = Math.PI/2*3, step = Math.PI/spikes;
        ctx.beginPath(); ctx.moveTo(cx, cy-outerR);
        for(let i=0;i<spikes;i++) {
            ctx.lineTo(cx+Math.cos(rot)*outerR, cy+Math.sin(rot)*outerR); rot+=step;
            ctx.lineTo(cx+Math.cos(rot)*innerR, cy+Math.sin(rot)*innerR); rot+=step;
        }
        ctx.closePath();
        ctx.fillStyle = \'#FFD700\'; ctx.fill();
        ctx.strokeStyle = \'#FFA500\'; ctx.lineWidth=1; ctx.stroke();
    }

    function togglePause() {
        paused = !paused;
        document.getElementById(\'pauseBtn\').innerText = paused ? \'▶️ Resume\' : \'⏸ Pause\';
    }

    function gameOver() {
        clearInterval(gameLoop); clearInterval(starInterval);
        if(score > bestScore) bestScore = score;
        playGameOverSound();

        ctx.fillStyle = \'rgba(0,0,0,0.75)\'; ctx.fillRect(0,0,300,300);
        ctx.fillStyle = \'#FF4444\'; ctx.font = \'bold 28px Arial\'; ctx.textAlign = \'center\';
        ctx.fillText(\'Game Over! 💀\', 150, 110);
        ctx.fillStyle = \'#FFD700\'; ctx.font = \'20px Arial\';
        ctx.fillText(\'Score: \' + score, 150, 150);
        ctx.fillStyle = \'#7FFF00\'; ctx.font = \'16px Arial\';
        ctx.fillText(\'Best: \' + bestScore, 150, 180);
        ctx.fillStyle = \'white\'; ctx.font = \'14px Arial\';
        ctx.fillText(\'Tap Restart to play again\', 150, 220);

        const pb = document.getElementById(\'pauseBtn\');
        pb.innerText = \'🔄 Restart\';
        pb.onclick = () => {
            document.getElementById(\'settingsScreen\').style.display = \'flex\';
            pb.style.display = \'none\';
        };
    }

    document.addEventListener(\'keydown\', e => {
        if(e.key===\'ArrowLeft\' && dx!==1) { dx=-1; dy=0; }
        if(e.key===\'ArrowRight\' && dx!==-1) { dx=1; dy=0; }
        if(e.key===\'ArrowUp\' && dy!==1) { dx=0; dy=-1; }
        if(e.key===\'ArrowDown\' && dy!==-1) { dx=0; dy=1; }
        if(e.key===\' \') togglePause();
    });

    let touchX, touchY;
    canvas.addEventListener(\'touchstart\', e => { touchX=e.touches[0].clientX; touchY=e.touches[0].clientY; }, {passive:true});
    canvas.addEventListener(\'touchend\', e => {
        let tx=e.changedTouches[0].clientX-touchX;
        let ty=e.changedTouches[0].clientY-touchY;
        if(Math.abs(tx)>Math.abs(ty)) {
            if(tx>0 && dx!==1) { dx=1; dy=0; }
            else if(tx<0 && dx!==-1) { dx=-1; dy=0; }
        } else {
            if(ty>0 && dy!==1) { dx=0; dy=1; }
            else if(ty<0 && dy!==-1) { dx=0; dy=-1; }
        }
    }, {passive:true});
</script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
