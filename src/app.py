from flask import Flask, render_template, url_for

import os

app = Flask(__name__)

@app.route("/")
def root():
    video_list_url = url_for("video_list")
    return render_template('root.html', video_list_url=video_list_url)

@app.route("/video-list")
def video_list():
    BASE_PATH = 'src/static/videos'
    dirs = [url_for('video', filepath=f) for f in os.listdir(BASE_PATH)]
    return render_template('video_list.html', paths=dirs)

@app.route("/videos/<filepath>")
def video(filepath=None):
    print(filepath)
    filepath = os.path.normpath(filepath)
    name, ext = os.path.splitext(filepath)
    static_path = url_for('static', filename=f'videos/{filepath}')
    codec = ext[1:]
    return render_template('video_player.html', filepath=static_path, codec=codec, ext=ext)
