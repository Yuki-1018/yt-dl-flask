from flask import Flask, request, render_template, jsonify
import yt_dlp

app = Flask(__name__)

def get_direct_link(url, format):
    ydl_opts = {
        'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo+bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format == 'mp3' else [],
        'outtmpl': '%(id)s.%(ext)s',
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            if format == 'mp3':
                return info_dict['url']
            else:
                formats = info_dict.get('formats', [info_dict])
                for f in formats:
                    if f.get('ext') == 'mp4':
                        return f['url']
                return None
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_link', methods=['POST'])
def get_link():
    url = request.form.get('url')
    format = request.form.get('format')

    if not url or not format:
        return jsonify({'error': 'URL and format are required.'}), 400

    direct_link = get_direct_link(url, format)
    if not direct_link:
        return jsonify({'error': 'Failed to retrieve direct link.'}), 500

    return jsonify({'direct_link': direct_link})

if __name__ == '__main__':
    app.run(debug=True)
