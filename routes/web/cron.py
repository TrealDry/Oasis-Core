from . import web
from utils import *
from time import time


@web.route("/cron/<key>/<type_key>", methods=("POST", "GET"))
def cron(key, type_key):
    if masterkey_db.count_documents({
        "key_name": "cron",
        "key": key
    }) == 0:
        return ""

    responce = ""

    if type_key == "1":

        """ Выдача креатор поинтов """

        creator_list = {}

        levels = tuple(level_db.find({
            "star": {"$gt": 0},
            "deleted": 0
        }))

        if len(levels) != 0:
            for i in levels:
                if i["account_id"] not in creator_list:
                    creator_list["account_id"] = 0

                if i["featured"] == 0 and i["epic"] == 0:
                    creator_list["account_id"] += 1
                elif i["featured"] == 1 and i["epic"] == 0:
                    creator_list["account_id"] += 2
                if i["epic"] == 1:
                    creator_list["account_id"] += 4

            for i in creator_list:
                responce += f"{i} = {creator_list[i]} cp<br>"
                user_db.update_one({"account_id": i}, {"$set": {
                    "creator_point": creator_list[i]
                }})

        del levels
        del creator_list

        """ Античит """

        levels = tuple(level_db.find({
            "star": {"$gt": 0},
        }))

        max_star = 190
        max_demon = 3
        max_gold_coin = 66
        max_silver_coin = 0

        users = tuple(user_db.find({"is_top_banned": 0}))
        mappacks = tuple(mappack_db.find())
        gauntlets = tuple(gauntlet_db.find())
        daily_levels = tuple(dailylevel_db.find())

        for i in levels:
            max_star += i["star"]
            max_demon += i["demon"]
            max_silver_coin += i["coin"] if i["silver_coin"] == 1 else 0

        if len(mappacks) != 0:
            for i in mappacks:
                max_star += i["star"]
                max_gold_coin += i["coin"]

        if len(gauntlets) != 0:
            for i in gauntlets:
                level_ids = i["level"].split(",")
                for j in level_ids:
                    level = tuple(level_db.find({"level_id": int(j)}))

                    max_star += level[0]["star"]
                    max_demon += level[0]["demon"]
                    max_silver_coin += level[0]["coin"] if level[0]["silver_coin"] == 1 else 0

        if len(daily_levels) != 0:
            for i in daily_levels:
                level = tuple(level_db.find({"level_id": i["level_id"]}))

                max_star += level[0]["star"]
                max_demon += level[0]["demon"]
                max_silver_coin += level[0]["coin"] if level[0]["silver_coin"] == 1 else 0

        for i in users:
            if not limit_check(i["star"], max_star) or \
               not limit_check(i["demon"], max_demon) or \
               not limit_check(i["secret_coin"], max_gold_coin) or \
               not limit_check(i["user_coin"], max_silver_coin):
                user_db.update_one({"user_id": i["user_id"]}, {"$set": {
                    "is_top_banned": 1
                }})

        """ Очистка не активированных аккаунтов """

        account_db.delete_many({
            "valid": 0,
            "date": {"$lte": int(time()) - 43200}
        })

        return responce

    else:
        return ""
