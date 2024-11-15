from flask import Flask, request, redirect, render_template_string
import hashlib
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)

#Ping to keep server alive
def keep_alive():
    try:
        requests.get("0.0.0.0:10000", timeout=10) 
        response.raise_for_status()
        print("Ping successful:", response.status_code)
    except Exception as e:
        print("Error pinging the server:", e)

#ping every 14 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(keep_alive, 'interval', minutes=2)
scheduler.start()

@app.route('/')
def forward():
    video = request.args.get('video')
    ctrl = request.args.get('ctrl')

    if not video or not ctrl:
        return "<h2>Smth went wrong</h2>"

    #Hash
    hashed = hashlib.sha256(video.encode('utf-8')).hexdigest()[6:12]

    if ctrl == hashed:
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <!-- Google tag (gtag.js) -->
            <script async src="https://www.googletagmanager.com/gtag/js?id=G-GBNE0PD6WN"></script>
            <script>
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('config', 'G-GBNE0PD6WN');
            </script>
            <meta http-equiv="refresh" content="3;url=https://www.youtube.com/watch?v={{ video }}">
        </head>
        <body>
            <p>Hopescrolling forwarding you to the Youtube...</p>
        </body>
        </html>
        '''
        return render_template_string(html, video=video)
    else:
        return "<h2>Smth went wrong</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
