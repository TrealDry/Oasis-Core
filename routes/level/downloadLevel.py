import pymongo
from . import level
from utils import *
from config import *
from time import time
from flask import request


@level.route(f"{Path.TO_DATABASE}/downloadGJLevel22.php", methods=("POST", "GET"))
def download_level():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    level_id = int_arg(get_arg("levelID"))
    featured_id = 0
    featured_bool = False

    if level_id < 0:  # Дейли и Викли
        type_daily = 0 if level_id == -1 else 1

        time_now = int(time())

        daily_level = tuple(dailylevel_db.find({
            "timestamp": {"$lte": time_now - 1},
            "daily_type": type_daily
        }).sort([("timestamp", pymongo.DESCENDING)]).limit(1))

        level_id = daily_level[0]["level_id"]
        featured_id = daily_level[0]["daily_id"]

        featured_id = featured_id if type_daily == 0 else featured_id + 100001
        featured_bool = True

    elif level_id == 0:
        return "-1"

    single_level = tuple(level_db.find({"level_id": level_id}))
    user_info = ""
    responce = ""

    for i in single_level:
        difficulty = 0

        if i["difficulty"] > 0:
            difficulty = i["difficulty"] * 10
            dd = 10
        else:
            dd = 0

        demon = "" if i["demon"] == 0 else 1
        auto = "" if i["auto"] == 0 else 1
        ldm = "" if i["ldm"] == 0 else 1

        with open(f"{Path.TO_ROOT}/data/level/{str(level_id)}.level", "r") as f:
            level_string = f.read()

        single_response = {
            1: i["level_id"], 2: i["level_name"], 3: i["level_desc"], 4: level_string, 5: i["level_version"],
            6: i["user_id"], 8: dd, 9: difficulty, 10: i["download"], 12: i["official_song"], 13: 21,
            14: i["like"], 17: demon, 43: demon_type_conv(i["demon_type"]), 25: auto, 18: i["star"],
            19: i["featured"], 42: i["epic"], 45: i["object"], 15: i["level_length"], 30: i["original_id"],
            31: i["two_player"], 28: 0, 29: 0, 35: i["non_official_song"], 36: i["extra_string"], 37: i["coin"],
            38: i["silver_coin"], 39: 0, 46: 1, 47: 2, 40: ldm, 27: base64_encode(xor_cipher(str(
                i["level_password"]), "26364"))
        }

        if featured_bool:
            user_info = f"#{i['user_id']}:{i['username']}:{i['account_id']}"
            single_response.update({41: featured_id})

        hash_string = f"{i['user_id']},{i['star']},{i['demon']},{i['level_id']},{i['silver_coin']}," \
                      f"{i['featured']},{i['level_password']},{featured_id}"

        responce = resp_proc(single_response) + f"#{return_hash2(level_string)}#{return_hash(hash_string)}"
    else:
        account_id = int_arg(get_arg("accountID"))
        password = get_arg("gjp")

        ip = get_ip()

        confirmed_download = False

        if check_password(account_id, password, ip=get_ip()):
            if actiondownload_db.count_documents({
                "level_id": level_id,
                "account_id": account_id
            }) == 0:
                confirmed_download = True
        elif actiondownload_db.count_documents({
            "level_id": level_id,
            "ip": ip
        }) == 0:
            account_id = 0
            confirmed_download = True

        if confirmed_download:
            actiondownload_db.insert_one({
                "level_id": level_id,
                "account_id": account_id,
                "ip": ip,
                "timestamp": int(time())
            })
            level_db.update_one({"level_id": level_id}, {"$inc": {"download": 1}})

    return responce + user_info
