from flask import Flask, render_template, request, redirect, url_for
import yt_dlp

app = Flask(__name__)

# ダウンロードリンクを取得する関数
def get_download_links(youtube_link):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_link, download=False)
        video_url = ydl.prepare_filename(info)
        mp3_url = video_url.replace('.mp4', '.mp3')
    return video_url, mp3_url

# ホームページ
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_link = request.form['youtube_link']
        video_url, mp3_url = get_download_links(youtube_link)
        return render_template('index.html', video_url=video_url, mp3_url=mp3_url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
