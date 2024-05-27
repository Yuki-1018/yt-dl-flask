from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_format = ydl.get_suitable_formats(info)[0]
            video_link = video_format['url']
            audio_link = None
            for fmt in ydl.get_suitable_formats(info):
                if fmt['ext'] == 'm4a':
                    audio_link = fmt['url']
                    break

        return jsonify({'video_link': video_link, 'audio_link': audio_link})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
