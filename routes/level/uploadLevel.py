from . import level
from utils import *
from config import *
from time import time
from sys import getsizeof
from flask import request


maximum_level_size = 10485760  # 10 МБ
minimum_number_blocks = 99


@level.route(f"{Path.TO_DATABASE}/uploadGJLevel21.php", methods=("POST", "GET"))
def upload_level():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    level_string = char_clear(get_arg("levelString"))

    if getsizeof(level_string) > maximum_level_size:
        return "-1"

    level_name = char_clear(get_arg("levelName"))

    if not limit_check(len(base64_decode(get_arg("levelDesc"))), 140) or \
       not limit_check(int_arg(get_arg("coins")), 3) or \
       not limit_check(int_arg(get_arg("levelLength")), 4) or \
       not limit_check(int_arg(get_arg("twoPlayer")), 1) or \
       not limit_check(int_arg(get_arg("unlisted")), 1) or \
       not limit_check(int_arg(get_arg("ldm")), 1) or \
       limit_check(int_arg(get_arg("objects")), minimum_number_blocks) or \
       not limit_check(len(get_arg("password")), 6) or \
       not limit_check(len(get_arg("original")), 12) or \
       not limit_check(len(level_name), 20):
        return "-1"

    song_id = int_arg(get_arg("songID"))

    if song_db.count_documents({
        "song_id": song_id
    }) == 0 and song_id != 0:
        return "-1"

    level_id = int_arg(get_arg("levelID"))

    if int_arg(get_arg("levelID")) == 0:
        if not restric_reupload(level_db, {"account_id": account_id}, "level_id", "upload_date", 120):
            return "-1"

        level_id = last_id(level_db, "level_id")

        single_level = {
            "level_id": int(level_id), "account_id": account_id,
            "user_id": user_db.find_one({"account_id": account_id})["user_id"],
            "username": user_db.find_one({"account_id": account_id})["username"], "level_name": level_name,
            "level_desc": get_arg("levelDesc"), "level_version": 1,
            "level_length": int_arg(get_arg("levelLength")), "level_password": int_arg(get_arg("password")),
            "extra_string": char_clear(get_arg("extraString")),
            "official_song": int_arg(get_arg("audioTrack")), "non_official_song": song_id,
            "original_id": int_arg(get_arg("original")), "two_player": int_arg(get_arg("twoPlayer")),
            "unlisted": int_arg(get_arg("unlisted")), "ldm": int_arg(get_arg("ldm")),
            "coin": int_arg(get_arg("coins")), "silver_coin": 0, "object": int_arg(get_arg("objects")),
            "like": 0, "download": 0, "difficulty": 0, "auto": 0, "star": 0, "featured": 0, "epic": 0,
            "demon": 0, "demon_type": 0, "upload_date": int(time()), "update_date": 0, "rate_date": 0,
            "deleted": 0, "delete_prohibition": 0, "update_prohibition": 0
        }

        with open(f"{Path.TO_ROOT}/data/level/{str(level_id)}.level", "w") as level_file:
            level_file.write(level_string)

        level_db.insert_one(single_level)

        return str(level_id)

    elif level_db.count_documents({
        "account_id": account_id,
        "level_id": level_id,
        "update_prohibition": 0,
        "deleted": 0
    }) == 1:
        if not restric_reupload(level_db, {"account_id": account_id}, "update_date", "update_date", 120):
            return "-1"

        single_level = tuple(level_db.find({"level_id": level_id}))
        level_info = ""

        for key, value in single_level[0].items():
            level_info += f"{str(key)}:{str(value)}:"

        level_version = single_level[0]["level_version"]

        with open(f"{Path.TO_ROOT}/data/level/{str(level_id)}.level", "r") as level_file:
            old_level_string = level_file.read()

        with open(f"{Path.TO_ROOT}/data/level/{str(level_id)}.level", "w") as level_file:
            level_file.write(level_string)

        with open(f"{Path.TO_ROOT}/data/old_level/{str(level_id)}v{level_version}.old.level", "w") as level_file:
            level_file.write(old_level_string)

        with open(f"{Path.TO_ROOT}/data/old_level/{str(level_id)}v{level_version}.old.level.db", "w") as level_file:
            level_file.write(level_info)

        level_db.update_one({"level_id": level_id}, {"$set": {
            "level_desc": get_arg("levelDesc"),
            "level_version": level_version + 1,
            "level_password": int(get_arg("password")),
            "official_song": int_arg(get_arg("audioTrack")),
            "non_official_song": song_id,
            "two_player": int_arg(get_arg("twoPlayer")),
            "object": int_arg(get_arg("objects")),
            "coin": int_arg(get_arg("coins")),
            "extra_string": get_arg("extraString"),
            "update_date": int(time()),
            "ldm": int_arg(get_arg("ldm"))
        }})

        return str(level_id)

    return "-1"
