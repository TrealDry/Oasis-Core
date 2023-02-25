import pymongo
from . import level
from utils import *
from config import *
from time import time
from flask import request


@level.route(f"{Path.TO_DATABASE}/getGJLevels21.php", methods=("POST", "GET"))
def get_levels():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg('account_id'))
    password = get_arg('gjp')

    gauntlet = int_arg(get_arg('gauntlet'))
    type_pack = get_arg('type')
    demon_filter = int_arg(get_arg('demonFilter'))
    difficulty = get_arg('diff')

    long = get_arg('len')
    uncompleted = int_arg(get_arg('uncompleted'))
    only_completed = int_arg(get_arg('onlyCompleted'))
    completed_levels = get_arg('completedLevels')

    gauntlet_bool = "" if gauntlet == 0 else "1"
    follow = get_arg('Follow')
    search = get_arg("str")

    query = {
        "unlisted": 0,
        "deleted": 0,
        "$or": []
    }

    sort = [("like", pymongo.DESCENDING)]

    if gauntlet != 0:  # Гаунтлет уровни
        gauntlet_levels = gauntlet_db.find_one({"gauntlet_id": int_arg(gauntlet)})["level"].split(",")
        for i in gauntlet_levels:
            query["$or"].append({"level_id": int_arg(i)})
    else:  # Не гаунтлет
        if bool_str(get_arg("featured")):
            query["featured"] = 1
            query["epic"] = 0
        if bool_str(get_arg("epic")):
            query["epic"] = 1
        if bool_str(get_arg("original")):
            query["original_id"] = {"$gt": 0}
        if bool_str(get_arg("twoPlayer")):
            query["two_player"] = 1
        if bool_str(get_arg("coins")):
            query["silver_coin"] = 1

        if bool_str(get_arg("star")):
            query["star"] = {"$gt": 0}
        if bool_str(get_arg("noStar")):
            query["star"] = {"$lt": 1}
        if bool_str(get_arg("audioTrack")):
            query["official_song"] = int_arg(get_arg("audioTrack"))
        if bool_str(get_arg("customSong")):
            query["non_official_song"] = int_arg(get_arg("customSong"))

        if uncompleted == 1 or only_completed == 1:
            completed_levels_arr = completed_levels[1:-1].split(",")
            if uncompleted == 1:
                query["$nor"] = []
                for i in completed_levels_arr:
                    query["$nor"].append({"level_id": int_arg(i)})
            else:
                for i in completed_levels_arr:
                    query["$or"].append({"level_id": int_arg(i)})

        if difficulty != "-":
            if difficulty == "-2":  # Демон
                query["demon"] = 1
                if demon_filter != 0:
                    query["demon_type"] = demon_filter
            elif difficulty == "-3":  # Авто
                query["auto"] = 1
            elif len(difficulty.split(",")) > 1:  # Много аргументов
                diff_arr = difficulty.split(",")
                for i in diff_arr:
                    query["$or"].append({"difficulty": int_arg(i)})
                query["demon"] = 0
            else:  # Один аргумент
                query["difficulty"] = int_arg(difficulty)
                query["demon"] = 0

        if long != "-":
            if len(long.split(",")) <= 1:
                query["level_length"] = int_arg(long)
            else:
                long_arr = long.split(",")
                for i in range(len(long_arr)):
                    query["$or"].append({"level_length": int_arg(i)})

        if type_pack == "0":  # Поиск
            if int_arg(search) > 0:
                query = {"level_id": int_arg(search), "$or": []}
                sort = None
            elif search != "":
                query["level_name"] = {"$regex": f"(?i)^{search}"}
        elif type_pack == "1":  # Больше всего загрузок
            sort = [("download", pymongo.DESCENDING)]
        elif type_pack == "3":  # Тренды
            last_week = time() - (7 * 24 * 60 * 60)
            query["upload_date"] = {"$gt": last_week}
        elif type_pack == "4":  # Новые уровни
            sort = [("level_id", pymongo.DESCENDING)]
        elif type_pack == "5":  # Уровни игрока
            sort = [("level_id", pymongo.DESCENDING)]
            query["user_id"] = int_arg(search)
        elif type_pack == "6":  # Вкладка Featured
            sort = [("rate_date", pymongo.DESCENDING)]
            query["featured"] = 1
        elif type_pack == "7":  # Вкладка Magic
            last_week = time() - (7 * 24 * 60 * 60)
            query["upload_date"] = {"$gt": last_week}
            query["object"] = {"$gt": 9999}
        elif type_pack == "10":  # Вкладка Map packs
            query = {"deleted": 0, "$or": []}
            for i in search.split(","):
                query["$or"].append({"level_id": int_arg(i)})
        elif type_pack == "11":  # Вкладка Awarded (недавно оценённые)
            sort = [("rate_date", pymongo.DESCENDING)]
            query["star"] = {"$gt": 0}
        elif type_pack == "16":  # Вкладка Hall of fame
            sort = [("rate_date", pymongo.DESCENDING)]
            query["epic"] = 1

    page = int_arg(get_arg('page'))
    offset = page * 10

    if len(query["$or"]) == 0:
        query.pop("$or")

    levels = level_db.find(query).skip(offset).limit(10)
    if sort:
        levels.sort(sort)

    levels = tuple(levels)

    responce = ""

    for i in levels:
        diff = 0

        if i["difficulty"] > 0:
            diff = i["difficulty"] * 10
            dd = 10
        else:
            dd = 0

        demon = "" if i["demon"] == 0 else 1
        auto = "" if i["auto"] == 0 else 1

        single_response = {
            1: i["level_id"], 2: i["level_name"], 5: i["level_version"], 6: i["user_id"],
            8: dd, 9: diff, 10: i["download"], 12: i["official_song"], 13: 21,
            14: i["like"], 17: demon, 43: demon_type_conv(i["demon_type"]), 25: auto,
            18: i["star"], 19: i["featured"], 42: i["epic"], 45: i["object"], 3: i["level_desc"],
            15: i["level_length"], 30: i["original_id"], 31: i["two_player"], 37: i["coin"],
            38: i["silver_coin"], 39: 0, 46: 1, 47: 2, 35: i["non_official_song"], 44: gauntlet_bool
        }

        responce += resp_proc(single_response) + "|"
    else:
        responce = responce[:-1] + "#"

    hash_string = ""

    for i in levels:
        responce += f"{i['user_id']}:{i['username']}:{i['account_id']}|"
        hash_string += str(i["level_id"])[0] + str(i["level_id"])[-1] + \
            str(i["star"]) + str(i["silver_coin"])
    else:
        responce = responce[:-1] + "#"

    is_non_song = False

    for i in levels:
        if i["non_official_song"] != 0:
            is_non_song = True
            song_info = tuple(song_db.find({"song_id": i["non_official_song"]}))
            single_song = {
                1: i["non_official_song"], 2: song_info[0]["name"], 3: 0,
                4: song_info[0]["artist_name"], 5: "{0:.2f}".format(song_info[0]["size"]),
                6: "", 10: song_info[0]["link"], 7: "", 8: 1
            }
            responce += resp_proc(single_song, 3)[:-2] + ":~"
    else:
        if is_non_song:
            responce = responce[:-3]

    responce += f"#{level_db.count_documents(query)}:{offset}:10#{return_hash(hash_string)}"

    return responce
