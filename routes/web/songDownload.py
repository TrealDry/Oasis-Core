from . import web
from config import Path
from flask import send_from_directory


@web.route("/song/<path:filename>", methods=['POST', 'GET'])
def song_download(filename):
    directory = Path.TO_ROOT + "/data/song/"
    return send_from_directory(directory=directory, path=filename)
