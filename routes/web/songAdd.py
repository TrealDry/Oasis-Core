import os
from . import web
from utils import *
from time import time
from config import Security, Path
from flask import render_template, request


@web.route("/song_add", methods=("POST", "GET"))
def song_add():
    message = ""
    if request.method == 'POST':
        try:
            login = get_arg_form("login")
            password = get_arg_form("password")

            account_info = tuple(account_db.find({"username": {"$regex": f"(?i){login}"}}))

            account_id = account_info[0]["account_id"]

            song = request.files['song_file']
        except KeyError:
            return "Error!"
        except IndexError:
            return "Incorrect login!"

        if song is not None:
            if not hcaptcha.verify():
                message = "Captcha failed!"
            elif check_password(account_id, password, gjp=False, ip=get_ip()):
                filename = song.filename
                if not filename.rsplit('.', 1)[1] in ".mp3":
                    message = "File is not mp3!"
                elif not restric_reupload(
                    song_db, {"account_id": account_id},
                    "song_id", "upload_date", 3600
                ):
                    message = "You have recently uploaded music to the server, please wait an hour!"
                else:
                    song_id = last_id(song_db, "song_id")
                    song_path = f"{Path.TO_ROOT}/data/song/{song_id}.mp3"
                    song.save(os.path.join(f"{Path.TO_ROOT}/data/song", f"{song_id}.mp3"))
                    song_info = os.stat(song_path)

                    if song_info.st_size / (1024 * 1024) >= 10:
                        os.remove(song_path)
                        message = "File larger than 10 megabytes!"

                    else:
                        song_db.insert_one({
                            "song_id": song_id,
                            "name": filename.partition('.mp3')[0],
                            "artist_name": "PleasantSpace",
                            "account_id": account_id,
                            "size": song_info.st_size / (1024 * 1024),
                            "link": Path.TO_SONG + f"/{song_id}.mp3",
                            "upload_date": int(time())
                        })
                        message = f"Music added successfully! Song ID = {song_id}"
            else:
                message = "Incorrect password!"

    return render_template('song_add.html', SITE_KEY=Security.SITE_KEY, message=message)
