from flask import Flask, render_template, url_for

import os

app = Flask(__name__)

BASE_PATH = 'src/static/videos'


def build_tree(path):
    if os.path.isdir(path):
        return {
            'type': 'directory',
            'name': os.path.basename(path),
            'children': [
                build_tree(os.path.join(path, entry))
                for entry in sorted(os.listdir(path))
            ]
        }
    elif os.path.isfile(path):
        return {
            'type': 'file',
            'name': os.path.basename(path),
            'path': os.path.relpath(path, BASE_PATH)
        }


@app.route("/")
def root():
    video_list_url = url_for("video_list")
    return render_template('root.html', video_list_url=video_list_url)


@app.route("/video-list")
def video_list():
    tree = [build_tree(os.path.join(BASE_PATH, entry)) for entry in sorted(os.listdir(BASE_PATH))]
    return render_template('video_list.html', tree=tree)

@app.route("/videos/<path:filepath>")
def video(filepath):
    print(filepath)
    filepath = os.path.normpath(filepath)
    name, ext = os.path.splitext(filepath)
    static_path = url_for('static', filename=f'videos/{filepath}')
    codec = ext[1:]
    return render_template('video_player.html', filepath=static_path, codec=codec, ext=ext)
