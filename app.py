import yt_dlp
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["video_url"]

        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": "%(id)s.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_id = info["id"]

            mp4_url = url_for("download", filename=f"{video_id}.mp4")
            mp3_url = url_for("download", filename=f"{video_id}.m4a")

            return render_template("index.html", mp4_url=mp4_url, mp3_url=mp3_url)

    return render_template("index.html")

@app.route("/download/<filename>")
def download(filename):
    return redirect(url_for("static", filename=filename))

if __name__ == "__main__":
    app.run(debug=True)
