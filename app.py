from flask import Flask, render_template, request, redirect, url_for
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        video_link = request.form['video_link']
        try:
            with yt_dlp.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(video_link, download=False)
                video_url = info_dict['url']
                return redirect(video_url)
        except Exception as e:
            return render_template('index.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
