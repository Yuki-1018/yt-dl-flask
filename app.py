from flask import Flask, render_template, request, redirect, url_for, send_file
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

# 保存先ディレクトリ
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def get_download_link(url, format):
    ydl_opts = {
        'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo+bestaudio',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}] if format == 'mp3' else []
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        ydl.download([url])
        filename = ydl.prepare_filename(info_dict)
        if format == 'mp3':
            filename = os.path.splitext(filename)[0] + '.mp3'
        return filename

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        format = request.form['format']
        try:
            filename = get_download_link(url, format)
            return redirect(url_for('download_file', filename=os.path.basename(filename)))
        except Exception as e:
            return str(e)
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
