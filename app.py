# app.py
from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_url = ydl.prepare_filename(info_dict)
        audio_url = video_url.replace('.mp4', '.mp3')

    return render_template('result.html', video_url=video_url, audio_url=audio_url)

if __name__ == '__main__':
    app.run(debug=True)
