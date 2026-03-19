from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    show = False

    if request.method == 'POST':
        name = request.form.get('name')
        if name and name.lower() == "chitti":
            show = True

    return f"""
    <html>
    <head>
    <style>
        body {{
            text-align:center;
            font-family:Arial;
            background: linear-gradient(to right, pink, lavender);
            overflow:hidden;
        }}

        .box {{
            background:white;
            padding:30px;
            border-radius:20px;
            width:300px;
            margin:auto;
            margin-top:100px;
            box-shadow:0px 0px 10px gray;
            position:relative;
            z-index:2;
        }}

        input {{
            padding:10px;
            width:80%;
            border-radius:10px;
        }}

        button {{
            padding:10px 20px;
            margin-top:10px;
            background:pink;
            color:white;
            border:none;
            border-radius:10px;
        }}

        .rain {{
            position:fixed;
            top:0;
            width:100%;
            height:100%;
            pointer-events:none;
        }}

        .flower {{
            position:absolute;
            font-size:25px;
            animation: fall linear infinite;
        }}

        @keyframes fall {{
            0% {{ transform: translateY(-100px); }}
            100% {{ transform: translateY(100vh); }}
        }}

        .result {{
            font-size:28px;
            margin-top:20px;
            animation: pop 1s infinite alternate;
        }}

        @keyframes pop {{
            from {{ transform: scale(1); }}
            to {{ transform: scale(1.2); }}
        }}
    </style>
    </head>

    <body>

        <div class="box">
            <h1>🌸 Chitti Magic 🌸</h1>

            <form method="POST">
                <input name="name" placeholder="Enter name...">
                <br>
                <button>✨ Show Magic</button>
            </form>

            <div class="result">
                {"💖✨🌸🌷💐🌺😍🥰💃👑🌈✨💖" if show else ""}
            </div>
        </div>

        {"<div class='rain' id='rain'></div>" if show else ""}

        {"<audio autoplay loop><source src='https://www.soundjay.com/human/applause-8.mp3'></audio>" if show else ""}

        <script>
        {"let rain = document.getElementById('rain');\
        let flowers = ['🌸','🌷','💐','🌹','🌺','🌼','🌻'];\
        for(let i=0;i<50;i++){\
            let f = document.createElement('div');\
            f.className='flower';\
            f.innerText = flowers[Math.floor(Math.random()*flowers.length)];\
            f.style.left = Math.random()*100+'%';\
            f.style.animationDuration = (3+Math.random()*5)+'s';\
            rain.appendChild(f);\
        }" if show else ""}
        </script>

    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
  
