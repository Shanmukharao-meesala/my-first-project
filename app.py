
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Snake Game 🐍</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            font-family: Arial;
            color: white;
        }
        h1 { font-size: 2em; margin-bottom: 10px; }
        #score { font-size: 1.5em; margin-bottom: 10px; color: #FFD700; }
        canvas {
            border: 3px solid #FFD700;
            border-radius: 10px;
            background: #0a0a1a;
        }
        .controls {
            display: grid;
            grid-template-columns: repeat(3, 60px);
            gap: 5px;
            margin-top: 15px;
        }
        .btn {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            font-size: 1.5em;
            padding: 15px;
            border-radius: 10px;
            cursor: pointer;
        }
        .btn:active { background: #FFD700; color: black; }
        #startBtn {
            margin-top: 15px;
            padding: 12px 30px;
            background: #FFD700;
            color: black;
            border: none;
            border-radius: 25px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>🐍 Snake Game</h1>
    <div id="score">Score: 0</div>
    <canvas id="canvas" width="300" height="300"></canvas>
    <div class="controls">
        <div></div>
        <button class="btn" onclick="changeDir(0,-1)">⬆️</button>
        <div></div>
        <button class="btn" onclick="changeDir(-1,0)">⬅️</button>
        <button class="btn" onclick="changeDir(0,1)">⬇️</button>
        <button class="btn" onclick="changeDir(1,0)">➡️</button>
    </div>
    <button id="startBtn" onclick="startGame()">▶️ Start</button>

<script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const box = 20;
    let snake, food, dx, dy, score, gameLoop;

    function startGame() {
        snake = [{x:7, y:7}];
        dx = 1; dy = 0;
        score = 0;
        placeFood();
        document.getElementById('score').innerText = 'Score: 0';
        if(gameLoop) clearInterval(gameLoop);
        gameLoop = setInterval(update, 150);
        document.getElementById('startBtn').innerText = '🔄 Restart';
    }

    function placeFood() {
        food = {
            x: Math.floor(Math.random() * 15),
            y: Math.floor(Math.random() * 15)
        };
    }

    function update() {
        const head = {x: snake[0].x + dx, y: snake[0].y + dy};

        if(head.x < 0 || head.x >= 15 || head.y < 0 || head.y >= 15) {
            gameOver(); return;
        }
        if(snake.some(s => s.x === head.x && s.y === head.y)) {
            gameOver(); return;
        }

        snake.unshift(head);

        if(head.x === food.x && head.y === food.y) {
            score += 10;
            document.getElementById('score').innerText = 'Score: ' + score;
            placeFood();
        } else {
            snake.pop();
        }

        draw();
    }

    function draw() {
        ctx.fillStyle = '#0a0a1a';
        ctx.fillRect(0, 0, 300, 300);

        // Food
        ctx.fillStyle = '#FF4444';
        ctx.beginPath();
        ctx.arc(food.x * box + box/2, food.y * box + box/2, box/2 - 2, 0, Math.PI*2);
        ctx.fill();

        // Snake
        snake.forEach((s, i) => {
            ctx.fillStyle = i === 0 ? '#00FF00' : '#00CC00';
            ctx.fillRect(s.x * box + 1, s.y * box + 1, box - 2, box - 2);
        });
    }

    function changeDir(x, y) {
        if(x !== 0 && dx !== 0) return;
        if(y !== 0 && dy !== 0) return;
        dx = x; dy = y;
    }

    function gameOver() {
        clearInterval(gameLoop);
        ctx.fillStyle = 'rgba(0,0,0,0.7)';
        ctx.fillRect(0, 0, 300, 300);
        ctx.fillStyle = 'white';
        ctx.font = 'bold 30px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Game Over!', 150, 130);
        ctx.font = '20px Arial';
        ctx.fillText('Score: ' + score, 150, 170);
    }

    // Keyboard support
    document.addEventListener('keydown', e => {
        if(e.key === 'ArrowLeft') changeDir(-1, 0);
        if(e.key === 'ArrowRight') changeDir(1, 0);
        if(e.key === 'ArrowUp') changeDir(0, -1);
        if(e.key === 'ArrowDown') changeDir(0, 1);
    });
</script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
