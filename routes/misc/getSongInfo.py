from . import misc
from utils import *
from config import *
from flask import request


@misc.route(f"{Path.TO_DATABASE}/getGJSongInfo.php", methods=("POST", "GET"))
def get_song_info():
    if not secret_check(request.values.get("secret"), 2):
        return ""

    song_id = int_arg(get_arg("songID"))

    if song_db.count_documents({
        "song_id": song_id
    }) == 0:
        return "-1"

    song_info = tuple(song_db.find({"song_id": song_id}))
    responce = ""

    single_song = {
        1: song_id, 2: song_info[0]["name"], 3: 0, 4: song_info[0]["artist_name"],
        5: "{0:.2f}".format(song_info[0]["size"]), 6: "", 10: song_info[0]["link"], 7: "", 8: 1
    }

    responce += resp_proc(single_song, 3)[:-3]

    return responce
